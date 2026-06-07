"""argparse wiring for the ``nlp2uri`` CLI."""

from __future__ import annotations

import argparse

from nlp2uri.models import HostPlatform


def add_common_args(parser: argparse.ArgumentParser) -> None:
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nlp2uri",
        description="NL → URI compiler with CLI, shell, REST, and MCP adapters",
    )
    add_common_args(parser)

    sub = parser.add_subparsers(dest="command", required=True)

    p_plan = sub.add_parser("plan", help="full NL → URI + OSActions plan")
    add_common_args(p_plan)
    p_plan.add_argument("text")

    p_resolve = sub.add_parser("resolve", help="resolve natural language to a URI")
    add_common_args(p_resolve)
    p_resolve.add_argument("text")

    p_compile = sub.add_parser("compile", help="compile URI to OS actions")
    add_common_args(p_compile)
    p_compile.add_argument("uri")

    p_exec = sub.add_parser("execute", help="resolve and execute (or execute a raw URI)")
    add_common_args(p_exec)
    p_exec.add_argument("text")
    p_exec.add_argument("--dry-run", action="store_true")
    p_exec.add_argument("--uri-only", action="store_true")

    p_open = sub.add_parser("open", help="shorthand for execute")
    add_common_args(p_open)
    p_open.add_argument("text")
    p_open.add_argument("--dry-run", action="store_true")

    p_shell = sub.add_parser("shell", help="bash-friendly exports")
    shell_sub = p_shell.add_subparsers(dest="shell_command", required=True)
    p_export = shell_sub.add_parser("export", help="eval exports for a prompt")
    add_common_args(p_export)
    p_export.add_argument("text")
    p_eval = shell_sub.add_parser("eval-uri", help="eval exports for a raw URI")
    add_common_args(p_eval)
    p_eval.add_argument("uri")

    p_config = sub.add_parser("config", help="show or write nlp2uri.yaml defaults")
    config_sub = p_config.add_subparsers(dest="config_command", required=True)
    p_cfg_show = config_sub.add_parser("show", help="print effective config")
    add_common_args(p_cfg_show)
    p_cfg_init = config_sub.add_parser("init", help="write nlp2uri.yaml with detected defaults")
    p_cfg_init.add_argument(
        "--path",
        default="nlp2uri.yaml",
        help="config file path (default: ./nlp2uri.yaml)",
    )

    p_envmap = sub.add_parser(
        "envmap",
        help="write env2llm environment.* with nlp2uri desktop URI mapping",
    )
    add_common_args(p_envmap)
    envmap_sub = p_envmap.add_subparsers(dest="envmap_command", required=True)
    p_envmap_write = envmap_sub.add_parser(
        "write",
        help="generate .nlp2dsl/registry/environment.* for a project directory",
    )
    add_common_args(p_envmap_write)
    p_envmap_write.add_argument(
        "--project",
        default=".",
        help="project directory (default: current directory)",
    )
    p_envmap_write.add_argument(
        "--project-id",
        default="",
        help="override example_id / project id (default: directory name)",
    )
    p_envmap_write.add_argument(
        "--format",
        default="doql.less",
        help="output format: doql.less, yaml, json, markdown (default: doql.less)",
    )
    p_envmap_write.add_argument(
        "--no-probe-desktop",
        action="store_true",
        help="skip live desktop window probe",
    )
    p_envmap_write.add_argument(
        "--no-merge",
        action="store_true",
        help="do not merge existing registry observations",
    )

    return parser
