#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

out="$(nlp2uri shell export "open firefox")"
grep -q 'NLP2URI_URI=' <<<"$out"
grep -q 'app://firefox/open' <<<"$out"
eval "$out"
test "$NLP2URI_URI" = "app://firefox/open"
echo "examples/integrators/shell-export: OK"
