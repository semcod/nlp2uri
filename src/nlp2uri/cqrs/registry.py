"""Load drivers from schemas/registry.yaml."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

from nlp2uri.cqrs.base import UriDriver
from nlp2uri.cqrs.drivers import (
    ArtifactFilesystemDriver,
    CommandCurlDriver,
    DelegateCompileDriver,
    EndpointCurlDriver,
    GetvCliDriver,
    ResourceProbeDriver,
    RuntimeCurlDriver,
    ServiceCurlDriver,
    ServiceDockerDriver,
    ServiceSystemdDriver,
)

_REGISTRY_PATH = Path(__file__).resolve().parents[3] / "schemas" / "registry.yaml"

_BUILTIN: dict[tuple[str, str], type[UriDriver]] = {
    ("artifact", "filesystem"): ArtifactFilesystemDriver,
    ("command", "curl"): CommandCurlDriver,
    ("getv", "getv_cli"): GetvCliDriver,
    ("resource", "probe"): ResourceProbeDriver,
    ("runtime", "curl"): RuntimeCurlDriver,
    ("endpoint", "curl"): EndpointCurlDriver,
    ("service", "curl"): ServiceCurlDriver,
    ("service", "docker"): ServiceDockerDriver,
    ("service", "systemd"): ServiceSystemdDriver,
}

_DESKTOP_SCHEMES = frozenset({"app", "desktop-screenshot", "desktop-window", "file", "http"})


class DriverRegistry:
    def __init__(self, registry_path: Path | None = None) -> None:
        self.path = registry_path or _REGISTRY_PATH
        self._data = yaml.safe_load(self.path.read_text(encoding="utf-8"))

    @property
    def schemes(self) -> dict[str, Any]:
        return self._data.get("schemes", {})

    def targets_for(self, scheme: str) -> list[str]:
        meta = self.schemes.get(scheme, {})
        return list(meta.get("drivers", []))

    def default_target(self, scheme: str) -> str | None:
        targets = self.targets_for(scheme)
        return targets[0] if targets else None

    def get_driver(self, scheme: str, target: str | None = None) -> UriDriver:
        chosen = target or self.default_target(scheme)
        if not chosen:
            raise KeyError(f"no driver target for scheme: {scheme}")

        key = (scheme, chosen)
        if key in _BUILTIN:
            return _BUILTIN[key]()

        if scheme in _DESKTOP_SCHEMES or scheme.replace("_", "-") in _DESKTOP_SCHEMES:
            return DelegateCompileDriver(scheme, chosen)

        if chosen == "curl" and scheme in self.schemes:
            return DelegateCompileDriver(scheme, chosen)

        raise KeyError(f"no implementation for driver {scheme}/{chosen}")

    def driver_for_uri(self, uri: str, target: str | None = None) -> UriDriver:
        scheme = urlparse(uri).scheme.lower()
        if scheme == "desktop-screenshot":
            return DelegateCompileDriver("desktop_screenshot", target or "linux")
        if scheme == "desktop-window":
            return DelegateCompileDriver("desktop_window", target or "linux")
        return self.get_driver(scheme, target)


@lru_cache(maxsize=1)
def default_registry() -> DriverRegistry:
    return DriverRegistry()
