"""Entry-point plugin loader for CQRS URI drivers."""

from __future__ import annotations

import importlib
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nlp2uri.cqrs.base import UriDriver

logger = logging.getLogger(__name__)

ENTRY_POINT_GROUP = "nlp2uri.drivers"


def _parse_entry_point_name(name: str) -> tuple[str, str] | None:
    """Entry point name format: {scheme}-{target}, e.g. container-docker."""
    if "-" not in name:
        return None
    scheme, target = name.split("-", 1)
    if not scheme or not target:
        return None
    return scheme.replace("_", "-"), target


def load_driver_plugins() -> dict[tuple[str, str], type[UriDriver]]:
    """Load driver classes registered via [project.entry-points.nlp2uri.drivers]."""
    plugins: dict[tuple[str, str], type[UriDriver]] = {}
    try:
        from importlib.metadata import entry_points
    except ImportError:
        return plugins

    eps = entry_points()
    group = eps.select(group=ENTRY_POINT_GROUP) if hasattr(eps, "select") else eps.get(ENTRY_POINT_GROUP, [])

    for ep in group:
        key = _parse_entry_point_name(ep.name)
        if key is None:
            logger.warning("skip driver plugin %s: name must be scheme-target", ep.name)
            continue
        try:
            driver_cls = ep.load()
            if isinstance(driver_cls, type):
                plugins[key] = driver_cls
            else:
                logger.warning("skip driver plugin %s: not a class", ep.name)
        except Exception as exc:
            logger.warning("failed to load driver plugin %s: %s", ep.name, exc)
    return plugins


def resolve_driver_class(
    scheme: str,
    target: str,
    builtins: dict[tuple[str, str], type[UriDriver]],
) -> type[UriDriver] | None:
    """Builtins first, then entry-point plugins."""
    key = (scheme, target)
    if key in builtins:
        return builtins[key]
    plugins = load_driver_plugins()
    return plugins.get(key)
