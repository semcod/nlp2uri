"""Canonical URI builders for env2llm SystemMapIR entities."""

from __future__ import annotations

from typing import Any

from nlp2uri.systemmap.encode import encode_path, encode_segment


def _get(obj: Any, key: str, default: str = "") -> str:
    if isinstance(obj, dict):
        return str(obj.get(key, default) or default)
    return str(getattr(obj, key, default) or default)


def _get_list(obj: Any, key: str) -> list[str]:
    if isinstance(obj, dict):
        raw = obj.get(key) or []
    else:
        raw = getattr(obj, key, None) or []
    return [str(item) for item in raw]


def uri_for_runtime(rt: Any) -> str:
    """``runtime://{kind}/{id}`` — e.g. ``runtime://worker/executor%3Aworker``."""
    kind = _get(rt, "kind", "worker")
    runtime_id = _get(rt, "id")
    return f"runtime://{encode_segment(kind)}/{encode_segment(runtime_id)}"


def uri_for_command(cmd: Any, *, runtime_id: str | None = None) -> str:
    """``command://{runtime_id}/{name}``."""
    name = _get(cmd, "name")
    rt = runtime_id or _get(cmd, "runtime") or "unknown"
    return f"command://{encode_segment(rt)}/{encode_segment(name)}"


def uri_for_resource(res: Any) -> str:
    """``resource://{connector}/{id}``."""
    connector = _get(res, "connector") or "default"
    resource_id = _get(res, "id")
    return f"resource://{encode_segment(connector)}/{encode_segment(resource_id)}"


def uri_for_access(grant: Any) -> str:
    """``access://{agent}/{resource_area}/{actions}``."""
    agent = _get(grant, "agent") or "unknown"
    area = _get(grant, "resource_area") or "all"
    actions = ",".join(_get_list(grant, "actions")) or "*"
    return (
        f"access://{encode_segment(agent)}/"
        f"{encode_segment(area)}/"
        f"{encode_segment(actions)}"
    )


def uri_for_artifact(art: Any, *, example_id: str) -> str:
    """``artifact://{example_id}/{path}``."""
    path = _get(art, "path").lstrip("/")
    return f"artifact://{encode_segment(example_id)}/{encode_path(path)}"


def uri_for_conversation(*, example_id: str) -> str:
    """``conversation://{example_id}/policy``."""
    return f"conversation://{encode_segment(example_id)}/policy"


def uri_for_process(*, example_id: str) -> str:
    """``process://{example_id}/policy``."""
    return f"process://{encode_segment(example_id)}/policy"


def uri_for_validation(val: Any, *, example_id: str) -> str:
    """``validation://{example_id}/{code}``."""
    code = _get(val, "code")
    return f"validation://{encode_segment(example_id)}/{encode_segment(code)}"


def uri_for_schedule(sched: Any) -> str:
    """``schedule://{example_id}/{id}`` — example_id taken from parent IR when building index."""
    schedule_id = _get(sched, "id")
    return f"schedule://{encode_segment(schedule_id)}"


def uri_for_generated_service(svc: Any) -> str:
    """``service://generated/{name}``."""
    name = _get(svc, "name")
    return f"service://generated/{encode_segment(name)}"


def uri_for_environment(example_id: str) -> str:
    """``environment://{example_id}`` — whole environment block."""
    return f"environment://{encode_segment(example_id)}"


def uri_for_desktop_session() -> str:
    """``desktop://session`` — live GUI session."""
    return "desktop://session"


def uri_for_desktop_window_focus(window: Any) -> str:
    """``desktop-window://focus?title=…`` — focus a window by title."""
    from nlp2uri.schemes.util import abstract_url

    params: dict[str, str] = {}
    title = _get(window, "title")
    if title:
        params["title"] = title
    window_id = _get(window, "id")
    if window_id:
        params["wm_id"] = window_id
    return abstract_url("desktop-window", "focus", params=params)


def uri_for_desktop_window_screenshot(window: Any) -> str:
    """``desktop-screenshot://window?title=…`` — capture a window by title."""
    from nlp2uri.schemes.util import abstract_url

    params: dict[str, str] = {"mode": "title"}
    title = _get(window, "title")
    if title:
        params["title"] = title
    return abstract_url("desktop-screenshot", "window", params=params)
