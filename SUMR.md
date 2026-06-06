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
- **version**: `0.4.4`
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
  version: 0.4.4;
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

*154 nodes · 212 edges · 31 modules · CC̄=3.6*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `build_uri_index` *(in src.nlp2uri.systemmap.index)* | 31 ⚠ | 4 | 52 | **56** |
| `_build_parser` *(in src.nlp2uri.cli)* | 1 | 1 | 35 | **36** |
| `resolve_prompt_against_system_map` *(in src.nlp2uri.systemmap.resolve)* | 26 ⚠ | 2 | 23 | **25** |
| `_compile_app` *(in src.nlp2uri.compile)* | 16 ⚠ | 1 | 21 | **22** |
| `_load_from_path` *(in src.nlp2uri.config)* | 6 | 3 | 17 | **20** |
| `_compile_runtime` *(in src.nlp2uri.systemmap.compile)* | 12 ⚠ | 1 | 18 | **19** |
| `load_ir_from_arguments` *(in src.nlp2uri.systemmap.context)* | 8 | 2 | 16 | **18** |
| `compile_uri_to_actions` *(in src.nlp2uri.compile)* | 11 ⚠ | 4 | 14 | **18** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/nlp2uri
# generated in 0.07s
# nodes: 154 | edges: 212 | modules: 31
# CC̄=3.6

HUBS[20]:
  src.nlp2uri.systemmap.index.build_uri_index
    CC=31  in:4  out:52  total:56
  src.nlp2uri.cli._build_parser
    CC=1  in:1  out:35  total:36
  src.nlp2uri.systemmap.resolve.resolve_prompt_against_system_map
    CC=26  in:2  out:23  total:25
  src.nlp2uri.compile._compile_app
    CC=16  in:1  out:21  total:22
  src.nlp2uri.config._load_from_path
    CC=6  in:3  out:17  total:20
  src.nlp2uri.systemmap.compile._compile_runtime
    CC=12  in:1  out:18  total:19
  src.nlp2uri.systemmap.context.load_ir_from_arguments
    CC=8  in:2  out:16  total:18
  src.nlp2uri.compile.compile_uri_to_actions
    CC=11  in:4  out:14  total:18
  src.nlp2uri.systemmap.encode.encode_segment
    CC=1  in:17  out:1  total:18
  src.nlp2uri.schemes.build.build_uri
    CC=13  in:2  out:15  total:17
  src.nlp2uri.systemmap.uri._get
    CC=4  in:12  out:5  total:17
  src.nlp2uri.systemmap.index._ir_field
    CC=2  in:14  out:3  total:17
  src.nlp2uri.runtime.execute_uri
    CC=9  in:1  out:15  total:16
  src.nlp2uri.compile._first_available
    CC=3  in:15  out:1  total:16
  src.nlp2uri.compile._open_uri
    CC=5  in:11  out:5  total:16
  src.nlp2uri.config.config_search_paths
    CC=5  in:1  out:15  total:16
  src.nlp2uri.systemmap.index._add_entry
    CC=3  in:11  out:4  total:15
  src.nlp2uri.compile._compile_window
    CC=11  in:2  out:13  total:15
  src.nlp2uri.systemmap.index._get_id_field
    CC=4  in:9  out:5  total:14
  examples.resolve.new-intents.e2e.print
    CC=0  in:14  out:0  total:14

