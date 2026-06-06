"""Tests for platform execution."""

from __future__ import annotations

from nlp2uri.models import HostPlatform
from nlp2uri.runtime import execute_uri


def test_linux_dry_run_open_app():
    result = execute_uri(
        "app://firefox/open",
        platform=HostPlatform.LINUX,
        dry_run=True,
    )
    assert result.ok
    assert "firefox" in result.output.lower() or "gtk-launch" in result.output.lower()
    assert len(result.actions) >= 1


def test_macos_dry_run_capture_screen():
    result = execute_uri(
        "desktop-screenshot://screen",
        platform=HostPlatform.MACOS,
        dry_run=True,
    )
    assert result.ok
    assert "screencapture" in result.output


def test_windows_dry_run_settings():
    result = execute_uri(
        "ms-settings:",
        platform=HostPlatform.WINDOWS,
        dry_run=True,
    )
    assert result.ok
    assert "start" in result.output.lower()


def test_linux_dry_run_file_uri():
    result = execute_uri(
        "app://file/open?path=/tmp/demo.txt",
        platform=HostPlatform.LINUX,
        dry_run=True,
    )
    assert result.ok
    assert "xdg-open" in result.output or "file://" in result.output
