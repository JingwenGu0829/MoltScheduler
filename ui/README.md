# MoltFocus UI

Lightweight web UI for the file-backed MoltFocus planner. Usually runs on a server and is opened from your laptop browser.

## Files it reads/writes
- `planner/latest/plan.md` (editable plan)
- `planner/latest/checkin_draft.json` (auto-saved check-in draft)
- `reflections/reflections.md` (nightly finalize appends entries)
- `planner/state.json` (streak, summary, finalize metadata)

## Run

```bash
./scripts/install_ui.sh

# Workspace root must contain planner/ and reflections/
export PLANNER_ROOT=/path/to/workspace_root
export HOST=0.0.0.0
export PORT=8787

./scripts/run_ui.sh
```

## Open in browser
- Same machine as server: `http://localhost:8787`
- Remote server via SSH tunnel (recommended):
  ```bash
  ssh -N -L 8787:127.0.0.1:8787 <user>@<server-ip-or-hostname>
  ```
  then open `http://localhost:8787` on your laptop.
- Remote server via Tailscale: `http://<SERVER_TAILSCALE_IP>:8787`

## If server stops

```bash
cd MoltFocus
export PLANNER_ROOT=/path/to/workspace_root
export HOST=0.0.0.0
export PORT=8787
./scripts/run_ui.sh
```

## Notes
- Check-in auto-saves; no submit button needed.
- Nightly finalize should call `POST /api/finalize` once per day (usually via OpenClaw/cron).
- Task bookkeeping updates in `tasks.yaml` are handled by the agent workflow, not this UI.
