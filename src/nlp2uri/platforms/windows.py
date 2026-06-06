"""Windows URI executor."""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlparse

from nlp2uri.models import HostPlatform
from nlp2uri.platforms.base import UriExecutor


class WindowsExecutor(UriExecutor):
    platform = HostPlatform.WINDOWS

    def execute(self, uri: str, *, dry_run: bool = False) -> ActionResult:
        parsed = urlparse(uri)
        scheme = parsed.scheme

        if scheme in {"http", "https", "file", "cursor", "vscode", "vscode-insiders", "ms-settings"}:
            return self._start(uri, dry_run=dry_run)

        if scheme == "nlp2uri":
            path, params = self._parse_nlp2uri(uri)
            if path in {"settings/linux", "settings/generic"}:
                return self._start("ms-settings:", dry_run=dry_run)
            if path == "app/open":
                return self._open_app(params.get("name", ""), uri=uri, dry_run=dry_run)
            if path == "app/focus":
                return self._focus_app(params.get("name", ""), uri=uri, dry_run=dry_run)
            if path.startswith("capture/"):
                return self._capture(path.split("/", 1)[1], params, uri=uri, dry_run=dry_run)

        return self._result(ok=False, uri=uri, error=f"unsupported uri on windows: {uri}", returncode=2)

    def _start(self, uri: str, *, dry_run: bool) -> ActionResult:
        command = ["cmd", "/c", "start", "", uri]
        if dry_run:
            return self._dry(uri, command)
        return self._run(uri, command)

    def _open_app(self, name: str, *, uri: str, dry_run: bool) -> ActionResult:
        if not name:
            return self._result(ok=False, uri=uri, error="missing app name", returncode=2)
        command = ["cmd", "/c", "start", "", name]
        if dry_run:
            return self._dry(uri, command)
        return self._run(uri, command)

    def _focus_app(self, name: str, *, uri: str, dry_run: bool) -> ActionResult:
        if not name:
            return self._result(ok=False, uri=uri, error="missing app name", returncode=2)
        ps = (
            f"(Get-Process -Name '{name}' -ErrorAction SilentlyContinue | "
            f"Select-Object -First 1).MainWindowHandle"
        )
        command = ["powershell", "-NoProfile", "-Command", ps]
        if dry_run:
            return self._dry(uri, command)
        return self._run(uri, command)

    def _capture(
        self,
        target: str,
        params: dict[str, str],
        *,
        uri: str,
        dry_run: bool,
    ) -> ActionResult:
        out_dir = Path(os.environ.get("NLP2URI_CAPTURE_DIR", os.path.expandvars(r"%TEMP%\nlp2uri-captures")))
        out_dir.mkdir(parents=True, exist_ok=True)
        outfile = out_dir / f"capture-{target}.png"

        if target == "screen":
            ps = (
                "Add-Type -AssemblyName System.Windows.Forms; "
                "[System.Windows.Forms.Screen]::PrimaryScreen.Bounds"
            )
            command = ["powershell", "-NoProfile", "-Command", ps]
        else:
            title = params.get("title", "")
            command = ["snippingtool", "/clip"] if not title else [
                "powershell",
                "-NoProfile",
                "-Command",
                f"Write-Output 'window:{title}' | Out-File -FilePath '{outfile}'",
            ]

        if dry_run:
            return self._dry(uri, command)
        result = self._run(uri, command)
        if outfile.exists():
            return self._result(ok=True, uri=uri, output=str(outfile), returncode=0)
        return result
