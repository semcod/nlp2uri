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
- **version**: `0.1.2`
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
  version: 0.1.2;
}

dependencies {
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
  version: 0.1.2
  env: local
```

## Dependencies

### Runtime

*(see pyproject.toml)*

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
# nlp2uri | 58f 3886L | python:47,shell:10,less:1 | 2026-06-06
# stats: 141 func | 21 cls | 58 mod | CC̄=3.3 | critical:3 | cycles:0
# alerts[5]: CC _compile_app=11; CC build_uri=11; CC _compile_window=10; CC execute_uri=9; CC abstract_url=9
# hotspots[5]: _compile_app fan=13; _compile_legacy_nlp2uri fan=12; test_xdg_custom_scheme_handler fan=12; _run_config fan=10; _run_execute fan=10
# evolution: baseline
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[58]:
  app.doql.less,29
  examples/execute/dry-run/e2e.sh,12
  examples/execute/dry-run/main.py,30
  examples/integrators/mcp-stdio/e2e.sh,11
  examples/integrators/rest-api/e2e.sh,24
  examples/integrators/shell-export/e2e.sh,13
  examples/mcp/tool-handoff/e2e.sh,12
  examples/mcp/tool-handoff/main.py,28
  examples/resolve/nl-to-uri/e2e.sh,12
  examples/resolve/nl-to-uri/main.py,43
  examples/run-e2e.sh,40
  project.sh,59
  scripts/testapp-handler.sh,7
  src/nlp2uri/__init__.py,29
  src/nlp2uri/adapters/__init__.py,18
  src/nlp2uri/adapters/base.py,60
  src/nlp2uri/adapters/cli.py,40
  src/nlp2uri/adapters/mcp.py,184
  src/nlp2uri/adapters/rest.py,88
  src/nlp2uri/adapters/shell.py,67
  src/nlp2uri/cli.py,200
  src/nlp2uri/compile.py,306
  src/nlp2uri/config.py,231
  src/nlp2uri/integrators/__init__.py,23
  src/nlp2uri/integrators/mcp_server.py,129
  src/nlp2uri/integrators/rest_server.py,91
  src/nlp2uri/mcp.py,82
  src/nlp2uri/models.py,175
  src/nlp2uri/parse_nl.py,275
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
  src/nlp2uri/schemes/build.py,60
  src/nlp2uri/schemes/desktop.py,95
  src/nlp2uri/schemes/file.py,26
  src/nlp2uri/schemes/http.py,23
  src/nlp2uri/schemes/ide.py,36
  src/nlp2uri/schemes/util.py,48
  src/nlp2uri/service.py,72
  tests/conftest.py,18
  tests/integration/test_xdg_handler.py,99
  tests/test_adapters.py,76
  tests/test_cli.py,31
  tests/test_compile.py,34
  tests/test_config.py,65
  tests/test_mcp.py,25
  tests/test_platforms.py,48
  tests/test_resolve.py,77
  tests/test_rest_server.py,48
  tests/test_service.py,27
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
    McpAdapter: handle(1),call_tool(2),tool_dispatch(0),_args_from_request(1),_args_to_request(2),mcp_content(1),_tool_plan(1),_tool_resolve(1),_tool_compile(1),_tool_execute(1),_tool_handle(1)
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
    e: compile_uri_to_actions,_query_params,_first_available,_open_uri,_compile_app,_compile_settings,_compile_launch_app,_capture_outfile,_linux_screen_capture,_macos_screen_capture,_windows_screen_capture,_compile_screen_capture,_linux_window_capture,_macos_window_capture,_windows_window_capture,_compile_window_capture,_compile_screenshot,_compile_window,_compile_legacy_nlp2uri,_desktop_id_for_app
    compile_uri_to_actions(uri;os)
    _query_params(parsed)
    _first_available(names)
    _open_uri(host;uri)
    _compile_app(host;authority;path;params;uri)
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
    e: _strip_quotes,_normalize_aliases,_parse_absolute_uri,_parse_http_url,_parse_ide_project,_parse_file_open,_parse_settings,_parse_active_window,_capture_target,_parse_capture,_parse_focus,_parse_app_open,_parse_path,_parse_open_prefix,_parse_fallback,parse_text
    _strip_quotes(value)
    _normalize_aliases(text)
    _parse_absolute_uri(raw;_lowered)
    _parse_http_url(raw;_lowered)
    _parse_ide_project(raw;_lowered)
    _parse_file_open(raw;_lowered)
    _parse_settings(_raw;lowered)
    _parse_active_window(raw;_lowered)
    _capture_target(lowered;title)
    _parse_capture(raw;lowered)
    _parse_focus(raw;_lowered)
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
    e: build_capture,build_focus,build_app_open,build_settings
    build_capture(intent)
    build_focus(intent)
    build_app_open(intent)
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
    NLP2URIService: default(1),for_platform(2),_cfg(0),_host(0),from_prompt(1),resolve(1),compile(1),execute(1),handle_prompt(1),handle_uri(1)  # Reusable facade: prompt → URI → compile → execute.
  tests/conftest.py:
    e: isolated_config
    isolated_config(tmp_path;monkeypatch)
  tests/integration/test_xdg_handler.py:
    e: test_xdg_custom_scheme_handler
    test_xdg_custom_scheme_handler(tmp_path)
  tests/test_adapters.py:
    e: test_cli_adapter_plan,test_rest_adapter_plan,test_shell_adapter_export,test_mcp_adapter_tools,test_mcp_stdio_initialize,test_mcp_stdio_tools_call
    test_cli_adapter_plan()
    test_rest_adapter_plan()
    test_shell_adapter_export()
    test_mcp_adapter_tools()
    test_mcp_stdio_initialize()
    test_mcp_stdio_tools_call()
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
  tests/test_rest_server.py:
    e: _post,test_rest_server_plan
    _post(url;payload)
    test_rest_server_plan()
  tests/test_service.py:
    e: test_from_prompt,test_handle_prompt_dry_run,test_handle_uri
    test_from_prompt()
    test_handle_prompt_dry_run()
    test_handle_uri()
```

### `project/logic.pl`

```prolog markpact:analysis path=project/logic.pl
% ── Project Metadata ─────────────────────────────────────
project_metadata('nlp2uri', '0.1.2', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 29, 'less').
project_file('examples/execute/dry-run/e2e.sh', 12, 'shell').
project_file('examples/execute/dry-run/main.py', 30, 'python').
project_file('examples/integrators/mcp-stdio/e2e.sh', 11, 'shell').
project_file('examples/integrators/rest-api/e2e.sh', 24, 'shell').
project_file('examples/integrators/shell-export/e2e.sh', 13, 'shell').
project_file('examples/mcp/tool-handoff/e2e.sh', 12, 'shell').
project_file('examples/mcp/tool-handoff/main.py', 28, 'python').
project_file('examples/resolve/nl-to-uri/e2e.sh', 12, 'shell').
project_file('examples/resolve/nl-to-uri/main.py', 43, 'python').
project_file('examples/run-e2e.sh', 40, 'shell').
project_file('project.sh', 59, 'shell').
project_file('scripts/testapp-handler.sh', 7, 'shell').
project_file('src/nlp2uri/__init__.py', 29, 'python').
project_file('src/nlp2uri/adapters/__init__.py', 18, 'python').
project_file('src/nlp2uri/adapters/base.py', 60, 'python').
project_file('src/nlp2uri/adapters/cli.py', 40, 'python').
project_file('src/nlp2uri/adapters/mcp.py', 184, 'python').
project_file('src/nlp2uri/adapters/rest.py', 88, 'python').
project_file('src/nlp2uri/adapters/shell.py', 67, 'python').
project_file('src/nlp2uri/cli.py', 200, 'python').
project_file('src/nlp2uri/compile.py', 306, 'python').
project_file('src/nlp2uri/config.py', 231, 'python').
project_file('src/nlp2uri/integrators/__init__.py', 23, 'python').
project_file('src/nlp2uri/integrators/mcp_server.py', 129, 'python').
project_file('src/nlp2uri/integrators/rest_server.py', 91, 'python').
project_file('src/nlp2uri/mcp.py', 82, 'python').
project_file('src/nlp2uri/models.py', 175, 'python').
project_file('src/nlp2uri/parse_nl.py', 275, 'python').
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
project_file('src/nlp2uri/schemes/build.py', 60, 'python').
project_file('src/nlp2uri/schemes/desktop.py', 95, 'python').
project_file('src/nlp2uri/schemes/file.py', 26, 'python').
project_file('src/nlp2uri/schemes/http.py', 23, 'python').
project_file('src/nlp2uri/schemes/ide.py', 36, 'python').
project_file('src/nlp2uri/schemes/util.py', 48, 'python').
project_file('src/nlp2uri/service.py', 72, 'python').
project_file('tests/conftest.py', 18, 'python').
project_file('tests/integration/test_xdg_handler.py', 99, 'python').
project_file('tests/test_adapters.py', 76, 'python').
project_file('tests/test_cli.py', 31, 'python').
project_file('tests/test_compile.py', 34, 'python').
project_file('tests/test_config.py', 65, 'python').
project_file('tests/test_mcp.py', 25, 'python').
project_file('tests/test_platforms.py', 48, 'python').
project_file('tests/test_resolve.py', 77, 'python').
project_file('tests/test_rest_server.py', 48, 'python').
project_file('tests/test_service.py', 27, 'python').
project_file('tree.sh', 2, 'shell').

% ── Python Functions ─────────────────────────────────────
python_function('examples/execute/dry-run/main.py', 'main', 0, 3, 4).
python_function('examples/mcp/tool-handoff/main.py', 'main', 0, 2, 4).
python_function('examples/resolve/nl-to-uri/main.py', 'main', 0, 3, 4).
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
python_function('src/nlp2uri/compile.py', 'compile_uri_to_actions', 2, 8, 10).
python_function('src/nlp2uri/compile.py', '_query_params', 1, 3, 3).
python_function('src/nlp2uri/compile.py', '_first_available', 1, 3, 1).
python_function('src/nlp2uri/compile.py', '_open_uri', 2, 5, 2).
python_function('src/nlp2uri/compile.py', '_compile_app', 5, 11, 13).
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
python_function('src/nlp2uri/compile.py', '_compile_window', 4, 10, 5).
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
python_function('src/nlp2uri/parse_nl.py', '_parse_settings', 2, 2, 2).
python_function('src/nlp2uri/parse_nl.py', '_parse_active_window', 2, 2, 2).
python_function('src/nlp2uri/parse_nl.py', '_capture_target', 2, 4, 1).
python_function('src/nlp2uri/parse_nl.py', '_parse_capture', 2, 6, 8).
python_function('src/nlp2uri/parse_nl.py', '_parse_focus', 2, 2, 4).
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
python_function('src/nlp2uri/schemes/build.py', 'build_uri', 1, 11, 10).
python_function('src/nlp2uri/schemes/build.py', '_build_navigate', 1, 4, 5).
python_function('src/nlp2uri/schemes/desktop.py', 'build_capture', 1, 5, 5).
python_function('src/nlp2uri/schemes/desktop.py', 'build_focus', 1, 1, 4).
python_function('src/nlp2uri/schemes/desktop.py', 'build_app_open', 1, 3, 4).
python_function('src/nlp2uri/schemes/desktop.py', 'build_settings', 0, 1, 3).
python_function('src/nlp2uri/schemes/file.py', 'build_file', 1, 3, 6).
python_function('src/nlp2uri/schemes/http.py', 'build_http', 1, 4, 3).
python_function('src/nlp2uri/schemes/ide.py', 'build_ide', 1, 4, 8).
python_function('src/nlp2uri/schemes/util.py', 'abstract_url', 4, 9, 5).
python_function('src/nlp2uri/schemes/util.py', 'nlp2uri_url', 2, 5, 3).
python_function('src/nlp2uri/schemes/util.py', 'normalize_path', 1, 2, 4).
python_function('src/nlp2uri/schemes/util.py', 'file_uri', 1, 1, 3).
python_function('src/nlp2uri/schemes/util.py', 'percent_encode_segment', 1, 1, 1).
python_function('tests/conftest.py', 'isolated_config', 2, 1, 6).
python_function('tests/integration/test_xdg_handler.py', 'test_xdg_custom_scheme_handler', 1, 7, 12).
python_function('tests/test_adapters.py', 'test_cli_adapter_plan', 0, 3, 4).
python_function('tests/test_adapters.py', 'test_rest_adapter_plan', 0, 3, 2).
python_function('tests/test_adapters.py', 'test_shell_adapter_export', 0, 4, 3).
python_function('tests/test_adapters.py', 'test_mcp_adapter_tools', 0, 4, 3).
python_function('tests/test_adapters.py', 'test_mcp_stdio_initialize', 0, 3, 2).
python_function('tests/test_adapters.py', 'test_mcp_stdio_tools_call', 0, 3, 2).
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
python_function('tests/test_mcp.py', 'test_text_uri_list_mime', 0, 3, 1).
python_function('tests/test_mcp.py', 'test_tool_resolve_desktop_action', 0, 3, 2).
python_function('tests/test_mcp.py', 'test_mcp_handoff_includes_actions', 0, 3, 1).
python_function('tests/test_platforms.py', 'test_linux_dry_run_open_app', 0, 4, 3).
python_function('tests/test_platforms.py', 'test_macos_dry_run_capture_screen', 0, 3, 1).
python_function('tests/test_platforms.py', 'test_windows_dry_run_settings', 0, 3, 2).
python_function('tests/test_platforms.py', 'test_linux_dry_run_file_uri', 0, 3, 1).
python_function('tests/test_resolve.py', 'test_resolve_linux', 3, 3, 3).
python_function('tests/test_resolve.py', 'test_polish_open_vscode_in_folder', 0, 3, 2).
python_function('tests/test_resolve.py', 'test_polish_active_browser_screenshot', 0, 3, 2).
python_function('tests/test_resolve.py', 'test_nlp2uri_returns_actions', 0, 5, 2).
python_function('tests/test_resolve.py', 'test_parse_absolute_uri_passthrough', 0, 3, 2).
python_function('tests/test_resolve.py', 'test_settings_windows', 0, 2, 1).
python_function('tests/test_resolve.py', 'test_settings_macos', 0, 2, 1).
python_function('tests/test_resolve.py', 'test_empty_input_raises', 0, 1, 2).
python_function('tests/test_rest_server.py', '_post', 2, 1, 7).
python_function('tests/test_rest_server.py', 'test_rest_server_plan', 0, 7, 8).
python_function('tests/test_service.py', 'test_from_prompt', 0, 3, 3).
python_function('tests/test_service.py', 'test_handle_prompt_dry_run', 0, 3, 3).
python_function('tests/test_service.py', 'test_handle_uri', 0, 2, 2).

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
python_method('UriIntent', 'intent_name', 0, 7, 1).
python_method('UriIntent', 'to_slots', 0, 11, 2).
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
```

## Call Graph

*75 nodes · 100 edges · 21 modules · CC̄=3.9*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `parse_text` *(in src.nlp2uri.parse_nl)* | 27 ⚠ | 2 | 55 | **57** |
| `main` *(in src.nlp2uri.cli)* | 20 ⚠ | 0 | 43 | **43** |
| `_build_parser` *(in src.nlp2uri.cli)* | 1 | 1 | 35 | **36** |
| `_compile_screenshot` *(in src.nlp2uri.compile)* | 17 ⚠ | 2 | 24 | **26** |
| `_load_from_path` *(in src.nlp2uri.config)* | 6 | 3 | 17 | **20** |
| `_compile_app` *(in src.nlp2uri.compile)* | 11 ⚠ | 1 | 18 | **19** |
| `config_search_paths` *(in src.nlp2uri.config)* | 5 | 1 | 15 | **16** |
| `execute_uri` *(in src.nlp2uri.runtime)* | 9 | 1 | 15 | **16** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/nlp2uri
# generated in 0.14s
# nodes: 75 | edges: 100 | modules: 21
# CC̄=3.9

HUBS[20]:
  src.nlp2uri.parse_nl.parse_text
    CC=27  in:2  out:55  total:57
  src.nlp2uri.cli.main
    CC=20  in:0  out:43  total:43
  src.nlp2uri.cli._build_parser
    CC=1  in:1  out:35  total:36
  src.nlp2uri.compile._compile_screenshot
    CC=17  in:2  out:24  total:26
  src.nlp2uri.config._load_from_path
    CC=6  in:3  out:17  total:20
  src.nlp2uri.compile._compile_app
    CC=11  in:1  out:18  total:19
  src.nlp2uri.config.config_search_paths
    CC=5  in:1  out:15  total:16
  src.nlp2uri.runtime.execute_uri
    CC=9  in:1  out:15  total:16
  src.nlp2uri.compile.compile_uri_to_actions
    CC=8  in:4  out:11  total:15
  src.nlp2uri.schemes.build.build_uri
    CC=11  in:2  out:13  total:15
  src.nlp2uri.compile._compile_window
    CC=10  in:2  out:12  total:14
  src.nlp2uri.compile._compile_legacy_nlp2uri
    CC=7  in:1  out:12  total:13
  src.nlp2uri.compile._open_uri
    CC=5  in:8  out:5  total:13
  src.nlp2uri.config.ensure_config
    CC=4  in:4  out:9  total:13
  src.nlp2uri.config.load_config
    CC=4  in:10  out:3  total:13
  src.nlp2uri.integrators.mcp_server.run_stdio
    CC=6  in:1  out:12  total:13
  src.nlp2uri.compile._first_available
    CC=3  in:12  out:1  total:13
  src.nlp2uri.integrators.mcp_server.handle_message
    CC=8  in:1  out:12  total:13
  src.nlp2uri.cli._add_common_args
    CC=3  in:9  out:2  total:11
  src.nlp2uri.config.NLP2URIConfig.to_yaml
    CC=6  in:0  out:11  total:11

MODULES:
  examples.execute.dry-run.main  [1 funcs]
    main  CC=3  out:7
  examples.mcp.tool-handoff.main  [1 funcs]
    main  CC=2  out:8
  examples.resolve.nl-to-uri.main  [1 funcs]
    main  CC=3  out:5
  src.nlp2uri.adapters.base  [1 funcs]
    __init__  CC=2  out:2
  src.nlp2uri.cli  [6 funcs]
    _add_common_args  CC=3  out:2
    _build_parser  CC=1  out:35
    _emit  CC=3  out:4
    _platform  CC=2  out:1
    _request_from_args  CC=3  out:7
    main  CC=20  out:43
  src.nlp2uri.compile  [11 funcs]
    _compile_app  CC=11  out:18
    _compile_launch_app  CC=7  out:8
    _compile_legacy_nlp2uri  CC=7  out:12
    _compile_screenshot  CC=17  out:24
    _compile_settings  CC=5  out:5
    _compile_window  CC=10  out:12
    _desktop_id_for_app  CC=7  out:7
    _first_available  CC=3  out:1
    _open_uri  CC=5  out:5
    _query_params  CC=3  out:3
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
  src.nlp2uri.parse_nl  [2 funcs]
    _normalize_aliases  CC=2  out:4
    parse_text  CC=27  out:55
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
    build_uri  CC=11  out:13
  src.nlp2uri.schemes.desktop  [3 funcs]
    build_app_open  CC=3  out:5
    build_capture  CC=5  out:5
    build_focus  CC=1  out:5
  src.nlp2uri.schemes.file  [1 funcs]
    build_file  CC=3  out:6
  src.nlp2uri.schemes.ide  [1 funcs]
    build_ide  CC=4  out:10
  src.nlp2uri.schemes.util  [3 funcs]
    abstract_url  CC=9  out:5
    file_uri  CC=1  out:3
    normalize_path  CC=2  out:5
  src.nlp2uri.service  [8 funcs]
    _cfg  CC=2  out:1
    _host  CC=1  out:1
    compile  CC=1  out:2
    default  CC=1  out:2
    execute  CC=2  out:3
    for_platform  CC=2  out:4
    from_prompt  CC=2  out:3
    resolve  CC=1  out:2

EDGES:
  src.nlp2uri.parse_nl.parse_text → src.nlp2uri.parse_nl._normalize_aliases
  src.nlp2uri.integrators.mcp_server.handle_message → src.nlp2uri.integrators.mcp_server._jsonrpc_error
  src.nlp2uri.integrators.mcp_server.handle_message → src.nlp2uri.integrators.mcp_server._jsonrpc_response
  src.nlp2uri.integrators.mcp_server.handle_message → src.nlp2uri.integrators.mcp_server._handle_initialize
  src.nlp2uri.integrators.mcp_server.handle_message → src.nlp2uri.integrators.mcp_server._handle_tools_list
  src.nlp2uri.integrators.mcp_server.handle_message → src.nlp2uri.integrators.mcp_server._handle_tools_call
  src.nlp2uri.integrators.mcp_server.run_stdio → src.nlp2uri.config.ensure_config
  src.nlp2uri.integrators.mcp_server.run_stdio → src.nlp2uri.config.load_config
  src.nlp2uri.integrators.mcp_server.run_stdio → src.nlp2uri.integrators.mcp_server._log
  src.nlp2uri.integrators.mcp_server.run_stdio → src.nlp2uri.integrators.mcp_server.handle_message
  src.nlp2uri.integrators.mcp_server.run_stdio → src.nlp2uri.integrators.mcp_server._write_json
  src.nlp2uri.integrators.mcp_server.main → src.nlp2uri.integrators.mcp_server.run_stdio
  examples.execute.dry-run.main.main → src.nlp2uri.resolve.nlp2uri
  examples.execute.dry-run.main.main → src.nlp2uri.compile.compile_uri_to_actions
  src.nlp2uri.cli._build_parser → src.nlp2uri.cli._add_common_args
  src.nlp2uri.cli._request_from_args → src.nlp2uri.cli._platform
  src.nlp2uri.cli.main → src.nlp2uri.cli._build_parser
  src.nlp2uri.cli.main → src.nlp2uri.cli._emit
  src.nlp2uri.cli.main → src.nlp2uri.config.ensure_config
  src.nlp2uri.cli.main → src.nlp2uri.config.load_config
  src.nlp2uri.cli.main → src.nlp2uri.config.find_config_path
  src.nlp2uri.platforms.registry.get_executor → src.nlp2uri.platform_detect.detect_platform
  examples.resolve.nl-to-uri.main.main → src.nlp2uri.resolve.nlp2uri
  examples.mcp.tool-handoff.main.main → src.nlp2uri.mcp.mcp_handoff_payload
  examples.mcp.tool-handoff.main.main → src.nlp2uri.mcp.tool_resolve_desktop_action
  src.nlp2uri.compile.compile_uri_to_actions → src.nlp2uri.compile._query_params
  src.nlp2uri.compile.compile_uri_to_actions → src.nlp2uri.platform_detect.detect_platform
  src.nlp2uri.compile.compile_uri_to_actions → src.nlp2uri.compile._compile_app
  src.nlp2uri.compile.compile_uri_to_actions → src.nlp2uri.compile._compile_screenshot
  src.nlp2uri.compile.compile_uri_to_actions → src.nlp2uri.compile._compile_window
  src.nlp2uri.compile.compile_uri_to_actions → src.nlp2uri.compile._compile_legacy_nlp2uri
  src.nlp2uri.compile.compile_uri_to_actions → src.nlp2uri.compile._open_uri
  src.nlp2uri.compile._open_uri → src.nlp2uri.compile._first_available
  src.nlp2uri.compile._compile_app → src.nlp2uri.compile._compile_settings
  src.nlp2uri.compile._compile_app → src.nlp2uri.compile._first_available
  src.nlp2uri.compile._compile_app → src.nlp2uri.compile._compile_launch_app
  src.nlp2uri.compile._compile_app → src.nlp2uri.compile._open_uri
  src.nlp2uri.compile._compile_settings → src.nlp2uri.compile._first_available
  src.nlp2uri.compile._compile_settings → src.nlp2uri.compile._open_uri
  src.nlp2uri.compile._compile_launch_app → src.nlp2uri.compile._first_available
  src.nlp2uri.compile._compile_launch_app → src.nlp2uri.compile._desktop_id_for_app
  src.nlp2uri.compile._compile_screenshot → src.nlp2uri.compile._first_available
  src.nlp2uri.compile._compile_window → src.nlp2uri.compile._first_available
  src.nlp2uri.compile._compile_window → src.nlp2uri.compile._compile_launch_app
  src.nlp2uri.compile._compile_legacy_nlp2uri → src.nlp2uri.compile._query_params
  src.nlp2uri.compile._compile_legacy_nlp2uri → src.nlp2uri.compile._compile_settings
  src.nlp2uri.compile._compile_legacy_nlp2uri → src.nlp2uri.compile._compile_launch_app
  src.nlp2uri.compile._compile_legacy_nlp2uri → src.nlp2uri.compile._compile_window
  src.nlp2uri.compile._compile_legacy_nlp2uri → src.nlp2uri.compile._compile_screenshot
  src.nlp2uri.schemes.build.build_uri → src.nlp2uri.platform_detect.detect_platform
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
