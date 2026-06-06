"""Load SystemMapIR from MCP / service arguments."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nlp2uri.systemmap.load import (
    env2llm_available,
    env2llm_missing_message,
    load_system_map_from_doql,
    load_system_map_from_example,
)


def load_ir_from_arguments(arguments: dict[str, Any]) -> Any:
    """Resolve IR from inline dict, DOQL path, or nlp2dsl example directory."""
    if arguments.get("system_map"):
        raw = arguments["system_map"]
        if isinstance(raw, str):
            raw = json.loads(raw)
        return _coerce_ir(raw)

    doql_path = arguments.get("doql_path") or arguments.get("environment_path")
    if doql_path:
        return load_system_map_from_doql(Path(doql_path))

    example_dir = arguments.get("example_dir")
    if example_dir:
        return load_system_map_from_example(
            Path(example_dir),
            example_id=str(arguments.get("example_id") or ""),
        )

    raise ValueError(
        "provide one of: system_map (dict/JSON), doql_path, or example_dir "
        f"({env2llm_missing_message() if not env2llm_available() else 'env2llm ok'})"
    )


def _coerce_ir(raw: dict[str, Any]) -> Any:
    if env2llm_available():
        from env2llm.ir import SystemMapIR

        return SystemMapIR.model_validate(raw)
    return raw
