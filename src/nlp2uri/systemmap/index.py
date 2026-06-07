"""Build a URI index (UriMap) from env2llm SystemMapIR."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from nlp2uri.systemmap.uri import (
    uri_for_access,
    uri_for_artifact,
    uri_for_command,
    uri_for_conversation,
    uri_for_desktop_session,
    uri_for_desktop_window_focus,
    uri_for_desktop_window_screenshot,
    uri_for_environment,
    uri_for_generated_service,
    uri_for_process,
    uri_for_resource,
    uri_for_runtime,
    uri_for_schedule,
    uri_for_validation,
)


@dataclass(frozen=True)
class UriMapEntry:
    """One addressable entity in a SystemMap."""

    uri: str
    kind: str
    ref_type: str
    name: str | None = None
    ref: dict[str, Any] = field(default_factory=dict)
    links: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "uri": self.uri,
            "kind": self.kind,
            "ref_type": self.ref_type,
            "name": self.name,
            "ref": dict(self.ref),
            "links": list(self.links),
        }


@dataclass
class UriMap:
    """``system_map_uri.v1`` — canonical addressing layer over SystemMapIR."""

    format: str = "system_map_uri.v1"
    version: int = 1
    example_id: str = ""
    system_map_format: str = ""
    entries: dict[str, UriMapEntry] = field(default_factory=dict)
    by_name: dict[str, list[str]] = field(default_factory=dict)

    def lookup(self, uri: str) -> UriMapEntry | None:
        return self.entries.get(uri)

    def find_by_kind(self, kind: str) -> list[UriMapEntry]:
        return [entry for entry in self.entries.values() if entry.kind == kind]

    def find_command(self, name: str) -> UriMapEntry | None:
        uris = self.by_name.get(name)
        if not uris:
            return None
        return self.entries.get(uris[0])

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": self.format,
            "version": self.version,
            "example_id": self.example_id,
            "system_map_format": self.system_map_format,
            "entries": {uri: entry.to_dict() for uri, entry in self.entries.items()},
            "by_name": {k: list(v) for k, v in self.by_name.items()},
        }


def _model_dump(obj: Any) -> dict[str, Any]:
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, dict):
        return dict(obj)
    raise TypeError(f"unsupported ref type: {type(obj)!r}")


def _ir_field(ir: Any, name: str, default: Any = None) -> Any:
    if isinstance(ir, dict):
        return ir.get(name, default)
    return getattr(ir, name, default)


def _add_entry(
    uri_map: UriMap,
    *,
    uri: str,
    kind: str,
    ref_type: str,
    name: str | None,
    ref: Any,
    links: tuple[str, ...] = (),
) -> None:
    entry = UriMapEntry(
        uri=uri,
        kind=kind,
        ref_type=ref_type,
        name=name,
        ref=_model_dump(ref),
        links=links,
    )
    uri_map.entries[uri] = entry
    if name and kind == "command":
        uri_map.by_name.setdefault(name, []).append(uri)


def _index_environment(uri_map: UriMap, ir: Any, example_id: str) -> None:
    env_uri = uri_for_environment(example_id)
    _add_entry(
        uri_map,
        uri=env_uri,
        kind="environment",
        ref_type="SystemMapIR.environment",
        name=example_id,
        ref={"example_id": example_id, "keys": list((_ir_field(ir, "environment") or {}).keys())},
    )


def _index_runtimes(uri_map: UriMap, ir: Any) -> dict[str, str]:
    runtime_uris: dict[str, str] = {}
    for rt in _ir_field(ir, "runtimes") or []:
        uri = uri_for_runtime(rt)
        runtime_uris[_get_id(rt)] = uri
        _add_entry(
            uri_map,
            uri=uri,
            kind="runtime",
            ref_type="RuntimeSpecIR",
            name=_get_id(rt),
            ref=rt,
        )
    return runtime_uris


def _index_commands(uri_map: UriMap, ir: Any, runtime_uris: dict[str, str]) -> None:
    for cmd in _ir_field(ir, "commands") or []:
        runtime_id = _get_id_field(cmd, "runtime")
        runtime_uri = runtime_uris.get(runtime_id) if runtime_id else None
        links = (runtime_uri,) if runtime_uri else ()
        uri = uri_for_command(cmd, runtime_id=runtime_id or None)
        _add_entry(
            uri_map,
            uri=uri,
            kind="command",
            ref_type="CommandSchemaIR",
            name=_get_id_field(cmd, "name"),
            ref=cmd,
            links=links,
        )


def _index_resources(uri_map: UriMap, ir: Any) -> None:
    for res in _ir_field(ir, "resources") or []:
        uri = uri_for_resource(res)
        _add_entry(
            uri_map,
            uri=uri,
            kind="resource",
            ref_type="ResourceSpecIR",
            name=_get_id_field(res, "id"),
            ref=res,
        )


def _index_access(uri_map: UriMap, ir: Any) -> None:
    for grant in _ir_field(ir, "access") or []:
        uri = uri_for_access(grant)
        _add_entry(
            uri_map,
            uri=uri,
            kind="access",
            ref_type="AccessGrantIR",
            name=_get_id_field(grant, "agent"),
            ref=grant,
        )


def _index_artifacts(uri_map: UriMap, ir: Any, example_id: str) -> None:
    for art in _ir_field(ir, "artifacts") or []:
        uri = uri_for_artifact(art, example_id=example_id or "unknown")
        _add_entry(
            uri_map,
            uri=uri,
            kind="artifact",
            ref_type="ArtifactSpecIR",
            name=_get_id_field(art, "path"),
            ref=art,
        )


def _index_policies(uri_map: UriMap, ir: Any, example_id: str) -> None:
    for policy_kind, policy_ref, policy_uri_fn in (
        ("conversation", _ir_field(ir, "conversation"), uri_for_conversation),
        ("process", _ir_field(ir, "process"), uri_for_process),
    ):
        if policy_ref is not None:
            uri = policy_uri_fn(example_id=example_id)
            _add_entry(
                uri_map,
                uri=uri,
                kind=policy_kind,
                ref_type=f"{policy_kind.title()}PolicyIR",
                name=example_id,
                ref=policy_ref,
            )


def _index_schedules(uri_map: UriMap, ir: Any) -> None:
    for sched in _ir_field(ir, "schedules") or []:
        uri = uri_for_schedule(sched)
        _add_entry(
            uri_map,
            uri=uri,
            kind="schedule",
            ref_type="ScheduleSpecIR",
            name=_get_id_field(sched, "id"),
            ref=sched,
        )


def _index_generated_services(uri_map: UriMap, ir: Any) -> None:
    for svc in _ir_field(ir, "generated_services") or []:
        uri = uri_for_generated_service(svc)
        _add_entry(
            uri_map,
            uri=uri,
            kind="service",
            ref_type="GeneratedServiceIR",
            name=_get_id_field(svc, "name"),
            ref=svc,
        )


def _index_deploy(uri_map: UriMap, ir: Any, example_id: str) -> None:
    deploy = _ir_field(ir, "deploy")
    if deploy is None:
        return
    uri = f"deploy://{example_id}"
    _add_entry(
        uri_map,
        uri=uri,
        kind="deploy",
        ref_type="DeploySpecIR",
        name=example_id,
        ref=deploy,
    )


def _index_desktop(uri_map: UriMap, ir: Any) -> None:
    desktop = _ir_field(ir, "desktop")
    if not desktop:
        return

    session_uri = uri_for_desktop_session()
    _add_entry(
        uri_map,
        uri=session_uri,
        kind="desktop_session",
        ref_type="DesktopProbeIR",
        name="session",
        ref=desktop,
    )

    for window in _ir_field(desktop, "windows") or []:
        title = _get_id_field(window, "title") or _get_id(window)
        focus_uri = uri_for_desktop_window_focus(window)
        _add_entry(
            uri_map,
            uri=focus_uri,
            kind="desktop_window",
            ref_type="DesktopWindowIR",
            name=title or None,
            ref=window,
            links=(session_uri,),
        )
        screenshot_uri = uri_for_desktop_window_screenshot(window)
        _add_entry(
            uri_map,
            uri=screenshot_uri,
            kind="desktop_window_capture",
            ref_type="DesktopWindowIR",
            name=f"{title}:screenshot" if title else None,
            ref=window,
            links=(focus_uri, session_uri),
        )


def _index_validations(uri_map: UriMap, ir: Any, example_id: str) -> None:
    for val in _ir_field(ir, "validations") or []:
        uri = uri_for_validation(val, example_id=example_id or "unknown")
        _add_entry(
            uri_map,
            uri=uri,
            kind="validation",
            ref_type="ProfileValidationIR",
            name=_get_id_field(val, "code"),
            ref=val,
        )


def build_uri_index(ir: Any) -> UriMap:
    """Derive deterministic URIs for all entities in a SystemMapIR."""
    example_id = str(_ir_field(ir, "example_id", "") or "")
    uri_map = UriMap(
        example_id=example_id,
        system_map_format=str(_ir_field(ir, "format", "") or ""),
    )

    if example_id:
        _index_environment(uri_map, ir, example_id)

    runtime_uris = _index_runtimes(uri_map, ir)
    _index_commands(uri_map, ir, runtime_uris)
    _index_resources(uri_map, ir)
    _index_access(uri_map, ir)
    _index_artifacts(uri_map, ir, example_id)

    if example_id:
        _index_policies(uri_map, ir, example_id)

    _index_schedules(uri_map, ir)
    _index_generated_services(uri_map, ir)
    _index_desktop(uri_map, ir)

    if example_id:
        _index_deploy(uri_map, ir, example_id)

    _index_validations(uri_map, ir, example_id)
    return uri_map


def _get_id(obj: Any) -> str:
    return _get_id_field(obj, "id")


def _get_id_field(obj: Any, key: str) -> str:
    if isinstance(obj, dict):
        return str(obj.get(key, "") or "")
    return str(getattr(obj, key, "") or "")
