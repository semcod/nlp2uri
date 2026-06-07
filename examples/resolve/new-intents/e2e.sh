#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

out="$(python -c "
from nlp2uri.resolve import resolve_text
from nlp2uri.models import HostPlatform

samples = [
    ('open terminal in folder /tmp', 'app://terminal/open'),
    ('move window Slack to second monitor', 'desktop-window://move'),
    ('open network settings', 'ms-settings:network'),
    ('zrób screenshot okna Edge', 'desktop-screenshot://window'),
]
for text, prefix in samples:
    spec = resolve_text(text, platform=HostPlatform.LINUX)
    print(spec.uri)
" 2>&1)"

grep -q 'app://terminal/open' <<<"$out"
grep -q 'desktop-window://move' <<<"$out"
grep -q 'title=Edge' <<<"$out"
echo "examples/resolve/new-intents: OK"
