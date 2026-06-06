"""Surface adapters for nlp2uri (CLI, REST, MCP, shell)."""

from nlp2uri.adapters.base import AdapterRequest, AdapterResponse, BaseAdapter
from nlp2uri.adapters.cli import CliAdapter
from nlp2uri.adapters.mcp import McpAdapter
from nlp2uri.adapters.rest import RestAdapter
from nlp2uri.adapters.shell import ShellAdapter

__all__ = [
    "AdapterRequest",
    "AdapterResponse",
    "BaseAdapter",
    "CliAdapter",
    "McpAdapter",
    "RestAdapter",
    "ShellAdapter",
]
