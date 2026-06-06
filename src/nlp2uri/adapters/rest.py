"""REST adapter — HTTP-friendly request/response mapping."""

from __future__ import annotations

from typing import Any

from nlp2uri.adapters.base import AdapterRequest, AdapterResponse, BaseAdapter
from nlp2uri.models import HostPlatform


class RestAdapter(BaseAdapter):
    name = "rest"

    ROUTES: dict[str, str] = {
        "GET /health": "health",
        "POST /v1/plan": "plan",
        "POST /v1/resolve": "resolve",
        "POST /v1/compile": "compile",
        "POST /v1/execute": "execute",
        "POST /v1/handle": "handle",
    }

    def handle(self, request: AdapterRequest) -> AdapterResponse:
        return self.dispatch(request.operation, request)

    def dispatch(self, route: str, body: AdapterRequest | dict[str, Any]) -> AdapterResponse:
        if isinstance(body, dict):
            body = self.body_to_request(body, operation=route)
        svc = self._service_for(body)

        try:
            if route == "health":
                return AdapterResponse(ok=True, data={"status": "ok", "service": "nlp2uri"})

            if route == "plan":
                result = svc.from_prompt(body.prompt, locale=body.locale)
                return AdapterResponse(ok=True, data=result.to_dict())

            if route == "resolve":
                spec = svc.resolve(body.prompt)
                return AdapterResponse(ok=True, data=spec.to_dict())

            if route == "compile":
                actions = svc.compile(body.uri)
                return AdapterResponse(
                    ok=True,
                    data={"uri": body.uri, "actions": [a.to_dict() for a in actions]},
                )

            if route == "execute":
                payload = svc.handle_uri(body.uri, dry_run=body.dry_run)
                ok = bool(payload.get("result", {}).get("ok", False))
                return AdapterResponse(ok=ok, data=payload, status_code=200 if ok else 500)

            if route == "handle":
                if body.uri:
                    payload = svc.handle_uri(body.uri, dry_run=body.dry_run)
                else:
                    payload = svc.handle_prompt(body.prompt, dry_run=body.dry_run)
                ok = bool(payload.get("result", {}).get("ok", False))
                return AdapterResponse(ok=ok, data=payload, status_code=200 if ok else 500)

            return AdapterResponse(ok=False, error=f"unknown route: {route}", status_code=404)
        except ValueError as exc:
            return AdapterResponse(ok=False, error=str(exc), status_code=400)
        except Exception as exc:  # pragma: no cover
            return AdapterResponse(ok=False, error=str(exc), status_code=500)

    @staticmethod
    def body_to_request(body: dict[str, Any], *, operation: str) -> AdapterRequest:
        platform = body.get("platform")
        host = HostPlatform(platform) if platform else None  # None → nlp2uri.yaml / auto-detect
        return AdapterRequest(
            operation=operation,
            prompt=str(body.get("prompt") or ""),
            uri=str(body.get("uri") or ""),
            platform=host,
            dry_run=bool(body.get("dry_run", False)),
            locale=body.get("locale"),
        )

    @staticmethod
    def match_route(method: str, path: str) -> str | None:
        key = f"{method.upper()} {path.rstrip('/') or '/'}"
        if key == "GET /":
            return "health"
        return RestAdapter.ROUTES.get(key)
