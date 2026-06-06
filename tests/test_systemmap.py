"""Tests for system_map_uri.v1 layer over env2llm SystemMapIR."""

from __future__ import annotations

import pytest

from nlp2uri.systemmap import (
    build_uri_index,
    env2llm_available,
    resolve_prompt_against_system_map,
    uri_for_command,
    uri_for_runtime,
)
from nlp2uri.systemmap.encode import encode_segment


def _sample_ir() -> dict:
    return {
        "format": "nlp2dsl.system_map.v1",
        "version": 1,
        "example_id": "01-invoice",
        "environment": {"NLP2DSL_BACKEND_URL": "http://localhost:8010"},
        "runtimes": [
            {"id": "executor:worker", "kind": "worker", "status": "available"},
            {"id": "orchestrator:nlp-service", "kind": "orchestrator", "status": "available"},
        ],
        "commands": [
            {
                "name": "send_invoice",
                "description": "Send invoice email with PDF attachment",
                "runtime": "executor:worker",
                "fields": [
                    {"name": "amount", "required": True},
                    {"name": "to", "required": True},
                ],
            }
        ],
        "resources": [
            {
                "id": "user",
                "title": "User filesystem",
                "connector": "filesystem",
                "uri_patterns": ["file://~/"],
            }
        ],
        "access": [
            {"agent": "mail_agent", "resource_area": "email", "actions": ["send", "read"]}
        ],
        "artifacts": [{"path": "invoices/out.pdf", "kind": "file"}],
        "conversation": {"autofill": True},
        "process": {"mode": "balanced"},
        "validations": [{"code": "profile.dsl_action", "action": "send_invoice"}],
    }


def test_encode_segment_colon() -> None:
    assert encode_segment("executor:worker") == "executor%3Aworker"


def test_uri_for_runtime_and_command() -> None:
    ir = _sample_ir()
    rt_uri = uri_for_runtime(ir["runtimes"][0])
    assert rt_uri == "runtime://worker/executor%3Aworker"

    cmd_uri = uri_for_command(ir["commands"][0])
    assert cmd_uri == "command://executor%3Aworker/send_invoice"


def test_build_uri_index_covers_entities() -> None:
    index = build_uri_index(_sample_ir())
    assert index.format == "system_map_uri.v1"
    assert index.example_id == "01-invoice"
    assert index.find_command("send_invoice") is not None
    kinds = {entry.kind for entry in index.entries.values()}
    assert {
        "environment",
        "runtime",
        "command",
        "resource",
        "access",
        "artifact",
        "conversation",
        "process",
        "validation",
    }.issubset(kinds)

    cmd = index.find_command("send_invoice")
    assert cmd is not None
    assert "runtime://worker/executor%3Aworker" in cmd.links


def test_resolve_prompt_command_name() -> None:
    ir = _sample_ir()
    hits = resolve_prompt_against_system_map("please send_invoice for 1500", ir)
    assert hits
    assert hits[0].kind == "command"
    assert hits[0].entry_name == "send_invoice"
    assert "send_invoice" in hits[0].uri


def test_resolve_prompt_command_spaced_name() -> None:
    ir = _sample_ir()
    hits = resolve_prompt_against_system_map("send invoice to client@example.com", ir)
    assert hits
    assert hits[0].entry_name == "send_invoice"


def test_resolve_prompt_runtime() -> None:
    ir = _sample_ir()
    hits = resolve_prompt_against_system_map("check orchestrator:nlp-service health", ir)
    assert any(hit.kind == "runtime" for hit in hits)


@pytest.mark.skipif(not env2llm_available(), reason="env2llm not installed")
def test_env2llm_roundtrip_index(tmp_path) -> None:
    from env2llm.ir import SystemMapIR
    from env2llm.system_map_render import render_system_map_doql
    from nlp2uri.systemmap.load import load_system_map_from_doql

    ir = SystemMapIR.model_validate(_sample_ir())
    doql = render_system_map_doql(ir)
    path = tmp_path / "environment.doql.less"
    path.write_text(doql, encoding="utf-8")
    loaded = load_system_map_from_doql(path)
    index = build_uri_index(loaded)
    assert index.find_command("send_invoice") is not None
