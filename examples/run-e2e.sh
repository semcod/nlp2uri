#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== pytest =="
python -m pytest

echo "== integration (x-scheme-handler) =="
export NLP2URI_INTEGRATION=1
python -m pytest tests/integration -m integration -q

for script in \
    examples/resolve/nl-to-uri/e2e.sh \
    examples/resolve/new-intents/e2e.sh \
    examples/execute/dry-run/e2e.sh \
    examples/mcp/tool-handoff/e2e.sh \
    examples/integrators/shell-export/e2e.sh \
    examples/integrators/mcp-stdio/e2e.sh
do
    echo "== $script =="
    bash "$script"
done

if command -v curl >/dev/null 2>&1; then
    echo "== examples/integrators/rest-api/e2e.sh =="
    bash examples/integrators/rest-api/e2e.sh
else
    echo "== skip rest-api (curl not installed) =="
fi

echo "== cli (auto platform from nlp2uri.yaml / host OS) =="
nlp2uri config show --json
nlp2uri plan "open firefox" --json
nlp2uri compile "app://firefox/open" --json
nlp2uri execute "capture screen" --dry-run --json
eval "$(nlp2uri shell export 'open firefox')"

echo "ALL EXAMPLES OK"
