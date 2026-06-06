#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

out="$(nlp2uri shell export "open firefox")"
echo "$out" | grep -q 'NLP2URI_URI='
echo "$out" | grep -q 'app://firefox/open'
eval "$out"
test "$NLP2URI_URI" = "app://firefox/open"
echo "examples/integrators/shell-export: OK"
