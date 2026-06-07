"""Build URI index entries from live Koru autopilot status."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from nlp2uri.schemes.util import abstract_url
from nlp2uri.systemmap.index import UriMap, _add_entry


def _workspace_query(workspace: str) -> str:
    return quote(workspace, safe="")


def build_koru_ide_uri_index(
    status: dict[str, Any],
    *,
    socket_path: str = "",
) -> UriMap:
    """Derive ide:// / ide-chat:// / koru-control:// entries from autopilot status."""
    uri_map = UriMap(
        example_id="koru-ide-live",
        system_map_format="koru.autopilot.status.v1",
    )

    daemon = status.get("daemon") if isinstance(status.get("daemon"), dict) else {}
    plugins = status.get("plugins") if isinstance(status.get("plugins"), list) else []

    drive_uri = abstract_url("koru-control", "ide", "/drive")
    _add_entry(
        uri_map,
        uri=drive_uri,
        kind="control_surface",
        ref_type="KoruControlSurface",
        name="ide_drive",
        ref={
            "operation": "drive",
            "transport": "koruide_socket",
            "socket": socket_path,
        },
        links=(),
    )

    status_uri = abstract_url("koru-control", "ide", "/status")
    _add_entry(
        uri_map,
        uri=status_uri,
        kind="control_surface",
        ref_type="KoruControlSurface",
        name="ide_status",
        ref={"operation": "status", "socket": socket_path},
        links=(drive_uri,),
    )

    if daemon:
        daemon_uri = abstract_url(
            "koru-control",
            "daemon",
            "/status",
            params={"socket": socket_path} if socket_path else None,
        )
        _add_entry(
            uri_map,
            uri=daemon_uri,
            kind="koru_daemon",
            ref_type="KoruDaemon",
            name=str(daemon.get("version") or "daemon"),
            ref=daemon,
            links=(status_uri,),
        )

    for plugin in plugins:
        if not isinstance(plugin, dict):
            continue
        ide = str(plugin.get("ide") or "auto").lower()
        ide_uri = f"ide://{ide}"
        _add_entry(
            uri_map,
            uri=ide_uri,
            kind="ide",
            ref_type="IdeInstance",
            name=ide,
            ref={
                "ide": ide,
                "version": plugin.get("version"),
                "buildSha": plugin.get("buildSha"),
                "protocolVersion": plugin.get("protocolVersion"),
            },
            links=(drive_uri, status_uri),
        )

        plugin_uri = abstract_url(
            "koru-control",
            "plugin",
            f"/{ide}",
            params={"version": str(plugin.get("version") or "")},
        )
        _add_entry(
            uri_map,
            uri=plugin_uri,
            kind="ide_plugin",
            ref_type="IdePlugin",
            name=f"{ide}@{plugin.get('version', '?')}",
            ref=plugin,
            links=(ide_uri, drive_uri),
        )

        workspaces = plugin.get("workspaceFolders") or []
        if not isinstance(workspaces, list):
            workspaces = []
        for folder in workspaces:
            if not isinstance(folder, str) or not folder.strip():
                continue
            workspace = folder.strip()
            ws_segment = _workspace_query(workspace)
            workspace_uri = f"ide://{ide}/workspace/{ws_segment}"
            chat_uri = abstract_url(
                "ide-chat",
                ide,
                "/send",
                params={"workspace": workspace, "submit": "true"},
            )
            _add_entry(
                uri_map,
                uri=workspace_uri,
                kind="ide_workspace",
                ref_type="IdeWorkspace",
                name=workspace,
                ref={"ide": ide, "workspace": workspace, "workspaceName": plugin.get("workspaceName")},
                links=(ide_uri, chat_uri),
            )
            _add_entry(
                uri_map,
                uri=chat_uri,
                kind="ide_chat",
                ref_type="IdeChatSurface",
                name=f"{ide}:{workspace}",
                ref={
                    "ide": ide,
                    "workspace": workspace,
                    "transport": "koruide_socket",
                },
                links=(workspace_uri, plugin_uri, drive_uri),
            )

        catalog = plugin.get("commandCatalog") or plugin.get("matchingCommands")
        if isinstance(catalog, dict):
            for capability, commands in catalog.items():
                if not isinstance(commands, list):
                    continue
                for command in commands:
                    if not isinstance(command, str) or not command:
                        continue
                    cmd_uri = abstract_url(
                        "ide-command",
                        ide,
                        "/execute",
                        params={"command": command, "capability": str(capability)},
                    )
                    _add_entry(
                        uri_map,
                        uri=cmd_uri,
                        kind="ide_command",
                        ref_type="IdeCommand",
                        name=command,
                        ref={"ide": ide, "command": command, "capability": str(capability)},
                        links=(ide_uri, plugin_uri),
                    )
                    uri_map.by_name.setdefault(command, []).append(cmd_uri)

    return uri_map


def merge_koru_ide_index(base: UriMap, status: dict[str, Any], *, socket_path: str = "") -> UriMap:
    """Merge live Koru IDE entries into an existing UriMap."""
    live = build_koru_ide_uri_index(status, socket_path=socket_path)
    for uri, entry in live.entries.items():
        base.entries[uri] = entry
    for name, uris in live.by_name.items():
        base.by_name.setdefault(name, []).extend(uris)
    return base
