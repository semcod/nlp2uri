"""IDE-oriented URI builders."""

from __future__ import annotations

from pathlib import Path

from nlp2uri.models import UriIntent, UriSpec
from nlp2uri.schemes.util import abstract_url, normalize_path

_IDE_SCHEMES = {
    "cursor": "cursor",
    "vscode": "vscode",
    "code": "vscode",
}


def build_ide(intent: UriIntent) -> UriSpec:
    ide = (intent.params.get("ide") or "vscode").lower()
    path = intent.params.get("path") or intent.target
    if not path:
        raise ValueError("ide intent requires path")

    normalized = normalize_path(path)
    native_scheme = _IDE_SCHEMES.get(ide, ide)
    native_uri = f"{native_scheme}://file{Path(normalized).as_posix()}"
    uri = abstract_url("app", ide, "/open", params={"path": normalized})

    return UriSpec(
        uri=uri,
        scheme="app",
        action="open",
        platform_hints=("xdg-open", "open", "start"),
        metadata={"ide": ide, "path": normalized, "native_uri": native_uri},
        intent=intent,
    )


def build_ide_chat_send(intent: UriIntent) -> UriSpec:
    ide = (intent.params.get("ide") or "auto").lower()
    params = {
        "workspace": intent.params.get("workspace", ""),
        "submit": intent.params.get("submit", "true"),
        "require_plugin": intent.params.get("require_plugin", "false"),
        "strategy_hint": intent.params.get("strategy_hint", ""),
    }
    uri = abstract_url("ide-chat", ide, "/send", params=params)
    metadata = {
        "ide": ide,
        "workspace": params["workspace"],
        "surface": "ide_chat",
        "transport": "koruide_socket",
        "submit": params["submit"],
        "require_plugin": params["require_plugin"],
    }
    text = intent.params.get("text", "")
    if text:
        metadata["text"] = text

    return UriSpec(
        uri=uri,
        scheme="ide-chat",
        action="send",
        platform_hints=("koru", "koru_ide_drive", "koruide_socket"),
        metadata=metadata,
        intent=intent,
    )


def build_ide_command(intent: UriIntent) -> UriSpec:
    ide = (intent.params.get("ide") or "auto").lower()
    command = intent.params.get("command", intent.target)
    params = {
        "command": command,
        "workspace": intent.params.get("workspace", ""),
        "require_plugin": intent.params.get("require_plugin", "true"),
    }
    capability = intent.params.get("capability", "")
    if capability:
        params["capability"] = capability
    uri = abstract_url("ide-command", ide, "/execute", params=params)
    return UriSpec(
        uri=uri,
        scheme="ide-command",
        action="execute",
        platform_hints=("koru", "koruide_socket"),
        metadata={
            "ide": ide,
            "command": command,
            "capability": capability,
            "surface": "ide_command",
            "transport": "koruide_socket",
        },
        intent=intent,
    )


def build_koru_control_drive(intent: UriIntent) -> UriSpec:
    ide = (intent.params.get("ide") or "auto").lower()
    params = {
        "ide": ide,
        "workspace": intent.params.get("workspace", ""),
        "submit": intent.params.get("submit", "true"),
        "require_plugin": intent.params.get("require_plugin", "false"),
        "strategy_hint": intent.params.get("strategy_hint", ""),
    }
    uri = abstract_url("koru-control", "ide", "/drive", params=params)
    metadata = {
        "ide": ide,
        "surface": "ide",
        "transport": "koruide_socket",
        "operation": "drive",
    }
    text = intent.params.get("text", "")
    if text:
        metadata["text"] = text
    return UriSpec(
        uri=uri,
        scheme="koru-control",
        action="drive",
        platform_hints=("koru", "koru_ide_drive", "koruide_socket"),
        metadata=metadata,
        intent=intent,
    )


def build_ide_status(intent: UriIntent) -> UriSpec:
    ide = (intent.params.get("ide") or "auto").lower()
    uri = abstract_url("koru-control", "ide", "/status", params={"ide": ide})
    return UriSpec(
        uri=uri,
        scheme="koru-control",
        action="status",
        platform_hints=("koru", "koruide_socket"),
        metadata={"ide": ide, "surface": "ide", "transport": "koruide_socket"},
        intent=intent,
    )
