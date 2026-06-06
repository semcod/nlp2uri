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
- **version**: `0.4.6`
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
  version: 0.4.6;
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
| `resolve_artifact_path` *(in src.nlp2uri.host.artifact)* | 12 ⚠ | 1 | 22 | **23** |
| `encode_segment` *(in src.nlp2uri.systemmap.encode)* | 1 | 22 | 1 | **23** |
| `main` *(in schemas.codegen.export_driver_stubs)* | 11 ⚠ | 0 | 23 | **23** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/nlp2uri
# generated in 0.26s
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
  src.nlp2uri.host.artifact.resolve_artifact_path
    CC=12  in:1  out:22  total:23
  src.nlp2uri.systemmap.encode.encode_segment
    CC=1  in:22  out:1  total:23
  schemas.codegen.export_driver_stubs.main
    CC=11  in:0  out:23  total:23
  src.nlp2uri.compile.compile_uri_to_actions
    CC=13  in:5  out:18  total:23
  src.nlp2uri.compile._compile_app
    CC=16  in:1  out:21  total:22
  src.nlp2uri.config._load_from_path
    CC=6  in:3  out:17  total:20
  src.nlp2uri.systemmap.getv_uri.compile_getv_uri
    CC=14  in:2  out:18  total:20
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
  src.nlp2uri.systemmap.uri._get
    CC=4  in:12  out:5  total:17
  src.nlp2uri.schemes.build.build_uri
    CC=13  in:2  out:15  total:17

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

## Refactoring Analysis

*Pre-refactoring snapshot — use this section to identify targets. Generated from `project/` toon files.*

### Call Graph & Complexity (`project/calls.toon.yaml`)

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/nlp2uri
# generated in 0.26s
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
  src.nlp2uri.host.artifact.resolve_artifact_path
    CC=12  in:1  out:22  total:23
  src.nlp2uri.systemmap.encode.encode_segment
    CC=1  in:22  out:1  total:23
  schemas.codegen.export_driver_stubs.main
    CC=11  in:0  out:23  total:23
  src.nlp2uri.compile.compile_uri_to_actions
    CC=13  in:5  out:18  total:23
  src.nlp2uri.compile._compile_app
    CC=16  in:1  out:21  total:22
  src.nlp2uri.config._load_from_path
    CC=6  in:3  out:17  total:20
  src.nlp2uri.systemmap.getv_uri.compile_getv_uri
    CC=14  in:2  out:18  total:20
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
  src.nlp2uri.systemmap.uri._get
    CC=4  in:12  out:5  total:17
  src.nlp2uri.schemes.build.build_uri
    CC=13  in:2  out:15  total:17

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

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 262f 14257L | proto:138,python:72,yaml:31,shell:15,json:2,yml:1,toml:1 | 2026-06-06
# generated in 0.07s
# CC̅=3.5 | critical:4/346 | dups:0 | cycles:0

HEALTH[4]:
  🟡 CC    _compile_app CC=16 (limit:15)
  🟡 CC    _compile_terminal CC=16 (limit:15)
  🟡 CC    build_uri_index CC=31 (limit:15)
  🟡 CC    resolve_prompt_against_system_map CC=26 (limit:15)

REFACTOR[1]:
  1. split 4 high-CC methods  (CC>15)

