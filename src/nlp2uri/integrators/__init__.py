"""Runnable integrators (stdio MCP, HTTP REST)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

__all__ = ["run_mcp_stdio", "run_rest_server"]

if TYPE_CHECKING:
    from collections.abc import Callable


def __getattr__(name: str) -> Any:
    if name == "run_mcp_stdio":
        from nlp2uri.integrators.mcp_server import run_stdio

        return run_stdio
    if name == "run_rest_server":
        from nlp2uri.integrators.rest_server import run_server

        return run_server
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
