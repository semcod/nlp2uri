# MCP tools — nlp2uri

Server: `nlp2uri-mcp` (stdio JSON-RPC, MCP 2024-11-05).

## Konfiguracja Cursor

Skopiuj do `.cursor/mcp.json` lub merge z szablonem:

[`examples/integrators/mcp-stdio/mcp-config.json`](../examples/integrators/mcp-stdio/mcp-config.json)

```json
{
  "mcpServers": {
    "nlp2uri": {
      "command": "nlp2uri-mcp",
      "env": {
        "NLP2URI_CONFIG": "/absolute/path/to/nlp2uri.yaml"
      }
    }
  }
}
```

Wymagania: `pip install -e .` w venv, z którego Cursor uruchamia `nlp2uri-mcp`.

Platforma: z `nlp2uri.yaml` (`platform: auto`) lub `NLP2URI_PLATFORM=linux|darwin|windows`.

---

## Narzędzia

### `nlp2uri_plan`

Pełny plan: NL → URI + `OSAction[]`.

**Input:**

```json
{
  "prompt": "otwórz vscode w folderze ~/projekty/foo",
  "platform": "linux",
  "locale": "pl-PL"
}
```

**Output (skrót):**

```json
{
  "uri": "app://vscode/open?path=/home/tom/projekty/foo",
  "intent": "open_app",
  "actions": [{ "os": "linux", "command": "xdg-open", "argv": ["..."] }]
}
```

Zwraca też `mcp_content` z `text/uri-list` dla hosta MCP.

---

### `nlp2uri_resolve`

Tylko URI + spec (bez wykonania).

```json
{ "prompt": "capture screen", "platform": "linux" }
```

→ `desktop-screenshot://screen`

---

### `nlp2uri_compile`

URI → komendy OS.

```json
{ "uri": "app://firefox/open", "platform": "linux" }
```

---

### `nlp2uri_execute`

Wykonaj URI (w CI używaj `dry_run: true`).

```json
{
  "uri": "desktop-screenshot://screen",
  "platform": "linux",
  "dry_run": true
}
```

---

### `nlp2uri_handle`

Pipeline: prompt → URI → execute.

```json
{
  "prompt": "open firefox",
  "platform": "linux",
  "dry_run": true
}
```

Domyślnie `dry_run: true` dla bezpieczeństwa agenta.

---

## Przepływ z innym MCP (desktop automation)

1. Agent woła `nlp2uri_plan` → dostaje `desktop-screenshot://window?title=Edge&mode=active`
2. Host przekazuje URI do `mcp-desktop-pro` lub lokalnego executora
3. Alternatywnie `nlp2uri_execute` z `dry_run: false` na zaufanym hoście

## Smoke test

```bash
./examples/integrators/mcp-stdio/e2e.sh
```

## REST equivalent

Te same operacje przez HTTP (`nlp2uri-serve`):

| MCP tool | REST |
|----------|------|
| `nlp2uri_plan` | `POST /v1/plan` |
| `nlp2uri_resolve` | `POST /v1/resolve` |
| `nlp2uri_compile` | `POST /v1/compile` |
| `nlp2uri_execute` | `POST /v1/execute` |
| `nlp2uri_handle` | `POST /v1/handle` |