PIPELINES[169]:
  [1] Src [main]: main → fix_api → _pascal
      PURITY: 100% pure
  [2] Src [main]: main → print
      PURITY: 100% pure
  [3] Src [main]: main → print
      PURITY: 100% pure
  [4] Src [main]: main → print
      PURITY: 100% pure
  [5] Src [main]: main → print
      PURITY: 100% pure
  [6] Src [main]: main → nlp2uri → get_effective_platform → load_config → ...(2 more)
      PURITY: 100% pure
  [7] Src [main]: main → nlp2uri → get_effective_platform → load_config → ...(2 more)
      PURITY: 100% pure
  [8] Src [get_executor]: get_executor
      PURITY: 100% pure
  [9] Src [resolved_platform]: resolved_platform → detect_platform
      PURITY: 100% pure
  [10] Src [apply_runtime_env]: apply_runtime_env
      PURITY: 100% pure
  [11] Src [to_dict]: to_dict → detect_platform
      PURITY: 100% pure
  [12] Src [to_yaml]: to_yaml → payload_keys
      PURITY: 100% pure
  [13] Src [text_uri_list]: text_uri_list
      PURITY: 100% pure
  [14] Src [tool_execute_desktop_uri]: tool_execute_desktop_uri
      PURITY: 100% pure
  [15] Src [main]: main → ensure_config → find_config_path → config_search_paths
      PURITY: 100% pure
  [16] Src [_parse_absolute_uri]: _parse_absolute_uri
      PURITY: 100% pure
  [17] Src [_parse_http_url]: _parse_http_url
      PURITY: 100% pure
  [18] Src [_parse_ide_project]: _parse_ide_project → _strip_quotes
      PURITY: 100% pure
  [19] Src [_parse_file_open]: _parse_file_open → _strip_quotes
      PURITY: 100% pure
  [20] Src [_parse_settings_panel]: _parse_settings_panel → _normalize_panel
      PURITY: 100% pure
  [21] Src [_parse_terminal]: _parse_terminal → _strip_quotes
      PURITY: 100% pure
  [22] Src [_parse_window_move]: _parse_window_move
      PURITY: 100% pure
  [23] Src [_parse_settings]: _parse_settings
      PURITY: 100% pure
  [24] Src [_parse_active_window]: _parse_active_window
      PURITY: 100% pure
  [25] Src [_parse_capture]: _parse_capture → _strip_quotes
      PURITY: 100% pure
  [26] Src [_parse_focus]: _parse_focus
      PURITY: 100% pure
  [27] Src [_parse_app_open]: _parse_app_open → _normalize_app_name
      PURITY: 100% pure
  [28] Src [_parse_path]: _parse_path → _strip_quotes
      PURITY: 100% pure
  [29] Src [_parse_open_prefix]: _parse_open_prefix → _normalize_app_name
      PURITY: 100% pure
  [30] Src [with_params]: with_params
      PURITY: 100% pure
  [31] Src [to_slots]: to_slots
      PURITY: 100% pure
  [32] Src [to_dict]: to_dict
      PURITY: 100% pure
  [33] Src [to_dict]: to_dict
      PURITY: 100% pure
  [34] Src [to_dict]: to_dict
      PURITY: 100% pure
  [35] Src [to_dict]: to_dict
      PURITY: 100% pure
  [36] Src [default]: default → ensure_config → find_config_path → config_search_paths
      PURITY: 100% pure
  [37] Src [for_platform]: for_platform → load_config → find_config_path → config_search_paths
      PURITY: 100% pure
  [38] Src [_cfg]: _cfg → load_config → find_config_path → config_search_paths
      PURITY: 100% pure
  [39] Src [_host]: _host → get_effective_platform → load_config → find_config_path → ...(1 more)
      PURITY: 100% pure
  [40] Src [from_prompt]: from_prompt → nlp2uri → get_effective_platform → load_config → ...(2 more)
      PURITY: 100% pure
  [41] Src [resolve]: resolve → resolve_text → parse_text → _normalize_aliases
      PURITY: 100% pure
  [42] Src [compile]: compile → compile_uri_to_actions → _query_params
      PURITY: 100% pure
  [43] Src [execute]: execute → execute_uri → get_effective_platform → load_config → ...(2 more)
      PURITY: 100% pure
  [44] Src [handle_prompt]: handle_prompt
      PURITY: 100% pure
  [45] Src [handle_uri]: handle_uri
      PURITY: 100% pure
  [46] Src [list_system_uris]: list_system_uris → build_uri_index → _ir_field
      PURITY: 100% pure
  [47] Src [resolve_system_map]: resolve_system_map → resolve_prompt_against_system_map → _normalize_token
      PURITY: 100% pure
  [48] Src [list_getv_uris]: list_getv_uris → build_getv_uri_index → getv_home
      PURITY: 100% pure
  [49] Src [resolve_getv]: resolve_getv → resolve_prompt_against_getv → build_getv_uri_index → getv_home
      PURITY: 100% pure
  [50] Src [read_getv_var]: read_getv_var → get_getv_var_value → _decode_segment
      PURITY: 100% pure

