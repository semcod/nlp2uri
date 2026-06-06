"""REST integrator smoke tests."""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request

from nlp2uri.integrators.rest_server import run_server


def _post(url: str, payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode("utf-8"))


def test_rest_server_plan():
    port = 18766
    thread = threading.Thread(target=run_server, kwargs={"host": "127.0.0.1", "port": port}, daemon=True)
    thread.start()

    import time

    for _ in range(30):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=1) as resp:
                assert resp.status == 200
            break
        except urllib.error.URLError:
            time.sleep(0.1)
    else:
        raise AssertionError("rest server did not start")

    data = _post(
        f"http://127.0.0.1:{port}/v1/plan",
        {"prompt": "open firefox", "platform": "linux"},
    )
    assert data["ok"] is True
    assert data["uri"].startswith("app://firefox/open")
