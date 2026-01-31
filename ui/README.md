# MoltScheduler UI (V0)

This is a tiny web UI intended to run on a **headless server** and be viewed from your laptop/phone browser.

It edits the same file-backed storage as the agent:
- `planner/latest/plan.md`
- `planner/latest/sglang_issues.md` (optional)
- `reflections/reflections.md`

## Run locally

```bash
./scripts/install_ui.sh
export PLANNER_ROOT=/path/to/your/workspace_root  # contains planner/ and reflections/
./scripts/run_ui.sh
```

Then open: `http://127.0.0.1:8787`

## Run on a server

Bind to all interfaces:

```bash
export HOST=0.0.0.0
export PORT=8787
./scripts/run_ui.sh
```

## Notes
- This is intentionally simple (V0): edit plan text + submit a check-in.
- Task updates from check-ins are not auto-applied in V0 (agent does the bookkeeping).
