"""Backward-compatible MCP helpers (prefer nlp2uri.adapters.mcp)."""

from __future__ import annotations

from typing import Any

from nlp2uri.adapters.mcp import MCP_TOOLS, McpAdapter
from nlp2uri.models import HostPlatform

_adapter = McpAdapter()


def text_uri_list(uris: list[str]) -> dict[str, Any]:
    body = "\r\n".join(uris) + ("\r\n" if uris else "")
    return {"type": "resource", "mimeType": "text/uri-list", "text": body}


def ui_resource(uri: str, *, title: str = "Desktop action") -> dict[str, Any]:
    return {
        "type": "resource",
        "mimeType": "text/uri-list",
        "uri": uri,
        "name": title,
        "description": f"Execute desktop action: {uri}",
    }


def tool_resolve_desktop_action(text: str, *, platform: HostPlatform | None = None) -> dict[str, Any]:
    args = {"prompt": text}
    if platform is not None:
        args["platform"] = platform.value
    response = _adapter.call_tool("nlp2uri_resolve", args)
    return {
        "tool": "resolve_desktop_action",
        "content": response.data.get("mcp_content", []),
        "structuredContent": response.data,
    }


def tool_execute_desktop_uri(
    uri: str,
    *,
    platform: HostPlatform | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    args = {"uri": uri, "dry_run": dry_run}
    if platform is not None:
        args["platform"] = platform.value
    response = _adapter.call_tool("nlp2uri_execute", args)
    return {
        "tool": "execute_desktop_uri",
        "content": response.data.get("mcp_content", []),
        "structuredContent": response.data,
    }


def mcp_handoff_payload(text: str, *, platform: HostPlatform | None = None) -> dict[str, Any]:
    args = {"prompt": text}
    if platform is not None:
        args["platform"] = platform.value
    response = _adapter.call_tool("nlp2uri_plan", args)
    data = response.data
    return {
        "tool": "resolve_desktop_action",
        "input": {"text": text},
        "output": data.get("spec", data),
        "actions": data.get("actions", []),
        "mcp_content": data.get("mcp_content", []),
        "next_step": "Pass output.uri to execute_desktop_uri or host desktop automation backend.",
    }


__all__ = [
    "MCP_TOOLS",
    "McpAdapter",
    "mcp_handoff_payload",
    "text_uri_list",
    "tool_execute_desktop_uri",
    "tool_resolve_desktop_action",
    "ui_resource",
]
