"""MCP adapter — tool definitions and handlers."""

from __future__ import annotations

import json
from typing import Any, Callable

from nlp2uri.adapters.base import AdapterRequest, AdapterResponse, BaseAdapter
from nlp2uri.models import HostPlatform
from nlp2uri.systemmap.context import load_ir_from_arguments

MCP_TOOLS: list[dict[str, Any]] = [
    {
        "name": "nlp2uri_plan",
        "description": "Convert natural language prompt to abstract URI and OS action plan.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "Natural language desktop intent"},
                "platform": {
                    "type": "string",
                    "enum": ["linux", "darwin", "windows"],
                    "description": "Target OS (default: auto-detect)",
                },
                "locale": {"type": "string", "description": "Optional locale hint (e.g. pl-PL)"},
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "nlp2uri_resolve",
        "description": "Resolve prompt to abstract URI only.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
                "platform": {"type": "string", "enum": ["linux", "darwin", "windows"]},
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "nlp2uri_compile",
        "description": "Compile abstract URI to concrete OS commands.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "uri": {"type": "string"},
                "platform": {"type": "string", "enum": ["linux", "darwin", "windows"]},
            },
            "required": ["uri"],
        },
    },
    {
        "name": "nlp2uri_execute",
        "description": "Execute a URI on the host (use dry_run in CI).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "uri": {"type": "string"},
                "platform": {"type": "string", "enum": ["linux", "darwin", "windows"]},
                "dry_run": {"type": "boolean", "default": False},
            },
            "required": ["uri"],
        },
    },
    {
        "name": "nlp2uri_handle",
        "description": "Full pipeline: prompt → URI → execute.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
                "platform": {"type": "string", "enum": ["linux", "darwin", "windows"]},
                "dry_run": {"type": "boolean", "default": True},
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "nlp2uri_list_system_uris",
        "description": (
            "List canonical URIs for all entities in an env2llm SystemMapIR "
            "(requires system_map, doql_path, or example_dir)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "system_map": {
                    "type": "object",
                    "description": "Inline SystemMapIR dict (env2llm.system_map.v1).",
                },
                "doql_path": {
                    "type": "string",
                    "description": "Path to environment.doql.less.",
                },
                "example_dir": {
                    "type": "string",
                    "description": "nlp2dsl example directory for env2llm introspection.",
                },
                "example_id": {"type": "string"},
            },
        },
    },
    {
        "name": "nlp2uri_resolve_system_map",
        "description": (
            "Resolve NL prompt against SystemMapIR URIs; falls back to desktop NL when no match."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
                "system_map": {"type": "object"},
                "doql_path": {"type": "string"},
                "example_dir": {"type": "string"},
                "example_id": {"type": "string"},
                "fallback_desktop": {"type": "boolean", "default": True},
                "platform": {"type": "string", "enum": ["linux", "darwin", "windows"]},
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "nlp2uri_list_getv_uris",
        "description": "List getv:// URIs for all ~/.getv profile variables (requires getv profiles on disk).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "getv_home": {
                    "type": "string",
                    "description": "Override GETV_HOME (default ~/.getv).",
                },
            },
        },
    },
    {
        "name": "nlp2uri_resolve_getv",
        "description": "Resolve NL prompt to getv:// env var or profile URI (e.g. GROQ_API_KEY).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
                "getv_home": {"type": "string"},
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "nlp2uri_get_getv_var",
        "description": "Read getv://category/profile/VAR — returns masked value metadata.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "uri": {
                    "type": "string",
                    "description": "getv://llm/groq/GROQ_API_KEY",
                },
            },
            "required": ["uri"],
        },
    },
]


