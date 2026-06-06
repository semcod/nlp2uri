"""resource:// URI — connector probes (filesystem, smtp, redis, http)."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from nlp2uri.models import HostPlatform, OSAction

RESOURCE_SCHEME = "resource"


def is_resource_uri(uri: str) -> bool:
    return urlparse(uri).scheme.lower() == RESOURCE_SCHEME


def _decode(value: str) -> str:
    return unquote(value or "")


def _filesystem_probe_path(resource_id: str, *, config: dict[str, str]) -> str:
    if config.get("path"):
        return str(Path(config["path"]).expanduser())
    if resource_id == "user":
        return str(Path.home())
    pattern = config.get("uri_pattern") or config.get("base_path") or "~"
    return str(Path(pattern.replace("file://", "")).expanduser())


def build_resource_actions(
    uri: str,
    host: HostPlatform,
    *,
    config: dict[str, str] | None = None,
) -> list[OSAction]:
    parsed = urlparse(uri)
    connector = _decode(parsed.netloc)
    resource_id = _decode(parsed.path.lstrip("/"))
    params = {k: v[0] for k, v in parse_qs(parsed.query).items() if v}
    cfg = dict(config or {})
    cfg.update({k: str(v) for k, v in params.items()})
    action = cfg.get("action", "probe")

    if connector == "filesystem":
        path = _filesystem_probe_path(resource_id, config=cfg)
        if action == "list":
            return [OSAction(host, "ls", ["-la", path])]
        return [OSAction(host, "test", ["-e", path])]

    if connector == "smtp":
        host_s = cfg.get("smtp_host", os.getenv("SMTP_HOST", "localhost"))
        port = cfg.get("smtp_port", "25")
        if shutil.which("nc"):
            return [OSAction(host, "nc", ["-z", "-w", "2", host_s, port])]
        return [OSAction(host, "bash", ["-c", f"echo smtp-probe:{host_s}:{port}"])]

    if connector == "redis":
        redis_url = cfg.get("url", os.getenv("REDIS_URL", "redis://127.0.0.1:6379"))
        if shutil.which("redis-cli"):
            return [OSAction(host, "redis-cli", ["-u", redis_url, "ping"])]
        return [OSAction(host, "bash", ["-c", f"echo redis-probe:{redis_url}"])]

    if connector in {"http", "https"}:
        url = cfg.get("url") or cfg.get("health") or f"http://{resource_id}/health"
        return [OSAction(host, "curl", ["-sf", url])]

    return [OSAction(host, "echo", [f"resource-probe:{connector}/{resource_id}"])]
