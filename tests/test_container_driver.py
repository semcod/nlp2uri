"""container:// Docker driver tests."""

from __future__ import annotations

from nlp2uri.cqrs import CqrsDispatcher
from nlp2uri.cqrs.drivers.container_docker import parse_container_uri
from nlp2uri.cqrs.registry import DriverRegistry
from nlp2uri.models import HostPlatform


def test_parse_container_uri() -> None:
    runtime, name, action, params = parse_container_uri(
        "container://docker/todomat-process-registry-1/logs?tail=50"
    )
    assert runtime == "docker"
    assert name == "todomat-process-registry-1"
    assert action == "logs"
    assert params["tail"] == "50"


def test_container_status_compile() -> None:
    d = CqrsDispatcher(platform=HostPlatform.LINUX)
    result = d.compile_uri("container://docker/nginx/status")
    assert result["ok"] is True
    argv = result["actions"][0]["argv"]
    assert argv[:3] == ["docker", "inspect", "-f"]
    assert "nginx" in argv


def test_container_logs_compile() -> None:
    d = CqrsDispatcher(platform=HostPlatform.LINUX)
    result = d.compile_uri("container://docker/app/logs?tail=20")
    assert result["ok"] is True
    assert result["actions"][0]["argv"] == ["docker", "logs", "--tail", "20", "app"]


def test_container_exec_requires_cmd() -> None:
    d = CqrsDispatcher(platform=HostPlatform.LINUX)
    result = d.compile_uri("container://docker/app/exec")
    assert result["ok"] is False
    assert "cmd" in result["error"].lower()


def test_container_exec_compile() -> None:
    d = CqrsDispatcher(platform=HostPlatform.LINUX)
    result = d.compile_uri("container://docker/app/exec?cmd=hostname")
    assert result["ok"] is True
    assert result["actions"][0]["argv"] == ["docker", "exec", "app", "sh", "-c", "hostname"]


def test_registry_lists_container_target() -> None:
    reg = DriverRegistry()
    assert reg.default_target("container") == "docker"
    driver = reg.get_driver("container", "docker")
    assert driver.scheme == "container"
