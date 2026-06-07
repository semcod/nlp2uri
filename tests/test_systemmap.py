"""Tests for system_map_uri.v1 layer over env2llm SystemMapIR."""

from __future__ import annotations

import pytest

from nlp2uri.compile import compile_uri_to_actions
from nlp2uri.models import HostPlatform
from nlp2uri.systemmap import (
    build_uri_index,
    compile_system_map_uri,
    env2llm_available,
    is_system_map_uri,
    resolve_prompt_against_system_map,
    resolve_prompt_with_fallback,
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


def test_is_system_map_uri() -> None:
    assert is_system_map_uri("command://executor%3Aworker/send_invoice")
    assert not is_system_map_uri("app://firefox/open")


def test_compile_command_handoff() -> None:
    uri = uri_for_command(_sample_ir()["commands"][0])
    actions = compile_system_map_uri(uri, HostPlatform.LINUX, config={"amount": "1500", "to": "a@b.pl"})
    assert len(actions) == 1
    assert actions[0].command == "curl"
    argv = " ".join(actions[0].argv())
    assert "/workflow/run" in argv
    assert "send_invoice" in argv


def test_compile_uri_to_actions_command_scheme() -> None:
    uri = "command://executor%3Aworker/send_invoice?amount=1500&to=a%40b.pl"
    actions = compile_uri_to_actions(uri, HostPlatform.LINUX)
    assert actions[0].command == "curl"
    assert "send_invoice" in " ".join(actions[0].argv())


def test_resolve_fallback_system_map_first() -> None:
    ir = _sample_ir()
    out = resolve_prompt_with_fallback("send invoice", ir, platform=HostPlatform.LINUX)
    assert out["source"] == "system_map"
    assert "send_invoice" in out["uri"]


def test_resolve_fallback_desktop_when_no_ir_match() -> None:
    ir = _sample_ir()
    out = resolve_prompt_with_fallback("open firefox", ir, platform=HostPlatform.LINUX)
    assert out["source"] == "desktop"
    assert out["uri"].startswith("app://firefox/open")


def test_resolve_fallback_desktop_without_ir() -> None:
    out = resolve_prompt_with_fallback("capture screen", ir=None, platform=HostPlatform.LINUX)
    assert out["source"] == "desktop"
    assert out["uri"].startswith("desktop-screenshot://")


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


@pytest.mark.skipif(not env2llm_available(), reason="env2llm not installed")
def test_apply_desktop_uri_mapping_and_index() -> None:
    from env2llm.ir import DesktopProbeIR, DesktopWindowIR, SystemMapIR

    from nlp2uri.systemmap.export import apply_desktop_uri_mapping

    ir = SystemMapIR(example_id="demo")
    ir.desktop = DesktopProbeIR(
        platform="linux",
        session="GNOME",
        windows=[
            DesktopWindowIR(
                id="0x01200004",
                title="Mozilla Firefox",
                active=True,
            )
        ],
        status="available",
    )
    apply_desktop_uri_mapping(ir)

    assert ir.data["desktop.windows[0].focus_uri"].startswith("desktop-window://focus")
    assert ir.data["desktop.windows[0].screenshot_uri"].startswith("desktop-screenshot://window")
    assert "title=Mozilla" in ir.data["desktop.windows[0].focus_uri"]
    assert ir.data["desktop.active_window.focus_uri"] == ir.data["desktop.windows[0].focus_uri"]

    index = build_uri_index(ir)
    windows = index.find_by_kind("desktop_window")
    assert len(windows) == 1
    assert windows[0].uri.startswith("desktop-window://focus")
    captures = index.find_by_kind("desktop_window_capture")
    assert len(captures) == 1


@pytest.mark.skipif(not env2llm_available(), reason="env2llm not installed")
def test_write_environment_map_includes_desktop_uris(tmp_path, monkeypatch) -> None:
    from env2llm.ir import DesktopProbeIR, DesktopWindowIR, SystemMapIR

    from nlp2uri.systemmap.export import write_environment_map

    probe = DesktopProbeIR(
        platform="linux",
        session="GNOME",
        tools_used=["wmctrl"],
        windows=[DesktopWindowIR(id="0x1", title="Terminal", active=True)],
        probed_at="2026-06-06T12:00:00+00:00",
        status="available",
    )

    def fake_generate(_root, *, example_id=None, environment=None, client=None):
        return SystemMapIR(example_id=example_id or "proj")

    monkeypatch.setattr("env2llm.generate.generate_system_map", fake_generate)
    monkeypatch.setattr(
        "env2llm.policy.desktop.collect_desktop_probe",
        lambda: probe,
    )

    path = write_environment_map(tmp_path, probe_desktop=True)
    content = path.read_text(encoding="utf-8")

    assert path.is_file()
    assert "desktop.windows[0].focus_uri" in content
    assert "desktop-window://focus" in content
    assert "desktop-screenshot://window" in content


def test_resolve_koru_mcp_command_aliases() -> None:
    ir = {
        "format": "nlp2dsl.system_map.v1",
        "version": 1,
        "example_id": "koru",
        "runtimes": [
            {"id": "mcp:koru", "kind": "external", "status": "available"},
        ],
        "commands": [
            {
                "name": "koru_list_tickets",
                "description": "List open koru tickets for a given project (planfile queue).",
                "runtime": "mcp:koru",
            },
            {
                "name": "koru_run_quality_gates",
                "description": "Run koru quality gates (regix, redup, vallm, sumr, etc.) for a project.",
                "runtime": "mcp:koru",
            },
        ],
    }
    tickets = resolve_prompt_against_system_map("list tickets", ir)
    assert tickets
    assert tickets[0].entry_name == "koru_list_tickets"
    assert tickets[0].uri.startswith("command://")

    gates = resolve_prompt_against_system_map("run quality gates", ir)
    assert gates
    assert gates[0].entry_name == "koru_run_quality_gates"