LAYERS:
  src/                            CC̄=3.6    ←in:0  →out:0
  │ !! compile                    431L  0C   23m  CC=16     ←5
  │ mcp                        382L  1C   18m  CC=6      ←0
  │ parse_nl                   376L  0C   21m  CC=6      ←1
  │ !! index                      267L  2C   11m  CC=31     ←4
  │ config                     230L  1C   17m  CC=8      ←7
  │ getv_uri                   225L  1C    9m  CC=14     ←3
  │ cli                        199L  0C   11m  CC=5      ←0
  │ models                     180L  7C    7m  CC=12     ←0
  │ compile                    179L  0C   11m  CC=12     ←5
  │ desktop                    166L  0C    6m  CC=6      ←0
  │ service                    151L  1C   15m  CC=5      ←0
  │ linux                      145L  1C    6m  CC=11     ←0
  │ base                       130L  1C    9m  CC=7      ←0
  │ mcp_server                 128L  0C   10m  CC=8      ←0
  │ service_ops                128L  3C    8m  CC=5      ←0
  │ !! resolve                    122L  1C    4m  CC=26     ←2
  │ dispatcher                 117L  1C    4m  CC=5      ←0
  │ base                        97L  5C    4m  CC=8      ←0
  │ getv_load                   97L  0C    8m  CC=8      ←1
  │ registry                    97L  1C    6m  CC=8      ←1
  │ macos                       94L  1C    5m  CC=7      ←0
  │ windows                     94L  1C    5m  CC=7      ←0
  │ artifact                    94L  0C    4m  CC=13     ←2
  │ uri                         93L  0C   13m  CC=5      ←1
  │ runtime                     92L  0C    2m  CC=9      ←1
  │ rest_server                 90L  1C    7m  CC=4      ←0
  │ container_docker            88L  1C    4m  CC=14     ←0
  │ rest                        87L  1C    4m  CC=14     ←0
  │ mcp                         81L  0C    5m  CC=2      ←1
  │ resource                    69L  0C    4m  CC=14     ←2
  │ __init__                    68L  0C    0m  CC=0.0    ←0
  │ event_store                 67L  2C    5m  CC=3      ←0
  │ shell                       66L  1C    2m  CC=11     ←0
  │ build                       64L  0C    2m  CC=13     ←1
  │ plugins                     64L  0C    3m  CC=7      ←1
  │ base                        59L  3C    5m  CC=2      ←0
  │ http_store                  52L  1C    3m  CC=3      ←0
  │ fallback                    52L  0C    1m  CC=6      ←1
  │ util                        47L  0C    5m  CC=9      ←3
  │ context                     47L  0C    2m  CC=8      ←1
  │ load                        46L  0C    4m  CC=3      ←1
  │ resolve                     40L  0C    2m  CC=4      ←4
  │ cli                         39L  1C    1m  CC=10     ←0
  │ command_curl                39L  1C    2m  CC=5      ←0
  │ ide                         35L  0C    1m  CC=4      ←0
  │ resource_probe              35L  1C    2m  CC=5      ←0
  │ endpoint                    34L  0C    3m  CC=8      ←2
  │ runtime_curl                34L  1C    2m  CC=3      ←0
  │ endpoint_curl               33L  1C    2m  CC=2      ←0
  │ artifact_filesystem         32L  1C    1m  CC=7      ←0
  │ delegate                    29L  1C    2m  CC=2      ←0
  │ __init__                    29L  0C    0m  CC=0.0    ←0
  │ __init__                    28L  0C    0m  CC=0.0    ←0
  │ getv_cli                    27L  1C    1m  CC=2      ←0
  │ file                        25L  0C    1m  CC=3      ←0
  │ registry                    24L  0C    1m  CC=3      ←0
  │ __init__                    22L  0C    1m  CC=3      ←0
  │ http                        22L  0C    1m  CC=4      ←0
  │ platform_detect             18L  0C    1m  CC=5      ←5
  │ __init__                    17L  0C    0m  CC=0.0    ←0
  │ encode                      15L  0C    2m  CC=1      ←2
  │ __init__                    15L  0C    0m  CC=0.0    ←0
  │ __init__                     8L  0C    0m  CC=0.0    ←0
  │ __init__                     6L  0C    0m  CC=0.0    ←0
  │ __init__                     5L  0C    0m  CC=0.0    ←0
  │
  schemas/                        CC̄=2.4    ←in:0  →out:0
  │ scaffold_scheme            357L  0C   13m  CC=4      ←0
  │ registry.yaml              184L  0C    0m  CC=0.0    ←0
  │ export_driver_stubs         97L  0C    1m  CC=11     ←0
  │ fix_proto_imports           83L  0C    4m  CC=4      ←0
  │ driver.proto                70L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                68L  0C    0m  CC=0.0    ←0
  │ events.proto                66L  0C    0m  CC=0.0    ←0
  │ queries.proto               60L  0C    0m  CC=0.0    ←0
  │ uri.proto                   60L  0C    0m  CC=0.0    ←0
  │ export_mcp_schemas          53L  0C    2m  CC=4      ←0
  │ generate.sh                 53L  0C    0m  CC=0.0    ←0
  │ commands.proto              45L  0C    0m  CC=0.0    ←0
  │ commands.proto              45L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ events.proto                42L  0C    0m  CC=0.0    ←0
  │ commands.proto              41L  0C    0m  CC=0.0    ←0
  │ api.proto                   32L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              31L  0C    0m  CC=0.0    ←0
  │ commands.proto              29L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ Makefile                    24L  0C    0m  CC=0.0    ←0
  │ buf.yaml                    15L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ driver.proto                14L  0C    0m  CC=0.0    ←0
  │ buf.gen.yaml                13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ aggregate.proto             13L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │ queries.proto               10L  0C    0m  CC=0.0    ←0
  │
  examples/                       CC̄=2.0    ←in:0  →out:0
  │ main                        46L  0C    1m  CC=3      ←0
  │ run-e2e.sh                  40L  0C    0m  CC=0.0    ←0
  │ main                        29L  0C    1m  CC=3      ←0
  │ main                        27L  0C    1m  CC=2      ←0
  │ e2e.sh                      25L  0C    1m  CC=0.0    ←10
  │ e2e.sh                      23L  0C    0m  CC=0.0    ←0
  │ e2e.sh                      15L  0C    0m  CC=0.0    ←0
  │ e2e.sh                      12L  0C    0m  CC=0.0    ←0
  │ mcp-config.cursor.json      11L  0C    0m  CC=0.0    ←0
  │ e2e.sh                      11L  0C    0m  CC=0.0    ←0
  │ e2e.sh                      11L  0C    0m  CC=0.0    ←0
  │ e2e.sh                      11L  0C    0m  CC=0.0    ←0
  │ mcp-config.json             10L  0C    0m  CC=0.0    ←0
  │
  scripts/                        CC̄=0.0    ←in:0  →out:0
  │ test-live-registry.sh       66L  0C    2m  CC=0.0    ←0
  │ test-cqrs-smoke.sh          55L  0C    1m  CC=0.0    ←0
  │ install-editable.sh         22L  0C    0m  CC=0.0    ←0
  │ testapp-handler.sh           6L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! planfile.yaml             1319L  0C    0m  CC=0.0    ←0
  │ !! goal.yaml                  511L  0C    0m  CC=0.0    ←0
  │ prefact.yaml                94L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              84L  0C    0m  CC=0.0    ←0
  │ project.sh                  59L  0C    0m  CC=0.0    ←0
  │ Dockerfile                  29L  0C    0m  CC=0.0    ←0
  │ nlp2uri.yaml                 8L  0C    0m  CC=0.0    ←0
  │ docker-compose.yml           6L  0C    0m  CC=0.0    ←0
  │ tree.sh                      1L  0C    0m  CC=0.0    ←0
  │
  testql-scenarios/               CC̄=0.0    ←in:0  →out:0
  │ generated-cli-tests.testql.toon.yaml    20L  0C    0m  CC=0.0    ←0
  │ generated-from-pytests.testql.toon.yaml    12L  0C    0m  CC=0.0    ←0
  │

