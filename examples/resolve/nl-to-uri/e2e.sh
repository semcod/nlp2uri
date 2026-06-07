#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

out="$(python examples/resolve/nl-to-uri/main.py 2>&1)"
grep -q 'app://firefox/open' <<<"$out"
grep -q 'desktop-screenshot://' <<<"$out"
grep -q 'app://vscode/open' <<<"$out"
echo "examples/resolve/nl-to-uri: OK"
