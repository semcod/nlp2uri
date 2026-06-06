"""resource:// driver probes."""

from __future__ import annotations

from nlp2uri.cqrs import CqrsDispatcher
from nlp2uri.host.resource import build_resource_actions
from nlp2uri.models import HostPlatform
from nlp2uri.systemmap import build_uri_index, compile_system_map_uri


def test_resource_filesystem_probe() -> None:
    actions = build_resource_actions("resource://filesystem/user", HostPlatform.LINUX)
    assert actions[0].command == "test"
    assert actions[0].args[0] == "-e"


def test_resource_smtp_probe() -> None:
    actions = build_resource_actions(
        "resource://smtp/default",
        HostPlatform.LINUX,
        config={"smtp_host": "127.0.0.1", "smtp_port": "2525"},
    )
    assert actions[0].command in ("nc", "bash")


def test_cqrs_resource_driver() -> None:
    d = CqrsDispatcher(platform=HostPlatform.LINUX)
    result = d.compile_uri("resource://filesystem/user", target="probe")
    assert result["ok"] is True
    probe = d.probe_uri("resource://filesystem/user", target="probe")
    assert probe["reachable"] is True


def test_resource_from_systemmap_index() -> None:
    ir = {
        "format": "nlp2dsl.system_map.v1",
        "example_id": "01-invoice",
        "resources": [{"id": "user", "connector": "filesystem", "uri_patterns": ["file://~/"]}],
    }
    index = build_uri_index(ir)
    entry = index.find_by_kind("resource")[0]
    actions = compile_system_map_uri(entry.uri, HostPlatform.LINUX)
    assert actions[0].command == "test"
