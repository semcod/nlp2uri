#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

out="$(python examples/mcp/tool-handoff/main.py 2>&1)"
echo "$out" | grep -q 'text/uri-list'
echo "$out" | grep -q 'resolve_desktop_action'
echo "$out" | grep -q 'desktop-screenshot://'
echo "examples/mcp/tool-handoff: OK"