MODULES:
  examples.execute.dry-run.main  [1 funcs]
    main  CC=3  out:7
  examples.mcp.tool-handoff.main  [1 funcs]
    main  CC=2  out:8
  examples.resolve.new-intents.e2e  [1 funcs]
    print  CC=0  out:0
  examples.resolve.nl-to-uri.main  [1 funcs]
    main  CC=3  out:5
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
  src.nlp2uri.service  [10 funcs]
    _cfg  CC=2  out:1
    _host  CC=1  out:1
    compile  CC=1  out:2
    default  CC=1  out:2
    execute  CC=2  out:3
    for_platform  CC=2  out:4
    from_prompt  CC=2  out:3
    list_system_uris  CC=3  out:5
    resolve  CC=1  out:2
    resolve_system_map  CC=5  out:5
  src.nlp2uri.systemmap.compile  [10 funcs]
    _backend_url  CC=1  out:2
    _compile_access  CC=2  out:5
    _compile_artifact  CC=1  out:4
    _compile_command  CC=4  out:8
    _compile_metadata  CC=2  out:4
    _compile_resource  CC=1  out:4
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
  examples.mcp.tool-handoff.main.main → examples.resolve.new-intents.e2e.print
  examples.mcp.tool-handoff.main.main → src.nlp2uri.mcp.mcp_handoff_payload
  examples.mcp.tool-handoff.main.main → src.nlp2uri.mcp.tool_resolve_desktop_action
  examples.execute.dry-run.main.main → src.nlp2uri.resolve.nlp2uri
  examples.execute.dry-run.main.main → src.nlp2uri.compile.compile_uri_to_actions
  examples.execute.dry-run.main.main → examples.resolve.new-intents.e2e.print
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
  src.nlp2uri.config.load_config → src.nlp2uri.config._load_from_path
  src.nlp2uri.config.load_config → src.nlp2uri.config.default_config
  src.nlp2uri.config.save_config → src.nlp2uri.platform_detect.detect_platform
  src.nlp2uri.config.ensure_config → src.nlp2uri.config.find_config_path
  src.nlp2uri.config.ensure_config → src.nlp2uri.config.default_config
  src.nlp2uri.config.ensure_config → src.nlp2uri.config.save_config
  src.nlp2uri.config.ensure_config → src.nlp2uri.config._load_from_path
  src.nlp2uri.config.get_effective_platform → src.nlp2uri.config.load_config
  src.nlp2uri.resolve.resolve_text → src.nlp2uri.parse_nl.parse_text
  src.nlp2uri.resolve.resolve_text → src.nlp2uri.schemes.build.build_uri
  src.nlp2uri.resolve.resolve_text → src.nlp2uri.config.get_effective_platform
  src.nlp2uri.resolve.nlp2uri → src.nlp2uri.config.get_effective_platform
  src.nlp2uri.resolve.nlp2uri → src.nlp2uri.parse_nl.parse_text
  src.nlp2uri.resolve.nlp2uri → src.nlp2uri.schemes.build.build_uri
  src.nlp2uri.resolve.nlp2uri → src.nlp2uri.compile.compile_uri_to_actions
  src.nlp2uri.resolve.nlp2uri → src.nlp2uri.config.load_config
  src.nlp2uri.integrators.rest_server.run_server → src.nlp2uri.config.ensure_config
  src.nlp2uri.integrators.rest_server.run_server → src.nlp2uri.config.load_config
  src.nlp2uri.integrators.rest_server.run_server → examples.resolve.new-intents.e2e.print
  src.nlp2uri.integrators.rest_server.main → src.nlp2uri.integrators.rest_server.run_server
  src.nlp2uri.integrators.mcp_server._log → examples.resolve.new-intents.e2e.print
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
# generated in 0.07s
# nodes: 154 | edges: 212 | modules: 31
# CC̄=3.6

