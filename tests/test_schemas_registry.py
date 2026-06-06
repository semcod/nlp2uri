"""uri_cqrs_es.v1 registry and scaffold consistency."""

from __future__ import annotations

from pathlib import Path

import yaml

SCHEMAS = Path(__file__).resolve().parents[1] / "schemas"
REGISTRY = SCHEMAS / "registry.yaml"
REQUIRED_PROTO = (
    "aggregate.proto",
    "commands.proto",
    "events.proto",
    "queries.proto",
    "driver.proto",
    "api.proto",
    "openapi.yaml",
    "README.md",
)


def test_registry_loads() -> None:
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    assert data["format"] == "uri_cqrs_es_registry.v1"
    assert len(data["schemes"]) >= 20


def test_every_scheme_has_cqrs_tree() -> None:
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    for scheme, meta in data["schemes"].items():
        version = meta.get("version", "v1")
        base = SCHEMAS / "schemes" / scheme / version
        for name in REQUIRED_PROTO:
            assert (base / name).is_file(), f"missing {scheme}/{version}/{name}"


def test_common_protos_exist() -> None:
    common = SCHEMAS / "common" / "v1"
    for name in ("uri.proto", "commands.proto", "events.proto", "queries.proto", "driver.proto", "api.proto"):
        assert (common / name).is_file()


def test_generated_mcp_tools_match_registry() -> None:
    import json

    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    tools_path = Path(__file__).resolve().parents[1] / "generated" / "mcp" / "tools.json"
    if not tools_path.exists():
        return
    tools = json.loads(tools_path.read_text(encoding="utf-8"))
    assert len(tools) == len(data["schemes"])
