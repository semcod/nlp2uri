"""Shell adapter — bash-friendly exports and eval snippets."""

from __future__ import annotations

import shlex

from nlp2uri.adapters.base import AdapterRequest, AdapterResponse, BaseAdapter


class ShellAdapter(BaseAdapter):
    name = "shell"

    def handle(self, request: AdapterRequest) -> AdapterResponse:
        svc = self._service_for(request)
        op = request.operation

        try:
            if op == "export":
                plan = svc.from_prompt(request.prompt, locale=request.locale)
                argv = plan.actions[0].argv() if plan.actions else []
                script = self._export_script(
                    uri=plan.uri,
                    argv=argv,
                    intent=plan.intent,
                )
                return AdapterResponse(ok=True, data={"script": script, "uri": plan.uri})

            if op == "eval-uri":
                actions = svc.compile(request.uri)
                argv = actions[0].argv() if actions else []
                script = self._export_script(uri=request.uri, argv=argv, intent="uri")
                return AdapterResponse(ok=True, data={"script": script, "uri": request.uri})

            if op == "run":
                plan = svc.from_prompt(request.prompt, locale=request.locale)
                result = svc.execute(plan.uri, dry_run=request.dry_run)
                argv = result.actions[0].argv() if result.actions else []
                script = self._export_script(uri=plan.uri, argv=argv, intent=plan.intent)
                script += f"\n# exit={result.returncode}\n"
                if result.output:
                    script += f"# output={shlex.quote(result.output)}\n"
                return AdapterResponse(
                    ok=result.ok,
                    data={
                        "script": script,
                        "uri": plan.uri,
                        "result": result.to_dict(),
                    },
                    status_code=0 if result.ok else result.returncode or 1,
                )

            return AdapterResponse(ok=False, error=f"unknown shell operation: {op}", status_code=2)
        except ValueError as exc:
            return AdapterResponse(ok=False, error=str(exc), status_code=2)

    @staticmethod
    def _export_script(*, uri: str, argv: list[str], intent: str) -> str:
        cmd = shlex.join(argv)
        return "\n".join(
            [
                f"export NLP2URI_INTENT={shlex.quote(intent)}",
                f"export NLP2URI_URI={shlex.quote(uri)}",
                f"export NLP2URI_CMD={shlex.quote(cmd)}",
                f"alias nlp2uri-run={shlex.quote(cmd)}",
            ]
        )
