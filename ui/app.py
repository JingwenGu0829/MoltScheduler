from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles


def _workspace_root() -> Path:
    # Default to a path that matches the OpenClaw workspace convention.
    return Path(os.environ.get("PLANNER_ROOT", str(Path.home() / "planner"))).expanduser().resolve()


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _save_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def _prepend_reflection(ref_path: Path, entry_md: str) -> None:
    existing = _read_text(ref_path)
    if existing.strip() == "":
        existing = "# Reflections (rolling)\n\nAppend newest entries at the top.\n\n---\n\n"
    # Insert after the first divider if present, otherwise just prepend.
    marker = "---\n\n"
    idx = existing.find(marker)
    if idx != -1:
        head = existing[: idx + len(marker)]
        tail = existing[idx + len(marker) :]
        new = head + "\n" + entry_md.strip() + "\n\n" + tail.lstrip()
    else:
        new = entry_md.strip() + "\n\n" + existing
    _write_text(ref_path, new)


app = FastAPI(title="MoltScheduler UI", version="0.1.0")

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"ok": "true"}


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    root = _workspace_root()
    plan_path = root / "planner" / "latest" / "plan.md"
    issues_path = root / "planner" / "latest" / "sglang_issues.md"
    tasks_path = root / "planner" / "tasks.yaml"
    profile_path = root / "planner" / "profile.yaml"

    plan_md = _read_text(plan_path) or "# Plan\n\n(no plan yet)\n"
    issues_md = _read_text(issues_path)

    tasks = _read_text(tasks_path)
    profile = _read_text(profile_path)

    html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>MoltScheduler</title>
  <link rel=\"stylesheet\" href=\"/static/style.css\" />
</head>
<body>
  <div class=\"container\">
    <header class=\"top\">
      <div>
        <h1>MoltScheduler</h1>
        <p class=\"muted\">File-backed daily planner (headless server → browser UI).</p>
      </div>
      <div class=\"pill\">root: <code>{root}</code></div>
    </header>

    <section class=\"grid\">
      <div class=\"card\">
        <h2>Today’s plan (editable)</h2>
        <form method=\"post\" action=\"/save_plan\">
          <textarea name=\"plan_md\" rows=\"20\">{_escape(plan_md)}</textarea>
          <div class=\"row\">
            <button type=\"submit\">Save plan</button>
          </div>
        </form>
      </div>

      <div class=\"card\">
        <h2>Quick check-in</h2>
        <form method=\"post\" action=\"/checkin\">
          <label>What did you do today? (bullets)</label>
          <textarea name=\"done\" rows=\"6\" placeholder=\"e.g.\n- Thesis 2h\n- Profiling 1.5h\n- Workout\"></textarea>

          <label>Blockers / notes</label>
          <textarea name=\"blockers\" rows=\"3\"></textarea>

          <label>Schedule changes (if any)</label>
          <textarea name=\"schedule_changes\" rows=\"3\"></textarea>

          <label>Reflection (optional)</label>
          <textarea name=\"reflection\" rows=\"4\"></textarea>

          <div class=\"row\">
            <button type=\"submit\">Submit check-in</button>
          </div>
        </form>

        <h3>SGLang issues (latest)</h3>
        <pre class=\"mono\">{_escape(issues_md or "(none yet)")}</pre>
      </div>
    </section>

    <section class=\"card\">
      <h2>Canonical files (view only)</h2>
      <details>
        <summary><b>profile.yaml</b></summary>
        <pre class=\"mono\">{_escape(profile)}</pre>
      </details>
      <details>
        <summary><b>tasks.yaml</b></summary>
        <pre class=\"mono\">{_escape(tasks)}</pre>
      </details>
    </section>

    <footer class=\"muted\">v0.1 · Tip: set <code>PLANNER_ROOT</code> to your workspace root. Default is <code>~/planner</code>.</footer>
  </div>
</body>
</html>"""
    return HTMLResponse(html)


def _escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


@app.post("/save_plan")
def save_plan(plan_md: str = Form(...)) -> RedirectResponse:
    root = _workspace_root()
    plan_path = root / "planner" / "latest" / "plan.md"
    _write_text(plan_path, plan_md.rstrip() + "\n")
    return RedirectResponse(url="/", status_code=303)


@app.post("/checkin")
def checkin(
    done: str = Form(""),
    blockers: str = Form(""),
    schedule_changes: str = Form(""),
    reflection: str = Form(""),
) -> RedirectResponse:
    root = _workspace_root()
    ref_path = root / "reflections" / "reflections.md"

    now = datetime.now().astimezone()
    title = now.strftime("%Y-%m-%d")

    def bullets(text: str) -> str:
        text = (text or "").strip()
        if not text:
            return "- (none)"
        # normalize lines to markdown bullets
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        out = []
        for ln in lines:
            if ln.startswith("-"):
                out.append(ln)
            else:
                out.append(f"- {ln}")
        return "\n".join(out)

    entry = (
        f"## {title}\n"
        f"- Time: {now.isoformat(timespec='minutes')}\n\n"
        f"**Done**\n{bullets(done)}\n\n"
        f"**Blockers / notes**\n{bullets(blockers)}\n\n"
        f"**Schedule changes**\n{bullets(schedule_changes)}\n\n"
        f"**Reflection**\n{bullets(reflection)}\n"
    )

    _prepend_reflection(ref_path, entry)

    # v0: do not mutate tasks.yaml automatically. Keep check-in as log only.
    return RedirectResponse(url="/", status_code=303)


@app.get("/raw/plan")
def raw_plan() -> PlainTextResponse:
    root = _workspace_root()
    plan_path = root / "planner" / "latest" / "plan.md"
    return PlainTextResponse(_read_text(plan_path) or "")
