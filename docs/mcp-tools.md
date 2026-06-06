# MCP tools — nlp2uri

Server: `nlp2uri-mcp` (stdio JSON-RPC, MCP 2024-11-05).

**Pełny przewodnik orchestracji** (wiele usług, artefaktów, zmiennych, todomat, koru):  
→ [orchestration.md](./orchestration.md)

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

### `nlp2uri_list_system_uris`

Kanoniczne URI dla wszystkich bytów `SystemMapIR` (env2llm).

**Input** (jedno z pól):

```json
{
  "system_map": { "format": "nlp2dsl.system_map.v1", "example_id": "01-invoice", "commands": [] },
  "doql_path": "/path/to/environment.doql.less",
  "example_dir": "/path/to/nlp2dsl/examples/01-invoice"
}
```

### `nlp2uri_resolve_system_map`

NL → URI względem SystemMap; przy braku trafienia → desktop (`open firefox`, …).

```json
{
  "prompt": "send invoice",
  "system_map": { "...": "..." },
  "fallback_desktop": true,
  "platform": "linux"
}
```

### `nlp2uri_list_getv_uris`

Indeks profili `~/.getv` jako `getv://category/profile/VAR`.

```json
{ "getv_home": "/home/tom/.getv" }
```

### `nlp2uri_resolve_getv`

NL → URI zmiennej środowiskowej.

```json
{ "prompt": "GROQ_API_KEY" }
```

→ `getv://llm/groq/GROQ_API_KEY`

### `nlp2uri_get_getv_var`

Metadane zmiennej (wartość zamaskowana).

```json
{ "uri": "getv://llm/groq/GROQ_API_KEY" }
```

---

## Orchestracja przez todomat-mcp

Jeden router MCP zamiast ręcznego wyboru narzędzia:

```text
todomat_run("otwórz firefox")                    → nlp2uri_handle
todomat_run("pokaż GROQ_API_KEY z getv")         → nlp2uri_resolve_getv
todomat_run("wyślij fakturę do klienta")         → nlp2dsl
todomat_trigger("...", pipeline="nlp2uri")       → HTTP nlp2uri-adapter
```

Konfiguracja: [todomat examples/mcp-cursor.json](https://github.com/wronai/todomat/blob/main/examples/mcp-cursor.json)

## Koru bridge

Te same operacje przez `koru_desktop_uri_*` gdy agent ma tylko serwer koru:

| nlp2uri tool | koru tool |
|--------------|-----------|
| `nlp2uri_plan` | `koru_desktop_uri_plan` |
| `nlp2uri_handle` | `koru_desktop_uri_handle` |
| `nlp2uri_list_getv_uris` | `koru_desktop_uri_list_getv_uris` |
| `nlp2uri_resolve_getv` | `koru_desktop_uri_resolve_getv` |
| `nlp2uri_get_getv_var` | `koru_desktop_uri_get_getv_var` |
| `nlp2uri_list_system_uris` | `koru_desktop_uri_list_system_uris` |
| `nlp2uri_resolve_system_map` | `koru_desktop_uri_resolve_system_map` |

→ [koru/docs/desktop-uri-orchestration.md](https://github.com/semcod/koru/blob/main/docs/desktop-uri-orchestration.md)

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
| `nlp2uri_list_getv_uris` | (MCP only; CLI: `nlp2uri list-getv`) |
| `nlp2uri_resolve_getv` | (MCP only) |
| `nlp2uri_list_system_uris` | (MCP only; CLI: `nlp2uri list-system-uris`) |
| `nlp2uri_resolve_system_map` | (MCP only) |
