"""MCP helper tests."""

from __future__ import annotations

from nlp2uri.mcp import mcp_handoff_payload, text_uri_list, tool_resolve_desktop_action
from nlp2uri.models import HostPlatform


def test_text_uri_list_mime():
    payload = text_uri_list(["app://firefox/open", "desktop-screenshot://screen"])
    assert payload["mimeType"] == "text/uri-list"
    assert "app://firefox/open" in payload["text"]


def test_tool_resolve_desktop_action():
    payload = tool_resolve_desktop_action("open firefox", platform=HostPlatform.LINUX)
    assert payload["tool"] == "resolve_desktop_action"
    assert payload["structuredContent"]["uri"].startswith("app://firefox/open")


def test_mcp_handoff_includes_actions():
    payload = mcp_handoff_payload("capture screen", platform=HostPlatform.LINUX)
    assert payload["actions"]
    assert payload["mcp_content"]
