#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

PORT="${NLP2URI_REST_PORT:-18767}"
python -m nlp2uri.integrators.rest_server --port "$PORT" &
pid=$!
trap 'kill "$pid" 2>/dev/null || true' EXIT

for _ in $(seq 1 30); do
  if curl -sf "http://127.0.0.1:${PORT}/health" >/dev/null; then
    break
  fi
  sleep 0.1
done

body="$(curl -sf -X POST "http://127.0.0.1:${PORT}/v1/plan" \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"open firefox"}')"
echo "$body" | grep -q 'app://firefox/open'
echo "examples/integrators/rest-api: OK"
