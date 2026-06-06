"""macOS URI executor."""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlparse

from nlp2uri.models import HostPlatform
from nlp2uri.platforms.base import UriExecutor


class MacOSExecutor(UriExecutor):
    platform = HostPlatform.MACOS

    def execute(self, uri: str, *, dry_run: bool = False) -> ActionResult:
        parsed = urlparse(uri)
        scheme = parsed.scheme

        if scheme in {
            "http",
            "https",
            "file",
            "cursor",
            "vscode",
            "vscode-insiders",
            "x-apple.systempreferences",
        }:
            return self._open(uri, dry_run=dry_run)

        if scheme == "nlp2uri":
            path, params = self._parse_nlp2uri(uri)
            if path == "settings/linux":
                return self._open("x-apple.systempreferences:", dry_run=dry_run)
            if path == "app/open":
                return self._open_app(params.get("name", ""), uri=uri, dry_run=dry_run)
            if path == "app/focus":
                return self._focus_app(params.get("name", ""), uri=uri, dry_run=dry_run)
            if path.startswith("capture/"):
                return self._capture(path.split("/", 1)[1], params, uri=uri, dry_run=dry_run)

        return self._result(ok=False, uri=uri, error=f"unsupported uri on macos: {uri}", returncode=2)

    def _open(self, uri: str, *, dry_run: bool) -> ActionResult:
        command = ["open", uri]
        if dry_run:
            return self._dry(uri, command)
        return self._run(uri, command)

    def _open_app(self, name: str, *, uri: str, dry_run: bool) -> ActionResult:
        if not name:
            return self._result(ok=False, uri=uri, error="missing app name", returncode=2)
        command = ["open", "-a", name]
        if dry_run:
            return self._dry(uri, command)
        return self._run(uri, command)

    def _focus_app(self, name: str, *, uri: str, dry_run: bool) -> ActionResult:
        if not name:
            return self._result(ok=False, uri=uri, error="missing app name", returncode=2)
        script = f'tell application "{name}" to activate'
        command = ["osascript", "-e", script]
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
        out_dir = Path(os.environ.get("NLP2URI_CAPTURE_DIR", "/tmp/nlp2uri-captures"))
        out_dir.mkdir(parents=True, exist_ok=True)
        outfile = out_dir / f"capture-{target}.png"

        if target == "screen":
            command = ["screencapture", "-x", str(outfile)]
        else:
            title = params.get("title", "")
            command = ["screencapture", "-l", title, str(outfile)] if title else [
                "screencapture",
                "-w",
                str(outfile),
            ]

        if dry_run:
            return self._dry(uri, command)
        result = self._run(uri, command)
        if result.ok:
            return self._result(ok=True, uri=uri, output=str(outfile), returncode=0)
        return result
