"""Load SystemMapIR from env2llm (optional dependency)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

_ENV2LLM_IMPORT_ERROR: str | None = None

try:
    from env2llm import generate_system_map
    from env2llm.bridge import doql_file_to_system_map

    _ENV2LLM_AVAILABLE = True
except ImportError as exc:
    _ENV2LLM_AVAILABLE = False
    _ENV2LLM_IMPORT_ERROR = str(exc)
    generate_system_map = None  # type: ignore[assignment,misc]
    doql_file_to_system_map = None  # type: ignore[assignment,misc]


def env2llm_available() -> bool:
    return _ENV2LLM_AVAILABLE


def env2llm_missing_message() -> str:
    if _ENV2LLM_IMPORT_ERROR:
        return (
            f"env2llm is not installed ({_ENV2LLM_IMPORT_ERROR}). "
            "Install with: pip install 'nlp2uri[envmap]' or pip install env2llm>=0.1.3"
        )
    return "env2llm is not installed. Install with: pip install 'nlp2uri[envmap]'"


def load_system_map_from_doql(path: Path | str) -> Any:
    """Parse ``environment.doql.less`` → SystemMapIR."""
    if not _ENV2LLM_AVAILABLE:
        raise RuntimeError(env2llm_missing_message())
    return doql_file_to_system_map(path)


def load_system_map_from_example(example_dir: Path | str, *, example_id: str = "") -> Any:
    """Run env2llm introspection on an nlp2dsl example directory."""
    if not _ENV2LLM_AVAILABLE:
        raise RuntimeError(env2llm_missing_message())
    return generate_system_map(example_dir, example_id=example_id or None)
