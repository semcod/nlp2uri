"""nlp2uri CLI."""

from __future__ import annotations

import argparse
import json
import sys

from nlp2uri.compile import compile_uri_to_actions
from nlp2uri.models import HostPlatform
from nlp2uri.resolve import nlp2uri, resolve_text
from nlp2uri.runtime import execute_uri


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--platform",
        choices=[p.value for p in HostPlatform if p != HostPlatform.UNKNOWN],
        help="override detected host platform for resolution/execution",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable JSON",
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nlp2uri",
        description="NL → abstract URI compiler and cross-platform desktop executor",
    )
    _add_common_args(parser)

    sub = parser.add_subparsers(dest="command", required=True)

    p_plan = sub.add_parser("plan", help="full NL → URI + OSActions plan")
    _add_common_args(p_plan)
    p_plan.add_argument("text")

    p_resolve = sub.add_parser("resolve", help="resolve natural language to a URI")
    _add_common_args(p_resolve)
    p_resolve.add_argument("text", help="natural language description")

    p_compile = sub.add_parser("compile", help="compile URI to OS actions")
    _add_common_args(p_compile)
    p_compile.add_argument("uri")

    p_exec = sub.add_parser("execute", help="resolve and execute (or execute a raw URI)")
    _add_common_args(p_exec)
    p_exec.add_argument("text", help="natural language description or absolute URI")
    p_exec.add_argument("--dry-run", action="store_true")
    p_exec.add_argument("--uri-only", action="store_true")

    p_open = sub.add_parser("open", help="shorthand for execute")
    _add_common_args(p_open)
    p_open.add_argument("text")
    p_open.add_argument("--dry-run", action="store_true")

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


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    platform = _platform(args.platform)

    if args.command == "plan":
        result = nlp2uri(args.text, os=platform)
        _emit(result.to_dict(), as_json=args.json)
        return 0

    if args.command == "resolve":
        spec = resolve_text(args.text, platform=platform)
        _emit(spec.to_dict(), as_json=args.json)
        return 0

    if args.command == "compile":
        actions = compile_uri_to_actions(args.uri, platform)
        payload = {"uri": args.uri, "actions": [a.to_dict() for a in actions]}
        _emit(payload, as_json=args.json)
        return 0

    dry_run = bool(getattr(args, "dry_run", False))
    uri_only = bool(getattr(args, "uri_only", False))

    if uri_only or "://" in args.text:
        uri = args.text
        spec_payload = {"uri": uri, "resolved_from": "raw"}
    else:
        spec = resolve_text(args.text, platform=platform)
        uri = spec.uri
        spec_payload = spec.to_dict()

    result = execute_uri(uri, platform=platform, dry_run=dry_run)
    payload = {"spec": spec_payload, "result": result.to_dict()}
    _emit(payload, as_json=args.json)
    return 0 if result.ok else result.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())
