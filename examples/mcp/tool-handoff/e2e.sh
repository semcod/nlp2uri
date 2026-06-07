#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

out="$(python examples/mcp/tool-handoff/main.py 2>&1)"
grep -q 'text/uri-list' <<<"$out"
grep -q 'resolve_desktop_action' <<<"$out"
grep -q 'desktop-screenshot://' <<<"$out"
echo "examples/mcp/tool-handoff: OK"
