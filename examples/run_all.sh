#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== pytest =="
python -m pytest

echo "== integration (x-scheme-handler) =="
export NLP2URI_INTEGRATION=1
python -m pytest tests/integration -m integration -q

echo "== basic_resolve (sample) =="
python -c "
import json
from nlp2uri import nlp2uri
from nlp2uri.models import HostPlatform
for text in ('open firefox', 'otwórz vscode w folderze /tmp/x'):
    print(json.dumps(nlp2uri(text, os=HostPlatform.LINUX).to_dict(), indent=2))
    print('---')
"

echo "== dry_run_execute =="
python examples/dry_run_execute.py

echo "== mcp_handoff (sample) =="
python -c "
import json
from nlp2uri.mcp import mcp_handoff_payload
from nlp2uri.models import HostPlatform
print(json.dumps(mcp_handoff_payload('capture screen', platform=HostPlatform.LINUX), indent=2))
"

echo "== cli =="
nlp2uri plan "open firefox" --platform linux --json
nlp2uri compile "app://firefox/open" --platform linux --json
nlp2uri execute "capture screen" --platform linux --dry-run --json

echo "ALL EXAMPLES OK"