HUBS[20]:
  src.nlp2uri.systemmap.index.build_uri_index
    CC=31  in:4  out:52  total:56
  src.nlp2uri.cli._build_parser
    CC=1  in:1  out:35  total:36
  src.nlp2uri.systemmap.resolve.resolve_prompt_against_system_map
    CC=26  in:2  out:23  total:25
  src.nlp2uri.compile._compile_app
    CC=16  in:1  out:21  total:22
  src.nlp2uri.config._load_from_path
    CC=6  in:3  out:17  total:20
  src.nlp2uri.systemmap.compile._compile_runtime
    CC=12  in:1  out:18  total:19
  src.nlp2uri.systemmap.context.load_ir_from_arguments
    CC=8  in:2  out:16  total:18
  src.nlp2uri.compile.compile_uri_to_actions
    CC=11  in:4  out:14  total:18
  src.nlp2uri.systemmap.encode.encode_segment
    CC=1  in:17  out:1  total:18
  src.nlp2uri.schemes.build.build_uri
    CC=13  in:2  out:15  total:17
  src.nlp2uri.systemmap.uri._get
    CC=4  in:12  out:5  total:17
  src.nlp2uri.systemmap.index._ir_field
    CC=2  in:14  out:3  total:17
  src.nlp2uri.runtime.execute_uri
    CC=9  in:1  out:15  total:16
  src.nlp2uri.compile._first_available
    CC=3  in:15  out:1  total:16
  src.nlp2uri.compile._open_uri
    CC=5  in:11  out:5  total:16
  src.nlp2uri.config.config_search_paths
    CC=5  in:1  out:15  total:16
  src.nlp2uri.systemmap.index._add_entry
    CC=3  in:11  out:4  total:15
  src.nlp2uri.compile._compile_window
    CC=11  in:2  out:13  total:15
  src.nlp2uri.systemmap.index._get_id_field
    CC=4  in:9  out:5  total:14
  examples.resolve.new-intents.e2e.print
    CC=0  in:14  out:0  total:14

MODULES:
  examples.execute.dry-run.main  [1 funcs]
    main  CC=3  out:7
  examples.mcp.tool-handoff.main  [1 funcs]
    main  CC=2  out:8
  examples.resolve.new-intents.e2e  [1 funcs]
    print  CC=0  out:0
  examples.resolve.nl-to-uri.main  [1 funcs]
    main  CC=3  out:5
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
  src.nlp2uri.service  [10 funcs]
    _cfg  CC=2  out:1
    _host  CC=1  out:1
    compile  CC=1  out:2
    default  CC=1  out:2
    execute  CC=2  out:3
    for_platform  CC=2  out:4
    from_prompt  CC=2  out:3
    list_system_uris  CC=3  out:5
    resolve  CC=1  out:2
    resolve_system_map  CC=5  out:5
  src.nlp2uri.systemmap.compile  [10 funcs]
    _backend_url  CC=1  out:2
    _compile_access  CC=2  out:5
    _compile_artifact  CC=1  out:4
    _compile_command  CC=4  out:8
    _compile_metadata  CC=2  out:4
    _compile_resource  CC=1  out:4
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
  examples.mcp.tool-handoff.main.main → examples.resolve.new-intents.e2e.print
  examples.mcp.tool-handoff.main.main → src.nlp2uri.mcp.mcp_handoff_payload
  examples.mcp.tool-handoff.main.main → src.nlp2uri.mcp.tool_resolve_desktop_action
  examples.execute.dry-run.main.main → src.nlp2uri.resolve.nlp2uri
  examples.execute.dry-run.main.main → src.nlp2uri.compile.compile_uri_to_actions
  examples.execute.dry-run.main.main → examples.resolve.new-intents.e2e.print
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
  src.nlp2uri.config.load_config → src.nlp2uri.config._load_from_path
  src.nlp2uri.config.load_config → src.nlp2uri.config.default_config
  src.nlp2uri.config.save_config → src.nlp2uri.platform_detect.detect_platform
  src.nlp2uri.config.ensure_config → src.nlp2uri.config.find_config_path
  src.nlp2uri.config.ensure_config → src.nlp2uri.config.default_config
  src.nlp2uri.config.ensure_config → src.nlp2uri.config.save_config
  src.nlp2uri.config.ensure_config → src.nlp2uri.config._load_from_path
  src.nlp2uri.config.get_effective_platform → src.nlp2uri.config.load_config
  src.nlp2uri.resolve.resolve_text → src.nlp2uri.parse_nl.parse_text
  src.nlp2uri.resolve.resolve_text → src.nlp2uri.schemes.build.build_uri
  src.nlp2uri.resolve.resolve_text → src.nlp2uri.config.get_effective_platform
  src.nlp2uri.resolve.nlp2uri → src.nlp2uri.config.get_effective_platform
  src.nlp2uri.resolve.nlp2uri → src.nlp2uri.parse_nl.parse_text
  src.nlp2uri.resolve.nlp2uri → src.nlp2uri.schemes.build.build_uri
  src.nlp2uri.resolve.nlp2uri → src.nlp2uri.compile.compile_uri_to_actions
  src.nlp2uri.resolve.nlp2uri → src.nlp2uri.config.load_config
  src.nlp2uri.integrators.rest_server.run_server → src.nlp2uri.config.ensure_config
  src.nlp2uri.integrators.rest_server.run_server → src.nlp2uri.config.load_config
  src.nlp2uri.integrators.rest_server.run_server → examples.resolve.new-intents.e2e.print
  src.nlp2uri.integrators.rest_server.main → src.nlp2uri.integrators.rest_server.run_server
  src.nlp2uri.integrators.mcp_server._log → examples.resolve.new-intents.e2e.print
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
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 68f 6256L | python:45,shell:12,yaml:6,json:2,yml:1,toml:1 | 2026-06-06
# generated in 0.01s
# CC̅=3.6 | critical:4/238 | dups:0 | cycles:0

