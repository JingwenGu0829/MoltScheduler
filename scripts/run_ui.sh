#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -d .venv ]; then
  echo "Missing .venv. Run: ./scripts/install_ui.sh" >&2
  exit 1
fi

source .venv/bin/activate

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8787}"

# Set PLANNER_ROOT to the workspace root that contains:
#   planner/  and  reflections/
# Example:
#   export PLANNER_ROOT=/home/jig040/.openclaw/workspace/jing

exec python -m uvicorn ui.app:app --host "$HOST" --port "$PORT"
