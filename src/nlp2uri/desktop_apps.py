"""Linux .desktop entry discovery for app launch."""

from __future__ import annotations

from pathlib import Path

DESKTOP_APP_DIRS: tuple[str, ...] = (
    "/usr/share/applications",
    "/var/lib/snapd/desktop/applications",
    "/usr/local/share/applications",
)


def desktop_id_candidate_names(name: str) -> tuple[str, str, str]:
    lowered = name.lower().removesuffix(".desktop")
    return (
        f"{lowered}.desktop",
        f"org.{lowered}.desktop",
        f"{lowered}-desktop.desktop",
    )


def _exact_desktop_match(base: Path, candidates: tuple[str, str, str]) -> str | None:
    for candidate in candidates:
        if (base / candidate).is_file():
            return candidate
    return None


def _fuzzy_desktop_match(base: Path, lowered: str) -> str | None:
    for entry in base.glob("*.desktop"):
        if lowered in entry.name.lower():
            return entry.name
    return None


def find_desktop_id_in_dir(
    desktop_dir: str | Path,
    *,
    candidates: tuple[str, str, str],
    lowered: str,
) -> str | None:
    base = Path(desktop_dir)
    if not base.is_dir():
        return None
    return _exact_desktop_match(base, candidates) or _fuzzy_desktop_match(base, lowered)


def desktop_id_for_app(name: str) -> str | None:
    lowered = name.lower().removesuffix(".desktop")
    candidates = desktop_id_candidate_names(name)
    for desktop_dir in DESKTOP_APP_DIRS:
        found = find_desktop_id_in_dir(
            desktop_dir,
            candidates=candidates,
            lowered=lowered,
        )
        if found is not None:
            return found
    return None
