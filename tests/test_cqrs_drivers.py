"""CQRS driver registry, dispatcher, and reference drivers."""

from __future__ import annotations

from nlp2uri.compile import compile_uri_to_actions
from nlp2uri.cqrs import CqrsDispatcher, DriverRegistry, InMemoryEventStore
from nlp2uri.host.endpoint import build_endpoint_url
from nlp2uri.cqrs.registry import default_registry
from nlp2uri.models import HostPlatform


def test_registry_loads_all_schemes() -> None:
    reg = default_registry()
    assert len(reg.schemes) >= 20
    assert reg.default_target("command") == "curl"
    assert reg.default_target("getv") == "getv_cli"


def test_command_curl_driver_compile() -> None:
    d = CqrsDispatcher(platform=HostPlatform.LINUX)
    result = d.compile_uri("command://executor%3Aworker/send_invoice")
    assert result["ok"] is True
    assert result["actions"][0]["command"] == "curl"
    assert "workflow/run" in result["actions"][0]["args"][2]
    assert "send_invoice" in result["actions"][0]["args"][-1]


def test_getv_driver_compile() -> None:
    d = CqrsDispatcher(platform=HostPlatform.LINUX)
    result = d.compile_uri("getv://llm/groq/GROQ_API_KEY")
    assert result["ok"] is True
    assert result["actions"][0]["command"].endswith("getv")


def test_endpoint_driver_compile() -> None:
    assert build_endpoint_url("endpoint://tcp/127.0.0.1/8010/health") == "http://127.0.0.1:8010/health"
    d = CqrsDispatcher(platform=HostPlatform.LINUX)
    result = d.compile_uri("endpoint://tcp/127.0.0.1/8010/health")
    assert result["ok"] is True
    assert result["actions"][0]["args"] == ["-sf", "http://127.0.0.1:8010/health"]


def test_endpoint_via_compile_uri_to_actions() -> None:
    actions = compile_uri_to_actions("endpoint://tcp/127.0.0.1/9099/health", os=HostPlatform.LINUX)
    assert actions[0].command == "curl"
    assert "9099" in actions[0].args[1]


def test_app_delegate_driver() -> None:
    d = CqrsDispatcher(platform=HostPlatform.LINUX)
    result = d.compile_uri("app://firefox/open")
    assert result["ok"] is True
    assert any("firefox" in str(a).lower() or "xdg-open" in str(a) for a in result["actions"])


def test_execute_dry_run_appends_events() -> None:
    store = InMemoryEventStore()
    d = CqrsDispatcher(event_store=store, platform=HostPlatform.LINUX)
    uri = "command://executor%3Aworker/send_invoice"
    d.execute_uri(uri, dry_run=True)
    stream = store.get_stream(uri)
    types = [e.event_type for e in stream]
    assert "UriCompiled" in types
    assert "UriExecuted" in types
    assert len(stream) == 2


def test_probe_endpoint() -> None:
    d = CqrsDispatcher(platform=HostPlatform.LINUX)
    probe = d.probe_uri("endpoint://tcp/127.0.0.1/8010/health")
    assert probe["reachable"] is True
    assert "8010" in probe["details"]["url"]


def test_runtime_curl_probe() -> None:
    d = CqrsDispatcher(platform=HostPlatform.LINUX)
    probe = d.probe_uri("runtime://worker/executor%3Aworker", target="curl")
    assert probe["reachable"] is True


def test_driver_registry_get_builtin() -> None:
    reg = DriverRegistry()
    driver = reg.get_driver("command", "curl")
    assert driver.scheme == "command"
    cap = driver.capabilities()
    assert cap.supports_compile is True


def test_service_curl_driver_maps_todomat_health() -> None:
    d = CqrsDispatcher(platform=HostPlatform.LINUX)
    result = d.compile_uri("service://generated/process-registry", target="curl")
    assert result["ok"] is True
    assert result["actions"][0]["command"] == "curl"
    assert "8083" in result["actions"][0]["args"][1]


def test_service_docker_driver_compose_ps() -> None:
    d = CqrsDispatcher(platform=HostPlatform.LINUX)
    result = d.compile_uri(
        "service://generated/trigger-gateway",
        target="docker",
        config={"compose_dir": "/home/tom/github/wronai/todomat"},
    )
    assert result["ok"] is True
    argv = result["actions"][0]["argv"]
    assert "docker" in argv[0]
    assert "trigger-gateway" in argv


def test_service_systemd_driver_unit() -> None:
    d = CqrsDispatcher(platform=HostPlatform.LINUX)
    result = d.compile_uri("service://generated/nginx", target="systemd")
    assert result["ok"] is True
    assert result["actions"][0]["argv"] == ["systemctl", "is-active", "nginx.service"]
