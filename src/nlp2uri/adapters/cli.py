"""CLI adapter — structured payloads for `nlp2uri` command."""

from __future__ import annotations

from nlp2uri.adapters.base import AdapterRequest, AdapterResponse, BaseAdapter


class CliAdapter(BaseAdapter):
    name = "cli"

    def handle(self, request: AdapterRequest) -> AdapterResponse:
        svc = self._service_for(request)
        op = request.operation

        payload_text = (request.extra.get("text") or "").strip() or None

        try:
            if op == "plan":
                result = svc.from_prompt(
                    request.prompt,
                    locale=request.locale,
                    text=payload_text,
                )
                return AdapterResponse(ok=True, data=result.to_dict())
            if op == "resolve":
                spec = svc.resolve(request.prompt, text=payload_text)
                return AdapterResponse(ok=True, data=spec.to_dict())
            if op == "compile":
                actions = svc.compile(request.uri, text=payload_text)
                return AdapterResponse(
                    ok=True,
                    data={"uri": request.uri, "actions": [a.to_dict() for a in actions]},
                )
            if op == "execute":
                if request.uri:
                    payload = svc.handle_uri(
                        request.uri,
                        dry_run=request.dry_run,
                        text=payload_text,
                    )
                else:
                    payload = svc.handle_prompt(
                        request.prompt,
                        dry_run=request.dry_run,
                        text=payload_text,
                    )
                ok = bool(payload.get("result", {}).get("ok", False))
                return AdapterResponse(ok=ok, data=payload, status_code=0 if ok else 1)
            return AdapterResponse(ok=False, error=f"unknown cli operation: {op}", status_code=2)
        except ValueError as exc:
            return AdapterResponse(ok=False, error=str(exc), status_code=2)
        except Exception as exc:  # pragma: no cover — defensive
            return AdapterResponse(ok=False, error=str(exc), status_code=1)
