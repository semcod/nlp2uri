"""Runtime execution helpers."""

from __future__ import annotations

import subprocess

from nlp2uri.compile import compile_uri_to_actions
from nlp2uri.models import ActionResult, HostPlatform
from nlp2uri.platform_detect import detect_platform
from nlp2uri.platforms.registry import get_executor as _get_executor


def get_executor(platform: HostPlatform | None = None):
    return _get_executor(platform)


def execute_uri(
    uri: str,
    *,
    platform: HostPlatform | None = None,
    dry_run: bool = False,
) -> ActionResult:
    host = platform or detect_platform()
    try:
        actions = tuple(compile_uri_to_actions(uri, host))
    except ValueError as exc:
        return ActionResult(
            ok=False,
            uri=uri,
            error=str(exc),
            returncode=2,
            platform=host,
        )

    if not actions:
        return ActionResult(
            ok=False,
            uri=uri,
            error="no actions compiled",
            returncode=2,
            platform=host,
            actions=actions,
        )

    action = actions[0]
    if dry_run:
        return ActionResult(
            ok=True,
            uri=uri,
            output=" ".join(action.argv()),
            returncode=0,
            platform=host,
            actions=actions,
        )

    try:
        proc = subprocess.run(
            action.argv(),
            capture_output=True,
            text=True,
            timeout=30.0,
            check=False,
        )
    except FileNotFoundError:
        return ActionResult(
            ok=False,
            uri=uri,
            error=f"command not found: {action.command}",
            returncode=127,
            platform=host,
            actions=actions,
        )
    except subprocess.TimeoutExpired:
        return ActionResult(
            ok=False,
            uri=uri,
            error="command timed out",
            returncode=124,
            platform=host,
            actions=actions,
        )

    output = (proc.stdout or proc.stderr or "").strip()
    return ActionResult(
        ok=proc.returncode == 0,
        uri=uri,
        output=output,
        error="" if proc.returncode == 0 else output,
        returncode=proc.returncode,
        platform=host,
        actions=actions,
    )
