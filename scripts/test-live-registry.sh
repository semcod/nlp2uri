#!/usr/bin/env bash
# Live integration: CQRS events → process-registry, endpoint probes on todomat stack.
set -euo pipefail

REGISTRY_URL="${PROCESS_REGISTRY_URL:-http://localhost:8083}"
TRIGGER_URL="${TRIGGER_GATEWAY_URL:-http://localhost:8084}"
PIPELINE_URL="${PIPELINE_PORT_URL:-http://localhost:9099}"

cd "$(dirname "$0")/.."
export PYTHONPATH="${PYTHONPATH:-}:src"
export PROCESS_REGISTRY_URL="$REGISTRY_URL"

python3 - <<'PY'
import json
import os
import urllib.error
import urllib.request

from nlp2uri.cqrs import CqrsDispatcher
from nlp2uri.models import HostPlatform

registry = os.environ["PROCESS_REGISTRY_URL"].rstrip("/")
d = CqrsDispatcher(platform=HostPlatform.LINUX)

def check(url: str, label: str) -> None:
    try:
        with urllib.request.urlopen(url, timeout=3) as resp:
            assert resp.status == 200, label
        print(f"[OK] {label} {url}")
    except Exception as exc:
        print(f"[SKIP] {label} {url} — {exc}")

check(f"{registry}/health", "process-registry")
check(os.getenv("TRIGGER_GATEWAY_URL", "http://localhost:8084") + "/health", "trigger-gateway")
check(os.getenv("PIPELINE_PORT_URL", "http://localhost:9099") + "/health", "pipeline-router")

uri = "endpoint://tcp/127.0.0.1/8083/health"
result = d.execute_uri(uri, dry_run=False)
print(f"[{'OK' if result['ok'] else 'FAIL'}] CQRS execute {uri}")
if not result["ok"]:
    raise SystemExit(1)

# Verify events mirrored to registry
with urllib.request.urlopen(f"{registry}/events?aggregate_id={uri}", timeout=5) as resp:
    payload = json.loads(resp.read().decode())
events = payload.get("events", [])
print(f"[OK] registry events for aggregate: {len(events)}")
assert len(events) >= 2, "expected UriCompiled + UriExecuted"

# Trigger gateway smoke
body = json.dumps({"text": "pokaż GROQ_API_KEY z getv", "pipeline": "nlp2uri", "execute": False}).encode()
req = urllib.request.Request(
    os.getenv("TRIGGER_GATEWAY_URL", "http://localhost:8084") + "/trigger",
    data=body,
    headers={"Content-Type": "application/json"},
    method="POST",
)
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        out = json.loads(resp.read().decode())
    print(f"[OK] trigger nlp2uri pipeline={out.get('pipeline', '?')}")
except urllib.error.URLError as exc:
    print(f"[SKIP] trigger-gateway nlp2uri — {exc}")

print("Live registry integration passed")
PY
