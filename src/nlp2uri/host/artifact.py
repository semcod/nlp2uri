"""artifact:// URI — read/open files from SystemMap example dirs."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from nlp2uri.models import HostPlatform, OSAction

ARTIFACT_SCHEME = "artifact"


def is_artifact_uri(uri: str) -> bool:
    return urlparse(uri).scheme.lower() == ARTIFACT_SCHEME


def _decode(value: str) -> str:
    return unquote(value or "")


def resolve_artifact_path(
    uri: str,
    *,
    example_dir: str | None = None,
    example_roots: list[str] | None = None,
) -> Path:
    """Resolve artifact://{example_id}/{rel_path} to absolute filesystem path."""
    parsed = urlparse(uri)
    example_id = _decode(parsed.netloc)
    rel_path = _decode(parsed.path.lstrip("/"))
    if not example_id or not rel_path:
        raise ValueError(f"artifact uri requires example_id and path: {uri}")

    candidates: list[Path] = []
    if example_dir:
        candidates.append(Path(example_dir).expanduser())
    for root in example_roots or []:
        candidates.append(Path(root).expanduser() / example_id)
    env_dir = os.getenv("NLP2URI_EXAMPLE_DIR") or os.getenv("NLP2DSL_EXAMPLE_DIR")
    if env_dir:
        candidates.append(Path(env_dir).expanduser() / example_id)

    for base in candidates:
        resolved = (base / rel_path).resolve()
        if resolved.is_file():
            return resolved

    if candidates:
        first = (candidates[0] / rel_path).resolve()
        if first.exists():
            return first
        raise FileNotFoundError(f"artifact not found: {first}")

    raise ValueError(
        f"no example_dir for artifact {uri}; set NLP2URI_EXAMPLE_DIR or pass example_dir in config"
    )


def build_artifact_actions(
    uri: str,
    host: HostPlatform,
    *,
    config: dict[str, str] | None = None,
) -> list[OSAction]:
    cfg = dict(config or {})
    parsed = urlparse(uri)
    params = {k: v[0] for k, v in parse_qs(parsed.query).items() if v}
    action = params.get("action") or cfg.get("action", "read")

    path = resolve_artifact_path(
        uri,
        example_dir=cfg.get("example_dir"),
        example_roots=[cfg["example_root"]] if cfg.get("example_root") else None,
    )
    path_str = str(path)

    if action == "open":
        if host == HostPlatform.LINUX:
            opener = shutil.which("xdg-open") or "xdg-open"
            return [OSAction(host, opener, [path_str])]
        if host == HostPlatform.MACOS:
            return [OSAction(host, "open", [path_str])]
        if host == HostPlatform.WINDOWS:
            return [OSAction(host, "cmd", ["/c", "start", "", path_str])]

    if action == "stat":
        return [OSAction(host, "test", ["-f", path_str])]

    # read (default)
    if host == HostPlatform.WINDOWS:
        return [OSAction(host, "type", [path_str])]
    return [OSAction(host, "cat", [path_str])]
