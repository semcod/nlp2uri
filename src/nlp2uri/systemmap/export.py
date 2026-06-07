"""Write env2llm ``environment.*`` maps with nlp2uri desktop URI mapping."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Mapping

from nlp2uri.systemmap.load import env2llm_missing_message, env2llm_available
from nlp2uri.systemmap.uri import (
    uri_for_desktop_window_focus,
    uri_for_desktop_window_screenshot,
)


def _require_env2llm() -> None:
    if not env2llm_available():
        raise RuntimeError(env2llm_missing_message())


def _ir_field(ir: Any, name: str, default: Any = None) -> Any:
    if isinstance(ir, dict):
        return ir.get(name, default)
    return getattr(ir, name, default)


def apply_desktop_uri_mapping(ir: Any) -> Any:
    """
    Mirror per-window nlp2uri URIs into ``ir.data`` for env2llm render/LLM context.

    Called after ``apply_desktop_probe`` so ``environment.doql.less`` carries
    addressable ``desktop-window://`` and ``desktop-screenshot://`` entries.
    """
    desktop = _ir_field(ir, "desktop")
    if desktop is None:
        return ir

    windows = _ir_field(desktop, "windows") or []
    data = _ir_field(ir, "data")
    if data is None:
        data = {}
        if hasattr(ir, "data"):
            ir.data = data
        elif isinstance(ir, dict):
            ir["data"] = data

    for index, window in enumerate(windows):
        prefix = f"desktop.windows[{index}]"
        focus_uri = uri_for_desktop_window_focus(window)
        screenshot_uri = uri_for_desktop_window_screenshot(window)
        data[f"{prefix}.focus_uri"] = focus_uri
        data[f"{prefix}.screenshot_uri"] = screenshot_uri

        title = _ir_field(window, "title", "")
        if title:
            data[f"{prefix}.title"] = title
        if _ir_field(window, "active"):
            data["desktop.active_window.focus_uri"] = focus_uri
            data["desktop.active_window.screenshot_uri"] = screenshot_uri

    data["desktop.uri_mapping"] = "nlp2uri.system_map_uri.v1"
    data["desktop.mapped_window_count"] = len(windows)
    return ir


def write_environment_map(
    project_dir: Path | str,
    *,
    project_id: str | None = None,
    output_format: str = "doql.less",
    environment: Mapping[str, str] | None = None,
    client: Any | None = None,
    merge_existing: bool = True,
    attachment: bool | None = None,
    auto_execute: bool | None = None,
    probe_desktop: bool | None = None,
    probe_mcp: bool | None = None,
    probe_testql: bool | None = None,
) -> Path:
    """
    Generate ``.nlp2dsl/registry/environment.*`` with desktop URI mapping.

    Same pipeline as ``env2llm.ensure_environment_map``, plus
    :func:`apply_desktop_uri_mapping` before render.
    """
    _require_env2llm()

    from env2llm.bootstrap import project_artifact_root
    from env2llm.env import collect_environment, merge_environment
    from env2llm.formats import default_output_name, render_format
    from env2llm.generate import generate_system_map
    from env2llm.layout import ensure_layout, write_registry
    from env2llm.policy.desktop import apply_desktop_probe
    from env2llm.policy.invoice import apply_invoice_policies
    from env2llm.policy.mcp import apply_mcp_probe
    from env2llm.policy.testql import apply_testql_probe
    from env2llm.policy.process import apply_process_policies
    from env2llm.registry import merge_registry_observations

    root = Path(project_dir).resolve()
    project = project_id or root.name
    artifact_root = project_artifact_root(root)
    ensure_layout(artifact_root)

    env = merge_environment(collect_environment(), environment)
    ir = generate_system_map(
        root,
        example_id=project,
        environment=env,
        client=client,
    )

    if auto_execute is None:
        auto_execute = os.environ.get("NLP2DSL_AUTO_EXECUTE", "1").strip().lower() in (
            "1",
            "true",
            "yes",
        )
    if auto_execute:
        ir.conversation.sync_auto_execute = True

    registry_path = artifact_root / "registry" / "environment.doql.less"
    if merge_existing and registry_path.is_file():
        merge_registry_observations(ir, registry_path)

    repo_root = root.parent.parent if root.parent.name == "examples" else root.parent
    apply_process_policies(ir, example_id=project, repo_root=repo_root)
    apply_invoice_policies(ir, example_id=project, attachment=attachment)
    apply_desktop_probe(ir, enabled=probe_desktop)
    apply_mcp_probe(ir, enabled=probe_mcp, project_dir=root)
    apply_testql_probe(ir, enabled=probe_testql, project_dir=root)
    apply_desktop_uri_mapping(ir)

    content = render_format(ir, output_format)
    out_name = default_output_name(output_format)
    if out_name == "environment.doql.less":
        path = write_registry(artifact_root, content)
    else:
        out_dir = artifact_root / "registry"
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / out_name
        path.write_text(content, encoding="utf-8")
        mirror = artifact_root / out_name
        if mirror != path:
            mirror.write_text(content, encoding="utf-8")

    os.environ.setdefault("ENV2LLM_CONTEXT", str(path))
    os.environ.setdefault("NLP2DSL_DOQL_CONTEXT", str(path))
    return path
