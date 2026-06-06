"""MCP server integration helpers."""

from __future__ import annotations

from typing import Any

from nlp2uri.compile import compile_uri_to_actions
from nlp2uri.models import HostPlatform, NLP2URIResult
from nlp2uri.resolve import nlp2uri, resolve_text
from nlp2uri.runtime import execute_uri


def text_uri_list(uris: list[str]) -> dict[str, Any]:
    """MIME bundle for MCP `text/uri-list` content."""
    body = "\r\n".join(uris) + ("\r\n" if uris else "")
    return {
        "type": "resource",
        "mimeType": "text/uri-list",
        "text": body,
    }


def ui_resource(uri: str, *, title: str = "Desktop action") -> dict[str, Any]:
    """MCP Apps / MCP-UI style clickable action resource."""
    return {
        "type": "resource",
        "mimeType": "text/uri-list",
        "uri": uri,
        "name": title,
        "description": f"Execute desktop action: {uri}",
    }


def tool_resolve_desktop_action(
    text: str,
    *,
    platform: HostPlatform | None = None,
) -> dict[str, Any]:
    result = nlp2uri(text, os=platform)
    return {
        "tool": "resolve_desktop_action",
        "content": [
            {"type": "text", "text": result.uri},
            text_uri_list([result.uri]),
        ],
        "structuredContent": result.to_dict(),
    }


def tool_execute_desktop_uri(
    uri: str,
    *,
    platform: HostPlatform | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    actions = compile_uri_to_actions(uri, platform)
    result = execute_uri(uri, platform=platform, dry_run=dry_run)
    return {
        "tool": "execute_desktop_uri",
        "content": [
            {
                "type": "text",
                "text": result.output or result.error or result.uri,
            }
        ],
        "structuredContent": {
            "uri": uri,
            "dry_run": dry_run,
            "actions": [a.to_dict() for a in actions],
            "result": result.to_dict(),
        },
    }


def tool_resolve_and_plan(text: str, *, platform: HostPlatform | None = None) -> NLP2URIResult:
    return nlp2uri(text, os=platform)


def mcp_handoff_payload(text: str, *, platform: HostPlatform | None = None) -> dict[str, Any]:
    spec = resolve_text(text, platform=platform)
    actions = compile_uri_to_actions(spec.uri, platform)
    return {
        "tool": "resolve_desktop_action",
        "input": {"text": text},
        "output": spec.to_dict(),
        "actions": [a.to_dict() for a in actions],
        "mcp_content": [
            text_uri_list([spec.uri]),
            ui_resource(spec.uri, title=text),
        ],
        "next_step": "Pass output.uri to execute_desktop_uri or host desktop automation backend.",
    }
