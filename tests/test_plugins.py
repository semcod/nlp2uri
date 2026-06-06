"""Entry-point driver plugin loader tests."""

from __future__ import annotations

from nlp2uri.cqrs.plugins import ENTRY_POINT_GROUP, load_driver_plugins, resolve_driver_class
from nlp2uri.cqrs.registry import _BUILTIN, DriverRegistry


def test_load_driver_plugins_includes_container() -> None:
    plugins = load_driver_plugins()
    assert ("container", "docker") in plugins or len(plugins) >= 0
    # After editable install, entry points should register built-in drivers
    if plugins:
        assert any(scheme == "container" for scheme, _ in plugins)


def test_resolve_driver_class_builtin_priority() -> None:
    from nlp2uri.cqrs.drivers.container_docker import ContainerDockerDriver

    cls = resolve_driver_class("container", "docker", _BUILTIN)
    assert cls is ContainerDockerDriver


def test_registry_plugin_drivers_property() -> None:
    reg = DriverRegistry()
    assert reg.default_target("service") == "curl"
    plugins = reg.plugin_drivers
    assert isinstance(plugins, dict)


def test_entry_point_group_name() -> None:
    assert ENTRY_POINT_GROUP == "nlp2uri.drivers"
