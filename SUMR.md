# nlp2uri

SUMD - Structured Unified Markdown Descriptor for AI-aware project refactorization

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Dependencies](#dependencies)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Refactoring Analysis](#refactoring-analysis)
- [Intent](#intent)

## Metadata

- **name**: `nlp2uri`
- **version**: `0.1.2`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, testql(2), app.doql.less, goal.yaml, .env.example, Dockerfile, docker-compose.yml, project/(5 analysis files)

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

## Refactoring Analysis

*Pre-refactoring snapshot — use this section to identify targets. Generated from `project/` toon files.*

### Call Graph & Complexity (`project/calls.toon.yaml`)

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

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 52f 3779L | python:36,shell:10,yaml:3,toml:1,yml:1 | 2026-06-06
# generated in 0.03s
# CC̅=3.9 | critical:3/148 | dups:0 | cycles:0

HEALTH[3]:
  🟡 CC    parse_text CC=27 (limit:15)
  🟡 CC    main CC=20 (limit:15)
  🟡 CC    _compile_screenshot CC=17 (limit:15)

REFACTOR[1]:
  1. split 3 high-CC methods  (CC>15)

PIPELINES[89]:
  [1] Src [main]: main → run_stdio → ensure_config → find_config_path → ...(1 more)
      PURITY: 100% pure
  [2] Src [main]: main → nlp2uri → get_effective_platform → load_config → ...(2 more)
      PURITY: 100% pure
  [3] Src [main]: main → _build_parser → _add_common_args
      PURITY: 100% pure
  [4] Src [_result]: _result
      PURITY: 100% pure
  [5] Src [_dry]: _dry
      PURITY: 100% pure
  [6] Src [_run]: _run
      PURITY: 100% pure
  [7] Src [_first_available]: _first_available
      PURITY: 100% pure
  [8] Src [_open_with_browser]: _open_with_browser
      PURITY: 100% pure
  [9] Src [_parse_nlp2uri]: _parse_nlp2uri
      PURITY: 100% pure
  [10] Src [_desktop_id_for_app]: _desktop_id_for_app
      PURITY: 100% pure
  [11] Src [slugify_app_name]: slugify_app_name
      PURITY: 100% pure
  [12] Src [get_executor]: get_executor → detect_platform
      PURITY: 100% pure
  [13] Src [__getattr__]: __getattr__
      PURITY: 100% pure
  [14] Src [execute]: execute
      PURITY: 100% pure
  [15] Src [_start]: _start
      PURITY: 100% pure
  [16] Src [_open_app]: _open_app
      PURITY: 100% pure
  [17] Src [_focus_app]: _focus_app
      PURITY: 100% pure
  [18] Src [_capture]: _capture
      PURITY: 100% pure
  [19] Src [execute]: execute
      PURITY: 100% pure
  [20] Src [_open]: _open
      PURITY: 100% pure
  [21] Src [_open_app]: _open_app
      PURITY: 100% pure
  [22] Src [_focus_app]: _focus_app
      PURITY: 100% pure
  [23] Src [_capture]: _capture
      PURITY: 100% pure
  [24] Src [text_uri_list]: text_uri_list
      PURITY: 100% pure
  [25] Src [tool_execute_desktop_uri]: tool_execute_desktop_uri
      PURITY: 100% pure
  [26] Src [main]: main → nlp2uri → get_effective_platform → load_config → ...(2 more)
      PURITY: 100% pure
  [27] Src [main]: main → mcp_handoff_payload
      PURITY: 100% pure
  [28] Src [build_http]: build_http
      PURITY: 100% pure
  [29] Src [execute]: execute
      PURITY: 100% pure
  [30] Src [_open_generic]: _open_generic
      PURITY: 100% pure
  [31] Src [_open_settings]: _open_settings
      PURITY: 100% pure
  [32] Src [_open_app]: _open_app
      PURITY: 100% pure
  [33] Src [_focus_app]: _focus_app
      PURITY: 100% pure
  [34] Src [_capture]: _capture
      PURITY: 100% pure
  [35] Src [build_file]: build_file → normalize_path
      PURITY: 100% pure
  [36] Src [build_ide]: build_ide → normalize_path
      PURITY: 100% pure
  [37] Src [nlp2uri_url]: nlp2uri_url
      PURITY: 100% pure
  [38] Src [percent_encode_segment]: percent_encode_segment
      PURITY: 100% pure
  [39] Src [build_capture]: build_capture → abstract_url
      PURITY: 100% pure
  [40] Src [build_focus]: build_focus → abstract_url
      PURITY: 100% pure
  [41] Src [build_app_open]: build_app_open → abstract_url
      PURITY: 100% pure
  [42] Src [build_settings]: build_settings
      PURITY: 100% pure
  [43] Src [handle]: handle
      PURITY: 100% pure
  [44] Src [with_params]: with_params
      PURITY: 100% pure
  [45] Src [to_slots]: to_slots
      PURITY: 100% pure
  [46] Src [to_dict]: to_dict
      PURITY: 100% pure
  [47] Src [to_dict]: to_dict
      PURITY: 100% pure
  [48] Src [to_dict]: to_dict
      PURITY: 100% pure
  [49] Src [to_dict]: to_dict
      PURITY: 100% pure
  [50] Src [get_executor]: get_executor
      PURITY: 100% pure

LAYERS:
  src/                            CC̄=3.9    ←in:0  →out:0
  │ !! compile                    258L  0C   11m  CC=17     ←4
  │ config                     230L  1C   17m  CC=8      ←7
  │ !! parse_nl                   218L  0C    3m  CC=27     ←1
  │ !! cli                        185L  0C    6m  CC=20     ←0
  │ mcp                        183L  1C   11m  CC=6      ←0
  │ models                     174L  7C    7m  CC=11     ←0
  │ linux                      145L  1C    6m  CC=11     ←0
  │ base                       130L  1C    9m  CC=7      ←0
  │ mcp_server                 128L  0C   10m  CC=8      ←0
  │ windows                     94L  1C    5m  CC=7      ←0
  │ macos                       94L  1C    5m  CC=7      ←0
  │ desktop                     94L  0C    4m  CC=5      ←0
  │ runtime                     92L  0C    2m  CC=9      ←1
  │ rest_server                 90L  1C    7m  CC=4      ←0
  │ rest                        87L  1C    4m  CC=14     ←0
  │ mcp                         81L  0C    5m  CC=2      ←1
  │ service                     71L  1C   10m  CC=2      ←0
  │ shell                       66L  1C    2m  CC=11     ←0
  │ build                       59L  0C    2m  CC=11     ←1
  │ base                        59L  3C    5m  CC=2      ←0
  │ util                        47L  0C    5m  CC=9      ←3
  │ resolve                     40L  0C    2m  CC=4      ←3
  │ cli                         39L  1C    1m  CC=10     ←0
  │ ide                         35L  0C    1m  CC=4      ←0
  │ __init__                    28L  0C    0m  CC=0.0    ←0
  │ file                        25L  0C    1m  CC=3      ←0
  │ registry                    24L  0C    1m  CC=3      ←0
  │ __init__                    22L  0C    1m  CC=3      ←0
  │ http                        22L  0C    1m  CC=4      ←0
  │ platform_detect             18L  0C    1m  CC=5      ←4
  │ __init__                    17L  0C    0m  CC=0.0    ←0
  │ __init__                     6L  0C    0m  CC=0.0    ←0
  │ __init__                     5L  0C    0m  CC=0.0    ←0
  │
  examples/                       CC̄=2.7    ←in:0  →out:0
  │ main                        42L  0C    1m  CC=3      ←0
  │ run-e2e.sh                  39L  0C    0m  CC=0.0    ←0
  │ main                        29L  0C    1m  CC=3      ←0
  │ main                        27L  0C    1m  CC=2      ←0
  │ e2e.sh                      23L  0C    0m  CC=0.0    ←0
  │ e2e.sh                      12L  0C    0m  CC=0.0    ←0
  │ e2e.sh                      11L  0C    0m  CC=0.0    ←0
  │ e2e.sh                      11L  0C    0m  CC=0.0    ←0
  │ e2e.sh                      11L  0C    0m  CC=0.0    ←0
  │ e2e.sh                      10L  0C    0m  CC=0.0    ←0
  │ nlp2uri.yaml                 8L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! goal.yaml                  511L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              70L  0C    0m  CC=0.0    ←0
  │ project.sh                  59L  0C    0m  CC=0.0    ←0
  │ Dockerfile                  29L  0C    0m  CC=0.0    ←0
  │ nlp2uri.yaml                 8L  0C    0m  CC=0.0    ←0
  │ docker-compose.yml           6L  0C    0m  CC=0.0    ←0
  │ tree.sh                      1L  0C    0m  CC=0.0    ←0
  │
  scripts/                        CC̄=0.0    ←in:0  →out:0
  │ testapp-handler.sh           6L  0C    0m  CC=0.0    ←0
  │

COUPLING:
                         src.nlp2uri  examples.execute      examples.mcp  examples.resolve
       src.nlp2uri                ──                ←2                ←2                ←1  hub
  examples.execute                 2                ──                                    
      examples.mcp                 2                                  ──                  
  examples.resolve                 1                                                    ──
  CYCLES: none
  HUB: src.nlp2uri/ (fan-in=5)

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 0 groups | 36f 2964L | 2026-06-06

SUMMARY:
  files_scanned: 36
  total_lines:   2964
  dup_groups:    0
  dup_fragments: 0
  saved_lines:   0
  scan_ms:       4217
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 145 func | 29f | 2026-06-06
# generated in 0.00s

NEXT[4] (ranked by impact):
  [1] !! SPLIT-FUNC      parse_text  CC=27  fan=26
      WHY: CC=27 exceeds 15
      EFFORT: ~1h  IMPACT: 702

  [2] !  SPLIT-FUNC      main  CC=20  fan=26
      WHY: CC=20 exceeds 15
      EFFORT: ~1h  IMPACT: 520

  [3] !  SPLIT-FUNC      _compile_screenshot  CC=17  fan=7
      WHY: CC=17 exceeds 15
      EFFORT: ~1h  IMPACT: 119

  [4] !! SPLIT           goal.yaml
      WHY: 511L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[1]:
  ⚠ Splitting goal.yaml may break 0 import paths

METRICS-TARGET:
  CC̄:          3.9 → ≤2.7
  max-CC:      27 → ≤13
  god-modules: 1 → 0
  high-CC(≥15): 3 → ≤1
  hub-types:   0 → ≤0

PATTERNS (language parser shared logic):
  _extract_declarations() in base.py — unified extraction for:
    - TypeScript: interfaces, types, classes, functions, arrow funcs
    - PHP: namespaces, traits, classes, functions, includes
    - Ruby: modules, classes, methods, requires
    - C++: classes, structs, functions, #includes
    - C#: classes, interfaces, methods, usings
    - Java: classes, interfaces, methods, imports
    - Go: packages, functions, structs
    - Rust: modules, functions, traits, use statements

  Shared regex patterns per language:
    - import: language-specific import/require/using patterns
    - class: class/struct/trait declarations with inheritance
    - function: function/method signatures with visibility
    - brace_tracking: for C-family languages ({ })
    - end_keyword_tracking: for Ruby (module/class/def...end)

  Benefits:
    - Consistent extraction logic across all languages
    - Reduced code duplication (~70% reduction in parser LOC)
    - Easier maintenance: fix once, apply everywhere
    - Standardized FunctionInfo/ClassInfo models

HISTORY:
  (first run — no previous data)
```

## Intent

Natural language to URI resolution and cross-platform local URI execution