COUPLING:
                    examples.resolve       src.nlp2uri  examples.execute      examples.mcp   schemas.codegen
  examples.resolve                ──                 1                ←4                ←4                ←5  hub
       src.nlp2uri                 4                ──                ←2                ←2                    hub
  examples.execute                 4                 2                ──                                    
      examples.mcp                 4                 2                                  ──                  
   schemas.codegen                 5                                                                      ──
  CYCLES: none
  HUB: src.nlp2uri/ (fan-in=5)
  HUB: examples.resolve/ (fan-in=17)

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 7 groups | 72f 6664L | 2026-06-06

SUMMARY:
  files_scanned: 72
  total_lines:   6664
  dup_groups:    7
  dup_fragments: 14
  saved_lines:   62
  scan_ms:       4215

HOTSPOTS[7] (files with most duplication):
  src/nlp2uri/schemes/desktop.py  dup=36L  groups=1  frags=2  (0.5%)
  src/nlp2uri/systemmap/compile.py  dup=24L  groups=1  frags=2  (0.4%)
  src/nlp2uri/parse_nl.py  dup=22L  groups=1  frags=2  (0.3%)
  src/nlp2uri/systemmap/uri.py  dup=14L  groups=2  frags=4  (0.2%)
  src/nlp2uri/systemmap/getv_uri.py  dup=8L  groups=1  frags=1  (0.1%)
  src/nlp2uri/systemmap/resolve.py  dup=8L  groups=1  frags=1  (0.1%)
  src/nlp2uri/cqrs/drivers/resource_probe.py  dup=6L  groups=1  frags=1  (0.1%)

