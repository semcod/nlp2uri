"""Host platform detection."""

from __future__ import annotations

import os
import sys

from nlp2uri.models import HostPlatform


def detect_platform() -> HostPlatform:
    if sys.platform.startswith("linux"):
        return HostPlatform.LINUX
    if sys.platform == "darwin":
        return HostPlatform.MACOS
    if sys.platform == "win32" or os.name == "nt":
        return HostPlatform.WINDOWS
    return HostPlatform.UNKNOWN
