"""SystemMap URI index from Koru autopilot status."""

from __future__ import annotations

from nlp2uri.adapters.mcp import McpAdapter
from nlp2uri.adapters.base import AdapterRequest
from nlp2uri.control_compile import compile_uri_to_control_plan
from nlp2uri.control_execute import compile_and_execute_control_uri
from nlp2uri.parse_nl import parse_text
from nlp2uri.systemmap.koru_ide import build_koru_ide_uri_index
from nlp2uri.models import HostPlatform, IntentKind


SAMPLE_STATUS = {
    "daemon": {"version": "0.1.317", "pid": 12345},
    "plugins": [
        {
            "ide": "cursor",
            "version": "0.2.34",
            "buildSha": "abc123",
            "protocolVersion": 2,
            "workspaceFolders": ["/home/tom/github/semcod/koru"],
            "workspaceName": "koru",
            "commandCatalog": {
                "submit": ["workbench.action.chat.submit"],
            },
        }
    ],
}


def test_build_koru_ide_uri_index_entries():
    index = build_koru_ide_uri_index(
        SAMPLE_STATUS,
        socket_path="/run/user/1000/koru-autopilot-cursor.sock",
    )
    kinds = {entry.kind for entry in index.entries.values()}
    assert "ide" in kinds
    assert "ide_plugin" in kinds
    assert "ide_workspace" in kinds
    assert "ide_chat" in kinds
    assert "control_surface" in kinds
    assert any(uri.startswith("ide-chat://cursor/send") for uri in index.entries)
    assert any("workbench.action.chat.submit" in uri for uri in index.entries)


def test_mcp_compile_control_tool():
    adapter = McpAdapter()
    response = adapter.call_tool(
        "nlp2uri_compile_control",
        {
            "uri": "ide-chat://cursor/send?workspace=/tmp/koru&submit=true",
            "text": "hello",
        },
    )
    assert response.ok is True
    plan = response.data["control_plan"]["actions"][0]
    assert plan["command_version"] == "koru.control.v1"
    assert plan["transport"] == "koruide_socket"


def test_mcp_execute_control_dry_run():
    adapter = McpAdapter()
    response = adapter.call_tool(
        "nlp2uri_execute_control",
        {
            "uri": "koru-control://ide/status?ide=cursor",
            "dry_run": True,
        },
    )
    assert response.ok is True
    assert response.data["results"][0]["dry_run"] is True


def test_mcp_list_koru_ide_uris():
    adapter = McpAdapter()
    response = adapter.call_tool(
        "nlp2uri_list_koru_ide_uris",
        {
            "status": SAMPLE_STATUS,
            "socket_path": "/tmp/koru.sock",
        },
    )
    assert response.ok is True
    assert response.data["count"] >= 5


def test_parse_polish_ide_command():
    intent = parse_text("uruchom komendę workbench.action.chat.submit w Cursor")
    assert intent.kind == IntentKind.IDE_COMMAND
    assert intent.params["command"] == "workbench.action.chat.submit"
    assert intent.params["ide"] == "cursor"


def test_round_trip_nl_to_control_plan_dry_run():
    from nlp2uri.resolve import nlp2uri

    result = nlp2uri("wyślij probe do cursor", os=HostPlatform.LINUX)
    assert result.control_plan is not None
    payload = compile_and_execute_control_uri(
        result.uri,
        text=result.spec.metadata.get("text") or "probe",
        dry_run=True,
    )
    assert payload["ok"] is True
    assert payload["results"][0]["verification_status"] == "planned"