DUPLICATES[7] (ranked by impact):
  [b1482ea46475566a]   STRU  build_focus  L=18 N=2 saved=18 sim=1.00
      src/nlp2uri/schemes/desktop.py:40-57  (build_focus)
      src/nlp2uri/schemes/desktop.py:102-119  (build_move)
  [f20ea3c3839b0415]   STRU  _compile_resource  L=12 N=2 saved=12 sim=1.00
      src/nlp2uri/systemmap/compile.py:141-152  (_compile_resource)
      src/nlp2uri/systemmap/compile.py:155-166  (_compile_artifact)
  [42faf2df3d26832c]   STRU  _parse_file_open  L=11 N=2 saved=11 sim=1.00
      src/nlp2uri/parse_nl.py:152-162  (_parse_file_open)
      src/nlp2uri/parse_nl.py:294-304  (_parse_app_open)
  [78c31a47ae2d1c13]   EXAC  to_dict  L=8 N=2 saved=8 sim=1.00
      src/nlp2uri/systemmap/getv_uri.py:105-112  (to_dict)
      src/nlp2uri/systemmap/resolve.py:22-29  (to_dict)
  [1079b0e4b2d5a43f]   EXAC  probe  L=6 N=2 saved=6 sim=1.00
      src/nlp2uri/cqrs/drivers/resource_probe.py:30-35  (probe)
      src/nlp2uri/cqrs/drivers/runtime_curl.py:29-34  (probe)
  [3d6c0029f92cde72]   STRU  uri_for_schedule  L=4 N=2 saved=4 sim=1.00
      src/nlp2uri/systemmap/uri.py:79-82  (uri_for_schedule)
      src/nlp2uri/systemmap/uri.py:85-88  (uri_for_generated_service)
  [ff8711d5a6139426]   STRU  uri_for_conversation  L=3 N=2 saved=3 sim=1.00
      src/nlp2uri/systemmap/uri.py:63-65  (uri_for_conversation)
      src/nlp2uri/systemmap/uri.py:68-70  (uri_for_process)

