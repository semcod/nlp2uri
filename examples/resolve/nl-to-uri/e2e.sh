#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

out="$(python examples/resolve/nl-to-uri/main.py 2>&1)"
echo "$out" | grep -q 'app://firefox/open'
echo "$out" | grep -q 'desktop-screenshot://'
echo "$out" | grep -q 'app://vscode/open'
echo "examples/resolve/nl-to-uri: OK"
