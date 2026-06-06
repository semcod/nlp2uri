# Orchestracja usług, artefaktów i zmiennych przez URI + MCP

**Status:** 2026-06-06  
**Ekosystem:** nlp2uri · getv · nlp2dsl/env2llm · todomat · koru · iterun · curllm

## Idea

Każdy byt ma **kanoniczny adres URI**. MCP udostępnia mały zestaw operacji nad tymi adresami — nie osobne narzędzie na każdy artefakt.

```text
Źródło prawdy          Indeks URI              Operacje MCP/HTTP
─────────────────────────────────────────────────────────────────
~/.getv profiles   →   getv://cat/prof/VAR  →  list / resolve / get / compile
SystemMapIR/DOQL   →   command://…          →  list / resolve / compile → NLP2DSL
                     artifact://…         →  list / resolve / read
                     service://…          →  list / resolve / health
                     runtime://…          →  probe / health
NL desktop         →   app://…            →  plan / handle / execute
Todomat registry   →   (HTTP log)         →  trigger / route / run
Koru planfile      →   ticket workflow    →  koru_list_tickets / koru_run_ticket
```

Szczegóły schematów: [system_map_uri.v1.md](./system_map_uri.v1.md), [getv_uri.v1.md](./getv_uri.v1.md).

---

## Szybki start — cały stack

### 1. Zmienne środowiskowe (getv)

```bash
# Zainstaluj getv + nlp2uri z warstwą env
pip install -e ~/github/wronai/getv
pip install -e ~/github/semcod/nlp2uri[envmap]

# Skopiuj klucz API z przeglądarki → ~/.getv
getv grab

# Eksport do .env projektu (np. todomat Docker)
~/github/wronai/todomat/scripts/sync-env-from-getv.sh llm/groq llm/openrouter
```

### 2. Stack orchestracji (todomat Docker)

```bash
cd ~/github/wronai/todomat
cp .env.example .env
./scripts/sync-env-from-getv.sh llm/groq   # opcjonalnie
MOCK_MODE=0 ./scripts/bootstrap.sh
./scripts/test-local.sh
```

| Usługa | URL | Rola |
|--------|-----|------|
| Pipeline Router | http://localhost:9099/v1 | Open WebUI / agenty OpenAI-compatible |
| Trigger Gateway | http://localhost:8084/trigger | Orchestrator HTTP + registry |
| NLP2DSL adapter | wewnętrzny :8081 | Workflow biznesowe |
| ITERUN adapter | wewnętrzny :8082 | Mikroserwisy / stack |
| curllm adapter | wewnętrzny :8085 | Dane z internetu |
| nlp2uri adapter | wewnętrzny :8086 | Desktop + getv + URI |
| Process Registry | wewnętrzny :8083 | Log wykonań |

### 3. Upstreamy (prawdziwe backendy)

```env
MOCK_MODE=0
NLP2DSL_UPSTREAM=http://host.docker.internal:8010
ITERUN_UPSTREAM=http://host.docker.internal:8800
CURLLM_UPSTREAM=http://host.docker.internal:8810
NLP2URI_MOCK_MODE=0          # gdy nlp2uri zainstalowany w obrazie
```

---

## Konfiguracja MCP w Cursor

Pełny zestaw serwerów — **jeden router + bezpośredni dostęp do URI + koru**:

```json
{
  "mcpServers": {
    "todomat": {
      "command": "todomat-mcp",
      "cwd": "/home/tom/github/wronai/todomat",
      "env": {
        "TRIGGER_GATEWAY_URL": "http://localhost:8084",
        "NLP2DSL_BACKEND_URL": "http://localhost:8010",
        "CURLLM_API_HOST": "http://localhost:8810",
        "CURLLM_LIGHT_FETCH": "1",
        "GETV_HOME": "/home/tom/.getv",
        "TODOMAT_NLP2URI_CWD": "/home/tom/github/semcod/nlp2uri"
      }
    },
    "nlp2uri": {
      "command": "nlp2uri-mcp",
      "cwd": "/home/tom/github/semcod/nlp2uri",
      "env": {
        "NLP2DSL_BACKEND_URL": "http://localhost:8010",
        "GETV_HOME": "/home/tom/.getv"
      }
    },
    "koru": {
      "command": "python",
      "args": ["-m", "koru.mcp_server"],
      "cwd": "/home/tom/github/semcod/koru"
    }
  }
}
```

