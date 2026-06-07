"""CLI for ``nlp2uri control`` — IDE control plan/execute/list-uris."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from nlp2uri.control_compile import compile_uri_to_control_plan, is_control_uri
from nlp2uri.control_execute import (
    compile_and_execute_control_uri,
    koruide_available,
    koruide_missing_message,
)
from nlp2uri.resolve import nlp2uri
from nlp2uri.schemes.util import abstract_url
from nlp2uri.service import NLP2URIService


def _add_lane_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--ide", default="auto", help="IDE lane (default: auto).")
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Project dir for workspace match.")
    parser.add_argument("--workspace", default="", help="Workspace path for ide-chat URI.")
    parser.add_argument("--socket", type=Path, default=None, help="Autopilot socket override.")
    parser.add_argument(
        "--instance",
        default=None,
        help="KORU_AUTOPILOT_INSTANCE for this run (e.g. cursor-main).",
    )


def add_control_parser(sub: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    control = sub.add_parser(
        "control",
        help="Koru IDE control: plan, execute, list-uris (mirror koru ide control).",
    )
    nested = control.add_subparsers(dest="control_action", required=True)

    from nlp2uri.cli_parser import add_text_args

    plan = nested.add_parser("plan", help="NL → koru.control.v1 plan.")
    plan.add_argument("prompt", help="Natural-language IDE control request.")
    plan.add_argument("--locale", default=None)
    add_text_args(plan)
    _add_lane_args(plan)
    plan.add_argument("--json", action="store_true", help="emit JSON")

    execute = nested.add_parser("execute", help="Plan + drive via koruide socket or CLI fallback.")
    execute.add_argument(
        "prompt",
        help="NL request or raw chat message when NL does not match.",
    )
    execute.add_argument("--locale", default=None)
    execute.add_argument("--dry-run", action="store_true", help="Plan only; do not drive.")
    execute.add_argument("--no-submit", action="store_true", help="Paste only; do not submit.")
    add_text_args(execute)
    _add_lane_args(execute)
    execute.add_argument("--json", action="store_true", help="emit JSON")

    list_uris = nested.add_parser("list-uris", help="URI index from Koru autopilot status JSON.")
    list_uris.add_argument(
        "--status-json",
        type=Path,
        default=None,
        help="Path to koru autopilot status --format systemmap JSON (default: run koru).",
    )
    _add_lane_args(list_uris)
    list_uris.add_argument("--json", action="store_true", help="emit JSON")


def _print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def _resolve_ide(args: argparse.Namespace) -> str:
    ide = (getattr(args, "ide", None) or "auto").strip().lower()
    if ide and ide != "auto":
        return ide
    instance = (
        getattr(args, "instance", None) or os.environ.get("KORU_AUTOPILOT_INSTANCE") or ""
    ).strip()
    if instance:
        return instance.split("-", 1)[0] if "-" in instance else instance
    return "cursor"


def _with_instance_env(args: argparse.Namespace) -> dict[str, str]:
    instance = (getattr(args, "instance", None) or "").strip()
    if not instance:
        return {}
    return {"KORU_AUTOPILOT_INSTANCE": instance}


def _socket_basename(instance: str) -> str:
    if not instance or instance.lower() == "auto":
        return "koru-autopilot.sock"
    slug_chars: list[str] = []
    for ch in instance[:64]:
        slug_chars.append(ch if ch.isalnum() or ch in "-_" else "-")
    slug = "".join(slug_chars).strip("-") or "instance"
    return f"koru-autopilot-{slug}.sock"


def _resolve_socket_path(args: argparse.Namespace, ide: str) -> Path:
    if getattr(args, "socket", None):
        return Path(args.socket).expanduser().resolve()
    explicit = os.environ.get("KORU_AUTOPILOT_SOCKET", "").strip()
    if explicit:
        return Path(explicit).expanduser().resolve()
    instance = (
        getattr(args, "instance", None)
        or os.environ.get("KORU_AUTOPILOT_INSTANCE")
        or ""
    ).strip()
    name = _socket_basename(instance)
    runtime = os.environ.get("XDG_RUNTIME_DIR")
    if runtime:
        return Path(runtime) / name
    return Path(f"/run/user/{os.getuid()}") / name


def _client_factory(args: argparse.Namespace, ide: str):
    socket_path = _resolve_socket_path(args, ide)

    def factory():
        from koruide.client import KoruIDEClient

        return KoruIDEClient(socket_path=socket_path)

    return factory, socket_path


def _fetch_autopilot_status(args: argparse.Namespace, ide: str) -> tuple[dict[str, Any] | None, str]:
    if not koruide_available():
        return None, koruide_missing_message()
    _factory, socket_path = _client_factory(args, ide)
    try:
        from koruide.client import KoruIDEClient
    except ImportError as exc:
        return None, str(exc)
    client = KoruIDEClient(socket_path=socket_path)
    if not client.is_running():
        return None, f"autopilot daemon not running on {socket_path}"
    try:
        status = client.status()
        return status if isinstance(status, dict) else None, ""
    except (OSError, RuntimeError) as exc:
        return None, str(exc)


def _resolve_workspace_from_status(
    status: dict[str, Any],
    ide: str,
    project: Path,
) -> str:
    plugins = status.get("plugins") if isinstance(status.get("plugins"), list) else []
    project_path = str(project.expanduser().resolve())
    for row in plugins:
        if not isinstance(row, dict):
            continue
        if str(row.get("ide") or "").strip().lower() != ide.strip().lower():
            continue
        folders = row.get("workspaceFolders")
        if not isinstance(folders, list) or not folders:
            continue
        for folder in folders:
            folder_s = str(folder).strip()
            if folder_s == project_path:
                return folder_s
        return str(folders[0]).strip()
    return ""


def _resolve_workspace(args: argparse.Namespace, ide: str) -> str:
    explicit = (getattr(args, "workspace", None) or "").strip()
    if explicit:
        return explicit
    status, _err = _fetch_autopilot_status(args, ide)
    if status:
        project = getattr(args, "project", None) or Path.cwd()
        return _resolve_workspace_from_status(status, ide, Path(project))
    return ""


def _default_strategy_hint(ide: str, submit: bool) -> str:
    if submit and ide.strip().lower() == "cursor":
        return "submit_alt_glass_first"
    return ""


def _control_uri(
    *,
    ide: str,
    message: str,
    submit: bool,
    workspace: str,
    require_plugin: bool = False,
) -> str:
    params: dict[str, str] = {
        "submit": "true" if submit else "false",
        "require_plugin": "true" if require_plugin else "false",
    }
    if workspace:
        params["workspace"] = workspace
    hint = _default_strategy_hint(ide, submit)
    if hint:
        params["strategy_hint"] = hint
    return abstract_url("ide-chat", ide, "/send", params=params)


def _apply_runtime_overrides(
    uri: str,
    *,
    ide: str,
    submit: bool,
    workspace: str,
) -> str:
    parsed = urlsplit(uri)
    if parsed.scheme.lower() != "ide-chat":
        return uri
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["submit"] = "true" if submit else "false"
    if workspace:
        query["workspace"] = workspace
    hint = _default_strategy_hint(ide, submit)
    if hint:
        query["strategy_hint"] = hint
    return urlunsplit((parsed.scheme, ide, parsed.path, urlencode(query), parsed.fragment))


def _text_ref_from_payload(payload: dict[str, Any], *, fallback: str = "") -> str:
    actions = (payload.get("control_plan") or {}).get("actions") or []
    if actions:
        ref = (actions[0] or {}).get("text_ref") or ""
        if ref:
            return ref
    plan = payload.get("plan")
    if isinstance(plan, dict):
        slots = plan.get("slots")
        if isinstance(slots, dict) and slots.get("text"):
            return str(slots["text"])
        spec = plan.get("spec")
        if isinstance(spec, dict):
            meta = spec.get("metadata")
            if isinstance(meta, dict) and meta.get("text"):
                return str(meta["text"])
    return fallback


def _submit_from_payload(payload: dict[str, Any], *, default: bool = True) -> bool:
    actions = (payload.get("control_plan") or {}).get("actions") or []
    if actions and "submit" in (actions[0] or {}):
        return bool((actions[0] or {})["submit"])
    plan = payload.get("plan")
    if isinstance(plan, dict):
        slots = plan.get("slots")
        if isinstance(slots, dict) and slots.get("submit") is not None:
            return str(slots["submit"]).strip().lower() in {"1", "true", "yes", "on"}
    return default


def _finalize_control_plan_payload(
    payload: dict[str, Any],
    *,
    ide: str,
    workspace: str,
    submit: bool | None = None,
    text_ref: str | None = None,
) -> dict[str, Any]:
    uri = str(payload.get("uri") or "")
    if not is_control_uri(uri):
        return payload
    effective_submit = submit if submit is not None else _submit_from_payload(payload)
    message = (text_ref or _text_ref_from_payload(payload)).strip()
    enriched_uri = _apply_runtime_overrides(
        uri,
        ide=ide,
        submit=effective_submit,
        workspace=workspace,
    )
    plan = compile_uri_to_control_plan(enriched_uri, text=message or None)
    if plan is None:
        return {**payload, "uri": enriched_uri}
    enriched = {**payload, "uri": enriched_uri, "control_plan": plan.to_dict()}
    nested = enriched.get("plan")
    if isinstance(nested, dict):
        nested_plan = dict(nested)
        nested_plan["uri"] = enriched_uri
        nested_plan["control_plan"] = plan.to_dict()
        spec = nested_plan.get("spec")
        if isinstance(spec, dict):
            nested_spec = dict(spec)
            nested_spec["uri"] = enriched_uri
            meta = nested_spec.get("metadata")
            if isinstance(meta, dict):
                nested_meta = dict(meta)
                if workspace:
                    nested_meta["workspace"] = workspace
                if message:
                    nested_meta["text"] = message
                nested_spec["metadata"] = nested_meta
            nested_plan["spec"] = nested_spec
        enriched["plan"] = nested_plan
    return enriched


def _plan_payload(
    prompt: str,
    *,
    text: str | None = None,
    locale: str | None = None,
    ide: str = "cursor",
    workspace: str = "",
    submit: bool | None = None,
) -> dict[str, Any]:
    result = nlp2uri(prompt, text=text, locale=locale)
    if result.control_plan is not None:
        payload = {
            "ok": True,
            "prompt": prompt,
            "drive_mode": "nlp",
            "uri": result.uri,
            "control_plan": result.control_plan.to_dict(),
            "plan": result.to_dict(),
            "control_surface": result.control_plan.actions[0].surface
            if result.control_plan.actions
            else "",
        }
        return _finalize_control_plan_payload(
            payload,
            ide=ide,
            workspace=workspace,
            submit=submit,
            text_ref=(text or "").strip() or None,
        )
    message = (text or prompt).strip()
    if message:
        effective_submit = True if submit is None else submit
        uri = _control_uri(
            ide=ide,
            message=message,
            submit=effective_submit,
            workspace=workspace,
        )
        plan = compile_uri_to_control_plan(uri, text=message)
        payload = {
            "ok": True,
            "prompt": prompt,
            "drive_mode": "direct",
            "uri": uri,
            "control_plan": plan.to_dict() if plan else None,
            "plan_hint": "NL did not match; showing direct ide-chat plan",
        }
        return _finalize_control_plan_payload(
            payload,
            ide=ide,
            workspace=workspace,
            submit=submit,
            text_ref=message,
        )
    return {
        "ok": False,
        "prompt": prompt,
        "error": "prompt did not resolve to an IDE control URI",
        "plan": result.to_dict(),
    }


def action_control_plan(args: argparse.Namespace) -> int:
    ide = _resolve_ide(args)
    workspace = _resolve_workspace(args, ide)
    payload_text = (getattr(args, "prompt_body", None) or "").strip() or None
    payload = _plan_payload(
        args.prompt,
        text=payload_text,
        locale=args.locale,
        ide=ide,
        workspace=workspace,
    )
    if args.json:
        _print_json(payload)
    else:
        if not payload.get("ok"):
            print(f"nlp2uri control plan: {payload.get('error', '?')}", file=sys.stderr)
            return 1
        print(payload.get("control_plan") or payload.get("uri", "?"))
    return 0 if payload.get("ok") else 1


def action_control_execute(args: argparse.Namespace) -> int:
    ide = _resolve_ide(args)
    workspace = _resolve_workspace(args, ide)
    submit = not args.no_submit
    payload_text = (getattr(args, "prompt_body", None) or "").strip() or None
    plan_payload = _plan_payload(
        args.prompt,
        text=payload_text,
        locale=args.locale,
        ide=ide,
        workspace=workspace,
        submit=submit,
    )
    if not plan_payload.get("ok"):
        if args.json:
            _print_json(plan_payload)
        else:
            print(f"nlp2uri control execute: {plan_payload.get('error', '?')}", file=sys.stderr)
        return 1

    uri = plan_payload["uri"]
    text_ref = payload_text or _text_ref_from_payload(
        plan_payload,
        fallback=args.prompt.strip() if plan_payload.get("drive_mode") == "direct" else "",
    ) or None

    client_factory = None
    if koruide_available():
        client_factory, _socket = _client_factory(args, ide)

    execution = compile_and_execute_control_uri(
        uri,
        text=text_ref,
        dry_run=args.dry_run,
        client_factory=client_factory,
    )
    payload = {
        "ok": bool(execution.get("ok")),
        "prompt": args.prompt,
        "uri": uri,
        "drive_mode": plan_payload.get("drive_mode"),
        "control_plan": execution.get("plan") or plan_payload.get("control_plan"),
        "execution": execution,
    }
    if args.json:
        _print_json(payload)
    else:
        if not payload["ok"]:
            results = execution.get("results") or []
            err = (results[0] or {}).get("error") if results else execution.get("error")
            print(f"nlp2uri control execute: {err or '?'}", file=sys.stderr)
            return 1
        top = (execution.get("results") or [{}])[0]
        print(
            f"ok={payload['ok']} backend={top.get('backend', '?')} "
            f"mode={plan_payload.get('drive_mode', '?')}"
        )
    return 0 if payload["ok"] else 1


def _load_status_json(args: argparse.Namespace) -> tuple[dict[str, Any] | None, str]:
    if args.status_json is not None:
        path = Path(args.status_json).expanduser()
        if not path.is_file():
            return None, f"status file not found: {path}"
        try:
            return json.loads(path.read_text(encoding="utf-8")), ""
        except json.JSONDecodeError as exc:
            return None, f"invalid status JSON: {exc}"

    cmd = ["koru", "autopilot", "status", "--format", "systemmap"]
    ide = _resolve_ide(args)
    if ide and ide != "auto":
        cmd.extend(["--ide", ide])
    env = {**os.environ, **_with_instance_env(args)}
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
            env=env,
        )
    except FileNotFoundError:
        return None, "koru not found; pass --status-json <path>"
    if proc.returncode != 0:
        return None, (proc.stderr or proc.stdout or "koru autopilot status failed").strip()
    try:
        return json.loads(proc.stdout), ""
    except json.JSONDecodeError as exc:
        return None, f"invalid koru status output: {exc}"


def action_control_list_uris(args: argparse.Namespace) -> int:
    status, err = _load_status_json(args)
    if status is None:
        print(f"nlp2uri control list-uris: {err}", file=sys.stderr)
        return 1
    ide = _resolve_ide(args)
    socket_path = str(status.get("socket") or _resolve_socket_path(args, ide))
    svc = NLP2URIService.default()
    payload = svc.list_koru_ide_uris(status, socket_path=socket_path)
    payload["ok"] = True
    plugins = status.get("plugins") if isinstance(status.get("plugins"), list) else []
    if args.json:
        _print_json(payload)
    else:
        entries = payload.get("entries") or {}
        print(f"socket={socket_path} entries={len(entries)}")
        for uri in sorted(entries):
            print(uri)
    if not plugins:
        print(
            "hint: no IDE plugin in status — connect VSIX in IDE or pass --status-json",
            file=sys.stderr,
        )
    return 0


def dispatch_control_action(args: argparse.Namespace) -> int:
    if args.control_action == "plan":
        return action_control_plan(args)
    if args.control_action == "execute":
        return action_control_execute(args)
    if args.control_action == "list-uris":
        return action_control_list_uris(args)
    print(f"nlp2uri control: unknown action {args.control_action}", file=sys.stderr)
    return 2