HEALTH[4]:
  🟡 CC    _compile_app CC=16 (limit:15)
  🟡 CC    _compile_terminal CC=16 (limit:15)
  🟡 CC    resolve_prompt_against_system_map CC=26 (limit:15)
  🟡 CC    build_uri_index CC=31 (limit:15)

REFACTOR[1]:
  1. split 4 high-CC methods  (CC>15)

PIPELINES[116]:
  [1] Src [main]: main → print
      PURITY: 100% pure
  [2] Src [main]: main → nlp2uri → get_effective_platform → load_config → ...(2 more)
      PURITY: 100% pure
  [3] Src [get_executor]: get_executor
      PURITY: 100% pure
  [4] Src [resolved_platform]: resolved_platform → detect_platform
      PURITY: 100% pure
  [5] Src [apply_runtime_env]: apply_runtime_env
      PURITY: 100% pure
  [6] Src [to_dict]: to_dict → detect_platform
      PURITY: 100% pure
  [7] Src [to_yaml]: to_yaml → payload_keys
      PURITY: 100% pure
  [8] Src [text_uri_list]: text_uri_list
      PURITY: 100% pure
  [9] Src [tool_execute_desktop_uri]: tool_execute_desktop_uri
      PURITY: 100% pure
  [10] Src [__getattr__]: __getattr__
      PURITY: 100% pure
  [11] Src [_read_json]: _read_json
      PURITY: 100% pure
  [12] Src [_send]: _send
      PURITY: 100% pure
  [13] Src [do_GET]: do_GET
      PURITY: 100% pure
  [14] Src [do_POST]: do_POST
      PURITY: 100% pure
  [15] Src [main]: main → run_server → ensure_config → find_config_path → ...(1 more)
      PURITY: 100% pure
  [16] Src [main]: main → run_stdio → ensure_config → find_config_path → ...(1 more)
      PURITY: 100% pure
  [17] Src [_result]: _result
      PURITY: 100% pure
  [18] Src [_dry]: _dry
      PURITY: 100% pure
  [19] Src [_run]: _run
      PURITY: 100% pure
  [20] Src [_first_available]: _first_available
      PURITY: 100% pure
  [21] Src [_open_with_browser]: _open_with_browser
      PURITY: 100% pure
  [22] Src [_parse_nlp2uri]: _parse_nlp2uri
      PURITY: 100% pure
  [23] Src [_desktop_id_for_app]: _desktop_id_for_app
      PURITY: 100% pure
  [24] Src [slugify_app_name]: slugify_app_name
      PURITY: 100% pure
  [25] Src [execute]: execute
      PURITY: 100% pure
  [26] Src [_open_generic]: _open_generic
      PURITY: 100% pure
  [27] Src [_open_settings]: _open_settings
      PURITY: 100% pure
  [28] Src [_open_app]: _open_app
      PURITY: 100% pure
  [29] Src [_focus_app]: _focus_app
      PURITY: 100% pure
  [30] Src [_capture]: _capture
      PURITY: 100% pure
  [31] Src [get_executor]: get_executor → detect_platform
      PURITY: 100% pure
  [32] Src [execute]: execute
      PURITY: 100% pure
  [33] Src [_open]: _open
      PURITY: 100% pure
  [34] Src [_open_app]: _open_app
      PURITY: 100% pure
  [35] Src [_focus_app]: _focus_app
      PURITY: 100% pure
  [36] Src [_capture]: _capture
      PURITY: 100% pure
  [37] Src [execute]: execute
      PURITY: 100% pure
  [38] Src [_start]: _start
      PURITY: 100% pure
  [39] Src [_open_app]: _open_app
      PURITY: 100% pure
  [40] Src [_focus_app]: _focus_app
      PURITY: 100% pure
  [41] Src [_capture]: _capture
      PURITY: 100% pure
  [42] Src [to_dict]: to_dict
      PURITY: 100% pure
  [43] Src [__init__]: __init__ → load_config → find_config_path → config_search_paths
      PURITY: 100% pure
  [44] Src [with_platform]: with_platform
      PURITY: 100% pure
  [45] Src [_service_for]: _service_for
      PURITY: 100% pure
  [46] Src [handle]: handle
      PURITY: 100% pure
  [47] Src [handle]: handle
      PURITY: 100% pure
  [48] Src [_export_script]: _export_script
      PURITY: 100% pure
  [49] Src [handle]: handle
      PURITY: 100% pure
  [50] Src [dispatch]: dispatch
      PURITY: 100% pure

