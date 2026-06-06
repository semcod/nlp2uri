"""Base executor interface."""

from __future__ import annotations

import re
import shutil
import subprocess
import webbrowser
from abc import ABC, abstractmethod
from urllib.parse import parse_qs, unquote, urlparse

from nlp2uri.models import ActionResult, HostPlatform


class UriExecutor(ABC):
    platform: HostPlatform

    @abstractmethod
    def execute(self, uri: str, *, dry_run: bool = False) -> ActionResult:
        raise NotImplementedError

    def _result(
        self,
        *,
        ok: bool,
        uri: str,
        output: str = "",
        error: str = "",
        returncode: int = 0,
    ) -> ActionResult:
        return ActionResult(
            ok=ok,
            uri=uri,
            output=output,
            error=error,
            returncode=returncode,
            platform=self.platform,
        )

    def _dry(self, uri: str, command: list[str]) -> ActionResult:
        return self._result(
            ok=True,
            uri=uri,
            output=" ".join(command),
            returncode=0,
        )

    def _run(self, uri: str, command: list[str], *, timeout: float = 30.0) -> ActionResult:
        try:
            proc = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except FileNotFoundError:
            return self._result(
                ok=False,
                uri=uri,
                error=f"command not found: {command[0]}",
                returncode=127,
            )
        except subprocess.TimeoutExpired:
            return self._result(
                ok=False,
                uri=uri,
                error="command timed out",
                returncode=124,
            )

        output = (proc.stdout or proc.stderr or "").strip()
        return self._result(
            ok=proc.returncode == 0,
            uri=uri,
            output=output,
            error="" if proc.returncode == 0 else output,
            returncode=proc.returncode,
        )

    def _first_available(self, names: tuple[str, ...]) -> str | None:
        for name in names:
            if shutil.which(name):
                return name
        return None

    def _open_with_browser(self, uri: str, *, dry_run: bool) -> ActionResult:
        if dry_run:
            return self._dry(uri, ["webbrowser.open", uri])
        opened = webbrowser.open(uri, new=2)
        return self._result(ok=bool(opened), uri=uri, output="webbrowser.open")

    def _parse_nlp2uri(self, uri: str) -> tuple[str, dict[str, str]]:
        parsed = urlparse(uri)
        if parsed.scheme != "nlp2uri":
            raise ValueError(f"not an nlp2uri scheme: {uri}")
        segments = [parsed.netloc, parsed.path.lstrip("/")]
        path = "/".join(part for part in segments if part)
        raw = parse_qs(parsed.query, keep_blank_values=False)
        params = {k: unquote(v[0]) for k, v in raw.items() if v}
        return path, params

    def _desktop_id_for_app(self, name: str) -> str | None:
        lowered = name.lower().removesuffix(".desktop")
        candidates = (
            f"{lowered}.desktop",
            f"org.{lowered}.desktop",
            f"{lowered}-desktop.desktop",
        )
        for desktop_dir in (
            "/usr/share/applications",
            "/var/lib/snapd/desktop/applications",
            "/usr/local/share/applications",
        ):
            from pathlib import Path

            base = Path(desktop_dir)
            if not base.is_dir():
                continue
            for candidate in candidates:
                if (base / candidate).is_file():
                    return candidate
            for entry in base.glob("*.desktop"):
                if lowered in entry.name.lower():
                    return entry.name
        return None


def slugify_app_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
