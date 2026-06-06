#!/usr/bin/env bash
# Install nlp2uri into the active Python environment (or given venv).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${1:-}"

if [[ -n "$VENV" ]]; then
  PIP="$VENV/bin/pip"
  PYTHON="$VENV/bin/python"
else
  PIP="pip"
  PYTHON="python"
fi

if [[ -n "$VENV" && ! -x "$PIP" ]]; then
  echo "error: $PIP not found" >&2
  exit 1
fi

"$PIP" install -e "$ROOT[dev,envmap]"
"$PYTHON" -c "import nlp2uri; print('nlp2uri', nlp2uri.__version__, 'ok')"
