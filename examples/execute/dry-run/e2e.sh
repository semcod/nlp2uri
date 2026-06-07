#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

out="$(python examples/execute/dry-run/main.py 2>&1)"
grep -q 'app://firefox/open' <<<"$out"
grep -q 'screencapture' <<<"$out"
grep -q 'ms-settings' <<<"$out"
echo "examples/execute/dry-run: OK"