Instalacja jednym skryptem (todomat):

```bash
~/github/wronai/todomat/scripts/install-mcp-stack.sh
```

| Serwer MCP | Kiedy używać |
|------------|--------------|
| **todomat** | Auto-routing: jeden prompt → właściwy pipeline (nlp2dsl/iterun/curllm/nlp2uri) |
| **nlp2uri** | Bezpośrednia kontrola URI: desktop, getv, SystemMap |
| **koru** | Tickety planfile, IDE drive, bridge `koru_desktop_uri_*` |

---

## Mapa: typ bytu → URI → narzędzie MCP

| Byt | Scheme | List | Resolve (NL→URI) | Wykonaj |
|-----|--------|------|------------------|---------|
| Zmienna env | `getv://llm/groq/GROQ_API_KEY` | `nlp2uri_list_getv_uris` | `nlp2uri_resolve_getv` | `nlp2uri_get_getv_var` + `getv exec` |
| Komenda workflow | `command://runtime/send_invoice` | `nlp2uri_list_system_uris` | `nlp2uri_resolve_system_map` | compile → POST NLP2DSL |
| Artefakt (plik) | `artifact://01-invoice/out.pdf` | `nlp2uri_list_system_uris` | po nazwie w SystemMap | read/open (compile) |
| Mikroserwis | `service://generated/api` | `nlp2uri_list_system_uris` | po nazwie | health probe |
| Runtime worker | `runtime://worker/executor` | `nlp2uri_list_system_uris` | po id | `curl …/health` |
| Aplikacja OS | `app://firefox/open` | — | `nlp2uri_resolve` | `nlp2uri_handle` |
| Zadanie koru | planfile ticket | `koru_list_tickets` | — | `koru_run_ticket` |
| Prompt orchestrator | — | `todomat_route` | auto | `todomat_run` / `todomat_trigger` |

---

## Przykłady — zmienne (getv)

### MCP (nlp2uri)

```json
// Lista wszystkich zmiennych w ~/.getv
{ "tool": "nlp2uri_list_getv_uris", "arguments": {} }

// NL → URI
{ "tool": "nlp2uri_resolve_getv", "arguments": { "prompt": "GROQ_API_KEY" } }
// → getv://llm/groq/GROQ_API_KEY

// Metadane (wartość zamaskowana)
{ "tool": "nlp2uri_get_getv_var", "arguments": { "uri": "getv://llm/groq/GROQ_API_KEY" } }
```

### CLI

```bash
nlp2uri resolve-getv "klucz api groq" --json
getv get llm groq GROQ_API_KEY
getv exec llm groq -- python -c "import os; print(bool(os.getenv('GROQ_API_KEY')))"
```

### Todomat (Open WebUI lub trigger)

Model: `nlp2uri-desktop-agent` lub auto-routing.

```bash
curl -s -X POST http://localhost:8084/trigger \
  -H 'Content-Type: application/json' \
  -d '{"text":"pokaż GROQ_API_KEY z getv","pipeline":"nlp2uri","execute":false}'
```

---

## Przykłady — usługi i workflow (SystemMap + NLP2DSL)

### Indeks URI z przykładu nlp2dsl

```bash
cd ~/github/semcod/nlp2uri
nlp2uri list-system-uris \
  --example-dir ~/github/wronai/nlp2dsl/examples/01-invoice \
  --json | jq '.entries[:5]'
```

### Resolve komendy z NL

```json
{
  "tool": "nlp2uri_resolve_system_map",
  "arguments": {
    "prompt": "wyślij fakturę do klienta",
    "example_dir": "/home/tom/github/wronai/nlp2dsl/examples/01-invoice",
    "fallback_desktop": false
  }
}
```

Wynik: `command://executor%3Aworker/send_invoice` → compile wykonuje:

```bash
curl -sfX POST http://localhost:8010/workflow/run \
  -H 'Content-Type: application/json' \
  -d '{"action":"send_invoice","runtime":"executor:worker","config":{}}'
```

### Orchestrator todomat (pełny flow)

