# MCP stdio integrator

Runs `nlp2uri-mcp` — JSON-RPC over stdin/stdout with tools:

- `nlp2uri_plan`
- `nlp2uri_resolve`
- `nlp2uri_compile`
- `nlp2uri_execute`
- `nlp2uri_handle`

## Cursor / Windsurf config

- Szablon: [`mcp-config.cursor.json`](mcp-config.cursor.json)
- Dokumentacja narzędzi: [`docs/mcp-tools.md`](../../../docs/mcp-tools.md)

Minimalny snippet:

```json
{
  "mcpServers": {
    "nlp2uri": {
      "command": "nlp2uri-mcp",
      "env": { "NLP2URI_CONFIG": "${workspaceFolder}/nlp2uri.yaml" }
    }
  }
}
```

## Run smoke

```bash
./e2e.sh
```
