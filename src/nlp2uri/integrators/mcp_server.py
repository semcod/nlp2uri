"""Stdio MCP server for nlp2uri tools."""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from typing import Any

from nlp2uri import __version__
from nlp2uri.adapters.mcp import MCP_TOOLS, McpAdapter
from nlp2uri.config import ensure_config, load_config

_PROTOCOL_VERSION = "2024-11-05"
_SERVER_NAME = "nlp2uri"
_NOTIFICATIONS = frozenset({"notifications/initialized", "notifications/cancelled"})


def _jsonrpc_response(req_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def _jsonrpc_error(req_id: Any, code: int, message: str, data: Any = None) -> dict[str, Any]:
    err: dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        err["data"] = data
    return {"jsonrpc": "2.0", "id": req_id, "error": err}


def _write_json(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, separators=(",", ":"), default=str) + "\n")
    sys.stdout.flush()


def _log(message: str) -> None:
    print(message, file=sys.stderr)


def _handle_initialize(_params: dict[str, Any]) -> dict[str, Any]:
    return {
        "protocolVersion": _PROTOCOL_VERSION,
        "capabilities": {"tools": {}},
        "serverInfo": {"name": _SERVER_NAME, "version": __version__},
    }


def _handle_tools_list(_params: dict[str, Any]) -> dict[str, Any]:
    return {"tools": MCP_TOOLS}


def _handle_tools_call(params: dict[str, Any], *, adapter: McpAdapter) -> dict[str, Any]:
    tool_name = str(params.get("name") or "")
    arguments = params.get("arguments") or {}
    try:
        response = adapter.call_tool(tool_name, arguments)
        if not response.ok:
            return {
                "content": [{"type": "text", "text": response.error or "tool failed"}],
                "isError": True,
            }
        return {
            "content": response.data.get(
                "mcp_content",
                [{"type": "text", "text": json.dumps(response.data, indent=2, default=str)}],
            ),
        }
    except Exception as exc:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error in {tool_name}: {exc}\n{traceback.format_exc()}",
                }
            ],
            "isError": True,
        }


def handle_message(msg: dict[str, Any], *, adapter: McpAdapter) -> dict[str, Any] | None:
    req_id = msg.get("id")
    method = msg.get("method", "")

    if method in _NOTIFICATIONS:
        return None

    if method == "initialize":
        return _jsonrpc_response(req_id, _handle_initialize(msg.get("params") or {}))
    if method == "tools/list":
        return _jsonrpc_response(req_id, _handle_tools_list(msg.get("params") or {}))
    if method == "tools/call":
        return _jsonrpc_response(
            req_id,
            _handle_tools_call(msg.get("params") or {}, adapter=adapter),
        )

    return _jsonrpc_error(req_id, -32601, f"Method not found: {method}")


def run_stdio(*, adapter: McpAdapter | None = None) -> int:
    ensure_config()
    adapter = adapter or McpAdapter()
    cfg = load_config()
    _log(f"nlp2uri mcp-server: started (stdio, platform={cfg.resolved_platform().value})")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError as exc:
            _write_json(_jsonrpc_error(None, -32700, f"Parse error: {exc}"))
            continue
        response = handle_message(msg, adapter=adapter)
        if response is not None:
            _write_json(response)
    _log("nlp2uri mcp-server: stdin closed, exiting")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nlp2uri-mcp")
    parser.parse_args(argv)
    return run_stdio()


if __name__ == "__main__":
    raise SystemExit(main())
