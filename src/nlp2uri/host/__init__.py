"""Host-level URI schemes (endpoint, device, …)."""

from nlp2uri.host.artifact import build_artifact_actions, is_artifact_uri, resolve_artifact_path
from nlp2uri.host.endpoint import build_endpoint_actions, is_endpoint_uri
from nlp2uri.host.resource import build_resource_actions, is_resource_uri

__all__ = [
    "build_artifact_actions",
    "build_endpoint_actions",
    "build_resource_actions",
    "is_artifact_uri",
    "is_endpoint_uri",
    "is_resource_uri",
    "resolve_artifact_path",
]
