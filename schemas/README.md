# nlp2uri schemas — CQRS + ES + Protobuf

Standard źródłowy dla **każdego typu URI**: commands, events, queries, drivers, gRPC/REST API.

## Struktura

```text
schemas/
├── uri_cqrs_es.v1.md      # specyfikacja standardu
├── registry.yaml          # rejestr schematów + targety driverów
├── buf.yaml / buf.gen.yaml
├── common/v1/             # wspólne proto (Uri, Command, Event, Query, Driver, API)
├── schemes/{scheme}/v1/   # per-scheme CQRS+ES
│   ├── aggregate.proto
│   ├── commands.proto
│   ├── events.proto
│   ├── queries.proto
│   ├── driver.proto       # kontrakt drivera × platforma
│   ├── api.proto          # gRPC CommandService + QueryService
│   ├── openapi.yaml       # REST projection
│   └── README.md
└── codegen/
    ├── generate.sh
    ├── scaffold_scheme.py
    ├── export_mcp_schemas.py
    ├── export_driver_stubs.py
    └── templates/
```

## Warstwy URI (registry.yaml)

| Layer | Schemes |
|-------|---------|
| `desktop` | `app`, `desktop_screenshot`, `desktop_window`, `file`, `http` |
| `env` | `getv` |
| `systemmap` | `command`, `runtime`, `resource`, `access`, `artifact`, `conversation`, `process`, `validation`, `schedule`, `service`, `deploy`, `environment` |
| `host` | `endpoint`, `device`, `container`, `mount` (draft) |

## Generowanie

```bash
cd schemas

# Scaffold wszystkich scheme + MCP JSON + driver stubs
./codegen/generate.sh

# Jedna schema
./codegen/generate.sh --scheme command

# Protobuf (wymaga buf CLI)
brew install bufbuild/buf/buf   # lub https://buf.build/docs/installation
buf dep update
./codegen/generate.sh
```

Output:

| Artefakt | Ścieżka |
|----------|---------|
| Python protobuf + gRPC | `generated/python/` |
| OpenAPI | `generated/openapi/` |
| MCP tool schemas | `generated/mcp/tools.json` |
| Driver stubs | `generated/python/drivers/{scheme}/{target}.py` |

## CQRS flow (każdy scheme)

```text
Command → Aggregate (uri.raw) → Event append → Projection (UriMap)
Query   → read projection / live compile
Driver  → CompileUri / ExecuteUri / Probe per platform
```

## Runtime (Python)

Zaimplementowane drivery referencyjne w `src/nlp2uri/cqrs/`:

| Driver | Scheme | Target |
|--------|--------|--------|
| `CommandCurlDriver` | `command` | `curl` |
| `GetvCliDriver` | `getv` | `getv_cli` |
| `RuntimeCurlDriver` | `runtime` | `curl` |
| `EndpointCurlDriver` | `endpoint` | `curl` |
| `DelegateCompileDriver` | desktop schemes | `linux`/`darwin`/… |

```python
from nlp2uri.cqrs import CqrsDispatcher

d = CqrsDispatcher()
d.compile_uri("command://executor%3Aworker/send_invoice")
d.execute_uri("endpoint://tcp/127.0.0.1/8010/health", dry_run=True)
```

Testy: `pytest tests/test_cqrs_drivers.py` · smoke: `./scripts/test-cqrs-smoke.sh`

## Dodanie nowego scheme

1. Wpis w `registry.yaml`
2. `./codegen/generate.sh --scheme nowy_scheme`
3. Implementacja stubów w `generated/python/drivers/nowy_scheme/`
4. Podłączenie w `nlp2uri.compile.compile_uri_to_actions()`

## Dokumentacja

- [uri_cqrs_es.v1.md](./uri_cqrs_es.v1.md)
- [../docs/system_map_uri.v1.md](../docs/system_map_uri.v1.md)
- [../docs/getv_uri.v1.md](../docs/getv_uri.v1.md)
- [../docs/orchestration.md](../docs/orchestration.md)
