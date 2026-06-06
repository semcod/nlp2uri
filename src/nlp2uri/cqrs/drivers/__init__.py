"""Reference drivers — implement generated stubs from schemas/codegen."""

from nlp2uri.cqrs.drivers.artifact_filesystem import ArtifactFilesystemDriver
from nlp2uri.cqrs.drivers.command_curl import CommandCurlDriver
from nlp2uri.cqrs.drivers.delegate import DelegateCompileDriver
from nlp2uri.cqrs.drivers.endpoint_curl import EndpointCurlDriver
from nlp2uri.cqrs.drivers.getv_cli import GetvCliDriver
from nlp2uri.cqrs.drivers.resource_probe import ResourceProbeDriver
from nlp2uri.cqrs.drivers.runtime_curl import RuntimeCurlDriver
from nlp2uri.cqrs.drivers.service_ops import (
    ServiceCurlDriver,
    ServiceDockerDriver,
    ServiceSystemdDriver,
)
from nlp2uri.cqrs.drivers.container_docker import ContainerDockerDriver

__all__ = [
    "ArtifactFilesystemDriver",
    "CommandCurlDriver",
    "DelegateCompileDriver",
    "EndpointCurlDriver",
    "GetvCliDriver",
    "ResourceProbeDriver",
    "RuntimeCurlDriver",
    "ServiceCurlDriver",
    "ServiceDockerDriver",
    "ServiceSystemdDriver",
    "ContainerDockerDriver",
]
