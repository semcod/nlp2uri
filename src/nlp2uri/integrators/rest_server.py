"""stdlib HTTP REST server for nlp2uri."""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse

from nlp2uri import __version__
from nlp2uri.adapters.base import AdapterRequest
from nlp2uri.adapters.rest import RestAdapter
from nlp2uri.config import ensure_config, load_config


class NLP2URIRequestHandler(BaseHTTPRequestHandler):
    adapter: RestAdapter = RestAdapter()

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def _send(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        route = RestAdapter.match_route("GET", urlparse(self.path).path)
        if route is None:
            self._send(404, {"ok": False, "error": "not found"})
            return
        response = self.adapter.dispatch(route, AdapterRequest(operation=route))
        self._send(response.status_code, response.to_dict())

    def do_POST(self) -> None:  # noqa: N802
        route = RestAdapter.match_route("POST", urlparse(self.path).path)
        if route is None:
            self._send(404, {"ok": False, "error": "not found"})
            return
        try:
            body = self._read_json()
        except json.JSONDecodeError:
            self._send(400, {"ok": False, "error": "invalid json"})
            return
        response = self.adapter.dispatch(route, body)
        self._send(response.status_code, response.to_dict())


def run_server(host: str = "127.0.0.1", port: int = 8766) -> int:
    ensure_config()
    cfg = load_config()
    server = ThreadingHTTPServer((host, port), NLP2URIRequestHandler)
    platform = cfg.resolved_platform().value
    print(
        f"nlp2uri REST listening on http://{host}:{port} "
        f"(v{__version__}, platform={platform})",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nlp2uri-serve")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8766)
    args = parser.parse_args(argv)
    return run_server(host=args.host, port=args.port)


if __name__ == "__main__":
    raise SystemExit(main())
