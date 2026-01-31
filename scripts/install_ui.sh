#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v uv >/dev/null 2>&1; then
  echo "Missing 'uv'. Install uv or use python3-venv + pip manually." >&2
  exit 1
fi

uv venv .venv
source .venv/bin/activate
uv pip install -r ui/requirements.txt

echo "OK: UI deps installed into .venv. Run: ./scripts/run_ui.sh"
