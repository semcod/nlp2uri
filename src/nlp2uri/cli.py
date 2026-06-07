"""nlp2uri CLI — uses CliAdapter and ShellAdapter."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from nlp2uri.adapters.base import AdapterRequest
from nlp2uri.adapters.cli import CliAdapter
from nlp2uri.adapters.shell import ShellAdapter
from nlp2uri.cli_parser import build_parser
from nlp2uri.config import (
    default_config,
    ensure_config,
    find_config_path,
    load_config,
    save_config,
)
from nlp2uri.models import HostPlatform


def _platform(raw: str | None) -> HostPlatform | None:
    if not raw:
        return None
    return HostPlatform(raw)


def _emit(payload: dict, *, as_json: bool) -> None:
    if as_json:
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")


def _request_from_args(args, *, operation: str) -> AdapterRequest:
    return AdapterRequest(
        operation=operation,
        prompt=getattr(args, "text", "") or "",
        uri=getattr(args, "uri", "") or "",
        platform=_platform(getattr(args, "platform", None)),
        dry_run=bool(getattr(args, "dry_run", False)),
    )


def _with_platform(payload: dict, *, as_json: bool) -> dict:
    if as_json:
        payload["platform"] = load_config().resolved_platform().value
    return payload


def _run_config(args) -> int:
    if args.config_command == "init":
        path = save_config(default_config(), Path(args.path))
        print(f"wrote {path}")
        return 0
    cfg = load_config()
    found = find_config_path()
    payload = {
        "config_path": str(found) if found else None,
        "effective_platform": cfg.resolved_platform().value,
        **cfg.to_dict(),
    }
    _emit(payload, as_json=args.json)
    return 0


def _run_shell(args) -> int:
    shell = ShellAdapter()
    if args.shell_command == "export":
        response = shell.handle(_request_from_args(args, operation="export"))
    else:
        response = shell.handle(
            AdapterRequest(
                operation="eval-uri",
                uri=args.uri,
                platform=_platform(args.platform),
            )
        )
    if args.json:
        _emit(response.to_dict(), as_json=True)
    else:
        sys.stdout.write(response.data.get("script", "") + "\n")
    return 0 if response.ok else response.status_code or 1


def _run_adapter_command(args, *, operation: str) -> int:
    cli = CliAdapter()
    if operation == "compile":
        req = AdapterRequest(operation="compile", uri=args.uri, platform=_platform(args.platform))
    else:
        req = _request_from_args(args, operation=operation)
    response = cli.handle(req)
    _emit(_with_platform(response.to_dict(), as_json=args.json), as_json=args.json)
    return 0 if response.ok else response.status_code or 1


def _run_envmap(args) -> int:
    from nlp2uri.systemmap.export import write_environment_map
    from nlp2uri.systemmap.index import build_uri_index
    from nlp2uri.systemmap.load import load_system_map_from_doql

    path = write_environment_map(
        args.project,
        project_id=args.project_id or None,
        output_format=args.format,
        merge_existing=not args.no_merge,
        probe_desktop=False if args.no_probe_desktop else None,
    )
    index = build_uri_index(load_system_map_from_doql(path))
    desktop_windows = index.find_by_kind("desktop_window")
    payload = {
        "path": str(path),
        "desktop_window_uris": len(desktop_windows),
        "uri_entries": len(index.entries),
    }
    _emit(payload, as_json=args.json)
    if not args.json:
        print(f"wrote {path}")
    return 0


def _run_execute(args) -> int:
    cli = CliAdapter()
    if getattr(args, "uri_only", False) or "://" in args.text:
        req = AdapterRequest(
            operation="execute",
            uri=args.text,
            platform=_platform(args.platform),
            dry_run=bool(args.dry_run),
        )
    else:
        req = _request_from_args(args, operation="execute")
    response = cli.handle(req)
    _emit(_with_platform(response.to_dict(), as_json=args.json), as_json=args.json)
    return 0 if response.ok else response.status_code or 1


_ADAPTER_COMMANDS = frozenset({"plan", "resolve", "compile"})
_EXECUTE_COMMANDS = frozenset({"execute", "open"})


def _dispatch_command(args) -> int:
    command = args.command
    if command == "config":
        return _run_config(args)
    if command == "envmap":
        return _run_envmap(args)

    ensure_config()

    if command == "shell":
        return _run_shell(args)
    if command in _ADAPTER_COMMANDS:
        return _run_adapter_command(args, operation=command)
    if command in _EXECUTE_COMMANDS:
        return _run_execute(args)
    raise SystemExit(f"unknown command: {command}")


def main(argv: list[str] | None = None) -> int:
    return _dispatch_command(build_parser().parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
