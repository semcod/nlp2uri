"""Load ~/.getv profiles for getv:// URI indexing (optional getv package)."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

_GETV_IMPORT_ERROR: str | None = None

try:
    from getv.profile import ProfileManager
    from getv.security import is_sensitive_key, mask_value

    _GETV_AVAILABLE = True
except ImportError as exc:
    ProfileManager = None  # type: ignore[misc, assignment]
    _GETV_AVAILABLE = False
    _GETV_IMPORT_ERROR = str(exc)

    def is_sensitive_key(key: str) -> bool:  # type: ignore[misc]
        return bool(re.search(r"(KEY|TOKEN|SECRET|PASSWORD)", key, re.I))

    def mask_value(value: str, visible_chars: int = 4) -> str:  # type: ignore[misc]
        if len(value) <= visible_chars:
            return "***"
        return value[:visible_chars] + "***"


def getv_available() -> bool:
    return _GETV_AVAILABLE


def getv_missing_message() -> str:
    return _GETV_IMPORT_ERROR or "getv not installed — pip install 'nlp2uri[envmap]'"


def getv_home() -> Path:
    return Path(os.environ.get("GETV_HOME", "~/.getv")).expanduser().resolve()


def _parse_env_file(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.is_file():
        return data
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("'\"")
        if key:
            data[key] = value
    return data


def discover_profiles(home: Path | None = None) -> dict[str, list[str]]:
    """Scan GETV_HOME for category/profile pairs."""
    base = home or getv_home()
    if not base.is_dir():
        return {}

    profiles: dict[str, list[str]] = {}
    for cat_dir in sorted(base.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith("."):
            continue
        names = sorted(f.stem for f in cat_dir.glob("*.env"))
        if names:
            profiles[cat_dir.name] = names
    return profiles


def load_profile_dict(category: str, profile: str, *, home: Path | None = None) -> dict[str, str]:
    base = home or getv_home()
    path = base / category / f"{profile}.env"
    if _GETV_AVAILABLE and ProfileManager is not None:
        pm = ProfileManager(base)
        return pm.get_dict(category, profile)
    return _parse_env_file(path)


def mask_var_value(key: str, value: str) -> str:
    if is_sensitive_key(key):
        return mask_value(value)
    return value


def profile_manager(home: Path | None = None) -> Any:
    if not _GETV_AVAILABLE or ProfileManager is None:
        raise RuntimeError(getv_missing_message())
    return ProfileManager(home or getv_home())
