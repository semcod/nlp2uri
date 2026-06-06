#!/usr/bin/env bash
# Smoke test CQRS drivers against local endpoints (todomat stack optional).
set -euo pipefail

cd "$(dirname "$0")/.."
export PYTHONPATH="${PYTHONPATH:-}:src"

python3 - <<'PY'
from nlp2uri.cqrs import CqrsDispatcher
from nlp2uri.models import HostPlatform

d = CqrsDispatcher(platform=HostPlatform.LINUX)

checks = [
    ("command://executor%3Aworker/send_invoice", "curl"),
    ("getv://llm/groq/GROQ_API_KEY", "getv_cli"),
    ("endpoint://tcp/127.0.0.1/8010/health", "curl"),
    ("service://generated/process-registry", "curl"),
    ("app://firefox/open", None),
]

import tempfile
from pathlib import Path
with tempfile.TemporaryDirectory() as tmp:
    p = Path(tmp) / "smoke.txt"
    p.write_text("ok", encoding="utf-8")
    r = d.compile_uri(f"artifact://demo/smoke.txt", target="filesystem", config={"example_dir": tmp})
    print(f"[{'OK' if r['ok'] else 'FAIL'}] artifact://demo/smoke.txt")
    if not r["ok"]:
        raise SystemExit(1)

for uri, target in checks:
    r = d.compile_uri(uri, target=target)
    status = "OK" if r["ok"] else "FAIL"
    print(f"[{status}] {uri}")
    if not r["ok"]:
        print(f"       {r.get('error')}")
        raise SystemExit(1)
    if r["actions"]:
        print(f"       → {r['actions'][0]['command']} {' '.join(r['actions'][0].get('args', [])[:4])}")

# Optional live probe (non-fatal)
for uri in (
    "endpoint://tcp/127.0.0.1/8084/health",
    "endpoint://tcp/127.0.0.1/9099/health",
):
    ex = d.execute_uri(uri, dry_run=False)
    if ex["ok"]:
        print(f"[LIVE OK] {uri}")
    else:
        print(f"[LIVE SKIP] {uri} — {ex.get('error', ex.get('output', ''))[:80]}")

print("CQRS smoke passed")
PY
