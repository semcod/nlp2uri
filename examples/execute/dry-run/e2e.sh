#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

out="$(python examples/execute/dry-run/main.py 2>&1)"
echo "$out" | grep -q 'app://firefox/open'
echo "$out" | grep -q 'screencapture'
echo "$out" | grep -q 'ms-settings'
echo "examples/execute/dry-run: OK"
