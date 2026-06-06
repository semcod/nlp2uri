"""Platform-specific URI executors."""

from nlp2uri.platforms.base import UriExecutor
from nlp2uri.platforms.registry import get_executor

__all__ = ["UriExecutor", "get_executor"]