LAYERS:
  src/                            CC̄=3.6    ←in:0  →out:0
  │ !! compile                    423L  0C   23m  CC=16     ←4
  │ parse_nl                   376L  0C   21m  CC=6      ←1
  │ !! index                      267L  2C   11m  CC=31     ←3
  │ mcp                        255L  1C   13m  CC=6      ←0
  │ config                     230L  1C   17m  CC=8      ←7
  │ cli                        199L  0C   11m  CC=5      ←0
  │ models                     180L  7C    7m  CC=12     ←0
  │ desktop                    166L  0C    6m  CC=6      ←0
  │ compile                    163L  0C   11m  CC=12     ←1
  │ linux                      145L  1C    6m  CC=11     ←0
  │ base                       130L  1C    9m  CC=7      ←0
  │ mcp_server                 128L  0C   10m  CC=8      ←0
  │ !! resolve                    122L  1C    4m  CC=26     ←2
  │ service                    113L  1C   12m  CC=5      ←0
  │ macos                       94L  1C    5m  CC=7      ←0
  │ windows                     94L  1C    5m  CC=7      ←0
  │ uri                         93L  0C   13m  CC=5      ←1
  │ runtime                     92L  0C    2m  CC=9      ←1
  │ rest_server                 90L  1C    7m  CC=4      ←0
  │ rest                        87L  1C    4m  CC=14     ←0
  │ mcp                         81L  0C    5m  CC=2      ←1
  │ shell                       66L  1C    2m  CC=11     ←0
  │ build                       64L  0C    2m  CC=13     ←1
  │ base                        59L  3C    5m  CC=2      ←0
  │ fallback                    52L  0C    1m  CC=6      ←1
  │ __init__                    51L  0C    0m  CC=0.0    ←0
  │ util                        47L  0C    5m  CC=9      ←3
  │ context                     47L  0C    2m  CC=8      ←1
  │ load                        46L  0C    4m  CC=3      ←1
  │ resolve                     40L  0C    2m  CC=4      ←4
  │ cli                         39L  1C    1m  CC=10     ←0
  │ ide                         35L  0C    1m  CC=4      ←0
  │ __init__                    28L  0C    0m  CC=0.0    ←0
  │ file                        25L  0C    1m  CC=3      ←0
  │ registry                    24L  0C    1m  CC=3      ←0
  │ __init__                    22L  0C    1m  CC=3      ←0
  │ http                        22L  0C    1m  CC=4      ←0
  │ platform_detect             18L  0C    1m  CC=5      ←4
  │ __init__                    17L  0C    0m  CC=0.0    ←0
  │ encode                      15L  0C    2m  CC=1      ←1
  │ __init__                     6L  0C    0m  CC=0.0    ←0
  │ __init__                     5L  0C    0m  CC=0.0    ←0
  │
  examples/                       CC̄=2.0    ←in:0  →out:0
  │ main                        46L  0C    1m  CC=3      ←0
  │ run-e2e.sh                  40L  0C    0m  CC=0.0    ←0
  │ main                        29L  0C    1m  CC=3      ←0
  │ main                        27L  0C    1m  CC=2      ←0
  │ e2e.sh                      25L  0C    1m  CC=0.0    ←6
  │ e2e.sh                      23L  0C    0m  CC=0.0    ←0
  │ e2e.sh                      15L  0C    0m  CC=0.0    ←0
  │ e2e.sh                      12L  0C    0m  CC=0.0    ←0
  │ e2e.sh                      11L  0C    0m  CC=0.0    ←0
  │ e2e.sh                      11L  0C    0m  CC=0.0    ←0
  │ e2e.sh                      11L  0C    0m  CC=0.0    ←0
  │ mcp-config.cursor.json      11L  0C    0m  CC=0.0    ←0
  │ mcp-config.json             10L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! planfile.yaml              890L  0C    0m  CC=0.0    ←0
  │ !! goal.yaml                  511L  0C    0m  CC=0.0    ←0
  │ prefact.yaml                94L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              71L  0C    0m  CC=0.0    ←0
  │ project.sh                  59L  0C    0m  CC=0.0    ←0
  │ Dockerfile                  29L  0C    0m  CC=0.0    ←0
  │ nlp2uri.yaml                 8L  0C    0m  CC=0.0    ←0
  │ docker-compose.yml           6L  0C    0m  CC=0.0    ←0
  │ tree.sh                      1L  0C    0m  CC=0.0    ←0
  │
  scripts/                        CC̄=0.0    ←in:0  →out:0
  │ install-editable.sh         22L  0C    0m  CC=0.0    ←0
  │ testapp-handler.sh           6L  0C    0m  CC=0.0    ←0
  │
  testql-scenarios/               CC̄=0.0    ←in:0  →out:0
  │ generated-cli-tests.testql.toon.yaml    20L  0C    0m  CC=0.0    ←0
  │ generated-from-pytests.testql.toon.yaml    12L  0C    0m  CC=0.0    ←0
  │

