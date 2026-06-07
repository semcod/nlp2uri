"""Execute compiled Koru control plans via koruide socket or CLI fallback."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass, field
from typing import Any, Callable

from nlp2uri.control_compile import compile_uri_to_control_plan, is_control_uri
from nlp2uri.models import ControlAction, ControlPlan

_KORUIDE_IMPORT_ERROR: str | None = None

try:
    from koruide.client import KoruIDEClient

    _KORUIDE_AVAILABLE = True
except ImportError as exc:
    _KORUIDE_AVAILABLE = False
    _KORUIDE_IMPORT_ERROR = str(exc)
    KoruIDEClient = None  # type: ignore[assignment,misc]


def koruide_available() -> bool:
    return _KORUIDE_AVAILABLE


def koruide_missing_message() -> str:
    if _KORUIDE_IMPORT_ERROR:
        return f"koruide is not importable ({_KORUIDE_IMPORT_ERROR})"
    return "koruide is not importable; install koru editable or set PYTHONPATH"


@dataclass
class ControlExecutionResult:
    ok: bool
    uri: str
    operation: str
    transport: str
    backend: str
    dry_run: bool = False
    reply: dict[str, Any] = field(default_factory=dict)
    error: str = ""
    returncode: int = 0
    verification_status: str = ""

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "ok": self.ok,
            "uri": self.uri,
            "operation": self.operation,
            "transport": self.transport,
            "backend": self.backend,
            "dry_run": self.dry_run,
            "verification_status": self.verification_status,
            "returncode": self.returncode,
        }
        if self.reply:
            payload["reply"] = self.reply
        if self.error:
            payload["error"] = self.error
        return payload


def _verification_status(action: ControlAction, reply: dict[str, Any]) -> str:
    if action.operation == "status":
        return "status_ok" if reply else "status_empty"
    ok = bool(reply.get("ok"))
    if not ok:
        if action.require_plugin and reply.get("backend") == "plugin_required":
            return "blocked_require_plugin"
        return "failed"
    if action.verification.expect_message_sent:
        if reply.get("intent_status") == "unverified":
            return "verification_failed"
        return "verified" if ok else "ack_failed"
    if action.verification.expect_ack:
        return "acknowledged" if ok else "ack_failed"
    return "completed"


def _build_client(
    *,
    client_factory: Callable[[], Any] | None = None,
    timeout: float = 45.0,
) -> Any:
    if client_factory is not None:
        return client_factory()
    assert KoruIDEClient is not None
    return KoruIDEClient(timeout=timeout)


def execute_control_action(
    action: ControlAction,
    *,
    uri: str = "",
    text: str | None = None,
    dry_run: bool = False,
    client_factory: Callable[[], Any] | None = None,
) -> ControlExecutionResult:
    payload_text = (text or action.text_ref or "").strip()
    uri_ref = uri or f"{action.surface}://{action.ide}/{action.operation}"

    if dry_run:
        return ControlExecutionResult(
            ok=True,
            uri=uri_ref,
            operation=action.operation,
            transport=action.transport,
            backend="dry_run",
            dry_run=True,
            reply={"replay": {"cli": list(action.replay_cli), "mcp": action.replay_mcp}},
            verification_status="planned",
        )

    if action.operation == "drive":
        if not payload_text:
            return ControlExecutionResult(
                ok=False,
                uri=uri_ref,
                operation=action.operation,
                transport=action.transport,
                backend="validation",
                error="drive requires text_ref",
                returncode=2,
                verification_status="blocked_missing_text",
            )
        return _execute_drive(
            action,
            uri_ref=uri_ref,
            text=payload_text,
            client_factory=client_factory,
        )

    if action.operation == "status":
        return _execute_status(action, uri_ref=uri_ref, client_factory=client_factory)

    if action.operation in {"execute", "command"}:
        return ControlExecutionResult(
            ok=False,
            uri=uri_ref,
            operation=action.operation,
            transport=action.transport,
            backend="not_implemented",
            error="ide command execution is planned; use koru_ide_commands MCP tool",
            returncode=2,
            verification_status="deferred",
        )

    return ControlExecutionResult(
        ok=False,
        uri=uri_ref,
        operation=action.operation,
        transport=action.transport,
        backend="unsupported",
        error=f"unsupported control operation: {action.operation}",
        returncode=2,
        verification_status="unsupported",
    )


def execute_control_plan(
    plan: ControlPlan,
    *,
    text: str | None = None,
    dry_run: bool = False,
    client_factory: Callable[[], Any] | None = None,
) -> list[ControlExecutionResult]:
    results: list[ControlExecutionResult] = []
    for action in plan.actions:
        results.append(
            execute_control_action(
                action,
                uri=plan.uri,
                text=text,
                dry_run=dry_run,
                client_factory=client_factory,
            )
        )
    return results


def compile_and_execute_control_uri(
    uri: str,
    *,
    text: str | None = None,
    dry_run: bool = False,
    client_factory: Callable[[], Any] | None = None,
) -> dict[str, Any]:
    plan = compile_uri_to_control_plan(uri, text=text)
    if plan is None:
        return {"ok": False, "error": f"not a control URI: {uri}"}
    results = execute_control_plan(
        plan,
        text=text,
        dry_run=dry_run,
        client_factory=client_factory,
    )
    ok = all(result.ok for result in results) if results else False
    return {
        "ok": ok,
        "uri": uri,
        "plan": plan.to_dict(),
        "results": [result.to_dict() for result in results],
        "koruide_available": koruide_available(),
    }


def _execute_drive(
    action: ControlAction,
    *,
    uri_ref: str,
    text: str,
    client_factory: Callable[[], Any] | None,
) -> ControlExecutionResult:
    if client_factory is not None or _KORUIDE_AVAILABLE:
        client = _build_client(client_factory=client_factory)
        if not client.is_running():
            return _execute_cli(action, uri_ref=uri_ref, text=text, reason="daemon_not_running")
        reply = client.drive(
            text,
            submit=action.submit,
            ide=action.ide or "auto",
            require_plugin=action.require_plugin,
            strategy_hint=action.strategy_hint or None,
        )
        ok = bool(reply.get("ok"))
        return ControlExecutionResult(
            ok=ok,
            uri=uri_ref,
            operation=action.operation,
            transport=action.transport,
            backend="koruide_socket",
            reply=reply,
            returncode=0 if ok else 1,
            verification_status=_verification_status(action, reply),
            error="" if ok else str(reply.get("message") or reply.get("error") or ""),
        )
    return _execute_cli(action, uri_ref=uri_ref, text=text, reason="koruide_unavailable")


def _execute_status(
    action: ControlAction,
    *,
    uri_ref: str,
    client_factory: Callable[[], Any] | None,
) -> ControlExecutionResult:
    if client_factory is not None or _KORUIDE_AVAILABLE:
        client = _build_client(client_factory=client_factory)
        if not client.is_running():
            return _execute_cli(action, uri_ref=uri_ref, text="", reason="daemon_not_running")
        reply = client.status()
        return ControlExecutionResult(
            ok=True,
            uri=uri_ref,
            operation=action.operation,
            transport=action.transport,
            backend="koruide_socket",
            reply=reply if isinstance(reply, dict) else {"status": reply},
            verification_status="status_ok",
        )
    return _execute_cli(action, uri_ref=uri_ref, text="", reason="koruide_unavailable")


def _execute_cli(
    action: ControlAction,
    *,
    uri_ref: str,
    text: str,
    reason: str,
) -> ControlExecutionResult:
    argv = list(action.replay_cli)
    if not argv:
        return ControlExecutionResult(
            ok=False,
            uri=uri_ref,
            operation=action.operation,
            transport=action.transport,
            backend="cli",
            error=f"no replay CLI for {action.operation} ({reason})",
            returncode=2,
            verification_status="blocked_no_replay",
        )
    if action.operation == "drive" and "--prompt" not in argv and text:
        argv = [*argv, "--prompt", text]
    try:
        proc = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=float(os.environ.get("NLP2URI_KORU_CLI_TIMEOUT", "180")),
            check=False,
        )
    except FileNotFoundError:
        return ControlExecutionResult(
            ok=False,
            uri=uri_ref,
            operation=action.operation,
            transport=action.transport,
            backend="cli",
            error=f"command not found: {argv[0]}",
            returncode=127,
            verification_status="cli_missing",
        )
    except subprocess.TimeoutExpired:
        return ControlExecutionResult(
            ok=False,
            uri=uri_ref,
            operation=action.operation,
            transport=action.transport,
            backend="cli",
            error="koru CLI timed out",
            returncode=124,
            verification_status="cli_timeout",
        )
    ok = proc.returncode == 0
    return ControlExecutionResult(
        ok=ok,
        uri=uri_ref,
        operation=action.operation,
        transport=action.transport,
        backend="cli",
        reply={"stdout": proc.stdout, "stderr": proc.stderr},
        returncode=proc.returncode,
        verification_status="cli_ok" if ok else "cli_failed",
        error=proc.stderr.strip() if not ok else "",
    )


__all__ = [
    "ControlExecutionResult",
    "compile_and_execute_control_uri",
    "execute_control_action",
    "execute_control_plan",
    "is_control_uri",
    "koruide_available",
    "koruide_missing_message",
]
