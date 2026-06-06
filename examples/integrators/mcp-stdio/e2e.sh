#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

payload='{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"nlp2uri_resolve","arguments":{"prompt":"open firefox"}}}'
out="$(printf '%s\n' "$payload" | nlp2uri-mcp)"
echo "$out" | grep -q 'app://firefox/open'
echo "examples/integrators/mcp-stdio: OK"
