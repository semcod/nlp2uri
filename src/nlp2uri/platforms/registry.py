"""Executor registry."""

from __future__ import annotations

from nlp2uri.models import HostPlatform
from nlp2uri.platform_detect import detect_platform
from nlp2uri.platforms.base import UriExecutor
from nlp2uri.platforms.linux import LinuxExecutor
from nlp2uri.platforms.macos import MacOSExecutor
from nlp2uri.platforms.windows import WindowsExecutor

_EXECUTORS: dict[HostPlatform, type[UriExecutor]] = {
    HostPlatform.LINUX: LinuxExecutor,
    HostPlatform.MACOS: MacOSExecutor,
    HostPlatform.WINDOWS: WindowsExecutor,
}


def get_executor(platform: HostPlatform | None = None) -> UriExecutor:
    host = platform or detect_platform()
    cls = _EXECUTORS.get(host)
    if cls is None:
        raise RuntimeError(f"unsupported platform: {host.value}")
    return cls()
