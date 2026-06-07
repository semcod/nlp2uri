"""Compile Koru IDE control URIs to koru.control.v1 plans."""

from __future__ import annotations

from urllib.parse import parse_qs, unquote, urlparse

from nlp2uri.models import ControlAction, ControlPlan, ControlVerification

_CONTROL_SCHEMES = frozenset({"ide-chat", "ide-command", "koru-control"})
_IDE_OPEN_SCHEMES = frozenset({"ide"})


def is_control_uri(uri: str) -> bool:
    scheme = urlparse(uri).scheme.lower()
    return scheme in _CONTROL_SCHEMES or scheme in _IDE_OPEN_SCHEMES


def _query_params(parsed) -> dict[str, str]:
    raw = parse_qs(parsed.query, keep_blank_values=False)
    return {k: unquote(v[0]) for k, v in raw.items() if v}


def _truthy(value: str | None, *, default: bool = False) -> bool:
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _default_strategy_hint(ide: str, submit: bool, hint: str) -> str:
    if hint:
        return hint
    if submit and ide.strip().lower() == "cursor":
        return "submit_alt_glass_first"
    return ""


def _replay_cli_drive(
    *,
    ide: str,
    workspace: str,
    submit: bool,
    require_plugin: bool,
    text: str,
) -> list[str]:
    args = ["koru", "autopilot", "drive", "--ide", ide or "auto"]
    if not submit:
        args.append("--no-submit")
    if require_plugin:
        args.append("--require-plugin")
    if workspace:
        args.extend(["--project", workspace])
    if text:
        args.extend(["--prompt", text])
    return args


def _replay_cli_status(*, ide: str, workspace: str) -> list[str]:
    args = ["koru", "autopilot", "status", "--ide", ide or "auto"]
    if workspace:
        args.extend(["--project", workspace])
    return args


def compile_uri_to_control_plan(
    uri: str,
    *,
    text: str | None = None,
) -> ControlPlan | None:
    """Compile a control URI into a structured koru.control.v1 plan."""
    parsed = urlparse(uri)
    scheme = parsed.scheme.lower()
    if scheme not in _CONTROL_SCHEMES and scheme not in _IDE_OPEN_SCHEMES:
        return None

    params = _query_params(parsed)
    authority = (parsed.netloc or params.get("ide") or "auto").lower()
    path_action = parsed.path.strip("/") or "send"
    payload_text = (text or params.get("text") or "").strip()

    if scheme == "ide":
        action = path_action or "open"
        workspace = params.get("workspace") or params.get("path") or ""
        return ControlPlan(
            uri=uri,
            actions=(
                ControlAction(
                    surface="ide",
                    transport="koru_cli",
                    operation=action,
                    ide=authority,
                    workspace=workspace,
                    submit=False,
                    require_plugin=False,
                    text_ref=payload_text,
                    verification=ControlVerification(
                        expect_ack=False,
                        expect_message_sent=False,
                    ),
                    replay_cli=["koru", "autopilot", "manage", "--ide", authority]
                    if action == "open"
                    else _replay_cli_status(ide=authority, workspace=workspace),
                    replay_mcp="",
                ),
            ),
        )

    if scheme == "ide-chat":
        if path_action != "send":
            raise ValueError(f"unsupported ide-chat action: {path_action}")
        workspace = params.get("workspace", "")
        submit = _truthy(params.get("submit"), default=True)
        require_plugin = _truthy(params.get("require_plugin"), default=False)
        strategy_hint = _default_strategy_hint(
            authority,
            submit,
            params.get("strategy_hint", ""),
        )
        return ControlPlan(
            uri=uri,
            actions=(
                ControlAction(
                    surface="ide_chat",
                    transport="koruide_socket",
                    operation="drive",
                    ide=authority,
                    workspace=workspace,
                    submit=submit,
                    require_plugin=require_plugin,
                    strategy_hint=strategy_hint,
                    text_ref=payload_text,
                    verification=ControlVerification(
                        expect_ack=True,
                        expect_message_sent=submit,
                    ),
                    replay_cli=_replay_cli_drive(
                        ide=authority,
                        workspace=workspace,
                        submit=submit,
                        require_plugin=require_plugin,
                        text=payload_text,
                    ),
                    replay_mcp="koru_ide_drive",
                ),
            ),
        )

    if scheme == "ide-command":
        command = params.get("command", "")
        capability = params.get("capability", "")
        workspace = params.get("workspace", "")
        return ControlPlan(
            uri=uri,
            actions=(
                ControlAction(
                    surface="ide_command",
                    transport="koruide_socket",
                    operation=path_action or "execute",
                    ide=authority,
                    workspace=workspace,
                    submit=False,
                    require_plugin=_truthy(params.get("require_plugin"), default=True),
                    text_ref=command,
                    verification=ControlVerification(expect_ack=True),
                    replay_cli=[
                        "koru",
                        "ide",
                        "command",
                        "--ide",
                        authority,
                        "--command",
                        command,
                    ]
                    if command
                    else [],
                    replay_mcp="koru_ide_commands",
                    metadata={"capability": capability} if capability else {},
                ),
            ),
        )

    if scheme == "koru-control":
        surface = authority
        operation = path_action or "status"
        ide = (params.get("ide") or "auto").lower()
        workspace = params.get("workspace", "")
        if surface != "ide":
            raise ValueError(f"unsupported koru-control surface: {surface}")
        if operation == "drive":
            submit = _truthy(params.get("submit"), default=True)
            require_plugin = _truthy(params.get("require_plugin"), default=False)
            strategy_hint = _default_strategy_hint(
                ide,
                submit,
                params.get("strategy_hint", ""),
            )
            return ControlPlan(
                uri=uri,
                actions=(
                    ControlAction(
                        surface="ide",
                        transport="koruide_socket",
                        operation="drive",
                        ide=ide,
                        workspace=workspace,
                        submit=submit,
                        require_plugin=require_plugin,
                        strategy_hint=strategy_hint,
                        text_ref=payload_text,
                        verification=ControlVerification(
                            expect_ack=True,
                            expect_message_sent=submit,
                        ),
                        replay_cli=_replay_cli_drive(
                            ide=ide,
                            workspace=workspace,
                            submit=submit,
                            require_plugin=require_plugin,
                            text=payload_text,
                        ),
                        replay_mcp="koru_ide_drive",
                    ),
                ),
            )
        if operation == "status":
            return ControlPlan(
                uri=uri,
                actions=(
                    ControlAction(
                        surface="ide",
                        transport="koruide_socket",
                        operation="status",
                        ide=ide,
                        workspace=workspace,
                        submit=False,
                        require_plugin=False,
                        verification=ControlVerification(expect_ack=False),
                        replay_cli=_replay_cli_status(ide=ide, workspace=workspace),
                        replay_mcp="koru_ide_commands",
                    ),
                ),
            )
        raise ValueError(f"unsupported koru-control operation: {operation}")

    return None
