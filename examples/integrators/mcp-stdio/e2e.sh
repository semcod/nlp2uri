#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

payload='{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"nlp2uri_resolve","arguments":{"prompt":"open firefox"}}}'
out="$(printf '%s\n' "$payload" | nlp2uri-mcp)"
grep -q 'app://firefox/open' <<<"$out"

map_payload='{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"nlp2uri_resolve_system_map","arguments":{"prompt":"send invoice","system_map":{"format":"nlp2dsl.system_map.v1","example_id":"e2e","commands":[{"name":"send_invoice","runtime":"executor:worker"}],"runtimes":[{"id":"executor:worker","kind":"worker"}]}}}}'
map_out="$(printf '%s\n' "$map_payload" | nlp2uri-mcp)"
grep -q 'send_invoice' <<<"$map_out"

echo "examples/integrators/mcp-stdio: OK"
