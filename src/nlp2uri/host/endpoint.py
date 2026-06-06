"""endpoint:// URI — TCP/HTTP health probes."""

from __future__ import annotations

from urllib.parse import unquote, urlparse

from nlp2uri.models import HostPlatform, OSAction

ENDPOINT_SCHEME = "endpoint"


def is_endpoint_uri(uri: str) -> bool:
    return urlparse(uri).scheme.lower() == ENDPOINT_SCHEME


def build_endpoint_url(uri: str) -> str:
    """endpoint://tcp/127.0.0.1/8010/health → http://127.0.0.1:8010/health"""
    parsed = urlparse(uri)
    proto = unquote(parsed.netloc or "tcp").lower()
    parts = [unquote(p) for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        raise ValueError(f"endpoint uri needs host and port: {uri}")
    host, port = parts[0], parts[1]
    path = "/" + "/".join(parts[2:]) if len(parts) > 2 else "/"
    if proto in {"tcp", "http"}:
        return f"http://{host}:{port}{path}"
    if proto == "https":
        return f"https://{host}:{port}{path}"
    raise ValueError(f"unsupported endpoint proto: {proto}")


def build_endpoint_actions(uri: str, host: HostPlatform) -> list[OSAction]:
    url = build_endpoint_url(uri)
    return [OSAction(host, "curl", ["-sf", url])]
