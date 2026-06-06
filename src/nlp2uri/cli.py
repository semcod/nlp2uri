"""nlp2uri CLI — uses CliAdapter and ShellAdapter."""

from __future__ import annotations

import argparse
import json
import sys

from nlp2uri.adapters.base import AdapterRequest
from nlp2uri.adapters.cli import CliAdapter
from nlp2uri.adapters.shell import ShellAdapter
from nlp2uri.config import ensure_config, find_config_path, load_config, save_config
from nlp2uri.models import HostPlatform


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--platform",
        choices=[p.value for p in HostPlatform if p != HostPlatform.UNKNOWN],
        help="override platform (default: auto-detect via nlp2uri.yaml / host OS)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable JSON",
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nlp2uri",
        description="NL → URI compiler with CLI, shell, REST, and MCP adapters",
    )
    _add_common_args(parser)

    sub = parser.add_subparsers(dest="command", required=True)

    p_plan = sub.add_parser("plan", help="full NL → URI + OSActions plan")
    _add_common_args(p_plan)
    p_plan.add_argument("text")

    p_resolve = sub.add_parser("resolve", help="resolve natural language to a URI")
    _add_common_args(p_resolve)
    p_resolve.add_argument("text")

    p_compile = sub.add_parser("compile", help="compile URI to OS actions")
    _add_common_args(p_compile)
    p_compile.add_argument("uri")

    p_exec = sub.add_parser("execute", help="resolve and execute (or execute a raw URI)")
    _add_common_args(p_exec)
    p_exec.add_argument("text")
    p_exec.add_argument("--dry-run", action="store_true")
    p_exec.add_argument("--uri-only", action="store_true")

    p_open = sub.add_parser("open", help="shorthand for execute")
    _add_common_args(p_open)
    p_open.add_argument("text")
    p_open.add_argument("--dry-run", action="store_true")

    p_shell = sub.add_parser("shell", help="bash-friendly exports")
    shell_sub = p_shell.add_subparsers(dest="shell_command", required=True)
    p_export = shell_sub.add_parser("export", help="eval exports for a prompt")
    _add_common_args(p_export)
    p_export.add_argument("text")
    p_eval = shell_sub.add_parser("eval-uri", help="eval exports for a raw URI")
    _add_common_args(p_eval)
    p_eval.add_argument("uri")

    p_config = sub.add_parser("config", help="show or write nlp2uri.yaml defaults")
    config_sub = p_config.add_subparsers(dest="config_command", required=True)
    p_cfg_show = config_sub.add_parser("show", help="print effective config")
    _add_common_args(p_cfg_show)
    p_cfg_init = config_sub.add_parser("init", help="write nlp2uri.yaml with detected defaults")
    p_cfg_init.add_argument(
        "--path",
        default="nlp2uri.yaml",
        help="config file path (default: ./nlp2uri.yaml)",
    )

    return parser


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


def _request_from_args(args: argparse.Namespace, *, operation: str) -> AdapterRequest:
    return AdapterRequest(
        operation=operation,
        prompt=getattr(args, "text", "") or "",
        uri=getattr(args, "uri", "") or "",
        platform=_platform(getattr(args, "platform", None)),
        dry_run=bool(getattr(args, "dry_run", False)),
    )


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command != "config":
        ensure_config()

    if args.command == "config":
        if args.config_command == "init":
            from pathlib import Path

            from nlp2uri.config import default_config

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

    cli = CliAdapter()

    if args.command == "shell":
        shell = ShellAdapter()
        if args.shell_command == "export":
            response = shell.handle(_request_from_args(args, operation="export"))
        else:
            req = AdapterRequest(
                operation="eval-uri",
                uri=args.uri,
                platform=_platform(args.platform),
            )
            response = shell.handle(req)
        if args.json:
            _emit(response.to_dict(), as_json=True)
        else:
            sys.stdout.write(response.data.get("script", "") + "\n")
        return 0 if response.ok else response.status_code or 1

    if args.command in {"plan", "resolve", "compile"}:
        if args.command == "compile":
            req = AdapterRequest(operation="compile", uri=args.uri, platform=_platform(args.platform))
        else:
            req = _request_from_args(args, operation=args.command)
        response = cli.handle(req)
        payload = response.to_dict()
        if args.json:
            payload["platform"] = load_config().resolved_platform().value
        _emit(payload, as_json=args.json)
        return 0 if response.ok else response.status_code or 1

    uri_only = bool(getattr(args, "uri_only", False))
    if uri_only or "://" in args.text:
        req = AdapterRequest(
            operation="execute",
            uri=args.text,
            platform=_platform(args.platform),
            dry_run=bool(args.dry_run),
        )
    else:
        req = _request_from_args(args, operation="execute")

    response = cli.handle(req)
    payload = response.to_dict()
    if args.json:
        payload["platform"] = load_config().resolved_platform().value
    _emit(payload, as_json=args.json)
    return 0 if response.ok else response.status_code or 1


if __name__ == "__main__":
    raise SystemExit(main())
