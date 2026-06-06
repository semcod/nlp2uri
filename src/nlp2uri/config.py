"""Load and persist defaults from nlp2uri.yaml."""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from nlp2uri.models import HostPlatform
from nlp2uri.platform_detect import detect_platform

_CONFIG_FILENAMES = ("nlp2uri.yaml", "nlp2uri.yml")
_ENV_CONFIG = "NLP2URI_CONFIG"
_ENV_PLATFORM = "NLP2URI_PLATFORM"
_ENV_CAPTURE_DIR = "NLP2URI_CAPTURE_DIR"
_CACHED: NLP2URIConfig | None = None


@dataclass
class NLP2URIConfig:
    """Persisted defaults (nlp2uri.yaml)."""

    platform: str = "auto"
    host_platform: str = ""
    locale: str | None = None
    dry_run: bool = False
    capture_dir: str = "/tmp/nlp2uri-captures"
    config_path: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def resolved_platform(self) -> HostPlatform:
        env = os.environ.get(_ENV_PLATFORM, "").strip().lower()
        if env:
            return HostPlatform(env)
        raw = (self.platform or "auto").strip().lower()
        if raw in {"", "auto", "detect"}:
            return detect_platform()
        return HostPlatform(raw)

    def apply_runtime_env(self) -> None:
        if self.capture_dir:
            os.environ.setdefault(_ENV_CAPTURE_DIR, self.capture_dir)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "platform": self.platform,
            "host_platform": self.host_platform or detect_platform().value,
            "locale": self.locale,
            "dry_run": self.dry_run,
            "capture_dir": self.capture_dir,
        }
        payload.update(self.extra)
        return payload

    def to_yaml(self) -> str:
        lines = [
            "# nlp2uri.yaml — desktop URI compiler defaults",
            "# platform: auto | linux | darwin | windows (auto = detect at runtime)",
            "",
            f"platform: {self.platform}",
            f"host_platform: {self.host_platform or detect_platform().value}",
        ]
        if self.locale:
            lines.append(f"locale: {self.locale}")
        else:
            lines.append("locale: null")
        lines.append(f"dry_run: {'true' if self.dry_run else 'false'}")
        lines.append(f"capture_dir: {self.capture_dir}")
        for key, value in sorted(self.extra.items()):
            if key in payload_keys():
                continue
            lines.append(f"{key}: {_yaml_scalar(value)}")
        return "\n".join(lines) + "\n"


def payload_keys() -> set[str]:
    return {"platform", "host_platform", "locale", "dry_run", "capture_dir"}


def _yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if text == "" or any(ch in text for ch in ":#{}[]&*!|>'\""):
        return repr(text)
    return text


def _parse_scalar(raw: str) -> Any:
    text = raw.strip()
    if text in {"null", "~", ""}:
        return None
    if text in {"true", "yes", "on"}:
        return True
    if text in {"false", "no", "off"}:
        return False
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        return text[1:-1]
    return text


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        data[key.strip()] = _parse_scalar(value)
    return data


def config_search_paths() -> list[Path]:
    paths: list[Path] = []
    env_path = os.environ.get(_ENV_CONFIG, "").strip()
    if env_path:
        paths.append(Path(env_path).expanduser())
    cwd = Path.cwd()
    for name in _CONFIG_FILENAMES:
        paths.append(cwd / name)
    xdg = os.environ.get("XDG_CONFIG_HOME", "").strip()
    config_base = Path(xdg).expanduser() if xdg else Path.home() / ".config"
    for name in _CONFIG_FILENAMES:
        paths.append(config_base / "nlp2uri" / name)
    paths.append(Path.home() / ".nlp2uri.yaml")
    return paths


def find_config_path() -> Path | None:
    for path in config_search_paths():
        if path.is_file():
            return path
    return None


def default_config() -> NLP2URIConfig:
    detected = detect_platform()
    return NLP2URIConfig(
        platform="auto",
        host_platform=detected.value,
        locale=None,
        dry_run=False,
        capture_dir=os.environ.get(_ENV_CAPTURE_DIR, "/tmp/nlp2uri-captures"),
    )


def _load_from_path(path: Path) -> NLP2URIConfig:
    raw = path.read_text(encoding="utf-8")
    data = _parse_simple_yaml(raw)
    known = payload_keys()
    cfg = NLP2URIConfig(
        platform=str(data.get("platform") or "auto"),
        host_platform=str(data.get("host_platform") or detect_platform().value),
        locale=data.get("locale"),
        dry_run=bool(data.get("dry_run", False)),
        capture_dir=str(data.get("capture_dir") or "/tmp/nlp2uri-captures"),
        config_path=str(path),
        extra={k: v for k, v in data.items() if k not in known},
    )
    cfg.apply_runtime_env()
    return cfg


def load_config(*, reload: bool = False) -> NLP2URIConfig:
    global _CACHED
    if _CACHED is not None and not reload:
        return _CACHED

    path = find_config_path()
    if path is None:
        cfg = default_config()
        _CACHED = cfg
        return cfg

    cfg = _load_from_path(path)
    _CACHED = cfg
    return cfg


def save_config(cfg: NLP2URIConfig, path: Path | None = None) -> Path:
    global _CACHED
    target = path or (Path(cfg.config_path) if cfg.config_path else None)
    if target is None:
        target = Path.cwd() / "nlp2uri.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    cfg.host_platform = detect_platform().value
    target.write_text(cfg.to_yaml(), encoding="utf-8")
    cfg.config_path = str(target)
    _CACHED = cfg
    cfg.apply_runtime_env()
    return target


def ensure_config(path: Path | None = None) -> NLP2URIConfig:
    """Create nlp2uri.yaml with detected defaults when missing."""
    global _CACHED

    if path is not None:
        if not path.is_file():
            save_config(default_config(), path)
        _CACHED = _load_from_path(path)
        return _CACHED

    existing = find_config_path()
    if existing is not None:
        _CACHED = _load_from_path(existing)
        return _CACHED

    cfg = default_config()
    target = Path.cwd() / "nlp2uri.yaml"
    save_config(cfg, target)
    return cfg


def get_effective_platform(override: HostPlatform | None = None) -> HostPlatform:
    if override is not None:
        return override
    return load_config().resolved_platform()


def reset_config_cache() -> None:
    global _CACHED
    _CACHED = None
