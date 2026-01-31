# MoltScheduler

A **file-backed, agent-assisted daily planning system** with an optional **web UI**.

V1 is intentionally simple: the “product” is a clean data model + an operating procedure an agent can follow.

## What it does
- You maintain canonical files (`planner/profile.yaml`, `planner/tasks.yaml`).
- An agent reads them and pushes a daily plan (time-blocked, estimated durations, top priorities).
- You can optionally edit the plan + submit check-ins via a browser UI.

## What it is not (yet)
- Not a calendar replacement.
- Not a full-featured GUI with drag-drop.

## Quick start (template only)
1. Copy `template/` to your private workspace.
2. Edit:
   - `planner/profile.yaml`
   - `planner/tasks.yaml`
3. Give your agent the instructions in **README_AGENT.md**.

## Run the UI on a headless server (recommended via Tailscale)

### 1) Install Tailscale
Install Tailscale on:
- the server running your agent
- your personal laptop/desktop (where you’ll view the UI)

Then connect both to the same tailnet.

### 2) Start the UI server
On the server:

```bash
./scripts/install_ui.sh
export PLANNER_ROOT=/path/to/your/workspace_root  # contains planner/ and reflections/
export HOST=0.0.0.0
export PORT=8787
./scripts/run_ui.sh
```

### 3) Open the UI from your laptop
Find the server’s Tailscale IP (or tailnet DNS name), then open:

```
http://<server-tailscale-ip>:8787
```

UI docs: see `ui/README.md`.

## Philosophy
- **Truth vs outputs**: keep one canonical source of truth, and regenerate outputs.
- **Tidy by default**: keep only `planner/latest/` artifacts unless you explicitly want history.

## License
MIT (see `LICENSE`).