REFACTOR[7] (ranked by priority):
  [1] ○ extract_function   → src/nlp2uri/schemes/utils/build_focus.py
      WHY: 2 occurrences of 18-line block across 1 files — saves 18 lines
      FILES: src/nlp2uri/schemes/desktop.py
  [2] ○ extract_function   → src/nlp2uri/systemmap/utils/_compile_resource.py
      WHY: 2 occurrences of 12-line block across 1 files — saves 12 lines
      FILES: src/nlp2uri/systemmap/compile.py
  [3] ○ extract_function   → src/nlp2uri/utils/_parse_file_open.py
      WHY: 2 occurrences of 11-line block across 1 files — saves 11 lines
      FILES: src/nlp2uri/parse_nl.py
  [4] ○ extract_function   → src/nlp2uri/systemmap/utils/to_dict.py
      WHY: 2 occurrences of 8-line block across 2 files — saves 8 lines
      FILES: src/nlp2uri/systemmap/getv_uri.py, src/nlp2uri/systemmap/resolve.py
  [5] ○ extract_function   → src/nlp2uri/cqrs/drivers/utils/probe.py
      WHY: 2 occurrences of 6-line block across 2 files — saves 6 lines
      FILES: src/nlp2uri/cqrs/drivers/resource_probe.py, src/nlp2uri/cqrs/drivers/runtime_curl.py
  [6] ○ extract_function   → src/nlp2uri/systemmap/utils/uri_for_schedule.py
      WHY: 2 occurrences of 4-line block across 1 files — saves 4 lines
      FILES: src/nlp2uri/systemmap/uri.py
  [7] ○ extract_function   → src/nlp2uri/systemmap/utils/uri_for_conversation.py
      WHY: 2 occurrences of 3-line block across 1 files — saves 3 lines
      FILES: src/nlp2uri/systemmap/uri.py

QUICK_WINS[5] (low risk, high savings — do first):
  [1] extract_function   saved=18L  → src/nlp2uri/schemes/utils/build_focus.py
      FILES: desktop.py
  [2] extract_function   saved=12L  → src/nlp2uri/systemmap/utils/_compile_resource.py
      FILES: compile.py
  [3] extract_function   saved=11L  → src/nlp2uri/utils/_parse_file_open.py
      FILES: parse_nl.py
  [4] extract_function   saved=8L  → src/nlp2uri/systemmap/utils/to_dict.py
      FILES: getv_uri.py, resolve.py
  [5] extract_function   saved=6L  → src/nlp2uri/cqrs/drivers/utils/probe.py
      FILES: resource_probe.py, runtime_curl.py

EFFORT_ESTIMATE (total ≈ 2.1h):
  medium build_focus                         saved=18L  ~36min
  easy   _compile_resource                   saved=12L  ~24min
  easy   _parse_file_open                    saved=11L  ~22min
  easy   to_dict                             saved=8L  ~16min
  easy   probe                               saved=6L  ~12min
  easy   uri_for_schedule                    saved=4L  ~8min
  easy   uri_for_conversation                saved=3L  ~6min

METRICS-TARGET:
  dup_groups:  7 → 0
  saved_lines: 62 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 339 func | 61f | 2026-06-06
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
      WHY: 1319L, 0 classes, max CC=0
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
  prev CC̄=3.5 → now CC̄=3.6
```

## Intent

Natural language to URI resolution and cross-platform local URI execution
