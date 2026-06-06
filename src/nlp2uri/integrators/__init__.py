"""Runnable integrators (stdio MCP, HTTP REST)."""

from nlp2uri.integrators.mcp_server import run_stdio as run_mcp_stdio
from nlp2uri.integrators.rest_server import run_server as run_rest_server

__all__ = ["run_mcp_stdio", "run_rest_server"]
