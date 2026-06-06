# MCP stdio integrator

Runs `nlp2uri-mcp` — JSON-RPC over stdin/stdout with tools:

- `nlp2uri_plan`
- `nlp2uri_resolve`
- `nlp2uri_compile`
- `nlp2uri_execute`
- `nlp2uri_handle`

## Cursor / Windsurf config snippet

```json
{
  "mcpServers": {
    "nlp2uri": {
      "command": "nlp2uri-mcp"
    }
  }
}
```

## Run smoke

```bash
./e2e.sh
```