```bash
# Auto: wykryje nlp2dsl vs iterun vs nlp2uri
curl -s -X POST http://localhost:8084/trigger \
  -H 'Content-Type: application/json' \
  -d '{"text":"wyślij fakturę po opłaceniu zamówienia","pipeline":"auto","execute":true}'

# Mikroserwis → iterun
curl -s -X POST http://localhost:8084/trigger \
  -d '{"text":"zbuduj mikroserwis fastapi z redis","pipeline":"iterun","execute":true}'

# Web research → curllm → downstream
curl -s -X POST http://localhost:8084/trigger \
  -d '{"text":"pobierz dane z https://example.com i zautomatyzuj proces","pipeline":"online-auto","execute":true}'
```

### MCP todomat (agent w Cursor)

```text
todomat_route("zbuduj api gateway z docker compose")
→ {"pipeline": "iterun", ...}

todomat_run("wyślij fakturę do klienta po opłaceniu")
→ child nlp2dsl-mcp → nlp2dsl_plan + execute

todomat_trigger("otwórz firefox", pipeline="nlp2uri")
→ HTTP nlp2uri-adapter → desktop handle
```

---

## Przykłady — artefakty

Artefakty są indeksowane z `SystemMapIR` jako `artifact://{example_id}/{path}`.

```bash
# Lista artefaktów w przykładzie
nlp2uri list-system-uris \
  --example-dir ~/github/wronai/nlp2dsl/examples/01-invoice \
  --json | jq '[.entries[] | select(.kind=="artifact")]'

# Resolve po opisie NL (gdy opis w IR pasuje)
nlp2uri resolve-system-map "pokaż fakturę pdf" \
  --example-dir ~/github/wronai/nlp2dsl/examples/01-invoice
```

Compile `artifact://` (faza rozwoju — podgląd ścieżki):

```bash
nlp2uri compile "artifact://01-invoice/invoices/out.pdf" --dry-run
```

---

## Przykłady — desktop i zadania OS

```bash
# Plan bez wykonania
nlp2uri plan "otwórz vscode w folderze ~/github/semcod/koru" --json

# Wykonanie (zaufany host)
nlp2uri handle "otwórz firefox" --dry-run=false

# MCP
{ "tool": "nlp2uri_plan", "arguments": { "prompt": "zrób screenshot ekranu", "platform": "linux" } }
```

Todomat auto-routing wykrywa desktop bez modelu:

```text
"otwórz firefox"           → pipeline nlp2uri
"otwórz terminal"          → pipeline nlp2uri
"pokaż OPENAI_API_KEY"     → pipeline nlp2uri (getv)
```

---

## Przykłady — zadania koru (planfile)

```json
{ "tool": "koru_list_tickets", "arguments": { "project_root": "/home/tom/github/semcod/koru" } }

{ "tool": "koru_run_ticket", "arguments": { "project_root": "...", "ticket_id": "KORU-42" } }
```

Bridge URI (gdy agent nie ma bezpośrednio nlp2uri):

```json
{ "tool": "koru_desktop_uri_resolve_getv", "arguments": { "prompt": "GITHUB_TOKEN" } }
{ "tool": "koru_desktop_uri_resolve_system_map", "arguments": {
    "prompt": "send invoice",
    "doql_path": "/path/to/environment.doql.less"
}}
```

---

## Scenariusze end-to-end

### A. Klient wdraża automatyzację faktur

1. `getv grab` — klucze SMTP, OpenAI w `~/.getv`
2. `./scripts/sync-env-from-getv.sh` — `.env` dla Docker
3. Open WebUI → `http://localhost:9099/v1`, model `nlp2dsl-process-agent`
4. Prompt: *„wyślij fakturę 1500 PLN na klient@firma.pl po opłaceniu zamówienia”*
5. Trigger gateway loguje wykonanie w process-registry

### B. Agent Cursor buduje mikroserwis

1. MCP `todomat_run("stwórz aplikację web kontaktu z formularzem i docker compose")`
2. Routing → `iterun` → `iterun_run_pipeline`
3. Artefakty w repo klienta; opcjonalnie `koru_list_tickets` dla follow-up

### C. DevOps: health wielu runtime'ów

```bash
# Z SystemMap
for uri in $(nlp2uri list-system-uris --example-dir ... --json | jq -r '.entries[] | select(.kind=="runtime") | .uri'); do
  echo "=== $uri"
  nlp2uri compile "$uri" --dry-run
done
```

### D. Research online + automatyzacja

Model `orchestrator-online` lub:

