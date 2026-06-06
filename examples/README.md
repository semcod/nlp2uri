# nlp2uri examples

Each sample lives under **`examples/<category>/<name>/`**.

## Index

| Path | Purpose |
|------|---------|
| `examples/resolve/nl-to-uri` | NL → abstract URI + `OSAction` plan |
| `examples/execute/dry-run` | Dry-run host commands |
| `examples/mcp/tool-handoff` | MCP payload shapes |
| `examples/integrators/rest-api` | HTTP REST server (`nlp2uri-serve`) |
| `examples/integrators/mcp-stdio` | MCP stdio server (`nlp2uri-mcp`) |
| `examples/integrators/shell-export` | Bash `eval "$(nlp2uri shell export …)"` |

## Run all

```bash
./examples/run-e2e.sh
```

## Reuse surfaces

| Surface | Entry | Package module |
|---------|-------|----------------|
| Library | `NLP2URIService` | `nlp2uri.service` |
| CLI | `nlp2uri` | `nlp2uri.adapters.cli` |
| Shell | `nlp2uri shell export` | `nlp2uri.adapters.shell` |
| REST | `nlp2uri-serve` | `nlp2uri.integrators.rest_server` |
| MCP | `nlp2uri-mcp` | `nlp2uri.integrators.mcp_server` |
