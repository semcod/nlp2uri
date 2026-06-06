"""Adapter layer tests."""

from __future__ import annotations

import json

from nlp2uri.adapters.base import AdapterRequest
from nlp2uri.adapters.cli import CliAdapter
from nlp2uri.adapters.mcp import McpAdapter
from nlp2uri.adapters.rest import RestAdapter
from nlp2uri.adapters.shell import ShellAdapter
from nlp2uri.integrators.mcp_server import handle_message
from nlp2uri.models import HostPlatform


def test_cli_adapter_plan():
    response = CliAdapter().handle(
        AdapterRequest(operation="plan", prompt="open firefox", platform=HostPlatform.LINUX)
    )
    assert response.ok
    assert response.data["uri"].startswith("app://firefox/open")


def test_rest_adapter_plan():
    response = RestAdapter().dispatch(
        "plan",
        {"prompt": "open firefox", "platform": "linux"},
    )
    assert response.ok
    assert "uri" in response.data


def test_shell_adapter_export():
    response = ShellAdapter().handle(
        AdapterRequest(operation="export", prompt="open firefox", platform=HostPlatform.LINUX)
    )
    assert response.ok
    assert "NLP2URI_URI=" in response.data["script"]
    assert "app://firefox/open" in response.data["script"]


def test_mcp_adapter_tools():
    adapter = McpAdapter()
    response = adapter.call_tool(
        "nlp2uri_plan",
        {"prompt": "capture screen", "platform": "linux"},
    )
    assert response.ok
    assert response.data["uri"].startswith("desktop-screenshot://")
    assert response.data["mcp_content"]


def test_mcp_stdio_initialize():
    adapter = McpAdapter()
    msg = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
    out = handle_message(msg, adapter=adapter)
    assert out is not None
    assert out["result"]["serverInfo"]["name"] == "nlp2uri"


def test_mcp_stdio_tools_call():
    adapter = McpAdapter()
    msg = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "nlp2uri_resolve",
            "arguments": {"prompt": "open firefox", "platform": "linux"},
        },
    }
    out = handle_message(msg, adapter=adapter)
    assert out is not None
    text = out["result"]["content"][0]["text"]
    assert "app://firefox/open" in text or "firefox" in text
