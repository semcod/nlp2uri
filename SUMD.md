# nlp2uri

Natural language to URI resolution and cross-platform local URI execution

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Interfaces](#interfaces)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Deployment](#deployment)
- [Environment Variables (`.env.example`)](#environment-variables-envexample)
- [Release Management (`goal.yaml`)](#release-management-goalyaml)
- [Code Analysis](#code-analysis)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Intent](#intent)

## Metadata

- **name**: `nlp2uri`
- **version**: `0.4.7`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, testql(2), app.doql.less, goal.yaml, .env.example, Dockerfile, docker-compose.yml, project/(3 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: nlp2uri;
  version: 0.4.7;
}

dependencies {
  runtime: pyyaml>=6.0;
  dev: "pytest>=8.0, pytest-cov>=5.0, goal>=2.1.0, costs>=0.1.20, pfix>=0.1.60";
}

interface[type="cli"] {
  framework: argparse;
}
interface[type="cli"] page[name="nlp2uri"] {

}

deploy {
  target: docker-compose;
  compose_file: docker-compose.yml;
}

environment[name="local"] {
  runtime: docker-compose;
  env_file: .env;
  python_version: >=3.10;
}
```

## Interfaces

### CLI Entry Points

- `nlp2uri`
- `nlp2uri-mcp`
- `nlp2uri-serve`

### testql Scenarios

#### `testql-scenarios/generated-cli-tests.testql.toon.yaml`

```toon markpact:testql path=testql-scenarios/generated-cli-tests.testql.toon.yaml
# SCENARIO: CLI Command Tests
# TYPE: cli
# GENERATED: true

CONFIG[2]{key, value}:
  cli_command, python -m nlp2uri
  timeout_ms, 10000

# Test 1: CLI help command
SHELL "python -m nlp2uri --help" 5000
ASSERT_EXIT_CODE 0
ASSERT_STDOUT_CONTAINS "usage"

# Test 2: CLI version command
SHELL "python -m nlp2uri --version" 5000
ASSERT_EXIT_CODE 0

# Test 3: CLI main workflow (dry-run)
SHELL "python -m nlp2uri --help" 10000
ASSERT_EXIT_CODE 0
```

#### `testql-scenarios/generated-from-pytests.testql.toon.yaml`

```toon markpact:testql path=testql-scenarios/generated-from-pytests.testql.toon.yaml
# SCENARIO: Auto-generated from Python Tests
# TYPE: integration
# GENERATED: true

CONFIG[2]{key, value}:
  base_url, ${api_url:-http://localhost:8101}
  timeout_ms, 10000

# Converted 2 assertions from pytest
ASSERT[2]{field, operator, expected}:
  status, ==, 200
  status, ==, 200
```

## Configuration

```yaml
project:
  name: nlp2uri
  version: 0.4.7
  env: local
```

## Dependencies

### Runtime

```text markpact:deps python
pyyaml>=6.0
```

### Development

```text markpact:deps python scope=dev
pytest>=8.0
pytest-cov>=5.0
goal>=2.1.0
costs>=0.1.20
pfix>=0.1.60
```

## Deployment

```bash markpact:run
pip install nlp2uri

# development install
pip install -e .[dev]
```

### Docker

- **base image**: `python:3.12-slim-bookworm`
- **entrypoint**: `["bash", "examples/run-e2e.sh"]`

### Docker Compose (`docker-compose.yml`)

- **nlp2uri-test** image=`nlp2uri:test`

## Environment Variables (`.env.example`)

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | `*(not set)*` | Required: OpenRouter API key (https://openrouter.ai/keys) |
| `LLM_MODEL` | `openrouter/qwen/qwen3-coder-next` | Model (default: openrouter/qwen/qwen3-coder-next) |
| `PFIX_AUTO_APPLY` | `true` | true = apply fixes without asking |
| `PFIX_AUTO_INSTALL_DEPS` | `true` | true = auto pip/uv install |
| `PFIX_AUTO_RESTART` | `false` | true = os.execv restart after fix |
| `PFIX_MAX_RETRIES` | `3` |  |
| `PFIX_DRY_RUN` | `false` |  |
| `PFIX_ENABLED` | `true` |  |
| `PFIX_GIT_COMMIT` | `false` | true = auto-commit fixes |
| `PFIX_GIT_PREFIX` | `pfix:` | commit message prefix |
| `PFIX_CREATE_BACKUPS` | `false` | false = disable .pfix_backups/ directory |

## Release Management (`goal.yaml`)

- **versioning**: `semver`
- **commits**: `conventional` scope=`nlp2uri`
- **changelog**: `keep-a-changelog`
- **build strategies**: `python`, `nodejs`, `rust`
- **version files**: `VERSION`, `pyproject.toml:version`, `venv/lib/python3.13/site-packages/cryptography/__init__.py:__version__`

## Code Analysis

### `project/map.toon.yaml`

```toon markpact:analysis path=project/map.toon.yaml
# nlp2uri | 109f 8551L | python:93,shell:15,less:1 | 2026-06-06
# stats: 316 func | 47 cls | 109 mod | CC̄=3.6 | critical:14 | cycles:0
# alerts[5]: CC build_uri_index=31; CC resolve_prompt_against_system_map=26; CC _compile_app=16; CC _compile_terminal=16; CC build_resource_actions=14
# hotspots[5]: build_uri_index fan=20; build_getv_uri_index fan=19; main fan=18; compile_uri_to_actions fan=17; _compile_app fan=15
# evolution: baseline
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[109]:
  app.doql.less,30
  examples/execute/dry-run/e2e.sh,12
  examples/execute/dry-run/main.py,30
  examples/integrators/mcp-stdio/e2e.sh,16
  examples/integrators/rest-api/e2e.sh,24
  examples/integrators/shell-export/e2e.sh,13
  examples/mcp/tool-handoff/e2e.sh,12
  examples/mcp/tool-handoff/main.py,28
  examples/resolve/new-intents/e2e.sh,26
  examples/resolve/nl-to-uri/e2e.sh,12
  examples/resolve/nl-to-uri/main.py,47
  examples/run-e2e.sh,41
  project.sh,59
  schemas/codegen/export_driver_stubs.py,98
  schemas/codegen/export_mcp_schemas.py,54
  schemas/codegen/fix_proto_imports.py,84
  schemas/codegen/generate.sh,54
  schemas/codegen/scaffold_scheme.py,358
  scripts/install-editable.sh,23
  scripts/test-cqrs-smoke.sh,56
  scripts/test-live-registry.sh,67
  scripts/testapp-handler.sh,7
  src/nlp2uri/__init__.py,29
  src/nlp2uri/adapters/__init__.py,18
  src/nlp2uri/adapters/base.py,60
  src/nlp2uri/adapters/cli.py,40
  src/nlp2uri/adapters/mcp.py,383
  src/nlp2uri/adapters/rest.py,88
  src/nlp2uri/adapters/shell.py,67
  src/nlp2uri/cli.py,200
  src/nlp2uri/compile.py,432
  src/nlp2uri/config.py,231
  src/nlp2uri/cqrs/__init__.py,9
  src/nlp2uri/cqrs/base.py,98
  src/nlp2uri/cqrs/dispatcher.py,118
  src/nlp2uri/cqrs/drivers/__init__.py,30
  src/nlp2uri/cqrs/drivers/artifact_filesystem.py,33
  src/nlp2uri/cqrs/drivers/command_curl.py,40
  src/nlp2uri/cqrs/drivers/container_docker.py,89
  src/nlp2uri/cqrs/drivers/delegate.py,30
  src/nlp2uri/cqrs/drivers/endpoint_curl.py,34
  src/nlp2uri/cqrs/drivers/getv_cli.py,28
  src/nlp2uri/cqrs/drivers/resource_probe.py,36
  src/nlp2uri/cqrs/drivers/runtime_curl.py,35
  src/nlp2uri/cqrs/drivers/service_ops.py,129
  src/nlp2uri/cqrs/event_store.py,68
  src/nlp2uri/cqrs/http_store.py,53
  src/nlp2uri/cqrs/plugins.py,65
  src/nlp2uri/cqrs/registry.py,98
  src/nlp2uri/host/__init__.py,16
  src/nlp2uri/host/artifact.py,95
  src/nlp2uri/host/endpoint.py,35
  src/nlp2uri/host/resource.py,70
  src/nlp2uri/integrators/__init__.py,23
  src/nlp2uri/integrators/mcp_server.py,129
  src/nlp2uri/integrators/rest_server.py,91
  src/nlp2uri/mcp.py,82
  src/nlp2uri/models.py,181
  src/nlp2uri/parse_nl.py,377
  src/nlp2uri/platform_detect.py,19
  src/nlp2uri/platforms/__init__.py,7
  src/nlp2uri/platforms/base.py,131
  src/nlp2uri/platforms/linux.py,146
  src/nlp2uri/platforms/macos.py,95
  src/nlp2uri/platforms/registry.py,25
  src/nlp2uri/platforms/windows.py,95
  src/nlp2uri/resolve.py,41
  src/nlp2uri/runtime.py,93
  src/nlp2uri/schemes/__init__.py,6
  src/nlp2uri/schemes/build.py,65
  src/nlp2uri/schemes/desktop.py,167
  src/nlp2uri/schemes/file.py,26
  src/nlp2uri/schemes/http.py,23
  src/nlp2uri/schemes/ide.py,36
  src/nlp2uri/schemes/util.py,48
  src/nlp2uri/service.py,152
  src/nlp2uri/systemmap/__init__.py,69
  src/nlp2uri/systemmap/compile.py,180
  src/nlp2uri/systemmap/context.py,48
  src/nlp2uri/systemmap/encode.py,16
  src/nlp2uri/systemmap/fallback.py,53
  src/nlp2uri/systemmap/getv_load.py,98
  src/nlp2uri/systemmap/getv_uri.py,226
  src/nlp2uri/systemmap/index.py,268
  src/nlp2uri/systemmap/load.py,47
  src/nlp2uri/systemmap/resolve.py,123
  src/nlp2uri/systemmap/uri.py,94
  tests/conftest.py,18
  tests/integration/test_xdg_handler.py,99
  tests/test_adapters.py,120
  tests/test_artifact_driver.py,57
  tests/test_cli.py,31
  tests/test_compile.py,34
  tests/test_config.py,65
  tests/test_container_driver.py,56
  tests/test_cqrs_drivers.py,115
  tests/test_getv_uri.py,74
  tests/test_http_event_store.py,51
  tests/test_intents_phase2.py,112
  tests/test_mcp.py,25
  tests/test_platforms.py,48
  tests/test_plugins.py,33
  tests/test_resolve.py,77
  tests/test_resource_driver.py,44
  tests/test_rest_server.py,48
  tests/test_schemas_registry.py,53
  tests/test_service.py,27
  tests/test_systemmap.py,174
  tree.sh,2
D:
  examples/execute/dry-run/main.py:
    e: main
    main()
  examples/mcp/tool-handoff/main.py:
    e: main
    main()
  examples/resolve/nl-to-uri/main.py:
    e: main
    main()
  schemas/codegen/export_driver_stubs.py:
    e: main
    main()
  schemas/codegen/export_mcp_schemas.py:
    e: tool_schema,main
    tool_schema(scheme;meta)
    main()
  schemas/codegen/fix_proto_imports.py:
    e: _pascal,fix_api,fix_driver,main
    _pascal(scheme)
    fix_api(path;scheme)
    fix_driver(path;scheme)
    main()
  schemas/codegen/scaffold_scheme.py:
    e: _pascal,_proto_package,_write,aggregate_proto,commands_proto,events_proto,queries_proto,driver_proto,api_proto,openapi_yaml,readme_md,scaffold_scheme,main
    _pascal(name)
    _proto_package(scheme;meta)
    _write(path;content)
    aggregate_proto(scheme;meta)
    commands_proto(scheme;meta)
    events_proto(scheme;meta)
    queries_proto(scheme;meta)
    driver_proto(scheme;meta)
    api_proto(scheme;meta)
    openapi_yaml(scheme;meta)
    readme_md(scheme;meta)
    scaffold_scheme(scheme;meta)
    main()
  src/nlp2uri/__init__.py:
  src/nlp2uri/adapters/__init__.py:
  src/nlp2uri/adapters/base.py:
    e: AdapterRequest,AdapterResponse,BaseAdapter
    AdapterRequest:
    AdapterResponse: to_dict(0)
    BaseAdapter: __init__(1),with_platform(1),handle(1),_service_for(1)
  src/nlp2uri/adapters/cli.py:
    e: CliAdapter
    CliAdapter: handle(1)
  src/nlp2uri/adapters/mcp.py:
    e: McpAdapter
    McpAdapter: handle(1),call_tool(2),tool_dispatch(0),_args_from_request(1),_args_to_request(2),mcp_content(1),_tool_plan(1),_tool_resolve(1),_tool_compile(1),_tool_execute(1),_tool_handle(1),_tool_list_system_uris(1),_tool_resolve_system_map(1),_tool_list_getv_uris(1),_tool_resolve_getv(1),_tool_get_getv_var(1),_tool_cqrs_compile(1),_tool_cqrs_execute(1)
  src/nlp2uri/adapters/rest.py:
    e: RestAdapter
    RestAdapter: handle(1),dispatch(2),body_to_request(1),match_route(2)
  src/nlp2uri/adapters/shell.py:
    e: ShellAdapter
    ShellAdapter: handle(1),_export_script(0)
  src/nlp2uri/cli.py:
    e: _add_common_args,_build_parser,_platform,_emit,_request_from_args,_with_platform,_run_config,_run_shell,_run_adapter_command,_run_execute,main
    _add_common_args(parser)
    _build_parser()
    _platform(raw)
    _emit(payload)
    _request_from_args(args)
    _with_platform(payload)
    _run_config(args)
    _run_shell(args)
    _run_adapter_command(args)
    _run_execute(args)
    main(argv)
  src/nlp2uri/compile.py:
    e: compile_uri_to_actions,_query_params,_first_available,_open_uri,_compile_app,_compile_settings_panel,_compile_terminal,_compile_settings,_compile_launch_app,_capture_outfile,_linux_screen_capture,_macos_screen_capture,_windows_screen_capture,_compile_screen_capture,_linux_window_capture,_macos_window_capture,_windows_window_capture,_compile_window_capture,_compile_screenshot,_compile_window_move,_compile_window,_compile_legacy_nlp2uri,_desktop_id_for_app
    compile_uri_to_actions(uri;os)
    _query_params(parsed)
    _first_available(names)
    _open_uri(host;uri)
    _compile_app(host;authority;path;params;uri)
    _compile_settings_panel(host;panel)
    _compile_terminal(host;params)
    _compile_settings(host)
    _compile_launch_app(host;name)
    _capture_outfile(target)
    _linux_screen_capture(host;outfile)
    _macos_screen_capture(host;outfile)
    _windows_screen_capture(host)
    _compile_screen_capture(host;outfile)
    _linux_window_capture(host;outfile)
    _macos_window_capture(host;outfile)
    _windows_window_capture(host;outfile)
    _compile_window_capture(host;outfile;params)
    _compile_screenshot(host;authority;params;uri)
    _compile_window_move(host;params)
    _compile_window(host;authority;params;uri)
    _compile_legacy_nlp2uri(host;uri)
    _desktop_id_for_app(name)
  src/nlp2uri/config.py:
    e: payload_keys,_yaml_scalar,_parse_scalar,_parse_simple_yaml,config_search_paths,find_config_path,default_config,_load_from_path,load_config,save_config,ensure_config,get_effective_platform,reset_config_cache,NLP2URIConfig
    NLP2URIConfig: resolved_platform(0),apply_runtime_env(0),to_dict(0),to_yaml(0)  # Persisted defaults (nlp2uri.yaml).
    payload_keys()
    _yaml_scalar(value)
    _parse_scalar(raw)
    _parse_simple_yaml(text)
    config_search_paths()
    find_config_path()
    default_config()
    _load_from_path(path)
    load_config()
    save_config(cfg;path)
    ensure_config(path)
    get_effective_platform(override)
    reset_config_cache()
  src/nlp2uri/cqrs/__init__.py:
  src/nlp2uri/cqrs/base.py:
    e: DriverCapabilities,CompileResult,ExecuteResult,ProbeResult,UriDriver
    DriverCapabilities:
    CompileResult:
    ExecuteResult:
    ProbeResult:
    UriDriver: capabilities(0),compile(1),execute(2),probe(1)
  src/nlp2uri/cqrs/dispatcher.py:
    e: CqrsDispatcher
    CqrsDispatcher: __init__(0),compile_uri(1),execute_uri(1),probe_uri(1)
  src/nlp2uri/cqrs/drivers/__init__.py:
  src/nlp2uri/cqrs/drivers/artifact_filesystem.py:
    e: ArtifactFilesystemDriver
    ArtifactFilesystemDriver: compile(1)
  src/nlp2uri/cqrs/drivers/command_curl.py:
    e: CommandCurlDriver
    CommandCurlDriver: compile(1),probe(1)
  src/nlp2uri/cqrs/drivers/container_docker.py:
    e: parse_container_uri,ContainerDockerDriver
    ContainerDockerDriver: compile(1),probe(1),_docker_argv(4)
    parse_container_uri(uri)
  src/nlp2uri/cqrs/drivers/delegate.py:
    e: DelegateCompileDriver
    DelegateCompileDriver: __init__(2),compile(1)
  src/nlp2uri/cqrs/drivers/endpoint_curl.py:
    e: EndpointCurlDriver
    EndpointCurlDriver: compile(1),probe(1)
  src/nlp2uri/cqrs/drivers/getv_cli.py:
    e: GetvCliDriver
    GetvCliDriver: compile(1)
  src/nlp2uri/cqrs/drivers/resource_probe.py:
    e: ResourceProbeDriver
    ResourceProbeDriver: compile(1),probe(1)
  src/nlp2uri/cqrs/drivers/runtime_curl.py:
    e: RuntimeCurlDriver
    RuntimeCurlDriver: compile(1),probe(1)
  src/nlp2uri/cqrs/drivers/service_ops.py:
    e: parse_service_name,_compose_dir,ServiceCurlDriver,ServiceDockerDriver,ServiceSystemdDriver
    ServiceCurlDriver: compile(1),probe(1)
    ServiceDockerDriver: compile(1),probe(1)
    ServiceSystemdDriver: compile(1),probe(1)
    parse_service_name(uri)
    _compose_dir(config)
  src/nlp2uri/cqrs/event_store.py:
    e: StoredEvent,InMemoryEventStore
    StoredEvent: to_dict(0)
    InMemoryEventStore: __init__(0),append(1),get_stream(1),all_events(0)
  src/nlp2uri/cqrs/http_store.py:
    e: HttpEventStore
    HttpEventStore: __init__(1),append(1),_post_remote(1)  # In-memory store with async-safe HTTP mirror to process-regis
  src/nlp2uri/cqrs/plugins.py:
    e: _parse_entry_point_name,load_driver_plugins,resolve_driver_class
    _parse_entry_point_name(name)
    load_driver_plugins()
    resolve_driver_class(scheme;target;builtins)
  src/nlp2uri/cqrs/registry.py:
    e: default_registry,DriverRegistry
    DriverRegistry: __init__(1),schemes(0),plugin_drivers(0),targets_for(1),default_target(1),get_driver(2),driver_for_uri(2)
    default_registry()
  src/nlp2uri/host/__init__.py:
  src/nlp2uri/host/artifact.py:
    e: is_artifact_uri,_decode,resolve_artifact_path,build_artifact_actions
    is_artifact_uri(uri)
    _decode(value)
    resolve_artifact_path(uri)
    build_artifact_actions(uri;host)
  src/nlp2uri/host/endpoint.py:
    e: is_endpoint_uri,build_endpoint_url,build_endpoint_actions
    is_endpoint_uri(uri)
    build_endpoint_url(uri)
    build_endpoint_actions(uri;host)
  src/nlp2uri/host/resource.py:
    e: is_resource_uri,_decode,_filesystem_probe_path,build_resource_actions
    is_resource_uri(uri)
    _decode(value)
    _filesystem_probe_path(resource_id)
    build_resource_actions(uri;host)
  src/nlp2uri/integrators/__init__.py:
    e: __getattr__
    __getattr__(name)
  src/nlp2uri/integrators/mcp_server.py:
    e: _jsonrpc_response,_jsonrpc_error,_write_json,_log,_handle_initialize,_handle_tools_list,_handle_tools_call,handle_message,run_stdio,main
    _jsonrpc_response(req_id;result)
    _jsonrpc_error(req_id;code;message;data)
    _write_json(payload)
    _log(message)
    _handle_initialize(_params)
    _handle_tools_list(_params)
    _handle_tools_call(params)
    handle_message(msg)
    run_stdio()
    main(argv)
  src/nlp2uri/integrators/rest_server.py:
    e: run_server,main,NLP2URIRequestHandler
    NLP2URIRequestHandler: log_message(1),_read_json(0),_send(2),do_GET(0),do_POST(0)
    run_server(host;port)
    main(argv)
  src/nlp2uri/mcp.py:
    e: text_uri_list,ui_resource,tool_resolve_desktop_action,tool_execute_desktop_uri,mcp_handoff_payload
    text_uri_list(uris)
    ui_resource(uri)
    tool_resolve_desktop_action(text)
    tool_execute_desktop_uri(uri)
    mcp_handoff_payload(text)
  src/nlp2uri/models.py:
    e: HostPlatform,IntentKind,UriIntent,UriSpec,OSAction,NLP2URIResult,ActionResult
    HostPlatform:
    IntentKind:
    UriIntent: with_params(0),intent_name(0),to_slots(0)  # Structured intent parsed from natural language.
    UriSpec: to_dict(0)  # Resolved abstract URI ready for execution or MCP handoff.
    OSAction: argv(0),to_dict(0)  # Concrete host command derived from an abstract URI.
    NLP2URIResult: to_dict(0)  # Full compiler output: NL → URI + OS action plan.
    ActionResult: to_dict(0)
  src/nlp2uri/parse_nl.py:
    e: _strip_quotes,_normalize_aliases,_parse_absolute_uri,_parse_http_url,_parse_ide_project,_parse_file_open,_normalize_panel,_parse_settings_panel,_parse_terminal,_parse_window_move,_parse_settings,_parse_active_window,_capture_target,_parse_capture,_parse_focus,_normalize_app_name,_parse_app_open,_parse_path,_parse_open_prefix,_parse_fallback,parse_text
    _strip_quotes(value)
    _normalize_aliases(text)
    _parse_absolute_uri(raw;_lowered)
    _parse_http_url(raw;_lowered)
    _parse_ide_project(raw;_lowered)
    _parse_file_open(raw;_lowered)
    _normalize_panel(raw)
    _parse_settings_panel(raw;lowered)
    _parse_terminal(raw;_lowered)
    _parse_window_move(raw;_lowered)
    _parse_settings(_raw;lowered)
    _parse_active_window(raw;_lowered)
    _capture_target(lowered;title)
    _parse_capture(raw;lowered)
    _parse_focus(raw;_lowered)
    _normalize_app_name(name)
    _parse_app_open(raw;_lowered)
    _parse_path(raw;_lowered)
    _parse_open_prefix(raw;lowered)
    _parse_fallback(raw;_lowered)
    parse_text(text)
  src/nlp2uri/platform_detect.py:
    e: detect_platform
    detect_platform()
  src/nlp2uri/platforms/__init__.py:
  src/nlp2uri/platforms/base.py:
    e: slugify_app_name,UriExecutor
    UriExecutor: execute(1),_result(0),_dry(2),_run(2),_first_available(1),_open_with_browser(1),_parse_nlp2uri(1),_desktop_id_for_app(1)
    slugify_app_name(name)
  src/nlp2uri/platforms/linux.py:
    e: LinuxExecutor
    LinuxExecutor: execute(1),_open_generic(1),_open_settings(0),_open_app(1),_focus_app(1),_capture(2)
  src/nlp2uri/platforms/macos.py:
    e: MacOSExecutor
    MacOSExecutor: execute(1),_open(1),_open_app(1),_focus_app(1),_capture(2)
  src/nlp2uri/platforms/registry.py:
    e: get_executor
    get_executor(platform)
  src/nlp2uri/platforms/windows.py:
    e: WindowsExecutor
    WindowsExecutor: execute(1),_start(1),_open_app(1),_focus_app(1),_capture(2)
  src/nlp2uri/resolve.py:
    e: resolve_text,nlp2uri
    resolve_text(text)
    nlp2uri(prompt)
  src/nlp2uri/runtime.py:
    e: get_executor,execute_uri
    get_executor(platform)
    execute_uri(uri)
  src/nlp2uri/schemes/__init__.py:
  src/nlp2uri/schemes/build.py:
    e: build_uri,_build_navigate
    build_uri(intent)
    _build_navigate(intent)
  src/nlp2uri/schemes/desktop.py:
    e: build_capture,build_focus,build_app_open,build_move,build_terminal,build_settings
    build_capture(intent)
    build_focus(intent)
    build_app_open(intent)
    build_move(intent)
    build_terminal(intent)
    build_settings()
  src/nlp2uri/schemes/file.py:
    e: build_file
    build_file(intent)
  src/nlp2uri/schemes/http.py:
    e: build_http
    build_http(intent)
  src/nlp2uri/schemes/ide.py:
    e: build_ide
    build_ide(intent)
  src/nlp2uri/schemes/util.py:
    e: abstract_url,nlp2uri_url,normalize_path,file_uri,percent_encode_segment
    abstract_url(scheme;authority;path;params)
    nlp2uri_url(path;params)
    normalize_path(path)
    file_uri(path)
    percent_encode_segment(value)
  src/nlp2uri/service.py:
    e: NLP2URIService
    NLP2URIService: default(1),for_platform(2),_cfg(0),_host(0),from_prompt(1),resolve(1),compile(1),execute(1),handle_prompt(1),handle_uri(1),list_system_uris(1),resolve_system_map(2),list_getv_uris(0),resolve_getv(1),read_getv_var(1)  # Reusable facade: prompt → URI → compile → execute.
  src/nlp2uri/systemmap/__init__.py:
  src/nlp2uri/systemmap/compile.py:
    e: is_system_map_uri,_decode_segment,_backend_url,_worker_url,compile_system_map_uri,_compile_command,_compile_runtime,_compile_resource,_compile_artifact,_compile_access,_compile_metadata
    is_system_map_uri(uri)
    _decode_segment(value)
    _backend_url()
    _worker_url()
    compile_system_map_uri(uri;host)
    _compile_command(host;parsed)
    _compile_runtime(host;parsed)
    _compile_resource(host;parsed)
    _compile_artifact(host;parsed)
    _compile_access(host;parsed)
    _compile_metadata(host;scheme;parsed)
  src/nlp2uri/systemmap/context.py:
    e: load_ir_from_arguments,_coerce_ir
    load_ir_from_arguments(arguments)
    _coerce_ir(raw)
  src/nlp2uri/systemmap/encode.py:
    e: encode_segment,encode_path
    encode_segment(value)
    encode_path(value)
  src/nlp2uri/systemmap/fallback.py:
    e: resolve_prompt_with_fallback
    resolve_prompt_with_fallback(prompt;ir)
  src/nlp2uri/systemmap/getv_load.py:
    e: getv_available,getv_missing_message,getv_home,_parse_env_file,discover_profiles,load_profile_dict,mask_var_value,profile_manager
    getv_available()
    getv_missing_message()
    getv_home()
    _parse_env_file(path)
    discover_profiles(home)
    load_profile_dict(category;profile)
    mask_var_value(key;value)
    profile_manager(home)
  src/nlp2uri/systemmap/getv_uri.py:
    e: uri_for_getv_profile,uri_for_getv_var,is_getv_uri,_decode_segment,build_getv_uri_index,resolve_prompt_against_getv,compile_getv_uri,get_getv_var_value,ResolvedGetvUri
    ResolvedGetvUri: to_dict(0)
    uri_for_getv_profile(category;profile)
    uri_for_getv_var(category;profile;var_name)
    is_getv_uri(uri)
    _decode_segment(value)
    build_getv_uri_index()
    resolve_prompt_against_getv(prompt)
    compile_getv_uri(uri;host)
    get_getv_var_value(uri)
  src/nlp2uri/systemmap/index.py:
    e: _model_dump,_ir_field,_add_entry,build_uri_index,_get_id,_get_id_field,UriMapEntry,UriMap
    UriMapEntry: to_dict(0)  # One addressable entity in a SystemMap.
    UriMap: lookup(1),find_by_kind(1),find_command(1),to_dict(0)  # ``system_map_uri.v1`` — canonical addressing layer over Syst
    _model_dump(obj)
    _ir_field(ir;name;default)
    _add_entry(uri_map)
    build_uri_index(ir)
    _get_id(obj)
    _get_id_field(obj;key)
  src/nlp2uri/systemmap/load.py:
    e: env2llm_available,env2llm_missing_message,load_system_map_from_doql,load_system_map_from_example
    env2llm_available()
    env2llm_missing_message()
    load_system_map_from_doql(path)
    load_system_map_from_example(example_dir)
  src/nlp2uri/systemmap/resolve.py:
    e: _normalize_token,_name_variants,resolve_prompt_against_system_map,ResolvedSystemUri
    ResolvedSystemUri: to_dict(0)  # One NL match against the SystemMap.
    _normalize_token(text)
    _name_variants(name)
    resolve_prompt_against_system_map(prompt;ir)
  src/nlp2uri/systemmap/uri.py:
    e: _get,_get_list,uri_for_runtime,uri_for_command,uri_for_resource,uri_for_access,uri_for_artifact,uri_for_conversation,uri_for_process,uri_for_validation,uri_for_schedule,uri_for_generated_service,uri_for_environment
    _get(obj;key;default)
    _get_list(obj;key)
    uri_for_runtime(rt)
    uri_for_command(cmd)
    uri_for_resource(res)
    uri_for_access(grant)
    uri_for_artifact(art)
    uri_for_conversation()
    uri_for_process()
    uri_for_validation(val)
    uri_for_schedule(sched)
    uri_for_generated_service(svc)
    uri_for_environment(example_id)
  tests/conftest.py:
    e: isolated_config
    isolated_config(tmp_path;monkeypatch)
  tests/integration/test_xdg_handler.py:
    e: test_xdg_custom_scheme_handler
    test_xdg_custom_scheme_handler(tmp_path)
  tests/test_adapters.py:
    e: test_cli_adapter_plan,test_rest_adapter_plan,test_shell_adapter_export,test_mcp_adapter_tools,test_mcp_stdio_initialize,test_mcp_list_system_uris_inline_map,test_mcp_resolve_system_map_with_fallback,test_mcp_stdio_tools_call
    test_cli_adapter_plan()
    test_rest_adapter_plan()
    test_shell_adapter_export()
    test_mcp_adapter_tools()
    test_mcp_stdio_initialize()
    test_mcp_list_system_uris_inline_map()
    test_mcp_resolve_system_map_with_fallback()
    test_mcp_stdio_tools_call()
  tests/test_artifact_driver.py:
    e: test_resolve_artifact_path_with_example_dir,test_build_artifact_actions_read,test_build_artifact_actions_open,test_cqrs_artifact_driver_compile
    test_resolve_artifact_path_with_example_dir()
    test_build_artifact_actions_read()
    test_build_artifact_actions_open()
    test_cqrs_artifact_driver_compile()
  tests/test_cli.py:
    e: test_cli_resolve_json,test_cli_execute_dry_run
    test_cli_resolve_json(capsys)
    test_cli_execute_dry_run(capsys)
  tests/test_compile.py:
    e: test_compile_app_open_linux,test_compile_screenshot_macos,test_compile_ide_native_deep_link,test_compile_settings_windows
    test_compile_app_open_linux()
    test_compile_screenshot_macos()
    test_compile_ide_native_deep_link()
    test_compile_settings_windows()
  tests/test_config.py:
    e: test_auto_platform_detection,test_config_resolved_platform_auto,test_env_platform_override,test_save_and_load_yaml,test_ensure_config_writes_defaults
    test_auto_platform_detection()
    test_config_resolved_platform_auto()
    test_env_platform_override(monkeypatch)
    test_save_and_load_yaml(tmp_path;monkeypatch)
    test_ensure_config_writes_defaults(tmp_path;monkeypatch)
  tests/test_container_driver.py:
    e: test_parse_container_uri,test_container_status_compile,test_container_logs_compile,test_container_exec_requires_cmd,test_container_exec_compile,test_registry_lists_container_target
    test_parse_container_uri()
    test_container_status_compile()
    test_container_logs_compile()
    test_container_exec_requires_cmd()
    test_container_exec_compile()
    test_registry_lists_container_target()
  tests/test_cqrs_drivers.py:
    e: test_registry_loads_all_schemes,test_command_curl_driver_compile,test_getv_driver_compile,test_endpoint_driver_compile,test_endpoint_via_compile_uri_to_actions,test_app_delegate_driver,test_execute_dry_run_appends_events,test_probe_endpoint,test_runtime_curl_probe,test_driver_registry_get_builtin,test_service_curl_driver_maps_todomat_health,test_service_docker_driver_compose_ps,test_service_systemd_driver_unit
    test_registry_loads_all_schemes()
    test_command_curl_driver_compile()
    test_getv_driver_compile()
    test_endpoint_driver_compile()
    test_endpoint_via_compile_uri_to_actions()
    test_app_delegate_driver()
    test_execute_dry_run_appends_events()
    test_probe_endpoint()
    test_runtime_curl_probe()
    test_driver_registry_get_builtin()
    test_service_curl_driver_maps_todomat_health()
    test_service_docker_driver_compose_ps()
    test_service_systemd_driver_unit()
  tests/test_getv_uri.py:
    e: getv_home,test_uri_for_getv_var,test_build_getv_uri_index,test_resolve_prompt_env_key,test_get_var_masked,test_compile_get_var,test_compile_getv_via_top_level
    getv_home(tmp_path)
    test_uri_for_getv_var()
    test_build_getv_uri_index(getv_home)
    test_resolve_prompt_env_key(getv_home)
    test_get_var_masked(getv_home)
    test_compile_get_var()
    test_compile_getv_via_top_level()
  tests/test_http_event_store.py:
    e: test_http_event_store_posts_to_registry,_Handler
    _Handler: do_POST(0),log_message(1)
    test_http_event_store_posts_to_registry()
  tests/test_intents_phase2.py:
    e: test_phase2_resolve_linux,test_terminal_path_in_uri,test_window_move_screen_param,test_settings_panel_windows,test_settings_panel_macos,test_polish_cursor_project_regression,test_capture_window_edge_title,test_compile_window_move_dry_run_linux,test_compile_terminal_linux,test_compile_settings_panel_windows
    test_phase2_resolve_linux(text;expected_uri_prefix;expected_action)
    test_terminal_path_in_uri()
    test_window_move_screen_param()
    test_settings_panel_windows()
    test_settings_panel_macos()
    test_polish_cursor_project_regression()
    test_capture_window_edge_title()
    test_compile_window_move_dry_run_linux()
    test_compile_terminal_linux()
    test_compile_settings_panel_windows()
  tests/test_mcp.py:
    e: test_text_uri_list_mime,test_tool_resolve_desktop_action,test_mcp_handoff_includes_actions
    test_text_uri_list_mime()
    test_tool_resolve_desktop_action()
    test_mcp_handoff_includes_actions()
  tests/test_platforms.py:
    e: test_linux_dry_run_open_app,test_macos_dry_run_capture_screen,test_windows_dry_run_settings,test_linux_dry_run_file_uri
    test_linux_dry_run_open_app()
    test_macos_dry_run_capture_screen()
    test_windows_dry_run_settings()
    test_linux_dry_run_file_uri()
  tests/test_plugins.py:
    e: test_load_driver_plugins_includes_container,test_resolve_driver_class_builtin_priority,test_registry_plugin_drivers_property,test_entry_point_group_name
    test_load_driver_plugins_includes_container()
    test_resolve_driver_class_builtin_priority()
    test_registry_plugin_drivers_property()
    test_entry_point_group_name()
  tests/test_resolve.py:
    e: test_resolve_linux,test_polish_open_vscode_in_folder,test_polish_active_browser_screenshot,test_nlp2uri_returns_actions,test_parse_absolute_uri_passthrough,test_settings_windows,test_settings_macos,test_empty_input_raises
    test_resolve_linux(text;expected_uri_prefix;expected_action)
    test_polish_open_vscode_in_folder()
    test_polish_active_browser_screenshot()
    test_nlp2uri_returns_actions()
    test_parse_absolute_uri_passthrough()
    test_settings_windows()
    test_settings_macos()
    test_empty_input_raises()
  tests/test_resource_driver.py:
    e: test_resource_filesystem_probe,test_resource_smtp_probe,test_cqrs_resource_driver,test_resource_from_systemmap_index
    test_resource_filesystem_probe()
    test_resource_smtp_probe()
    test_cqrs_resource_driver()
    test_resource_from_systemmap_index()
  tests/test_rest_server.py:
    e: _post,test_rest_server_plan
    _post(url;payload)
    test_rest_server_plan()
  tests/test_schemas_registry.py:
    e: test_registry_loads,test_every_scheme_has_cqrs_tree,test_common_protos_exist,test_generated_mcp_tools_match_registry
    test_registry_loads()
    test_every_scheme_has_cqrs_tree()
    test_common_protos_exist()
    test_generated_mcp_tools_match_registry()
  tests/test_service.py:
    e: test_from_prompt,test_handle_prompt_dry_run,test_handle_uri
    test_from_prompt()
    test_handle_prompt_dry_run()
    test_handle_uri()
  tests/test_systemmap.py:
    e: _sample_ir,test_encode_segment_colon,test_uri_for_runtime_and_command,test_build_uri_index_covers_entities,test_resolve_prompt_command_name,test_resolve_prompt_command_spaced_name,test_resolve_prompt_runtime,test_is_system_map_uri,test_compile_command_handoff,test_compile_uri_to_actions_command_scheme,test_resolve_fallback_system_map_first,test_resolve_fallback_desktop_when_no_ir_match,test_resolve_fallback_desktop_without_ir,test_env2llm_roundtrip_index
    _sample_ir()
    test_encode_segment_colon()
    test_uri_for_runtime_and_command()
    test_build_uri_index_covers_entities()
    test_resolve_prompt_command_name()
    test_resolve_prompt_command_spaced_name()
    test_resolve_prompt_runtime()
    test_is_system_map_uri()
    test_compile_command_handoff()
    test_compile_uri_to_actions_command_scheme()
    test_resolve_fallback_system_map_first()
    test_resolve_fallback_desktop_when_no_ir_match()
    test_resolve_fallback_desktop_without_ir()
    test_env2llm_roundtrip_index(tmp_path)
```

### `project/logic.pl`

```prolog markpact:analysis path=project/logic.pl
% ── Project Metadata ─────────────────────────────────────
project_metadata('nlp2uri', '0.4.7', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 30, 'less').
project_file('examples/execute/dry-run/e2e.sh', 12, 'shell').
project_file('examples/execute/dry-run/main.py', 30, 'python').
project_file('examples/integrators/mcp-stdio/e2e.sh', 16, 'shell').
project_file('examples/integrators/rest-api/e2e.sh', 24, 'shell').
project_file('examples/integrators/shell-export/e2e.sh', 13, 'shell').
project_file('examples/mcp/tool-handoff/e2e.sh', 12, 'shell').
project_file('examples/mcp/tool-handoff/main.py', 28, 'python').
project_file('examples/resolve/new-intents/e2e.sh', 26, 'shell').
project_file('examples/resolve/nl-to-uri/e2e.sh', 12, 'shell').
project_file('examples/resolve/nl-to-uri/main.py', 47, 'python').
project_file('examples/run-e2e.sh', 41, 'shell').
project_file('project.sh', 59, 'shell').
project_file('schemas/codegen/export_driver_stubs.py', 98, 'python').
project_file('schemas/codegen/export_mcp_schemas.py', 54, 'python').
project_file('schemas/codegen/fix_proto_imports.py', 84, 'python').
project_file('schemas/codegen/generate.sh', 54, 'shell').
project_file('schemas/codegen/scaffold_scheme.py', 358, 'python').
project_file('scripts/install-editable.sh', 23, 'shell').
project_file('scripts/test-cqrs-smoke.sh', 56, 'shell').
project_file('scripts/test-live-registry.sh', 67, 'shell').
project_file('scripts/testapp-handler.sh', 7, 'shell').
project_file('src/nlp2uri/__init__.py', 29, 'python').
project_file('src/nlp2uri/adapters/__init__.py', 18, 'python').
project_file('src/nlp2uri/adapters/base.py', 60, 'python').
project_file('src/nlp2uri/adapters/cli.py', 40, 'python').
project_file('src/nlp2uri/adapters/mcp.py', 383, 'python').
project_file('src/nlp2uri/adapters/rest.py', 88, 'python').
project_file('src/nlp2uri/adapters/shell.py', 67, 'python').
project_file('src/nlp2uri/cli.py', 200, 'python').
project_file('src/nlp2uri/compile.py', 432, 'python').
project_file('src/nlp2uri/config.py', 231, 'python').
project_file('src/nlp2uri/cqrs/__init__.py', 9, 'python').
project_file('src/nlp2uri/cqrs/base.py', 98, 'python').
project_file('src/nlp2uri/cqrs/dispatcher.py', 118, 'python').
project_file('src/nlp2uri/cqrs/drivers/__init__.py', 30, 'python').
project_file('src/nlp2uri/cqrs/drivers/artifact_filesystem.py', 33, 'python').
project_file('src/nlp2uri/cqrs/drivers/command_curl.py', 40, 'python').
project_file('src/nlp2uri/cqrs/drivers/container_docker.py', 89, 'python').
project_file('src/nlp2uri/cqrs/drivers/delegate.py', 30, 'python').
project_file('src/nlp2uri/cqrs/drivers/endpoint_curl.py', 34, 'python').
project_file('src/nlp2uri/cqrs/drivers/getv_cli.py', 28, 'python').
project_file('src/nlp2uri/cqrs/drivers/resource_probe.py', 36, 'python').
project_file('src/nlp2uri/cqrs/drivers/runtime_curl.py', 35, 'python').
project_file('src/nlp2uri/cqrs/drivers/service_ops.py', 129, 'python').
project_file('src/nlp2uri/cqrs/event_store.py', 68, 'python').
project_file('src/nlp2uri/cqrs/http_store.py', 53, 'python').
project_file('src/nlp2uri/cqrs/plugins.py', 65, 'python').
project_file('src/nlp2uri/cqrs/registry.py', 98, 'python').
project_file('src/nlp2uri/host/__init__.py', 16, 'python').
project_file('src/nlp2uri/host/artifact.py', 95, 'python').
project_file('src/nlp2uri/host/endpoint.py', 35, 'python').
project_file('src/nlp2uri/host/resource.py', 70, 'python').
project_file('src/nlp2uri/integrators/__init__.py', 23, 'python').
project_file('src/nlp2uri/integrators/mcp_server.py', 129, 'python').
project_file('src/nlp2uri/integrators/rest_server.py', 91, 'python').
project_file('src/nlp2uri/mcp.py', 82, 'python').
project_file('src/nlp2uri/models.py', 181, 'python').
project_file('src/nlp2uri/parse_nl.py', 377, 'python').
project_file('src/nlp2uri/platform_detect.py', 19, 'python').
project_file('src/nlp2uri/platforms/__init__.py', 7, 'python').
project_file('src/nlp2uri/platforms/base.py', 131, 'python').
project_file('src/nlp2uri/platforms/linux.py', 146, 'python').
project_file('src/nlp2uri/platforms/macos.py', 95, 'python').
project_file('src/nlp2uri/platforms/registry.py', 25, 'python').
project_file('src/nlp2uri/platforms/windows.py', 95, 'python').
project_file('src/nlp2uri/resolve.py', 41, 'python').
project_file('src/nlp2uri/runtime.py', 93, 'python').
project_file('src/nlp2uri/schemes/__init__.py', 6, 'python').
project_file('src/nlp2uri/schemes/build.py', 65, 'python').
project_file('src/nlp2uri/schemes/desktop.py', 167, 'python').
project_file('src/nlp2uri/schemes/file.py', 26, 'python').
project_file('src/nlp2uri/schemes/http.py', 23, 'python').
project_file('src/nlp2uri/schemes/ide.py', 36, 'python').
project_file('src/nlp2uri/schemes/util.py', 48, 'python').
project_file('src/nlp2uri/service.py', 152, 'python').
project_file('src/nlp2uri/systemmap/__init__.py', 69, 'python').
project_file('src/nlp2uri/systemmap/compile.py', 180, 'python').
project_file('src/nlp2uri/systemmap/context.py', 48, 'python').
project_file('src/nlp2uri/systemmap/encode.py', 16, 'python').
project_file('src/nlp2uri/systemmap/fallback.py', 53, 'python').
project_file('src/nlp2uri/systemmap/getv_load.py', 98, 'python').
project_file('src/nlp2uri/systemmap/getv_uri.py', 226, 'python').
project_file('src/nlp2uri/systemmap/index.py', 268, 'python').
project_file('src/nlp2uri/systemmap/load.py', 47, 'python').
project_file('src/nlp2uri/systemmap/resolve.py', 123, 'python').
project_file('src/nlp2uri/systemmap/uri.py', 94, 'python').
project_file('tests/conftest.py', 18, 'python').
project_file('tests/integration/test_xdg_handler.py', 99, 'python').
project_file('tests/test_adapters.py', 120, 'python').
project_file('tests/test_artifact_driver.py', 57, 'python').
project_file('tests/test_cli.py', 31, 'python').
project_file('tests/test_compile.py', 34, 'python').
project_file('tests/test_config.py', 65, 'python').
project_file('tests/test_container_driver.py', 56, 'python').
project_file('tests/test_cqrs_drivers.py', 115, 'python').
project_file('tests/test_getv_uri.py', 74, 'python').
project_file('tests/test_http_event_store.py', 51, 'python').
project_file('tests/test_intents_phase2.py', 112, 'python').
project_file('tests/test_mcp.py', 25, 'python').
project_file('tests/test_platforms.py', 48, 'python').
project_file('tests/test_plugins.py', 33, 'python').
project_file('tests/test_resolve.py', 77, 'python').
project_file('tests/test_resource_driver.py', 44, 'python').
project_file('tests/test_rest_server.py', 48, 'python').
project_file('tests/test_schemas_registry.py', 53, 'python').
project_file('tests/test_service.py', 27, 'python').
project_file('tests/test_systemmap.py', 174, 'python').
project_file('tree.sh', 2, 'shell').

% ── Python Functions ─────────────────────────────────────
python_function('examples/execute/dry-run/main.py', 'main', 0, 3, 4).
python_function('examples/mcp/tool-handoff/main.py', 'main', 0, 2, 4).
python_function('examples/resolve/nl-to-uri/main.py', 'main', 0, 3, 4).
python_function('schemas/codegen/export_driver_stubs.py', 'main', 0, 11, 18).
python_function('schemas/codegen/export_mcp_schemas.py', 'tool_schema', 2, 1, 1).
python_function('schemas/codegen/export_mcp_schemas.py', 'main', 0, 4, 13).
python_function('schemas/codegen/fix_proto_imports.py', '_pascal', 1, 2, 4).
python_function('schemas/codegen/fix_proto_imports.py', 'fix_api', 2, 1, 3).
python_function('schemas/codegen/fix_proto_imports.py', 'fix_driver', 2, 1, 3).
python_function('schemas/codegen/fix_proto_imports.py', 'main', 0, 4, 7).
python_function('schemas/codegen/scaffold_scheme.py', '_pascal', 1, 2, 4).
python_function('schemas/codegen/scaffold_scheme.py', '_proto_package', 2, 2, 2).
python_function('schemas/codegen/scaffold_scheme.py', '_write', 2, 2, 3).
python_function('schemas/codegen/scaffold_scheme.py', 'aggregate_proto', 2, 2, 4).
python_function('schemas/codegen/scaffold_scheme.py', 'commands_proto', 2, 1, 3).
python_function('schemas/codegen/scaffold_scheme.py', 'events_proto', 2, 1, 3).
python_function('schemas/codegen/scaffold_scheme.py', 'queries_proto', 2, 1, 3).
python_function('schemas/codegen/scaffold_scheme.py', 'driver_proto', 2, 1, 5).
python_function('schemas/codegen/scaffold_scheme.py', 'api_proto', 2, 1, 3).
python_function('schemas/codegen/scaffold_scheme.py', 'openapi_yaml', 2, 1, 2).
python_function('schemas/codegen/scaffold_scheme.py', 'readme_md', 2, 2, 4).
python_function('schemas/codegen/scaffold_scheme.py', 'scaffold_scheme', 2, 4, 12).
python_function('schemas/codegen/scaffold_scheme.py', 'main', 0, 4, 11).
python_function('src/nlp2uri/cli.py', '_add_common_args', 1, 3, 1).
python_function('src/nlp2uri/cli.py', '_build_parser', 0, 1, 5).
python_function('src/nlp2uri/cli.py', '_platform', 1, 2, 1).
python_function('src/nlp2uri/cli.py', '_emit', 1, 3, 4).
python_function('src/nlp2uri/cli.py', '_request_from_args', 1, 3, 4).
python_function('src/nlp2uri/cli.py', '_with_platform', 1, 2, 2).
python_function('src/nlp2uri/cli.py', '_run_config', 1, 3, 10).
python_function('src/nlp2uri/cli.py', '_run_shell', 1, 5, 9).
python_function('src/nlp2uri/cli.py', '_run_adapter_command', 1, 4, 8).
python_function('src/nlp2uri/cli.py', '_run_execute', 1, 5, 10).
python_function('src/nlp2uri/cli.py', 'main', 1, 4, 7).
python_function('src/nlp2uri/compile.py', 'compile_uri_to_actions', 2, 13, 17).
python_function('src/nlp2uri/compile.py', '_query_params', 1, 3, 3).
python_function('src/nlp2uri/compile.py', '_first_available', 1, 3, 1).
python_function('src/nlp2uri/compile.py', '_open_uri', 2, 5, 2).
python_function('src/nlp2uri/compile.py', '_compile_app', 5, 16, 15).
python_function('src/nlp2uri/compile.py', '_compile_settings_panel', 2, 5, 4).
python_function('src/nlp2uri/compile.py', '_compile_terminal', 2, 16, 3).
python_function('src/nlp2uri/compile.py', '_compile_settings', 1, 5, 3).
python_function('src/nlp2uri/compile.py', '_compile_launch_app', 2, 7, 3).
python_function('src/nlp2uri/compile.py', '_capture_outfile', 1, 1, 3).
python_function('src/nlp2uri/compile.py', '_linux_screen_capture', 2, 3, 2).
python_function('src/nlp2uri/compile.py', '_macos_screen_capture', 2, 1, 1).
python_function('src/nlp2uri/compile.py', '_windows_screen_capture', 1, 1, 1).
python_function('src/nlp2uri/compile.py', '_compile_screen_capture', 2, 4, 4).
python_function('src/nlp2uri/compile.py', '_linux_window_capture', 2, 4, 2).
python_function('src/nlp2uri/compile.py', '_macos_window_capture', 2, 2, 1).
python_function('src/nlp2uri/compile.py', '_windows_window_capture', 2, 2, 1).
python_function('src/nlp2uri/compile.py', '_compile_window_capture', 3, 4, 5).
python_function('src/nlp2uri/compile.py', '_compile_screenshot', 4, 4, 4).
python_function('src/nlp2uri/compile.py', '_compile_window_move', 2, 7, 4).
python_function('src/nlp2uri/compile.py', '_compile_window', 4, 11, 6).
python_function('src/nlp2uri/compile.py', '_compile_legacy_nlp2uri', 2, 7, 12).
python_function('src/nlp2uri/compile.py', '_desktop_id_for_app', 1, 7, 6).
python_function('src/nlp2uri/config.py', 'payload_keys', 0, 1, 0).
python_function('src/nlp2uri/config.py', '_yaml_scalar', 1, 8, 4).
python_function('src/nlp2uri/config.py', '_parse_scalar', 1, 8, 3).
python_function('src/nlp2uri/config.py', '_parse_simple_yaml', 1, 5, 5).
python_function('src/nlp2uri/config.py', 'config_search_paths', 0, 5, 7).
python_function('src/nlp2uri/config.py', 'find_config_path', 0, 3, 2).
python_function('src/nlp2uri/config.py', 'default_config', 0, 1, 3).
python_function('src/nlp2uri/config.py', '_load_from_path', 1, 6, 10).
python_function('src/nlp2uri/config.py', 'load_config', 0, 4, 3).
python_function('src/nlp2uri/config.py', 'save_config', 2, 4, 8).
python_function('src/nlp2uri/config.py', 'ensure_config', 1, 4, 6).
python_function('src/nlp2uri/config.py', 'get_effective_platform', 1, 2, 2).
python_function('src/nlp2uri/config.py', 'reset_config_cache', 0, 1, 0).
python_function('src/nlp2uri/cqrs/drivers/container_docker.py', 'parse_container_uri', 1, 8, 6).
python_function('src/nlp2uri/cqrs/drivers/service_ops.py', 'parse_service_name', 1, 4, 3).
python_function('src/nlp2uri/cqrs/drivers/service_ops.py', '_compose_dir', 1, 3, 3).
python_function('src/nlp2uri/cqrs/plugins.py', '_parse_entry_point_name', 1, 4, 2).
python_function('src/nlp2uri/cqrs/plugins.py', 'load_driver_plugins', 0, 7, 8).
python_function('src/nlp2uri/cqrs/plugins.py', 'resolve_driver_class', 3, 2, 2).
python_function('src/nlp2uri/cqrs/registry.py', 'default_registry', 0, 1, 2).
python_function('src/nlp2uri/host/artifact.py', 'is_artifact_uri', 1, 1, 2).
python_function('src/nlp2uri/host/artifact.py', '_decode', 1, 2, 1).
python_function('src/nlp2uri/host/artifact.py', 'resolve_artifact_path', 1, 12, 12).
python_function('src/nlp2uri/host/artifact.py', 'build_artifact_actions', 2, 13, 9).
python_function('src/nlp2uri/host/endpoint.py', 'is_endpoint_uri', 1, 1, 2).
python_function('src/nlp2uri/host/endpoint.py', 'build_endpoint_url', 1, 8, 7).
python_function('src/nlp2uri/host/endpoint.py', 'build_endpoint_actions', 2, 1, 2).
python_function('src/nlp2uri/host/resource.py', 'is_resource_uri', 1, 1, 2).
python_function('src/nlp2uri/host/resource.py', '_decode', 1, 2, 1).
python_function('src/nlp2uri/host/resource.py', '_filesystem_probe_path', 1, 5, 6).
python_function('src/nlp2uri/host/resource.py', 'build_resource_actions', 2, 14, 13).
python_function('src/nlp2uri/integrators/__init__.py', '__getattr__', 1, 3, 1).
python_function('src/nlp2uri/integrators/mcp_server.py', '_jsonrpc_response', 2, 1, 0).
python_function('src/nlp2uri/integrators/mcp_server.py', '_jsonrpc_error', 4, 2, 0).
python_function('src/nlp2uri/integrators/mcp_server.py', '_write_json', 1, 1, 3).
python_function('src/nlp2uri/integrators/mcp_server.py', '_log', 1, 1, 1).
python_function('src/nlp2uri/integrators/mcp_server.py', '_handle_initialize', 1, 1, 0).
python_function('src/nlp2uri/integrators/mcp_server.py', '_handle_tools_list', 1, 1, 0).
python_function('src/nlp2uri/integrators/mcp_server.py', '_handle_tools_call', 1, 6, 5).
python_function('src/nlp2uri/integrators/mcp_server.py', 'handle_message', 1, 8, 6).
python_function('src/nlp2uri/integrators/mcp_server.py', 'run_stdio', 0, 6, 10).
python_function('src/nlp2uri/integrators/mcp_server.py', 'main', 1, 1, 3).
python_function('src/nlp2uri/integrators/rest_server.py', 'run_server', 2, 2, 7).
python_function('src/nlp2uri/integrators/rest_server.py', 'main', 1, 1, 4).
python_function('src/nlp2uri/mcp.py', 'text_uri_list', 1, 2, 1).
python_function('src/nlp2uri/mcp.py', 'ui_resource', 1, 1, 0).
python_function('src/nlp2uri/mcp.py', 'tool_resolve_desktop_action', 1, 2, 2).
python_function('src/nlp2uri/mcp.py', 'tool_execute_desktop_uri', 1, 2, 2).
python_function('src/nlp2uri/mcp.py', 'mcp_handoff_payload', 1, 2, 2).
python_function('src/nlp2uri/parse_nl.py', '_strip_quotes', 1, 1, 1).
python_function('src/nlp2uri/parse_nl.py', '_normalize_aliases', 1, 2, 2).
python_function('src/nlp2uri/parse_nl.py', '_parse_absolute_uri', 2, 2, 3).
python_function('src/nlp2uri/parse_nl.py', '_parse_http_url', 2, 2, 3).
python_function('src/nlp2uri/parse_nl.py', '_parse_ide_project', 2, 2, 5).
python_function('src/nlp2uri/parse_nl.py', '_parse_file_open', 2, 2, 4).
python_function('src/nlp2uri/parse_nl.py', '_normalize_panel', 1, 1, 3).
python_function('src/nlp2uri/parse_nl.py', '_parse_settings_panel', 2, 6, 4).
python_function('src/nlp2uri/parse_nl.py', '_parse_terminal', 2, 3, 4).
python_function('src/nlp2uri/parse_nl.py', '_parse_window_move', 2, 3, 3).
python_function('src/nlp2uri/parse_nl.py', '_parse_settings', 2, 2, 2).
python_function('src/nlp2uri/parse_nl.py', '_parse_active_window', 2, 2, 2).
python_function('src/nlp2uri/parse_nl.py', '_capture_target', 2, 4, 1).
python_function('src/nlp2uri/parse_nl.py', '_parse_capture', 2, 6, 8).
python_function('src/nlp2uri/parse_nl.py', '_parse_focus', 2, 2, 4).
python_function('src/nlp2uri/parse_nl.py', '_normalize_app_name', 1, 2, 1).
python_function('src/nlp2uri/parse_nl.py', '_parse_app_open', 2, 2, 4).
python_function('src/nlp2uri/parse_nl.py', '_parse_path', 2, 2, 4).
python_function('src/nlp2uri/parse_nl.py', '_parse_open_prefix', 2, 5, 6).
python_function('src/nlp2uri/parse_nl.py', '_parse_fallback', 2, 1, 1).
python_function('src/nlp2uri/parse_nl.py', 'parse_text', 1, 5, 6).
python_function('src/nlp2uri/platform_detect.py', 'detect_platform', 0, 5, 1).
python_function('src/nlp2uri/platforms/base.py', 'slugify_app_name', 1, 1, 3).
python_function('src/nlp2uri/platforms/registry.py', 'get_executor', 1, 3, 4).
python_function('src/nlp2uri/resolve.py', 'resolve_text', 1, 2, 3).
python_function('src/nlp2uri/resolve.py', 'nlp2uri', 1, 4, 8).
python_function('src/nlp2uri/runtime.py', 'get_executor', 1, 1, 1).
python_function('src/nlp2uri/runtime.py', 'execute_uri', 1, 9, 9).
python_function('src/nlp2uri/schemes/build.py', 'build_uri', 1, 13, 12).
python_function('src/nlp2uri/schemes/build.py', '_build_navigate', 1, 4, 5).
python_function('src/nlp2uri/schemes/desktop.py', 'build_capture', 1, 5, 5).
python_function('src/nlp2uri/schemes/desktop.py', 'build_focus', 1, 1, 4).
python_function('src/nlp2uri/schemes/desktop.py', 'build_app_open', 1, 3, 4).
python_function('src/nlp2uri/schemes/desktop.py', 'build_move', 1, 1, 4).
python_function('src/nlp2uri/schemes/desktop.py', 'build_terminal', 1, 2, 4).
python_function('src/nlp2uri/schemes/desktop.py', 'build_settings', 0, 6, 4).
python_function('src/nlp2uri/schemes/file.py', 'build_file', 1, 3, 6).
python_function('src/nlp2uri/schemes/http.py', 'build_http', 1, 4, 3).
python_function('src/nlp2uri/schemes/ide.py', 'build_ide', 1, 4, 8).
python_function('src/nlp2uri/schemes/util.py', 'abstract_url', 4, 9, 5).
python_function('src/nlp2uri/schemes/util.py', 'nlp2uri_url', 2, 5, 3).
python_function('src/nlp2uri/schemes/util.py', 'normalize_path', 1, 2, 4).
python_function('src/nlp2uri/schemes/util.py', 'file_uri', 1, 1, 3).
python_function('src/nlp2uri/schemes/util.py', 'percent_encode_segment', 1, 1, 1).
python_function('src/nlp2uri/systemmap/compile.py', 'is_system_map_uri', 1, 1, 2).
python_function('src/nlp2uri/systemmap/compile.py', '_decode_segment', 1, 2, 1).
python_function('src/nlp2uri/systemmap/compile.py', '_backend_url', 0, 1, 2).
python_function('src/nlp2uri/systemmap/compile.py', '_worker_url', 0, 1, 2).
python_function('src/nlp2uri/systemmap/compile.py', 'compile_system_map_uri', 2, 8, 9).
python_function('src/nlp2uri/systemmap/compile.py', '_compile_command', 2, 4, 7).
python_function('src/nlp2uri/systemmap/compile.py', '_compile_runtime', 2, 12, 10).
python_function('src/nlp2uri/systemmap/compile.py', '_compile_resource', 2, 2, 1).
python_function('src/nlp2uri/systemmap/compile.py', '_compile_artifact', 2, 2, 1).
python_function('src/nlp2uri/systemmap/compile.py', '_compile_access', 2, 2, 4).
python_function('src/nlp2uri/systemmap/compile.py', '_compile_metadata', 3, 2, 3).
python_function('src/nlp2uri/systemmap/context.py', 'load_ir_from_arguments', 1, 8, 11).
python_function('src/nlp2uri/systemmap/context.py', '_coerce_ir', 1, 2, 2).
python_function('src/nlp2uri/systemmap/encode.py', 'encode_segment', 1, 1, 1).
python_function('src/nlp2uri/systemmap/encode.py', 'encode_path', 1, 1, 2).
python_function('src/nlp2uri/systemmap/fallback.py', 'resolve_prompt_with_fallback', 2, 6, 4).
python_function('src/nlp2uri/systemmap/getv_load.py', 'getv_available', 0, 1, 0).
python_function('src/nlp2uri/systemmap/getv_load.py', 'getv_missing_message', 0, 2, 0).
python_function('src/nlp2uri/systemmap/getv_load.py', 'getv_home', 0, 1, 4).
python_function('src/nlp2uri/systemmap/getv_load.py', '_parse_env_file', 1, 8, 6).
python_function('src/nlp2uri/systemmap/getv_load.py', 'discover_profiles', 1, 8, 6).
python_function('src/nlp2uri/systemmap/getv_load.py', 'load_profile_dict', 2, 4, 4).
python_function('src/nlp2uri/systemmap/getv_load.py', 'mask_var_value', 2, 2, 2).
python_function('src/nlp2uri/systemmap/getv_load.py', 'profile_manager', 1, 4, 4).
python_function('src/nlp2uri/systemmap/getv_uri.py', 'uri_for_getv_profile', 2, 1, 1).
python_function('src/nlp2uri/systemmap/getv_uri.py', 'uri_for_getv_var', 3, 1, 1).
python_function('src/nlp2uri/systemmap/getv_uri.py', 'is_getv_uri', 1, 1, 2).
python_function('src/nlp2uri/systemmap/getv_uri.py', '_decode_segment', 1, 2, 1).
python_function('src/nlp2uri/systemmap/getv_uri.py', 'build_getv_uri_index', 0, 6, 19).
python_function('src/nlp2uri/systemmap/getv_uri.py', 'resolve_prompt_against_getv', 1, 13, 10).
python_function('src/nlp2uri/systemmap/getv_uri.py', 'compile_getv_uri', 2, 14, 11).
python_function('src/nlp2uri/systemmap/getv_uri.py', 'get_getv_var_value', 1, 9, 8).
python_function('src/nlp2uri/systemmap/index.py', '_model_dump', 1, 3, 6).
python_function('src/nlp2uri/systemmap/index.py', '_ir_field', 3, 2, 3).
python_function('src/nlp2uri/systemmap/index.py', '_add_entry', 1, 3, 4).
python_function('src/nlp2uri/systemmap/index.py', 'build_uri_index', 1, 31, 20).
python_function('src/nlp2uri/systemmap/index.py', '_get_id', 1, 1, 1).
python_function('src/nlp2uri/systemmap/index.py', '_get_id_field', 2, 4, 4).
python_function('src/nlp2uri/systemmap/load.py', 'env2llm_available', 0, 1, 0).
python_function('src/nlp2uri/systemmap/load.py', 'env2llm_missing_message', 0, 2, 0).
python_function('src/nlp2uri/systemmap/load.py', 'load_system_map_from_doql', 1, 2, 3).
python_function('src/nlp2uri/systemmap/load.py', 'load_system_map_from_example', 1, 3, 3).
python_function('src/nlp2uri/systemmap/resolve.py', '_normalize_token', 1, 1, 3).
python_function('src/nlp2uri/systemmap/resolve.py', '_name_variants', 1, 3, 2).
python_function('src/nlp2uri/systemmap/resolve.py', 'resolve_prompt_against_system_map', 2, 26, 10).
python_function('src/nlp2uri/systemmap/uri.py', '_get', 3, 4, 4).
python_function('src/nlp2uri/systemmap/uri.py', '_get_list', 2, 5, 4).
python_function('src/nlp2uri/systemmap/uri.py', 'uri_for_runtime', 1, 1, 2).
python_function('src/nlp2uri/systemmap/uri.py', 'uri_for_command', 1, 3, 2).
python_function('src/nlp2uri/systemmap/uri.py', 'uri_for_resource', 1, 2, 2).
python_function('src/nlp2uri/systemmap/uri.py', 'uri_for_access', 1, 4, 4).
python_function('src/nlp2uri/systemmap/uri.py', 'uri_for_artifact', 1, 1, 4).
python_function('src/nlp2uri/systemmap/uri.py', 'uri_for_conversation', 0, 1, 1).
python_function('src/nlp2uri/systemmap/uri.py', 'uri_for_process', 0, 1, 1).
python_function('src/nlp2uri/systemmap/uri.py', 'uri_for_validation', 1, 1, 2).
python_function('src/nlp2uri/systemmap/uri.py', 'uri_for_schedule', 1, 1, 2).
python_function('src/nlp2uri/systemmap/uri.py', 'uri_for_generated_service', 1, 1, 2).
python_function('src/nlp2uri/systemmap/uri.py', 'uri_for_environment', 1, 1, 1).
python_function('tests/conftest.py', 'isolated_config', 2, 1, 6).
python_function('tests/integration/test_xdg_handler.py', 'test_xdg_custom_scheme_handler', 1, 7, 12).
python_function('tests/test_adapters.py', 'test_cli_adapter_plan', 0, 3, 4).
python_function('tests/test_adapters.py', 'test_rest_adapter_plan', 0, 3, 2).
python_function('tests/test_adapters.py', 'test_shell_adapter_export', 0, 4, 3).
python_function('tests/test_adapters.py', 'test_mcp_adapter_tools', 0, 4, 3).
python_function('tests/test_adapters.py', 'test_mcp_stdio_initialize', 0, 3, 2).
python_function('tests/test_adapters.py', 'test_mcp_list_system_uris_inline_map', 0, 4, 2).
python_function('tests/test_adapters.py', 'test_mcp_resolve_system_map_with_fallback', 0, 4, 2).
python_function('tests/test_adapters.py', 'test_mcp_stdio_tools_call', 0, 3, 2).
python_function('tests/test_artifact_driver.py', 'test_resolve_artifact_path_with_example_dir', 0, 2, 7).
python_function('tests/test_artifact_driver.py', 'test_build_artifact_actions_read', 0, 3, 5).
python_function('tests/test_artifact_driver.py', 'test_build_artifact_actions_open', 0, 2, 6).
python_function('tests/test_artifact_driver.py', 'test_cqrs_artifact_driver_compile', 0, 3, 6).
python_function('tests/test_cli.py', 'test_cli_resolve_json', 1, 3, 4).
python_function('tests/test_cli.py', 'test_cli_execute_dry_run', 1, 3, 3).
python_function('tests/test_compile.py', 'test_compile_app_open_linux', 0, 3, 2).
python_function('tests/test_compile.py', 'test_compile_screenshot_macos', 0, 2, 1).
python_function('tests/test_compile.py', 'test_compile_ide_native_deep_link', 0, 2, 3).
python_function('tests/test_compile.py', 'test_compile_settings_windows', 0, 2, 1).
python_function('tests/test_config.py', 'test_auto_platform_detection', 0, 2, 2).
python_function('tests/test_config.py', 'test_config_resolved_platform_auto', 0, 3, 2).
python_function('tests/test_config.py', 'test_env_platform_override', 1, 2, 3).
python_function('tests/test_config.py', 'test_save_and_load_yaml', 2, 4, 8).
python_function('tests/test_config.py', 'test_ensure_config_writes_defaults', 2, 4, 6).
python_function('tests/test_container_driver.py', 'test_parse_container_uri', 0, 5, 1).
python_function('tests/test_container_driver.py', 'test_container_status_compile', 0, 4, 2).
python_function('tests/test_container_driver.py', 'test_container_logs_compile', 0, 3, 2).
python_function('tests/test_container_driver.py', 'test_container_exec_requires_cmd', 0, 3, 3).
python_function('tests/test_container_driver.py', 'test_container_exec_compile', 0, 3, 2).
python_function('tests/test_container_driver.py', 'test_registry_lists_container_target', 0, 3, 3).
python_function('tests/test_cqrs_drivers.py', 'test_registry_loads_all_schemes', 0, 4, 3).
python_function('tests/test_cqrs_drivers.py', 'test_command_curl_driver_compile', 0, 5, 2).
python_function('tests/test_cqrs_drivers.py', 'test_getv_driver_compile', 0, 3, 3).
python_function('tests/test_cqrs_drivers.py', 'test_endpoint_driver_compile', 0, 4, 3).
python_function('tests/test_cqrs_drivers.py', 'test_endpoint_via_compile_uri_to_actions', 0, 3, 1).
python_function('tests/test_cqrs_drivers.py', 'test_app_delegate_driver', 0, 3, 5).
python_function('tests/test_cqrs_drivers.py', 'test_execute_dry_run_appends_events', 0, 5, 5).
python_function('tests/test_cqrs_drivers.py', 'test_probe_endpoint', 0, 3, 2).
python_function('tests/test_cqrs_drivers.py', 'test_runtime_curl_probe', 0, 2, 2).
python_function('tests/test_cqrs_drivers.py', 'test_driver_registry_get_builtin', 0, 3, 3).
python_function('tests/test_cqrs_drivers.py', 'test_service_curl_driver_maps_todomat_health', 0, 4, 2).
python_function('tests/test_cqrs_drivers.py', 'test_service_docker_driver_compose_ps', 0, 4, 2).
python_function('tests/test_cqrs_drivers.py', 'test_service_systemd_driver_unit', 0, 3, 2).
python_function('tests/test_getv_uri.py', 'getv_home', 1, 1, 2).
python_function('tests/test_getv_uri.py', 'test_uri_for_getv_var', 0, 3, 2).
python_function('tests/test_getv_uri.py', 'test_build_getv_uri_index', 1, 5, 5).
python_function('tests/test_getv_uri.py', 'test_resolve_prompt_env_key', 1, 3, 3).
python_function('tests/test_getv_uri.py', 'test_get_var_masked', 1, 4, 2).
python_function('tests/test_getv_uri.py', 'test_compile_get_var', 0, 3, 2).
python_function('tests/test_getv_uri.py', 'test_compile_getv_via_top_level', 0, 2, 2).
python_function('tests/test_http_event_store.py', 'test_http_event_store_posts_to_registry', 0, 4, 9).
python_function('tests/test_intents_phase2.py', 'test_phase2_resolve_linux', 3, 3, 3).
python_function('tests/test_intents_phase2.py', 'test_terminal_path_in_uri', 0, 2, 1).
python_function('tests/test_intents_phase2.py', 'test_window_move_screen_param', 0, 3, 1).
python_function('tests/test_intents_phase2.py', 'test_settings_panel_windows', 0, 2, 1).
python_function('tests/test_intents_phase2.py', 'test_settings_panel_macos', 0, 2, 2).
python_function('tests/test_intents_phase2.py', 'test_polish_cursor_project_regression', 0, 3, 2).
python_function('tests/test_intents_phase2.py', 'test_capture_window_edge_title', 0, 3, 2).
python_function('tests/test_intents_phase2.py', 'test_compile_window_move_dry_run_linux', 0, 3, 2).
python_function('tests/test_intents_phase2.py', 'test_compile_terminal_linux', 0, 3, 2).
python_function('tests/test_intents_phase2.py', 'test_compile_settings_panel_windows', 0, 2, 1).
python_function('tests/test_mcp.py', 'test_text_uri_list_mime', 0, 3, 1).
python_function('tests/test_mcp.py', 'test_tool_resolve_desktop_action', 0, 3, 2).
python_function('tests/test_mcp.py', 'test_mcp_handoff_includes_actions', 0, 3, 1).
python_function('tests/test_platforms.py', 'test_linux_dry_run_open_app', 0, 4, 3).
python_function('tests/test_platforms.py', 'test_macos_dry_run_capture_screen', 0, 3, 1).
python_function('tests/test_platforms.py', 'test_windows_dry_run_settings', 0, 3, 2).
python_function('tests/test_platforms.py', 'test_linux_dry_run_file_uri', 0, 3, 1).
python_function('tests/test_plugins.py', 'test_load_driver_plugins_includes_container', 0, 4, 3).
python_function('tests/test_plugins.py', 'test_resolve_driver_class_builtin_priority', 0, 2, 1).
python_function('tests/test_plugins.py', 'test_registry_plugin_drivers_property', 0, 3, 3).
python_function('tests/test_plugins.py', 'test_entry_point_group_name', 0, 2, 0).
python_function('tests/test_resolve.py', 'test_resolve_linux', 3, 3, 3).
python_function('tests/test_resolve.py', 'test_polish_open_vscode_in_folder', 0, 3, 2).
python_function('tests/test_resolve.py', 'test_polish_active_browser_screenshot', 0, 3, 2).
python_function('tests/test_resolve.py', 'test_nlp2uri_returns_actions', 0, 5, 2).
python_function('tests/test_resolve.py', 'test_parse_absolute_uri_passthrough', 0, 3, 2).
python_function('tests/test_resolve.py', 'test_settings_windows', 0, 2, 1).
python_function('tests/test_resolve.py', 'test_settings_macos', 0, 2, 1).
python_function('tests/test_resolve.py', 'test_empty_input_raises', 0, 1, 2).
python_function('tests/test_resource_driver.py', 'test_resource_filesystem_probe', 0, 3, 1).
python_function('tests/test_resource_driver.py', 'test_resource_smtp_probe', 0, 2, 1).
python_function('tests/test_resource_driver.py', 'test_cqrs_resource_driver', 0, 3, 3).
python_function('tests/test_resource_driver.py', 'test_resource_from_systemmap_index', 0, 2, 3).
python_function('tests/test_rest_server.py', '_post', 2, 1, 7).
python_function('tests/test_rest_server.py', 'test_rest_server_plan', 0, 7, 8).
python_function('tests/test_schemas_registry.py', 'test_registry_loads', 0, 3, 3).
python_function('tests/test_schemas_registry.py', 'test_every_scheme_has_cqrs_tree', 0, 4, 5).
python_function('tests/test_schemas_registry.py', 'test_common_protos_exist', 0, 3, 1).
python_function('tests/test_schemas_registry.py', 'test_generated_mcp_tools_match_registry', 0, 3, 7).
python_function('tests/test_service.py', 'test_from_prompt', 0, 3, 3).
python_function('tests/test_service.py', 'test_handle_prompt_dry_run', 0, 3, 3).
python_function('tests/test_service.py', 'test_handle_uri', 0, 2, 2).
python_function('tests/test_systemmap.py', '_sample_ir', 0, 1, 0).
python_function('tests/test_systemmap.py', 'test_encode_segment_colon', 0, 2, 1).
python_function('tests/test_systemmap.py', 'test_uri_for_runtime_and_command', 0, 3, 3).
python_function('tests/test_systemmap.py', 'test_build_uri_index_covers_entities', 0, 8, 5).
python_function('tests/test_systemmap.py', 'test_resolve_prompt_command_name', 0, 5, 2).
python_function('tests/test_systemmap.py', 'test_resolve_prompt_command_spaced_name', 0, 3, 2).
python_function('tests/test_systemmap.py', 'test_resolve_prompt_runtime', 0, 2, 3).
python_function('tests/test_systemmap.py', 'test_is_system_map_uri', 0, 3, 1).
python_function('tests/test_systemmap.py', 'test_compile_command_handoff', 0, 5, 6).
python_function('tests/test_systemmap.py', 'test_compile_uri_to_actions_command_scheme', 0, 3, 3).
python_function('tests/test_systemmap.py', 'test_resolve_fallback_system_map_first', 0, 3, 2).
python_function('tests/test_systemmap.py', 'test_resolve_fallback_desktop_when_no_ir_match', 0, 3, 3).
python_function('tests/test_systemmap.py', 'test_resolve_fallback_desktop_without_ir', 0, 3, 2).
python_function('tests/test_systemmap.py', 'test_env2llm_roundtrip_index', 1, 2, 9).

% ── Python Classes ───────────────────────────────────────
python_class('src/nlp2uri/adapters/base.py', 'AdapterRequest').
python_class('src/nlp2uri/adapters/base.py', 'AdapterResponse').
python_method('AdapterResponse', 'to_dict', 0, 2, 1).
python_class('src/nlp2uri/adapters/base.py', 'BaseAdapter').
python_method('BaseAdapter', '__init__', 1, 2, 2).
python_method('BaseAdapter', 'with_platform', 1, 2, 2).
python_method('BaseAdapter', 'handle', 1, 1, 0).
python_method('BaseAdapter', '_service_for', 1, 2, 1).
python_class('src/nlp2uri/adapters/cli.py', 'CliAdapter').
python_method('CliAdapter', 'handle', 1, 10, 11).
python_class('src/nlp2uri/adapters/mcp.py', 'McpAdapter').
python_method('McpAdapter', 'handle', 1, 1, 2).
python_method('McpAdapter', 'call_tool', 2, 2, 5).
python_method('McpAdapter', 'tool_dispatch', 0, 1, 0).
python_method('McpAdapter', '_args_from_request', 1, 6, 1).
python_method('McpAdapter', '_args_to_request', 2, 4, 5).
python_method('McpAdapter', 'mcp_content', 1, 3, 3).
python_method('McpAdapter', '_tool_plan', 1, 1, 5).
python_method('McpAdapter', '_tool_resolve', 1, 1, 5).
python_method('McpAdapter', '_tool_compile', 1, 2, 5).
python_method('McpAdapter', '_tool_execute', 1, 2, 6).
python_method('McpAdapter', '_tool_handle', 1, 2, 6).
python_method('McpAdapter', '_tool_list_system_uris', 1, 2, 6).
python_method('McpAdapter', '_tool_resolve_system_map', 1, 3, 8).
python_method('McpAdapter', '_tool_list_getv_uris', 1, 1, 5).
python_method('McpAdapter', '_tool_resolve_getv', 1, 2, 5).
python_method('McpAdapter', '_tool_get_getv_var', 1, 2, 7).
python_method('McpAdapter', '_tool_cqrs_compile', 1, 5, 6).
python_method('McpAdapter', '_tool_cqrs_execute', 1, 5, 7).
python_class('src/nlp2uri/adapters/rest.py', 'RestAdapter').
python_method('RestAdapter', 'handle', 1, 1, 1).
python_method('RestAdapter', 'dispatch', 2, 14, 13).
python_method('RestAdapter', 'body_to_request', 1, 4, 5).
python_method('RestAdapter', 'match_route', 2, 3, 3).
python_class('src/nlp2uri/adapters/shell.py', 'ShellAdapter').
python_method('ShellAdapter', 'handle', 1, 11, 10).
python_method('ShellAdapter', '_export_script', 0, 1, 2).
python_class('src/nlp2uri/config.py', 'NLP2URIConfig').
python_method('NLP2URIConfig', 'resolved_platform', 0, 4, 5).
python_method('NLP2URIConfig', 'apply_runtime_env', 0, 2, 1).
python_method('NLP2URIConfig', 'to_dict', 0, 2, 2).
python_method('NLP2URIConfig', 'to_yaml', 0, 6, 7).
python_class('src/nlp2uri/cqrs/base.py', 'DriverCapabilities').
python_class('src/nlp2uri/cqrs/base.py', 'CompileResult').
python_class('src/nlp2uri/cqrs/base.py', 'ExecuteResult').
python_class('src/nlp2uri/cqrs/base.py', 'ProbeResult').
python_class('src/nlp2uri/cqrs/base.py', 'UriDriver').
python_method('UriDriver', 'capabilities', 0, 2, 3).
python_method('UriDriver', 'compile', 1, 1, 0).
python_method('UriDriver', 'execute', 2, 8, 5).
python_method('UriDriver', 'probe', 1, 1, 1).
python_class('src/nlp2uri/cqrs/dispatcher.py', 'CqrsDispatcher').
python_method('CqrsDispatcher', '__init__', 0, 5, 5).
python_method('CqrsDispatcher', 'compile_uri', 1, 4, 6).
python_method('CqrsDispatcher', 'execute_uri', 1, 4, 10).
python_method('CqrsDispatcher', 'probe_uri', 1, 1, 2).
python_class('src/nlp2uri/cqrs/drivers/artifact_filesystem.py', 'ArtifactFilesystemDriver').
python_method('ArtifactFilesystemDriver', 'compile', 1, 7, 5).
python_class('src/nlp2uri/cqrs/drivers/command_curl.py', 'CommandCurlDriver').
python_method('CommandCurlDriver', 'compile', 1, 5, 4).
python_method('CommandCurlDriver', 'probe', 1, 1, 3).
python_class('src/nlp2uri/cqrs/drivers/container_docker.py', 'ContainerDockerDriver').
python_method('ContainerDockerDriver', 'compile', 1, 5, 5).
python_method('ContainerDockerDriver', 'probe', 1, 1, 3).
python_method('ContainerDockerDriver', '_docker_argv', 4, 14, 4).
python_class('src/nlp2uri/cqrs/drivers/delegate.py', 'DelegateCompileDriver').
python_method('DelegateCompileDriver', '__init__', 2, 1, 0).
python_method('DelegateCompileDriver', 'compile', 1, 2, 3).
python_class('src/nlp2uri/cqrs/drivers/endpoint_curl.py', 'EndpointCurlDriver').
python_method('EndpointCurlDriver', 'compile', 1, 2, 3).
python_method('EndpointCurlDriver', 'probe', 1, 2, 3).
python_class('src/nlp2uri/cqrs/drivers/getv_cli.py', 'GetvCliDriver').
python_method('GetvCliDriver', 'compile', 1, 2, 3).
python_class('src/nlp2uri/cqrs/drivers/resource_probe.py', 'ResourceProbeDriver').
python_method('ResourceProbeDriver', 'compile', 1, 5, 4).
python_method('ResourceProbeDriver', 'probe', 1, 3, 4).
python_class('src/nlp2uri/cqrs/drivers/runtime_curl.py', 'RuntimeCurlDriver').
python_method('RuntimeCurlDriver', 'compile', 1, 2, 3).
python_method('RuntimeCurlDriver', 'probe', 1, 3, 4).
python_class('src/nlp2uri/cqrs/drivers/service_ops.py', 'ServiceCurlDriver').
python_method('ServiceCurlDriver', 'compile', 1, 3, 6).
python_method('ServiceCurlDriver', 'probe', 1, 1, 3).
python_class('src/nlp2uri/cqrs/drivers/service_ops.py', 'ServiceDockerDriver').
python_method('ServiceDockerDriver', 'compile', 1, 3, 6).
python_method('ServiceDockerDriver', 'probe', 1, 1, 6).
python_class('src/nlp2uri/cqrs/drivers/service_ops.py', 'ServiceSystemdDriver').
python_method('ServiceSystemdDriver', 'compile', 1, 3, 4).
python_method('ServiceSystemdDriver', 'probe', 1, 1, 2).
python_class('src/nlp2uri/cqrs/event_store.py', 'StoredEvent').
python_method('StoredEvent', 'to_dict', 0, 1, 0).
python_class('src/nlp2uri/cqrs/event_store.py', 'InMemoryEventStore').
python_method('InMemoryEventStore', '__init__', 0, 1, 0).
python_method('InMemoryEventStore', 'append', 1, 2, 8).
python_method('InMemoryEventStore', 'get_stream', 1, 3, 1).
python_method('InMemoryEventStore', 'all_events', 0, 2, 3).
python_class('src/nlp2uri/cqrs/http_store.py', 'HttpEventStore').
python_method('HttpEventStore', '__init__', 1, 2, 4).
python_method('HttpEventStore', 'append', 1, 2, 3).
python_method('HttpEventStore', '_post_remote', 1, 3, 5).
python_class('src/nlp2uri/cqrs/registry.py', 'DriverRegistry').
python_method('DriverRegistry', '__init__', 1, 2, 3).
python_method('DriverRegistry', 'schemes', 0, 1, 1).
python_method('DriverRegistry', 'plugin_drivers', 0, 2, 0).
python_method('DriverRegistry', 'targets_for', 1, 1, 2).
python_method('DriverRegistry', 'default_target', 1, 2, 1).
python_method('DriverRegistry', 'get_driver', 2, 8, 6).
python_method('DriverRegistry', 'driver_for_uri', 2, 5, 4).
python_class('src/nlp2uri/integrators/rest_server.py', 'NLP2URIRequestHandler').
python_method('NLP2URIRequestHandler', 'log_message', 1, 1, 0).
python_method('NLP2URIRequestHandler', '_read_json', 0, 4, 5).
python_method('NLP2URIRequestHandler', '_send', 2, 1, 8).
python_method('NLP2URIRequestHandler', 'do_GET', 0, 2, 6).
python_method('NLP2URIRequestHandler', 'do_POST', 0, 3, 6).
python_class('src/nlp2uri/models.py', 'HostPlatform').
python_class('src/nlp2uri/models.py', 'IntentKind').
python_class('src/nlp2uri/models.py', 'UriIntent').
python_method('UriIntent', 'with_params', 0, 3, 4).
python_method('UriIntent', 'intent_name', 0, 9, 1).
python_method('UriIntent', 'to_slots', 0, 12, 2).
python_class('src/nlp2uri/models.py', 'UriSpec').
python_method('UriSpec', 'to_dict', 0, 2, 3).
python_class('src/nlp2uri/models.py', 'OSAction').
python_method('OSAction', 'argv', 0, 1, 0).
python_method('OSAction', 'to_dict', 0, 2, 2).
python_class('src/nlp2uri/models.py', 'NLP2URIResult').
python_method('NLP2URIResult', 'to_dict', 0, 2, 2).
python_class('src/nlp2uri/models.py', 'ActionResult').
python_method('ActionResult', 'to_dict', 0, 2, 1).
python_class('src/nlp2uri/platforms/base.py', 'UriExecutor').
python_method('UriExecutor', 'execute', 1, 1, 0).
python_method('UriExecutor', '_result', 0, 1, 1).
python_method('UriExecutor', '_dry', 2, 1, 2).
python_method('UriExecutor', '_run', 2, 6, 3).
python_method('UriExecutor', '_first_available', 1, 3, 1).
python_method('UriExecutor', '_open_with_browser', 1, 2, 4).
python_method('UriExecutor', '_parse_nlp2uri', 1, 6, 7).
python_method('UriExecutor', '_desktop_id_for_app', 1, 7, 6).
python_class('src/nlp2uri/platforms/linux.py', 'LinuxExecutor').
python_method('LinuxExecutor', 'execute', 1, 8, 11).
python_method('LinuxExecutor', '_open_generic', 1, 3, 4).
python_method('LinuxExecutor', '_open_settings', 0, 4, 4).
python_method('LinuxExecutor', '_open_app', 1, 7, 5).
python_method('LinuxExecutor', '_focus_app', 1, 6, 5).
python_method('LinuxExecutor', '_capture', 2, 11, 9).
python_class('src/nlp2uri/platforms/macos.py', 'MacOSExecutor').
python_method('MacOSExecutor', 'execute', 1, 7, 10).
python_method('MacOSExecutor', '_open', 1, 2, 2).
python_method('MacOSExecutor', '_open_app', 1, 3, 3).
python_method('MacOSExecutor', '_focus_app', 1, 3, 3).
python_method('MacOSExecutor', '_capture', 2, 5, 7).
python_class('src/nlp2uri/platforms/windows.py', 'WindowsExecutor').
python_method('WindowsExecutor', 'execute', 1, 7, 10).
python_method('WindowsExecutor', '_start', 1, 2, 2).
python_method('WindowsExecutor', '_open_app', 1, 3, 3).
python_method('WindowsExecutor', '_focus_app', 1, 3, 3).
python_method('WindowsExecutor', '_capture', 2, 5, 9).
python_class('src/nlp2uri/service.py', 'NLP2URIService').
python_method('NLP2URIService', 'default', 1, 1, 2).
python_method('NLP2URIService', 'for_platform', 2, 2, 4).
python_method('NLP2URIService', '_cfg', 0, 2, 1).
python_method('NLP2URIService', '_host', 0, 1, 1).
python_method('NLP2URIService', 'from_prompt', 1, 2, 3).
python_method('NLP2URIService', 'resolve', 1, 1, 2).
python_method('NLP2URIService', 'compile', 1, 1, 2).
python_method('NLP2URIService', 'execute', 1, 2, 3).
python_method('NLP2URIService', 'handle_prompt', 1, 1, 4).
python_method('NLP2URIService', 'handle_uri', 1, 2, 4).
python_method('NLP2URIService', 'list_system_uris', 1, 3, 5).
python_method('NLP2URIService', 'resolve_system_map', 2, 5, 5).
python_method('NLP2URIService', 'list_getv_uris', 0, 3, 5).
python_method('NLP2URIService', 'resolve_getv', 1, 4, 3).
python_method('NLP2URIService', 'read_getv_var', 1, 1, 1).
python_class('src/nlp2uri/systemmap/getv_uri.py', 'ResolvedGetvUri').
python_method('ResolvedGetvUri', 'to_dict', 0, 1, 0).
python_class('src/nlp2uri/systemmap/index.py', 'UriMapEntry').
python_method('UriMapEntry', 'to_dict', 0, 3, 2).
python_class('src/nlp2uri/systemmap/index.py', 'UriMap').
python_method('UriMap', 'lookup', 1, 1, 1).
python_method('UriMap', 'find_by_kind', 1, 3, 1).
python_method('UriMap', 'find_command', 1, 2, 1).
python_method('UriMap', 'to_dict', 0, 3, 3).
python_class('src/nlp2uri/systemmap/resolve.py', 'ResolvedSystemUri').
python_method('ResolvedSystemUri', 'to_dict', 0, 1, 0).
python_class('tests/test_http_event_store.py', '_Handler').
python_method('_Handler', 'do_POST', 0, 2, 11).
python_method('_Handler', 'log_message', 1, 1, 0).

% ── Dependencies ─────────────────────────────────────────

% ── Makefile Targets ─────────────────────────────────────

% ── Taskfile Tasks ───────────────────────────────────────

% ── Environment Variables ────────────────────────────────
env_variable('OPENROUTER_API_KEY', '*(not set)*', 'Required: OpenRouter API key (https://openrouter.ai/keys)').
env_variable('LLM_MODEL', 'openrouter/qwen/qwen3-coder-next', 'Model (default: openrouter/qwen/qwen3-coder-next)').
env_variable('PFIX_AUTO_APPLY', 'true', 'true = apply fixes without asking').
env_variable('PFIX_AUTO_INSTALL_DEPS', 'true', 'true = auto pip/uv install').
env_variable('PFIX_AUTO_RESTART', 'false', 'true = os.execv restart after fix').
env_variable('PFIX_MAX_RETRIES', '3', '').
env_variable('PFIX_DRY_RUN', 'false', '').
env_variable('PFIX_ENABLED', 'true', '').
env_variable('PFIX_GIT_COMMIT', 'false', 'true = auto-commit fixes').
env_variable('PFIX_GIT_PREFIX', 'pfix:', 'commit message prefix').
env_variable('PFIX_CREATE_BACKUPS', 'false', 'false = disable .pfix_backups/ directory').

% ── TestQL Scenarios ─────────────────────────────────────
testql_scenario('generated-cli-tests.testql.toon.yaml', 'cli').
testql_scenario('generated-from-pytests.testql.toon.yaml', 'integration').

% ── Semantic Facts from SUMD.md ──────────────────────────
sumd_declared_file('app.doql.less', 'doql').
sumd_declared_file('testql-scenarios/generated-cli-tests.testql.toon.yaml', 'testql').
sumd_declared_file('testql-scenarios/generated-from-pytests.testql.toon.yaml', 'testql').
sumd_declared_file('project/map.toon.yaml', 'analysis').
sumd_declared_file('project/logic.pl', 'analysis').
sumd_declared_file('project/calls.toon.yaml', 'analysis').
sumd_interface('cli', 'argparse').
sumd_interface('cli', '').
sumd_deploy_target('docker_compose').
sumd_deploy_compose_file('docker-compose.yml').
```

## Call Graph

*225 nodes · 295 edges · 52 modules · CC̄=3.5*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `build_uri_index` *(in src.nlp2uri.systemmap.index)* | 31 ⚠ | 4 | 52 | **56** |
| `_build_parser` *(in src.nlp2uri.cli)* | 1 | 1 | 35 | **36** |
| `build_resource_actions` *(in src.nlp2uri.host.resource)* | 14 ⚠ | 2 | 29 | **31** |
| `build_getv_uri_index` *(in src.nlp2uri.systemmap.getv_uri)* | 6 | 3 | 24 | **27** |
| `resolve_prompt_against_system_map` *(in src.nlp2uri.systemmap.resolve)* | 26 ⚠ | 2 | 23 | **25** |
| `encode_segment` *(in src.nlp2uri.systemmap.encode)* | 1 | 22 | 1 | **23** |
| `main` *(in schemas.codegen.export_driver_stubs)* | 11 ⚠ | 0 | 23 | **23** |
| `resolve_artifact_path` *(in src.nlp2uri.host.artifact)* | 12 ⚠ | 1 | 22 | **23** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/nlp2uri
# generated in 0.12s
# nodes: 225 | edges: 295 | modules: 52
# CC̄=3.5

HUBS[20]:
  src.nlp2uri.systemmap.index.build_uri_index
    CC=31  in:4  out:52  total:56
  src.nlp2uri.cli._build_parser
    CC=1  in:1  out:35  total:36
  src.nlp2uri.host.resource.build_resource_actions
    CC=14  in:2  out:29  total:31
  src.nlp2uri.systemmap.getv_uri.build_getv_uri_index
    CC=6  in:3  out:24  total:27
  src.nlp2uri.systemmap.resolve.resolve_prompt_against_system_map
    CC=26  in:2  out:23  total:25
  src.nlp2uri.systemmap.encode.encode_segment
    CC=1  in:22  out:1  total:23
  schemas.codegen.export_driver_stubs.main
    CC=11  in:0  out:23  total:23
  src.nlp2uri.host.artifact.resolve_artifact_path
    CC=12  in:1  out:22  total:23
  src.nlp2uri.compile.compile_uri_to_actions
    CC=13  in:5  out:18  total:23
  src.nlp2uri.compile._compile_app
    CC=16  in:1  out:21  total:22
  src.nlp2uri.systemmap.getv_uri.compile_getv_uri
    CC=14  in:2  out:18  total:20
  src.nlp2uri.config._load_from_path
    CC=6  in:3  out:17  total:20
  examples.resolve.new-intents.e2e.print
    CC=0  in:19  out:0  total:19
  src.nlp2uri.systemmap.getv_uri.resolve_prompt_against_getv
    CC=13  in:1  out:18  total:19
  src.nlp2uri.host.artifact.build_artifact_actions
    CC=13  in:2  out:17  total:19
  src.nlp2uri.systemmap.compile._compile_runtime
    CC=12  in:1  out:18  total:19
  src.nlp2uri.systemmap.context.load_ir_from_arguments
    CC=8  in:2  out:16  total:18
  src.nlp2uri.systemmap.index._ir_field
    CC=2  in:14  out:3  total:17
  src.nlp2uri.schemes.build.build_uri
    CC=13  in:2  out:15  total:17
  src.nlp2uri.systemmap.uri._get
    CC=4  in:12  out:5  total:17

MODULES:
  examples.execute.dry-run.main  [1 funcs]
    main  CC=3  out:7
  examples.mcp.tool-handoff.main  [1 funcs]
    main  CC=2  out:8
  examples.resolve.new-intents.e2e  [1 funcs]
    print  CC=0  out:0
  examples.resolve.nl-to-uri.main  [1 funcs]
    main  CC=3  out:5
  schemas.codegen.export_driver_stubs  [1 funcs]
    main  CC=11  out:23
  schemas.codegen.export_mcp_schemas  [1 funcs]
    main  CC=4  out:13
  schemas.codegen.fix_proto_imports  [4 funcs]
    _pascal  CC=2  out:4
    fix_api  CC=1  out:3
    fix_driver  CC=1  out:3
    main  CC=4  out:7
  schemas.codegen.scaffold_scheme  [12 funcs]
    _pascal  CC=2  out:4
    _proto_package  CC=2  out:2
    aggregate_proto  CC=2  out:4
    api_proto  CC=1  out:3
    commands_proto  CC=1  out:3
    driver_proto  CC=1  out:5
    events_proto  CC=1  out:3
    main  CC=4  out:14
    openapi_yaml  CC=1  out:2
    queries_proto  CC=1  out:3
  src.nlp2uri.adapters.base  [1 funcs]
    __init__  CC=2  out:2
  src.nlp2uri.adapters.mcp  [2 funcs]
    _tool_list_system_uris  CC=2  out:7
    _tool_resolve_system_map  CC=3  out:10
  src.nlp2uri.cli  [11 funcs]
    _add_common_args  CC=3  out:2
    _build_parser  CC=1  out:35
    _emit  CC=3  out:4
    _platform  CC=2  out:1
    _request_from_args  CC=3  out:7
    _run_adapter_command  CC=4  out:8
    _run_config  CC=3  out:10
    _run_execute  CC=5  out:10
    _run_shell  CC=5  out:10
    _with_platform  CC=2  out:2
  src.nlp2uri.compile  [23 funcs]
    _capture_outfile  CC=1  out:3
    _compile_app  CC=16  out:21
    _compile_launch_app  CC=7  out:8
    _compile_legacy_nlp2uri  CC=7  out:12
    _compile_screen_capture  CC=4  out:4
    _compile_screenshot  CC=4  out:4
    _compile_settings  CC=5  out:5
    _compile_settings_panel  CC=5  out:7
    _compile_terminal  CC=16  out:11
    _compile_window  CC=11  out:13
  src.nlp2uri.config  [15 funcs]
    resolved_platform  CC=4  out:8
    to_dict  CC=2  out:2
    to_yaml  CC=6  out:11
    _load_from_path  CC=6  out:17
    _parse_scalar  CC=8  out:5
    _parse_simple_yaml  CC=5  out:6
    _yaml_scalar  CC=8  out:6
    config_search_paths  CC=5  out:15
    default_config  CC=1  out:3
    ensure_config  CC=4  out:9
  src.nlp2uri.cqrs.dispatcher  [1 funcs]
    __init__  CC=5  out:5
  src.nlp2uri.cqrs.drivers.artifact_filesystem  [1 funcs]
    compile  CC=7  out:7
  src.nlp2uri.cqrs.drivers.command_curl  [1 funcs]
    compile  CC=5  out:6
  src.nlp2uri.cqrs.drivers.container_docker  [3 funcs]
    compile  CC=5  out:9
    probe  CC=1  out:3
    parse_container_uri  CC=8  out:8
  src.nlp2uri.cqrs.drivers.delegate  [1 funcs]
    compile  CC=2  out:4
  src.nlp2uri.cqrs.drivers.endpoint_curl  [2 funcs]
    compile  CC=2  out:4
    probe  CC=2  out:4
  src.nlp2uri.cqrs.drivers.getv_cli  [1 funcs]
    compile  CC=2  out:4
  src.nlp2uri.cqrs.drivers.resource_probe  [1 funcs]
    compile  CC=5  out:6
  src.nlp2uri.cqrs.drivers.runtime_curl  [1 funcs]
    compile  CC=2  out:4
  src.nlp2uri.cqrs.drivers.service_ops  [8 funcs]
    compile  CC=5  out:9
    probe  CC=2  out:4
    compile  CC=2  out:7
    probe  CC=1  out:6
    compile  CC=3  out:4
    probe  CC=1  out:2
    _compose_dir  CC=3  out:5
    parse_service_name  CC=4  out:4
  src.nlp2uri.cqrs.plugins  [3 funcs]
    _parse_entry_point_name  CC=4  out:2
    load_driver_plugins  CC=7  out:10
    resolve_driver_class  CC=2  out:2
  src.nlp2uri.cqrs.registry  [3 funcs]
    __init__  CC=2  out:3
    get_driver  CC=8  out:8
    default_registry  CC=1  out:2
  src.nlp2uri.host.artifact  [3 funcs]
    _decode  CC=2  out:1
    build_artifact_actions  CC=13  out:17
    resolve_artifact_path  CC=12  out:22
  src.nlp2uri.host.endpoint  [3 funcs]
    build_endpoint_actions  CC=1  out:2
    build_endpoint_url  CC=8  out:10
    is_endpoint_uri  CC=1  out:2
  src.nlp2uri.host.resource  [3 funcs]
    _decode  CC=2  out:1
    _filesystem_probe_path  CC=5  out:12
    build_resource_actions  CC=14  out:29
  src.nlp2uri.integrators.mcp_server  [10 funcs]
    _handle_initialize  CC=1  out:0
    _handle_tools_call  CC=6  out:7
    _handle_tools_list  CC=1  out:0
    _jsonrpc_error  CC=2  out:0
    _jsonrpc_response  CC=1  out:0
    _log  CC=1  out:1
    _write_json  CC=1  out:3
    handle_message  CC=8  out:12
    main  CC=1  out:3
    run_stdio  CC=6  out:12
  src.nlp2uri.integrators.rest_server  [2 funcs]
    main  CC=1  out:5
    run_server  CC=2  out:7
  src.nlp2uri.mcp  [2 funcs]
    mcp_handoff_payload  CC=2  out:4
    tool_resolve_desktop_action  CC=2  out:2
  src.nlp2uri.parse_nl  [15 funcs]
    _capture_target  CC=4  out:2
    _normalize_aliases  CC=2  out:3
    _normalize_app_name  CC=2  out:1
    _normalize_panel  CC=1  out:3
    _parse_app_open  CC=2  out:4
    _parse_capture  CC=6  out:8
    _parse_fallback  CC=1  out:1
    _parse_file_open  CC=2  out:4
    _parse_ide_project  CC=2  out:6
    _parse_open_prefix  CC=5  out:7
  src.nlp2uri.platform_detect  [1 funcs]
    detect_platform  CC=5  out:1
  src.nlp2uri.platforms.registry  [1 funcs]
    get_executor  CC=3  out:4
  src.nlp2uri.resolve  [2 funcs]
    nlp2uri  CC=4  out:8
    resolve_text  CC=2  out:3
  src.nlp2uri.runtime  [1 funcs]
    execute_uri  CC=9  out:15
  src.nlp2uri.schemes.build  [2 funcs]
    _build_navigate  CC=4  out:5
    build_uri  CC=13  out:15
  src.nlp2uri.schemes.desktop  [6 funcs]
    build_app_open  CC=3  out:5
    build_capture  CC=5  out:5
    build_focus  CC=1  out:5
    build_move  CC=1  out:5
    build_settings  CC=6  out:8
    build_terminal  CC=2  out:5
  src.nlp2uri.schemes.file  [1 funcs]
    build_file  CC=3  out:6
  src.nlp2uri.schemes.ide  [1 funcs]
    build_ide  CC=4  out:10
  src.nlp2uri.schemes.util  [3 funcs]
    abstract_url  CC=9  out:5
    file_uri  CC=1  out:3
    normalize_path  CC=2  out:5
  src.nlp2uri.service  [13 funcs]
    _cfg  CC=2  out:1
    _host  CC=1  out:1
    compile  CC=1  out:2
    default  CC=1  out:2
    execute  CC=2  out:3
    for_platform  CC=2  out:4
    from_prompt  CC=2  out:3
    list_getv_uris  CC=3  out:5
    list_system_uris  CC=3  out:5
    read_getv_var  CC=1  out:1
  src.nlp2uri.systemmap.compile  [10 funcs]
    _backend_url  CC=1  out:2
    _compile_access  CC=2  out:5
    _compile_artifact  CC=2  out:1
    _compile_command  CC=4  out:8
    _compile_metadata  CC=2  out:4
    _compile_resource  CC=2  out:1
    _compile_runtime  CC=12  out:18
    _decode_segment  CC=2  out:1
    compile_system_map_uri  CC=8  out:10
    is_system_map_uri  CC=1  out:2
  src.nlp2uri.systemmap.context  [2 funcs]
    _coerce_ir  CC=2  out:2
    load_ir_from_arguments  CC=8  out:16
  src.nlp2uri.systemmap.encode  [2 funcs]
    encode_path  CC=1  out:2
    encode_segment  CC=1  out:1
  src.nlp2uri.systemmap.fallback  [1 funcs]
    resolve_prompt_with_fallback  CC=6  out:5
  src.nlp2uri.systemmap.getv_load  [7 funcs]
    _parse_env_file  CC=8  out:11
    discover_profiles  CC=8  out:8
    getv_home  CC=1  out:4
    getv_missing_message  CC=2  out:0
    load_profile_dict  CC=4  out:4
    mask_var_value  CC=2  out:2
    profile_manager  CC=4  out:4
  src.nlp2uri.systemmap.getv_uri  [8 funcs]
    _decode_segment  CC=2  out:1
    build_getv_uri_index  CC=6  out:24
    compile_getv_uri  CC=14  out:18
    get_getv_var_value  CC=9  out:10
    is_getv_uri  CC=1  out:2
    resolve_prompt_against_getv  CC=13  out:18
    uri_for_getv_profile  CC=1  out:2
    uri_for_getv_var  CC=1  out:3
  src.nlp2uri.systemmap.index  [6 funcs]
    _add_entry  CC=3  out:4
    _get_id  CC=1  out:1
    _get_id_field  CC=4  out:5
    _ir_field  CC=2  out:3
    _model_dump  CC=3  out:6
    build_uri_index  CC=31  out:52
  src.nlp2uri.systemmap.load  [4 funcs]
    env2llm_available  CC=1  out:0
    env2llm_missing_message  CC=2  out:0
    load_system_map_from_doql  CC=2  out:3
    load_system_map_from_example  CC=3  out:3
  src.nlp2uri.systemmap.resolve  [3 funcs]
    _name_variants  CC=3  out:3
    _normalize_token  CC=1  out:5
    resolve_prompt_against_system_map  CC=26  out:23
  src.nlp2uri.systemmap.uri  [13 funcs]
    _get  CC=4  out:5
    _get_list  CC=5  out:4
    uri_for_access  CC=4  out:7
    uri_for_artifact  CC=1  out:4
    uri_for_command  CC=3  out:4
    uri_for_conversation  CC=1  out:1
    uri_for_environment  CC=1  out:1
    uri_for_generated_service  CC=1  out:2
    uri_for_process  CC=1  out:1
    uri_for_resource  CC=2  out:4

EDGES:
  schemas.codegen.fix_proto_imports.fix_api → schemas.codegen.fix_proto_imports._pascal
  schemas.codegen.fix_proto_imports.fix_driver → schemas.codegen.fix_proto_imports._pascal
  schemas.codegen.fix_proto_imports.main → schemas.codegen.fix_proto_imports.fix_api
  schemas.codegen.fix_proto_imports.main → schemas.codegen.fix_proto_imports.fix_driver
  schemas.codegen.fix_proto_imports.main → examples.resolve.new-intents.e2e.print
  schemas.codegen.export_mcp_schemas.main → examples.resolve.new-intents.e2e.print
  schemas.codegen.export_driver_stubs.main → examples.resolve.new-intents.e2e.print
  schemas.codegen.scaffold_scheme.aggregate_proto → schemas.codegen.scaffold_scheme._proto_package
  schemas.codegen.scaffold_scheme.aggregate_proto → schemas.codegen.scaffold_scheme._pascal
  schemas.codegen.scaffold_scheme.commands_proto → schemas.codegen.scaffold_scheme._proto_package
  schemas.codegen.scaffold_scheme.commands_proto → schemas.codegen.scaffold_scheme._pascal
  schemas.codegen.scaffold_scheme.events_proto → schemas.codegen.scaffold_scheme._proto_package
  schemas.codegen.scaffold_scheme.events_proto → schemas.codegen.scaffold_scheme._pascal
  schemas.codegen.scaffold_scheme.queries_proto → schemas.codegen.scaffold_scheme._proto_package
  schemas.codegen.scaffold_scheme.queries_proto → schemas.codegen.scaffold_scheme._pascal
  schemas.codegen.scaffold_scheme.driver_proto → schemas.codegen.scaffold_scheme._proto_package
  schemas.codegen.scaffold_scheme.driver_proto → schemas.codegen.scaffold_scheme._pascal
  schemas.codegen.scaffold_scheme.api_proto → schemas.codegen.scaffold_scheme._proto_package
  schemas.codegen.scaffold_scheme.api_proto → schemas.codegen.scaffold_scheme._pascal
  schemas.codegen.scaffold_scheme.openapi_yaml → schemas.codegen.scaffold_scheme._pascal
  schemas.codegen.scaffold_scheme.readme_md → schemas.codegen.scaffold_scheme._pascal
  schemas.codegen.scaffold_scheme.scaffold_scheme → schemas.codegen.scaffold_scheme.aggregate_proto
  schemas.codegen.scaffold_scheme.scaffold_scheme → schemas.codegen.scaffold_scheme.commands_proto
  schemas.codegen.scaffold_scheme.scaffold_scheme → schemas.codegen.scaffold_scheme.events_proto
  schemas.codegen.scaffold_scheme.scaffold_scheme → schemas.codegen.scaffold_scheme.queries_proto
  schemas.codegen.scaffold_scheme.scaffold_scheme → schemas.codegen.scaffold_scheme.driver_proto
  schemas.codegen.scaffold_scheme.scaffold_scheme → schemas.codegen.scaffold_scheme.api_proto
  schemas.codegen.scaffold_scheme.scaffold_scheme → schemas.codegen.scaffold_scheme.openapi_yaml
  schemas.codegen.scaffold_scheme.scaffold_scheme → schemas.codegen.scaffold_scheme.readme_md
  schemas.codegen.scaffold_scheme.main → examples.resolve.new-intents.e2e.print
  examples.mcp.tool-handoff.main.main → examples.resolve.new-intents.e2e.print
  examples.mcp.tool-handoff.main.main → src.nlp2uri.mcp.mcp_handoff_payload
  examples.mcp.tool-handoff.main.main → src.nlp2uri.mcp.tool_resolve_desktop_action
  examples.execute.dry-run.main.main → src.nlp2uri.resolve.nlp2uri
  examples.execute.dry-run.main.main → src.nlp2uri.compile.compile_uri_to_actions
  examples.execute.dry-run.main.main → examples.resolve.new-intents.e2e.print
  examples.resolve.nl-to-uri.main.main → src.nlp2uri.resolve.nlp2uri
  examples.resolve.nl-to-uri.main.main → examples.resolve.new-intents.e2e.print
  src.nlp2uri.runtime.execute_uri → src.nlp2uri.config.get_effective_platform
  src.nlp2uri.runtime.execute_uri → src.nlp2uri.compile.compile_uri_to_actions
  src.nlp2uri.config.NLP2URIConfig.resolved_platform → src.nlp2uri.platform_detect.detect_platform
  src.nlp2uri.config.NLP2URIConfig.to_dict → src.nlp2uri.platform_detect.detect_platform
  src.nlp2uri.config.NLP2URIConfig.to_yaml → src.nlp2uri.config.payload_keys
  src.nlp2uri.config.NLP2URIConfig.to_yaml → src.nlp2uri.config._yaml_scalar
  src.nlp2uri.config._parse_simple_yaml → src.nlp2uri.config._parse_scalar
  src.nlp2uri.config.find_config_path → src.nlp2uri.config.config_search_paths
  src.nlp2uri.config.default_config → src.nlp2uri.platform_detect.detect_platform
  src.nlp2uri.config._load_from_path → src.nlp2uri.config._parse_simple_yaml
  src.nlp2uri.config._load_from_path → src.nlp2uri.config.payload_keys
  src.nlp2uri.config.load_config → src.nlp2uri.config.find_config_path
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Cli (1)

**`CLI Command Tests`**

### Integration (1)

**`Auto-generated from Python Tests`**
- assert `status == 200`
- assert `status == 200`

## Intent

Natural language to URI resolution and cross-platform local URI execution