COUPLING:
                    examples.resolve       src.nlp2uri  examples.execute      examples.mcp
  examples.resolve                ──                 1                ←4                ←4  hub
       src.nlp2uri                 4                ──                ←2                ←2  hub
  examples.execute                 4                 2                ──                  
      examples.mcp                 4                 2                                  ──
  CYCLES: none
  HUB: src.nlp2uri/ (fan-in=5)
  HUB: examples.resolve/ (fan-in=12)

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 5 groups | 45f 4358L | 2026-06-06

SUMMARY:
  files_scanned: 45
  total_lines:   4358
  dup_groups:    5
  dup_fragments: 10
  saved_lines:   40
  scan_ms:       2490

HOTSPOTS[4] (files with most duplication):
  src/nlp2uri/schemes/desktop.py  dup=36L  groups=1  frags=2  (0.8%)
  src/nlp2uri/parse_nl.py  dup=22L  groups=1  frags=2  (0.5%)
  src/nlp2uri/systemmap/uri.py  dup=14L  groups=2  frags=4  (0.3%)
  src/nlp2uri/systemmap/compile.py  dup=8L  groups=1  frags=2  (0.2%)

DUPLICATES[5] (ranked by impact):
  [b1482ea46475566a]   STRU  build_focus  L=18 N=2 saved=18 sim=1.00
      src/nlp2uri/schemes/desktop.py:40-57  (build_focus)
      src/nlp2uri/schemes/desktop.py:102-119  (build_move)
  [42faf2df3d26832c]   STRU  _parse_file_open  L=11 N=2 saved=11 sim=1.00
      src/nlp2uri/parse_nl.py:152-162  (_parse_file_open)
      src/nlp2uri/parse_nl.py:294-304  (_parse_app_open)
  [b578baca21b73515]   STRU  _compile_resource  L=4 N=2 saved=4 sim=1.00
      src/nlp2uri/systemmap/compile.py:141-144  (_compile_resource)
      src/nlp2uri/systemmap/compile.py:147-150  (_compile_artifact)
  [3d6c0029f92cde72]   STRU  uri_for_schedule  L=4 N=2 saved=4 sim=1.00
      src/nlp2uri/systemmap/uri.py:79-82  (uri_for_schedule)
      src/nlp2uri/systemmap/uri.py:85-88  (uri_for_generated_service)
  [ff8711d5a6139426]   STRU  uri_for_conversation  L=3 N=2 saved=3 sim=1.00
      src/nlp2uri/systemmap/uri.py:63-65  (uri_for_conversation)
      src/nlp2uri/systemmap/uri.py:68-70  (uri_for_process)

