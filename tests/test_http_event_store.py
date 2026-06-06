"""HttpEventStore + process-registry /events contract."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from nlp2uri.cqrs.http_store import HttpEventStore


class _Handler(BaseHTTPRequestHandler):
    events: list[dict] = []

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        if self.path == "/events":
            _Handler.events.append(body)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(body).encode())
            return
        self.send_response(404)
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        return


def test_http_event_store_posts_to_registry() -> None:
    _Handler.events.clear()
    server = HTTPServer(("127.0.0.1", 0), _Handler)
    port = server.server_address[1]
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        store = HttpEventStore(base_url=f"http://127.0.0.1:{port}")
        store.append(
            "command://x/y",
            scheme="command",
            event_type="UriCompiled",
            payload={"ok": True},
        )
        assert len(store.get_stream("command://x/y")) == 1
        assert len(_Handler.events) == 1
        assert _Handler.events[0]["aggregate_id"] == "command://x/y"
    finally:
        server.shutdown()
