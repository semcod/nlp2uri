"""Tests for URI → OSAction compilation."""

from __future__ import annotations

from nlp2uri.compile import compile_uri_to_actions
from nlp2uri.models import HostPlatform


def test_compile_app_open_linux():
    actions = compile_uri_to_actions("app://firefox/open", HostPlatform.LINUX)
    assert len(actions) == 1
    assert actions[0].command in {"xdg-open", "gtk-launch"}


def test_compile_screenshot_macos():
    actions = compile_uri_to_actions(
        "desktop-screenshot://window?title=Chrome&mode=active",
        HostPlatform.MACOS,
    )
    assert actions[0].command == "screencapture"


def test_compile_ide_native_deep_link():
    actions = compile_uri_to_actions(
        "app://vscode/open?path=/tmp/foo",
        HostPlatform.LINUX,
    )
    assert "vscode://file" in " ".join(actions[0].argv())


def test_compile_settings_windows():
    actions = compile_uri_to_actions("app://settings/open", HostPlatform.WINDOWS)
    assert "ms-settings:" in actions[0].args