REFACTOR[5] (ranked by priority):
  [1] ○ extract_function   → src/nlp2uri/schemes/utils/build_focus.py
      WHY: 2 occurrences of 18-line block across 1 files — saves 18 lines
      FILES: src/nlp2uri/schemes/desktop.py
  [2] ○ extract_function   → src/nlp2uri/utils/_parse_file_open.py
      WHY: 2 occurrences of 11-line block across 1 files — saves 11 lines
      FILES: src/nlp2uri/parse_nl.py
  [3] ○ extract_function   → src/nlp2uri/systemmap/utils/_compile_resource.py
      WHY: 2 occurrences of 4-line block across 1 files — saves 4 lines
      FILES: src/nlp2uri/systemmap/compile.py
  [4] ○ extract_function   → src/nlp2uri/systemmap/utils/uri_for_schedule.py
      WHY: 2 occurrences of 4-line block across 1 files — saves 4 lines
      FILES: src/nlp2uri/systemmap/uri.py
  [5] ○ extract_function   → src/nlp2uri/systemmap/utils/uri_for_conversation.py
      WHY: 2 occurrences of 3-line block across 1 files — saves 3 lines
      FILES: src/nlp2uri/systemmap/uri.py

QUICK_WINS[2] (low risk, high savings — do first):
  [1] extract_function   saved=18L  → src/nlp2uri/schemes/utils/build_focus.py
      FILES: desktop.py
  [2] extract_function   saved=11L  → src/nlp2uri/utils/_parse_file_open.py
      FILES: parse_nl.py

EFFORT_ESTIMATE (total ≈ 1.3h):
  medium build_focus                         saved=18L  ~36min
  easy   _parse_file_open                    saved=11L  ~22min
  easy   _compile_resource                   saved=4L  ~8min
  easy   uri_for_schedule                    saved=4L  ~8min
  easy   uri_for_conversation                saved=3L  ~6min

METRICS-TARGET:
  dup_groups:  5 → 0
  saved_lines: 40 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 234 func | 37f | 2026-06-06
# generated in 0.00s

NEXT[5] (ranked by impact):
  [1] !! SPLIT-FUNC      build_uri_index  CC=31  fan=20
      WHY: CC=31 exceeds 15
      EFFORT: ~1h  IMPACT: 620

  [2] !! SPLIT-FUNC      resolve_prompt_against_system_map  CC=26  fan=13
      WHY: CC=26 exceeds 15
      EFFORT: ~1h  IMPACT: 338

  [3] !  SPLIT-FUNC      _compile_app  CC=16  fan=16
      WHY: CC=16 exceeds 15
      EFFORT: ~1h  IMPACT: 256

  [4] !! SPLIT           planfile.yaml
      WHY: 890L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0

  [5] !! SPLIT           goal.yaml
      WHY: 511L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[2]:
  ⚠ Splitting planfile.yaml may break 0 import paths
  ⚠ Splitting goal.yaml may break 0 import paths

METRICS-TARGET:
  CC̄:          3.6 → ≤2.5
  max-CC:      31 → ≤15
  god-modules: 2 → 0
  high-CC(≥15): 4 → ≤2
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
  prev CC̄=3.9 → now CC̄=3.6
```

## Intent

Natural language to URI resolution and cross-platform local URI execution
