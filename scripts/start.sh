#!/usr/bin/env bash
# Usage: scripts/start.sh --lang es

set -euo pipefail
# Resolve repo root from this script's directory
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." &>/dev/null && pwd)"

# Use project venv if present, else fallback to system python
PY_BIN="${REPO_ROOT}/venv/bin/python"
if [[ ! -x "$PY_BIN" ]]; then
  PY_BIN="python3"
fi

cd "$REPO_ROOT"
export PYTHONPATH="$REPO_ROOT/src:${PYTHONPATH:-}"
exec "$PY_BIN" -m dictation "$@"