```text
todomat_run("pobierz dane z https://news.ycombinator.com i wygeneruj raport sprzedaży")
```

Flow: curllm (web_data) → wzbogacony prompt → nlp2dsl lub iterun.

---

## Open WebUI — modele

| Model | Pipeline | Zastosowanie |
|-------|----------|--------------|
| `nlp2dsl-process-agent` | nlp2dsl | Procesy biznesowe, emaile, workflow |
| `iterun-service-builder` | iterun | API, mikroserwisy, stack Docker |
| `curllm-web-research` | curllm | Pobieranie danych z WWW |
| `orchestrator-online` | online-auto | curllm → nlp2dsl/iterun |
| `orchestrator-auto` | auto | Auto-wybór nlp2dsl vs iterun |
| `nlp2uri-desktop-agent` | nlp2uri | Desktop, getv, URI SystemMap |

Connection: Base URL `http://host.docker.internal:9099/v1`, API Key `dev-key`.

---

## Narzędzia todomat-mcp

| Tool | Opis |
|------|------|
| `todomat_interfaces` | Backends, pipelines, gateway URL |
| `todomat_route` | Detekcja pipeline bez wykonania |
| `todomat_run` | Auto-routing + child MCP |
| `todomat_trigger` | HTTP trigger-gateway (+ registry) |
| `todomat_call` | Jawny proxy: `backend` + `tool` + args |
| `todomat_list_tools` | Narzędzia z child MCP |

Przykład jawnego wywołania nlp2uri:

```json
{
  "tool": "todomat_call",
  "arguments": {
    "backend": "nlp2uri",
    "tool": "nlp2uri_resolve_getv",
    "arguments": { "prompt": "GROQ_API_KEY" }
  }
}
```

---

## Rozszerzanie o nowe źródła URI

Nowy typ bytu (np. `container://`, `ticket://`) wymaga:

1. Spec `{name}_uri.v1.md`
2. `build_*_uri_index()` → `UriMap`
3. `resolve_prompt_against_*()`
4. `compile_*_uri()` → `OSAction[]` lub HTTP handoff
5. Opcjonalnie entry point `nlp2uri.schemes` (plugin registry)

MCP **nie musi** dostawać nowych nazw narzędzi — wystarczy rozszerzyć `nlp2uri_compile` / `nlp2uri_list_system_uris`.

---

## Troubleshooting

| Problem | Rozwiązanie |
|---------|-------------|
| Pusta odpowiedź Open WebUI | Sprawdź `NLP2DSL_UPSTREAM`, timeout 300s, logi `trigger-gateway` |
| `nlp2uri not installed` w koru | `pip install 'koru[desktop]'` lub `pip install nlp2uri[envmap]` |
| Mock zamiast realnych upstreamów | `MOCK_MODE=0` + per-engine `*_MOCK_MODE=0` |
| getv puste | `getv grab` + `GETV_HOME` w env MCP |
| Routing zły pipeline | `todomat_route("...")` — hinty w `todomat/domains/routing/intent.py` |
| pytest `todomat_mcp` not found | Użyj `python -m pytest` z venv projektu |

---

## CQRS + ES + Protobuf (standard per scheme)

Każdy `scheme://` ma własny kontrakt CQRS z Event Sourcing i protobuf — pod generowanie driverów (linux, getv_cli, curl, docker…) i API (gRPC + OpenAPI + MCP):

→ [schemas/uri_cqrs_es.v1.md](../schemas/uri_cqrs_es.v1.md)  
→ [schemas/README.md](../schemas/README.md)

```bash
cd schemas && ./codegen/generate.sh --scheme command
# → generated/python/drivers/command/curl.py (stub)
# → generated/mcp/tools.json
```

## Powiązane dokumenty

- [mcp-tools.md](./mcp-tools.md) — pełna lista narzędzi nlp2uri-mcp
- [system_map_uri.v1.md](./system_map_uri.v1.md) — schematy command/artifact/service/…
- [getv_uri.v1.md](./getv_uri.v1.md) — zmienne środowiskowe
- [todomat docs/MCP.md](https://github.com/wronai/todomat/blob/main/docs/MCP.md) — router MCP
- [koru desktop-uri](https://github.com/semcod/koru/blob/main/docs/desktop-uri-orchestration.md) — bridge MCP
