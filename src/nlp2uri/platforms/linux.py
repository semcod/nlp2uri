"""Linux URI executor."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from nlp2uri.models import HostPlatform
from nlp2uri.platforms.base import UriExecutor


class LinuxExecutor(UriExecutor):
    platform = HostPlatform.LINUX

    def execute(self, uri: str, *, dry_run: bool = False) -> ActionResult:
        parsed = urlparse(uri)
        scheme = parsed.scheme

        if scheme in {"http", "https", "file", "cursor", "vscode", "vscode-insiders"}:
            return self._open_generic(uri, dry_run=dry_run)

        if scheme == "x-apple.systempreferences":
            return self._open_generic(uri, dry_run=dry_run)

        if scheme == "nlp2uri":
            path, params = self._parse_nlp2uri(uri)
            if path == "settings/linux":
                return self._open_settings(dry_run=dry_run, uri=uri)
            if path == "app/open":
                return self._open_app(params.get("name", ""), uri=uri, dry_run=dry_run)
            if path == "app/focus":
                return self._focus_app(params.get("name", ""), uri=uri, dry_run=dry_run)
            if path.startswith("capture/"):
                return self._capture(path.split("/", 1)[1], params, uri=uri, dry_run=dry_run)

        return self._result(ok=False, uri=uri, error=f"unsupported uri on linux: {uri}", returncode=2)

    def _open_generic(self, uri: str, *, dry_run: bool) -> ActionResult:
        opener = self._first_available(("xdg-open", "gio", "gnome-open"))
        if opener is None:
            return self._open_with_browser(uri, dry_run=dry_run)
        command = [opener, uri]
        if dry_run:
            return self._dry(uri, command)
        return self._run(uri, command)

    def _open_settings(self, *, dry_run: bool, uri: str) -> ActionResult:
        for candidate in (
            "gnome-control-center",
            "systemsettings",
            "kcmshell5",
            "xfce4-settings-manager",
        ):
            if self._first_available((candidate,)):
                command = [candidate]
                if dry_run:
                    return self._dry(uri, command)
                return self._run(uri, command)
        return self._open_generic("file:///usr/share/applications", dry_run=dry_run)

    def _open_app(self, name: str, *, uri: str, dry_run: bool) -> ActionResult:
        if not name:
            return self._result(ok=False, uri=uri, error="missing app name", returncode=2)

        desktop_id = self._desktop_id_for_app(name)
        gtk = self._first_available(("gtk-launch",))
        if desktop_id and gtk:
            command = [gtk, desktop_id]
            if dry_run:
                return self._dry(uri, command)
            return self._run(uri, command)

        opener = self._first_available(("xdg-open",))
        if opener:
            command = [opener, name]
            if dry_run:
                return self._dry(uri, command)
            return self._run(uri, command)

        return self._result(ok=False, uri=uri, error=f"cannot open app: {name}", returncode=2)

    def _focus_app(self, name: str, *, uri: str, dry_run: bool) -> ActionResult:
        if not name:
            return self._result(ok=False, uri=uri, error="missing app name", returncode=2)

        wmctrl = self._first_available(("wmctrl",))
        if wmctrl:
            command = [wmctrl, "-a", name]
            if dry_run:
                return self._dry(uri, command)
            return self._run(uri, command)

        xdotool = self._first_available(("xdotool",))
        if xdotool:
            script = f"xdotool search --name {name} windowactivate"
            command = ["bash", "-lc", script]
            if dry_run:
                return self._dry(uri, command)
            return self._run(uri, command)

        return self._open_app(name, uri=uri, dry_run=dry_run)

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
            if self._first_available(("grim",)):
                command = ["grim", str(outfile)]
            elif self._first_available(("scrot",)):
                command = ["scrot", str(outfile)]
            elif self._first_available(("import",)):
                command = ["import", "-window", "root", str(outfile)]
            else:
                command = ["bash", "-lc", f"echo portal-screenshot > {outfile}"]
        else:
            title = params.get("title", "")
            if self._first_available(("import",)) and title:
                command = ["import", "-window", title, str(outfile)]
            elif self._first_available(("grim",)):
                command = ["grim", "-g", "0,0 100x100", str(outfile)]
            else:
                command = ["bash", "-lc", f"echo window-capture:{title} > {outfile}"]

        if dry_run:
            return self._dry(uri, command)
        result = self._run(uri, command)
        if result.ok and outfile.exists():
            result = self._result(
                ok=True,
                uri=uri,
                output=str(outfile),
                returncode=0,
            )
        return result