class McpAdapter(BaseAdapter):
    name = "mcp"

    def handle(self, request: AdapterRequest) -> AdapterResponse:
        return self.call_tool(request.operation, self._args_from_request(request))

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> AdapterResponse:
        handler = self.tool_dispatch().get(tool_name)
        if handler is None:
            return AdapterResponse(ok=False, error=f"unknown tool: {tool_name}", status_code=404)
        req = self._args_to_request(tool_name, arguments)
        return handler(self, req)

    def tool_dispatch(self) -> dict[str, Callable[["McpAdapter", AdapterRequest], AdapterResponse]]:
        return {
            "nlp2uri_plan": McpAdapter._tool_plan,
            "nlp2uri_resolve": McpAdapter._tool_resolve,
            "nlp2uri_compile": McpAdapter._tool_compile,
            "nlp2uri_execute": McpAdapter._tool_execute,
            "nlp2uri_handle": McpAdapter._tool_handle,
            "nlp2uri_list_system_uris": McpAdapter._tool_list_system_uris,
            "nlp2uri_resolve_system_map": McpAdapter._tool_resolve_system_map,
            "nlp2uri_list_getv_uris": McpAdapter._tool_list_getv_uris,
            "nlp2uri_resolve_getv": McpAdapter._tool_resolve_getv,
            "nlp2uri_get_getv_var": McpAdapter._tool_get_getv_var,
        }

    @staticmethod
    def _args_from_request(request: AdapterRequest) -> dict[str, Any]:
        args = dict(request.extra)
        if request.prompt:
            args["prompt"] = request.prompt
        if request.uri:
            args["uri"] = request.uri
        if request.platform is not None:
            args["platform"] = request.platform.value
        if request.dry_run:
            args["dry_run"] = True
        if request.locale:
            args["locale"] = request.locale
        return args

    @staticmethod
    def _args_to_request(tool_name: str, arguments: dict[str, Any]) -> AdapterRequest:
        platform = arguments.get("platform")
        host = HostPlatform(platform) if platform else None
        return AdapterRequest(
            operation=tool_name,
            prompt=str(arguments.get("prompt") or ""),
            uri=str(arguments.get("uri") or ""),
            platform=host,
            dry_run=bool(arguments.get("dry_run", tool_name == "nlp2uri_handle")),
            locale=arguments.get("locale"),
            extra=arguments,
        )

    @staticmethod
    def mcp_content(payload: dict[str, Any], *, uri: str | None = None) -> list[dict[str, Any]]:
        content: list[dict[str, Any]] = [
            {"type": "text", "text": json.dumps(payload, ensure_ascii=False, indent=2)},
        ]
        resolved = uri or payload.get("uri")
        if resolved:
            content.append(
                {
                    "type": "resource",
                    "mimeType": "text/uri-list",
                    "text": f"{resolved}\r\n",
                }
            )
        return content

    def _tool_plan(self, req: AdapterRequest) -> AdapterResponse:
        svc = self._service_for(req)
        result = svc.from_prompt(req.prompt, locale=req.locale)
        data = result.to_dict()
        data["mcp_content"] = self.mcp_content(data, uri=result.uri)
        return AdapterResponse(ok=True, data=data)

    def _tool_resolve(self, req: AdapterRequest) -> AdapterResponse:
        svc = self._service_for(req)
        spec = svc.resolve(req.prompt)
        data = spec.to_dict()
        data["mcp_content"] = self.mcp_content(data, uri=spec.uri)
        return AdapterResponse(ok=True, data=data)

    def _tool_compile(self, req: AdapterRequest) -> AdapterResponse:
        svc = self._service_for(req)
        actions = svc.compile(req.uri)
        data = {"uri": req.uri, "actions": [a.to_dict() for a in actions]}
        data["mcp_content"] = self.mcp_content(data, uri=req.uri)
        return AdapterResponse(ok=True, data=data)

    def _tool_execute(self, req: AdapterRequest) -> AdapterResponse:
        svc = self._service_for(req)
        payload = svc.handle_uri(req.uri, dry_run=req.dry_run)
        ok = bool(payload.get("result", {}).get("ok", False))
        payload["mcp_content"] = self.mcp_content(payload, uri=req.uri)
        return AdapterResponse(ok=ok, data=payload, status_code=0 if ok else 1)

    def _tool_handle(self, req: AdapterRequest) -> AdapterResponse:
        svc = self._service_for(req)
        payload = svc.handle_prompt(req.prompt, dry_run=req.dry_run)
        ok = bool(payload.get("result", {}).get("ok", False))
        uri = payload.get("plan", {}).get("uri")
        payload["mcp_content"] = self.mcp_content(payload, uri=uri)
        return AdapterResponse(ok=ok, data=payload, status_code=0 if ok else 1)

    def _tool_list_system_uris(self, req: AdapterRequest) -> AdapterResponse:
        try:
            ir = load_ir_from_arguments(req.extra)
        except (ValueError, RuntimeError) as exc:
            return AdapterResponse(ok=False, error=str(exc), status_code=400)
        svc = self._service_for(req)
        payload = svc.list_system_uris(ir)
        payload["mcp_content"] = self.mcp_content(payload)
        return AdapterResponse(ok=True, data=payload)

    def _tool_resolve_system_map(self, req: AdapterRequest) -> AdapterResponse:
        try:
            ir = load_ir_from_arguments(req.extra)
        except (ValueError, RuntimeError) as exc:
            return AdapterResponse(ok=False, error=str(exc), status_code=400)
        svc = self._service_for(req)
        payload = svc.resolve_system_map(
            req.prompt,
            ir,
            fallback_desktop=bool(req.extra.get("fallback_desktop", True)),
        )
        uri = payload.get("uri")
        payload["mcp_content"] = self.mcp_content(payload, uri=uri)
        return AdapterResponse(ok=uri is not None, data=payload, status_code=0 if uri else 1)

    def _tool_list_getv_uris(self, req: AdapterRequest) -> AdapterResponse:
        svc = self._service_for(req)
        payload = svc.list_getv_uris(getv_home=req.extra.get("getv_home"))
        payload["mcp_content"] = self.mcp_content(payload)
        return AdapterResponse(ok=True, data=payload)

    def _tool_resolve_getv(self, req: AdapterRequest) -> AdapterResponse:
        svc = self._service_for(req)
        payload = svc.resolve_getv(req.prompt, getv_home=req.extra.get("getv_home"))
        uri = payload.get("uri")
        payload["mcp_content"] = self.mcp_content(payload, uri=uri)
        return AdapterResponse(ok=uri is not None, data=payload, status_code=0 if uri else 1)

    def _tool_get_getv_var(self, req: AdapterRequest) -> AdapterResponse:
        svc = self._service_for(req)
        try:
            payload = svc.read_getv_var(req.uri)
        except ValueError as exc:
            return AdapterResponse(ok=False, error=str(exc), status_code=400)
        payload["mcp_content"] = self.mcp_content(payload, uri=req.uri)
        return AdapterResponse(ok=bool(payload.get("found")), data=payload)
