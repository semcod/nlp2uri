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
- **version**: `0.4.10`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, testql(3), app.doql.less, goal.yaml, .env.example, Dockerfile, docker-compose.yml, project/(5 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: nlp2uri;
  version: 0.4.10;
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

*320 nodes · 444 edges · 59 modules · CC̄=3.5*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `compile_uri_to_control_plan` *(in src.nlp2uri.control_compile)* | 25 ⚠ | 3 | 51 | **54** |
| `build_koru_ide_uri_index` *(in src.nlp2uri.systemmap.koru_ide)* | 22 ⚠ | 2 | 50 | **52** |
| `build_parser` *(in src.nlp2uri.cli_parser)* | 1 | 1 | 51 | **52** |
| `build_resource_actions` *(in src.nlp2uri.host.resource)* | 14 ⚠ | 2 | 29 | **31** |
| `write_environment_map` *(in src.nlp2uri.systemmap.export)* | 9 | 1 | 29 | **30** |
| `_add_entry` *(in src.nlp2uri.systemmap.index)* | 3 | 24 | 4 | **28** |
| `build_getv_uri_index` *(in src.nlp2uri.systemmap.getv_uri)* | 6 | 3 | 24 | **27** |
| `compile_uri_to_actions` *(in src.nlp2uri.compile)* | 18 ⚠ | 5 | 20 | **25** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/nlp2uri
# generated in 0.16s
# nodes: 320 | edges: 444 | modules: 59
# CC̄=3.5

HUBS[20]:
  src.nlp2uri.control_compile.compile_uri_to_control_plan
    CC=25  in:3  out:51  total:54
  src.nlp2uri.systemmap.koru_ide.build_koru_ide_uri_index
    CC=22  in:2  out:50  total:52
  src.nlp2uri.cli_parser.build_parser
    CC=1  in:1  out:51  total:52
  src.nlp2uri.host.resource.build_resource_actions
    CC=14  in:2  out:29  total:31
  src.nlp2uri.systemmap.export.write_environment_map
    CC=9  in:1  out:29  total:30
  src.nlp2uri.systemmap.index._add_entry
    CC=3  in:24  out:4  total:28
  src.nlp2uri.systemmap.getv_uri.build_getv_uri_index
    CC=6  in:3  out:24  total:27
  src.nlp2uri.compile.compile_uri_to_actions
    CC=18  in:5  out:20  total:25
  src.nlp2uri.systemmap.resolve._match_command_entry
    CC=16  in:1  out:24  total:25
  src.nlp2uri.schemes.util.abstract_url
    CC=9  in:20  out:5  total:25
  src.nlp2uri.schemes.build.build_uri
    CC=19  in:2  out:22  total:24
  src.nlp2uri.systemmap.encode.encode_segment
    CC=1  in:22  out:1  total:23
  schemas.codegen.export_driver_stubs.main
    CC=11  in:0  out:23  total:23
  src.nlp2uri.host.artifact.resolve_artifact_path
    CC=12  in:1  out:22  total:23
  src.nlp2uri.systemmap.index.build_uri_index
    CC=6  in:5  out:17  total:22
  src.nlp2uri.config._load_from_path
    CC=6  in:3  out:17  total:20
  src.nlp2uri.systemmap.uri._get
    CC=4  in:15  out:5  total:20
  examples.resolve.new-intents.e2e.print
    CC=0  in:20  out:0  total:20
  src.nlp2uri.systemmap.getv_uri.compile_getv_uri
    CC=14  in:2  out:18  total:20
  src.nlp2uri.systemmap.index._ir_field
    CC=2  in:16  out:3  total:19

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
  src.nlp2uri.adapters.mcp  [4 funcs]
    _tool_compile_control  CC=2  out:6
    _tool_execute_control  CC=2  out:8
    _tool_list_system_uris  CC=2  out:7
    _tool_resolve_system_map  CC=3  out:10
  src.nlp2uri.cli  [12 funcs]
    _dispatch_command  CC=6  out:7
    _emit  CC=3  out:4
    _payload_text  CC=3  out:6
    _platform  CC=2  out:1
    _request_from_args  CC=4  out:8
    _run_adapter_command  CC=5  out:9
    _run_config  CC=3  out:10
    _run_envmap  CC=4  out:9
    _run_execute  CC=6  out:11
    _run_shell  CC=5  out:10
  src.nlp2uri.cli_parser  [3 funcs]
    add_common_args  CC=3  out:2
    add_text_args  CC=1  out:3
    build_parser  CC=1  out:51
  src.nlp2uri.compile  [54 funcs]
    _capture_outfile  CC=1  out:3
    _compile_app  CC=4  out:5
    _compile_app_file_open  CC=2  out:6
    _compile_app_named  CC=6  out:3
    _compile_app_open  CC=3  out:3
    _compile_app_open_with_path  CC=2  out:6
    _compile_app_settings  CC=5  out:3
    _compile_ide_chat  CC=5  out:5
    _compile_koru_control  CC=7  out:10
    _compile_launch_app  CC=4  out:4
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
  src.nlp2uri.control_compile  [4 funcs]
    _query_params  CC=3  out:3
    _truthy  CC=3  out:2
    compile_uri_to_control_plan  CC=25  out:51
    is_control_uri  CC=2  out:2
  src.nlp2uri.control_execute  [9 funcs]
    _build_client  CC=3  out:2
    _execute_cli  CC=9  out:9
    _execute_drive  CC=10  out:12
    _execute_status  CC=5  out:7
    _verification_status  CC=11  out:4
    compile_and_execute_control_uri  CC=5  out:6
    execute_control_action  CC=9  out:8
    execute_control_plan  CC=2  out:2
    koruide_available  CC=1  out:0
  src.nlp2uri.cqrs.dispatcher  [2 funcs]
    __init__  CC=5  out:5
    execute_uri  CC=4  out:10
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
  src.nlp2uri.desktop_apps  [5 funcs]
    _exact_desktop_match  CC=3  out:1
    _fuzzy_desktop_match  CC=3  out:2
    desktop_id_candidate_names  CC=1  out:2
    desktop_id_for_app  CC=3  out:4
    find_desktop_id_in_dir  CC=3  out:4
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
  src.nlp2uri.parse_nl  [21 funcs]
    _bool_param  CC=2  out:0
    _capture_target  CC=4  out:2
    _normalize_aliases  CC=2  out:3
    _normalize_app_name  CC=2  out:1
    _normalize_ide_name  CC=2  out:3
    _normalize_panel  CC=1  out:3
    _parse_app_open  CC=2  out:4
    _parse_capture  CC=6  out:8
    _parse_fallback  CC=1  out:1
    _parse_file_open  CC=2  out:4
  src.nlp2uri.platform_detect  [1 funcs]
    detect_platform  CC=5  out:1
  src.nlp2uri.platforms.base  [1 funcs]
    _desktop_id_for_app  CC=7  out:7
  src.nlp2uri.platforms.registry  [1 funcs]
    get_executor  CC=3  out:4
  src.nlp2uri.resolve  [2 funcs]
    nlp2uri  CC=13  out:13
    resolve_text  CC=2  out:3
  src.nlp2uri.runtime  [1 funcs]
    execute_uri  CC=9  out:15
  src.nlp2uri.schemes.build  [2 funcs]
    _build_navigate  CC=4  out:5
    build_uri  CC=19  out:22
  src.nlp2uri.schemes.desktop  [6 funcs]
    build_app_open  CC=3  out:5
    build_capture  CC=5  out:5
    build_focus  CC=1  out:5
    build_move  CC=1  out:5
    build_settings  CC=6  out:8
    build_terminal  CC=2  out:5
  src.nlp2uri.schemes.file  [1 funcs]
    build_file  CC=3  out:6
  src.nlp2uri.schemes.ide  [5 funcs]
    build_ide  CC=4  out:10
    build_ide_chat_send  CC=3  out:9
    build_ide_command  CC=3  out:8
    build_ide_status  CC=2  out:4
    build_koru_control_drive  CC=3  out:9
  src.nlp2uri.schemes.util  [3 funcs]
    abstract_url  CC=9  out:5
    file_uri  CC=1  out:3
    normalize_path  CC=2  out:5
  src.nlp2uri.service  [15 funcs]
    _cfg  CC=2  out:1
    _host  CC=1  out:1
    compile  CC=3  out:3
    default  CC=1  out:2
    execute  CC=2  out:3
    for_platform  CC=2  out:4
    from_prompt  CC=2  out:3
    handle_prompt  CC=13  out:14
    list_getv_uris  CC=3  out:5
    list_koru_ide_uris  CC=1  out:3
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
  src.nlp2uri.systemmap.export  [4 funcs]
    _ir_field  CC=2  out:3
    _require_env2llm  CC=2  out:3
    apply_desktop_uri_mapping  CC=9  out:11
    write_environment_map  CC=9  out:29
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
  src.nlp2uri.systemmap.index  [18 funcs]
    _add_entry  CC=3  out:4
    _get_id  CC=1  out:1
    _get_id_field  CC=4  out:5
    _index_access  CC=3  out:4
    _index_artifacts  CC=4  out:4
    _index_commands  CC=6  out:6
    _index_deploy  CC=2  out:2
    _index_desktop  CC=7  out:10
    _index_environment  CC=2  out:5
    _index_generated_services  CC=3  out:4
  src.nlp2uri.systemmap.koru_ide  [2 funcs]
    build_koru_ide_uri_index  CC=22  out:50
    merge_koru_ide_index  CC=3  out:5
  src.nlp2uri.systemmap.load  [4 funcs]
    env2llm_available  CC=1  out:0
    env2llm_missing_message  CC=2  out:0
    load_system_map_from_doql  CC=2  out:3
    load_system_map_from_example  CC=3  out:3
  src.nlp2uri.systemmap.resolve  [8 funcs]
    _dedupe_hits  CC=4  out:3
    _entry_hits  CC=1  out:3
    _match_command_entry  CC=16  out:24
    _match_resource_entry  CC=7  out:5
    _match_runtime_entry  CC=5  out:2
    _name_variants  CC=6  out:8
    _normalize_token  CC=1  out:5
    resolve_prompt_against_system_map  CC=4  out:6
  src.nlp2uri.systemmap.uri  [16 funcs]
    _get  CC=4  out:5
    _get_list  CC=5  out:4
    uri_for_access  CC=4  out:7
    uri_for_artifact  CC=1  out:4
    uri_for_command  CC=3  out:4
    uri_for_conversation  CC=1  out:1
    uri_for_desktop_session  CC=1  out:0
    uri_for_desktop_window_focus  CC=3  out:3
    uri_for_desktop_window_screenshot  CC=2  out:2
    uri_for_environment  CC=1  out:1

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
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Cli (2)

**`CLI Command Tests`**

**`Koru IDE control NL → URI → koru.control.v1 dry-run`**

### Integration (1)

**`Auto-generated from Python Tests`**
- assert `status == 200`
- assert `status == 200`

## Refactoring Analysis

*Pre-refactoring snapshot — use this section to identify targets. Generated from `project/` toon files.*

### Call Graph & Complexity (`project/calls.toon.yaml`)

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/nlp2uri
# generated in 0.16s
# nodes: 320 | edges: 444 | modules: 59
# CC̄=3.5

HUBS[20]:
  src.nlp2uri.control_compile.compile_uri_to_control_plan
    CC=25  in:3  out:51  total:54
  src.nlp2uri.systemmap.koru_ide.build_koru_ide_uri_index
    CC=22  in:2  out:50  total:52
  src.nlp2uri.cli_parser.build_parser
    CC=1  in:1  out:51  total:52
  src.nlp2uri.host.resource.build_resource_actions
    CC=14  in:2  out:29  total:31
  src.nlp2uri.systemmap.export.write_environment_map
    CC=9  in:1  out:29  total:30
  src.nlp2uri.systemmap.index._add_entry
    CC=3  in:24  out:4  total:28
  src.nlp2uri.systemmap.getv_uri.build_getv_uri_index
    CC=6  in:3  out:24  total:27
  src.nlp2uri.compile.compile_uri_to_actions
    CC=18  in:5  out:20  total:25
  src.nlp2uri.systemmap.resolve._match_command_entry
    CC=16  in:1  out:24  total:25
  src.nlp2uri.schemes.util.abstract_url
    CC=9  in:20  out:5  total:25
  src.nlp2uri.schemes.build.build_uri
    CC=19  in:2  out:22  total:24
  src.nlp2uri.systemmap.encode.encode_segment
    CC=1  in:22  out:1  total:23
  schemas.codegen.export_driver_stubs.main
    CC=11  in:0  out:23  total:23
  src.nlp2uri.host.artifact.resolve_artifact_path
    CC=12  in:1  out:22  total:23
  src.nlp2uri.systemmap.index.build_uri_index
    CC=6  in:5  out:17  total:22
  src.nlp2uri.config._load_from_path
    CC=6  in:3  out:17  total:20
  src.nlp2uri.systemmap.uri._get
    CC=4  in:15  out:5  total:20
  examples.resolve.new-intents.e2e.print
    CC=0  in:20  out:0  total:20
  src.nlp2uri.systemmap.getv_uri.compile_getv_uri
    CC=14  in:2  out:18  total:20
  src.nlp2uri.systemmap.index._ir_field
    CC=2  in:16  out:3  total:19

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
  src.nlp2uri.adapters.mcp  [4 funcs]
    _tool_compile_control  CC=2  out:6
    _tool_execute_control  CC=2  out:8
    _tool_list_system_uris  CC=2  out:7
    _tool_resolve_system_map  CC=3  out:10
  src.nlp2uri.cli  [12 funcs]
    _dispatch_command  CC=6  out:7
    _emit  CC=3  out:4
    _payload_text  CC=3  out:6
    _platform  CC=2  out:1
    _request_from_args  CC=4  out:8
    _run_adapter_command  CC=5  out:9
    _run_config  CC=3  out:10
    _run_envmap  CC=4  out:9
    _run_execute  CC=6  out:11
    _run_shell  CC=5  out:10
  src.nlp2uri.cli_parser  [3 funcs]
    add_common_args  CC=3  out:2
    add_text_args  CC=1  out:3
    build_parser  CC=1  out:51
  src.nlp2uri.compile  [54 funcs]
    _capture_outfile  CC=1  out:3
    _compile_app  CC=4  out:5
    _compile_app_file_open  CC=2  out:6
    _compile_app_named  CC=6  out:3
    _compile_app_open  CC=3  out:3
    _compile_app_open_with_path  CC=2  out:6
    _compile_app_settings  CC=5  out:3
    _compile_ide_chat  CC=5  out:5
    _compile_koru_control  CC=7  out:10
    _compile_launch_app  CC=4  out:4
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
  src.nlp2uri.control_compile  [4 funcs]
    _query_params  CC=3  out:3
    _truthy  CC=3  out:2
    compile_uri_to_control_plan  CC=25  out:51
    is_control_uri  CC=2  out:2
  src.nlp2uri.control_execute  [9 funcs]
    _build_client  CC=3  out:2
    _execute_cli  CC=9  out:9
    _execute_drive  CC=10  out:12
    _execute_status  CC=5  out:7
    _verification_status  CC=11  out:4
    compile_and_execute_control_uri  CC=5  out:6
    execute_control_action  CC=9  out:8
    execute_control_plan  CC=2  out:2
    koruide_available  CC=1  out:0
  src.nlp2uri.cqrs.dispatcher  [2 funcs]
    __init__  CC=5  out:5
    execute_uri  CC=4  out:10
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
  src.nlp2uri.desktop_apps  [5 funcs]
    _exact_desktop_match  CC=3  out:1
    _fuzzy_desktop_match  CC=3  out:2
    desktop_id_candidate_names  CC=1  out:2
    desktop_id_for_app  CC=3  out:4
    find_desktop_id_in_dir  CC=3  out:4
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
  src.nlp2uri.parse_nl  [21 funcs]
    _bool_param  CC=2  out:0
    _capture_target  CC=4  out:2
    _normalize_aliases  CC=2  out:3
    _normalize_app_name  CC=2  out:1
    _normalize_ide_name  CC=2  out:3
    _normalize_panel  CC=1  out:3
    _parse_app_open  CC=2  out:4
    _parse_capture  CC=6  out:8
    _parse_fallback  CC=1  out:1
    _parse_file_open  CC=2  out:4
  src.nlp2uri.platform_detect  [1 funcs]
    detect_platform  CC=5  out:1
  src.nlp2uri.platforms.base  [1 funcs]
    _desktop_id_for_app  CC=7  out:7
  src.nlp2uri.platforms.registry  [1 funcs]
    get_executor  CC=3  out:4
  src.nlp2uri.resolve  [2 funcs]
    nlp2uri  CC=13  out:13
    resolve_text  CC=2  out:3
  src.nlp2uri.runtime  [1 funcs]
    execute_uri  CC=9  out:15
  src.nlp2uri.schemes.build  [2 funcs]
    _build_navigate  CC=4  out:5
    build_uri  CC=19  out:22
  src.nlp2uri.schemes.desktop  [6 funcs]
    build_app_open  CC=3  out:5
    build_capture  CC=5  out:5
    build_focus  CC=1  out:5
    build_move  CC=1  out:5
    build_settings  CC=6  out:8
    build_terminal  CC=2  out:5
  src.nlp2uri.schemes.file  [1 funcs]
    build_file  CC=3  out:6
  src.nlp2uri.schemes.ide  [5 funcs]
    build_ide  CC=4  out:10
    build_ide_chat_send  CC=3  out:9
    build_ide_command  CC=3  out:8
    build_ide_status  CC=2  out:4
    build_koru_control_drive  CC=3  out:9
  src.nlp2uri.schemes.util  [3 funcs]
    abstract_url  CC=9  out:5
    file_uri  CC=1  out:3
    normalize_path  CC=2  out:5
  src.nlp2uri.service  [15 funcs]
    _cfg  CC=2  out:1
    _host  CC=1  out:1
    compile  CC=3  out:3
    default  CC=1  out:2
    execute  CC=2  out:3
    for_platform  CC=2  out:4
    from_prompt  CC=2  out:3
    handle_prompt  CC=13  out:14
    list_getv_uris  CC=3  out:5
    list_koru_ide_uris  CC=1  out:3
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
  src.nlp2uri.systemmap.export  [4 funcs]
    _ir_field  CC=2  out:3
    _require_env2llm  CC=2  out:3
    apply_desktop_uri_mapping  CC=9  out:11
    write_environment_map  CC=9  out:29
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
  src.nlp2uri.systemmap.index  [18 funcs]
    _add_entry  CC=3  out:4
    _get_id  CC=1  out:1
    _get_id_field  CC=4  out:5
    _index_access  CC=3  out:4
    _index_artifacts  CC=4  out:4
    _index_commands  CC=6  out:6
    _index_deploy  CC=2  out:2
    _index_desktop  CC=7  out:10
    _index_environment  CC=2  out:5
    _index_generated_services  CC=3  out:4
  src.nlp2uri.systemmap.koru_ide  [2 funcs]
    build_koru_ide_uri_index  CC=22  out:50
    merge_koru_ide_index  CC=3  out:5
  src.nlp2uri.systemmap.load  [4 funcs]
    env2llm_available  CC=1  out:0
    env2llm_missing_message  CC=2  out:0
    load_system_map_from_doql  CC=2  out:3
    load_system_map_from_example  CC=3  out:3
  src.nlp2uri.systemmap.resolve  [8 funcs]
    _dedupe_hits  CC=4  out:3
    _entry_hits  CC=1  out:3
    _match_command_entry  CC=16  out:24
    _match_resource_entry  CC=7  out:5
    _match_runtime_entry  CC=5  out:2
    _name_variants  CC=6  out:8
    _normalize_token  CC=1  out:5
    resolve_prompt_against_system_map  CC=4  out:6
  src.nlp2uri.systemmap.uri  [16 funcs]
    _get  CC=4  out:5
    _get_list  CC=5  out:4
    uri_for_access  CC=4  out:7
    uri_for_artifact  CC=1  out:4
    uri_for_command  CC=3  out:4
    uri_for_conversation  CC=1  out:1
    uri_for_desktop_session  CC=1  out:0
    uri_for_desktop_window_focus  CC=3  out:3
    uri_for_desktop_window_screenshot  CC=2  out:2
    uri_for_environment  CC=1  out:1

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
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 298f 17195L | proto:162,python:79,yaml:36,shell:15,json:2,yml:1,toml:1 | 2026-06-07
# generated in 0.04s
# CC̅=3.5 | critical:6/450 | dups:0 | cycles:0

HEALTH[6]:
  🟡 CC    _match_command_entry CC=16 (limit:15)
  🟡 CC    compile_uri_to_control_plan CC=25 (limit:15)
  🟡 CC    build_koru_ide_uri_index CC=22 (limit:15)
  🟡 CC    compile_uri_to_actions CC=18 (limit:15)
  🟡 CC    build_uri CC=19 (limit:15)
  🟡 CC    to_slots CC=15 (limit:15)

REFACTOR[1]:
  1. split 6 high-CC methods  (CC>15)

PIPELINES[186]:
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
  [8] Src [resolved_platform]: resolved_platform → detect_platform
      PURITY: 100% pure
  [9] Src [apply_runtime_env]: apply_runtime_env
      PURITY: 100% pure
  [10] Src [to_dict]: to_dict → detect_platform
      PURITY: 100% pure
  [11] Src [to_yaml]: to_yaml → payload_keys
      PURITY: 100% pure
  [12] Src [text_uri_list]: text_uri_list
      PURITY: 100% pure
  [13] Src [tool_execute_desktop_uri]: tool_execute_desktop_uri
      PURITY: 100% pure
  [14] Src [desktop_id_for_app]: desktop_id_for_app → desktop_id_candidate_names
      PURITY: 100% pure
  [15] Src [__getattr__]: __getattr__
      PURITY: 100% pure
  [16] Src [_read_json]: _read_json
      PURITY: 100% pure
  [17] Src [_send]: _send
      PURITY: 100% pure
  [18] Src [do_GET]: do_GET
      PURITY: 100% pure
  [19] Src [do_POST]: do_POST
      PURITY: 100% pure
  [20] Src [main]: main → run_server → ensure_config → find_config_path → ...(1 more)
      PURITY: 100% pure
  [21] Src [main]: main → run_stdio → ensure_config → find_config_path → ...(1 more)
      PURITY: 100% pure
  [22] Src [_result]: _result
      PURITY: 100% pure
  [23] Src [_dry]: _dry
      PURITY: 100% pure
  [24] Src [_run]: _run
      PURITY: 100% pure
  [25] Src [_first_available]: _first_available
      PURITY: 100% pure
  [26] Src [_open_with_browser]: _open_with_browser
      PURITY: 100% pure
  [27] Src [_parse_nlp2uri]: _parse_nlp2uri
      PURITY: 100% pure
  [28] Src [slugify_app_name]: slugify_app_name
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
  [35] Src [get_executor]: get_executor → detect_platform
      PURITY: 100% pure
  [36] Src [execute]: execute
      PURITY: 100% pure
  [37] Src [_open]: _open
      PURITY: 100% pure
  [38] Src [_open_app]: _open_app
      PURITY: 100% pure
  [39] Src [_focus_app]: _focus_app
      PURITY: 100% pure
  [40] Src [_capture]: _capture
      PURITY: 100% pure
  [41] Src [execute]: execute
      PURITY: 100% pure
  [42] Src [_start]: _start
      PURITY: 100% pure
  [43] Src [_open_app]: _open_app
      PURITY: 100% pure
  [44] Src [_focus_app]: _focus_app
      PURITY: 100% pure
  [45] Src [_capture]: _capture
      PURITY: 100% pure
  [46] Src [is_artifact_uri]: is_artifact_uri
      PURITY: 100% pure
  [47] Src [is_resource_uri]: is_resource_uri
      PURITY: 100% pure
  [48] Src [to_dict]: to_dict
      PURITY: 100% pure
  [49] Src [__init__]: __init__ → load_config → find_config_path → config_search_paths
      PURITY: 100% pure
  [50] Src [with_platform]: with_platform
      PURITY: 100% pure

LAYERS:
  src/                            CC̄=3.6    ←in:0  →out:0
  │ !! compile                    650L  0C   54m  CC=18     ←5
  │ !! parse_nl                   540L  0C   30m  CC=7      ←1
  │ mcp                        462L  1C   21m  CC=6      ←0
  │ index                      351L  2C   23m  CC=7      ←6
  │ control_execute            339L  1C   11m  CC=11     ←2
  │ !! models                     272L  10C   10m  CC=15     ←0
  │ config                     230L  1C   17m  CC=8      ←7
  │ !! control_compile            228L  0C    6m  CC=25     ←4
  │ service                    228L  1C   16m  CC=13     ←0
  │ getv_uri                   225L  1C    9m  CC=14     ←3
  │ !! resolve                    189L  1C    9m  CC=16     ←2
  │ cli                        184L  0C   12m  CC=6      ←0
  │ !! koru_ide                   182L  0C    3m  CC=22     ←1
  │ compile                    179L  0C   11m  CC=12     ←5
  │ desktop                    166L  0C    6m  CC=6      ←0
  │ export                     149L  0C    4m  CC=9      ←1
  │ linux                      145L  1C    6m  CC=11     ←0
  │ cli_parser                 136L  0C    3m  CC=3      ←1
  │ ide                        136L  0C    5m  CC=4      ←0
  │ base                       130L  1C    9m  CC=7      ←1
  │ mcp_server                 128L  0C   10m  CC=8      ←0
  │ service_ops                128L  3C    8m  CC=5      ←0
  │ uri                        123L  0C   16m  CC=5      ←2
  │ dispatcher                 117L  1C    4m  CC=5      ←1
  │ base                        97L  5C    4m  CC=8      ←0
  │ registry                    97L  1C    6m  CC=8      ←1
  │ getv_load                   97L  0C    8m  CC=8      ←1
  │ macos                       94L  1C    5m  CC=7      ←0
  │ windows                     94L  1C    5m  CC=7      ←0
  │ artifact                    94L  0C    4m  CC=13     ←2
  │ runtime                     93L  0C    2m  CC=9      ←0
  │ rest_server                 90L  1C    7m  CC=4      ←0
  │ container_docker            88L  1C    4m  CC=14     ←0
  │ rest                        87L  1C    4m  CC=14     ←0
  │ mcp                         81L  0C    5m  CC=2      ←1
  │ __init__                    80L  0C    0m  CC=0.0    ←0
  │ !! build                       79L  0C    2m  CC=19     ←1
  │ resource                    69L  0C    4m  CC=14     ←2
  │ event_store                 67L  2C    5m  CC=3      ←0
  │ shell                       66L  1C    2m  CC=11     ←0
  │ plugins                     64L  0C    3m  CC=7      ←1
  │ desktop_apps                60L  0C    5m  CC=3      ←0
  │ resolve                     60L  0C    2m  CC=13     ←4
  │ base                        59L  3C    5m  CC=2      ←0
  │ cli                         53L  1C    1m  CC=12     ←0
  │ http_store                  52L  1C    3m  CC=3      ←0
  │ fallback                    52L  0C    1m  CC=6      ←1
  │ util                        47L  0C    5m  CC=9      ←5
  │ context                     47L  0C    2m  CC=8      ←1
  │ load                        46L  0C    4m  CC=3      ←3
  │ command_curl                39L  1C    2m  CC=5      ←0
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
  │ __main__                     9L  0C    0m  CC=0.0    ←0
  │ __init__                     8L  0C    0m  CC=0.0    ←0
  │ __init__                     6L  0C    0m  CC=0.0    ←0
  │ __init__                     5L  0C    0m  CC=0.0    ←0
  │
  schemas/                        CC̄=2.4    ←in:0  →out:0
  │ scaffold_scheme            357L  0C   13m  CC=4      ←0
  │ registry.yaml              218L  0C    0m  CC=0.0    ←0
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
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ api.proto                   26L  0C    0m  CC=0.0    ←0
  │ Makefile                    24L  0C    0m  CC=0.0    ←0
  │ buf.yaml                    15L  0C    0m  CC=0.0    ←0
  │ driver.proto                15L  0C    0m  CC=0.0    ←0
  │ driver.proto                15L  0C    0m  CC=0.0    ←0
  │ driver.proto                15L  0C    0m  CC=0.0    ←0
  │ driver.proto                15L  0C    0m  CC=0.0    ←0
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
  │ test-live-registry.sh       72L  0C    2m  CC=0.0    ←0
  │ test-cqrs-smoke.sh          55L  0C    1m  CC=0.0    ←0
  │ install-editable.sh         22L  0C    0m  CC=0.0    ←0
  │ testapp-handler.sh           6L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! planfile.yaml             1319L  0C    0m  CC=0.0    ←0
  │ !! goal.yaml                  511L  0C    0m  CC=0.0    ←0
  │ prefact.yaml                94L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              85L  0C    0m  CC=0.0    ←0
  │ project.sh                  59L  0C    0m  CC=0.0    ←0
  │ Dockerfile                  29L  0C    0m  CC=0.0    ←0
  │ nlp2uri.yaml                 8L  0C    0m  CC=0.0    ←0
  │ docker-compose.yml           6L  0C    0m  CC=0.0    ←0
  │ tree.sh                      1L  0C    0m  CC=0.0    ←0
  │
  testql-scenarios/               CC̄=0.0    ←in:0  →out:0
  │ generated-cli-tests.testql.toon.yaml    20L  0C    0m  CC=0.0    ←0
  │ koru-ide-control-roundtrip.testql.toon.yaml    13L  0C    0m  CC=0.0    ←0
  │ generated-from-pytests.testql.toon.yaml    12L  0C    0m  CC=0.0    ←0
  │

COUPLING:
                    examples.resolve       src.nlp2uri  examples.execute      examples.mcp   schemas.codegen
  examples.resolve                ──                 1                ←4                ←4                ←5  hub
       src.nlp2uri                 5                ──                ←2                ←2                    hub
  examples.execute                 4                 2                ──                                    
      examples.mcp                 4                 2                                  ──                  
   schemas.codegen                 5                                                                      ──
  CYCLES: none
  HUB: examples.resolve/ (fan-in=18)
  HUB: src.nlp2uri/ (fan-in=5)

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 15 groups | 79f 8728L | 2026-06-07

SUMMARY:
  files_scanned: 79
  total_lines:   8728
  dup_groups:    15
  dup_fragments: 33
  saved_lines:   154
  scan_ms:       2627

HOTSPOTS[7] (files with most duplication):
  src/nlp2uri/systemmap/index.py  dup=70L  groups=3  frags=7  (0.8%)
  src/nlp2uri/parse_nl.py  dup=51L  groups=2  frags=5  (0.6%)
  src/nlp2uri/schemes/desktop.py  dup=36L  groups=1  frags=2  (0.4%)
  src/nlp2uri/compile.py  dup=29L  groups=3  frags=5  (0.3%)
  src/nlp2uri/systemmap/compile.py  dup=24L  groups=1  frags=2  (0.3%)
  src/nlp2uri/systemmap/uri.py  dup=14L  groups=2  frags=4  (0.2%)
  src/nlp2uri/systemmap/getv_uri.py  dup=8L  groups=1  frags=1  (0.1%)

DUPLICATES[15] (ranked by impact):
  [6e4a9c83a57c317f] ! STRU  _index_resources  L=11 N=4 saved=33 sim=1.00
      src/nlp2uri/systemmap/index.py:164-174  (_index_resources)
      src/nlp2uri/systemmap/index.py:177-187  (_index_access)
      src/nlp2uri/systemmap/index.py:220-230  (_index_schedules)
      src/nlp2uri/systemmap/index.py:233-243  (_index_generated_services)
  [42faf2df3d26832c]   STRU  _parse_ide_status  L=11 N=3 saved=22 sim=1.00
      src/nlp2uri/parse_nl.py:254-264  (_parse_ide_status)
      src/nlp2uri/parse_nl.py:313-323  (_parse_file_open)
      src/nlp2uri/parse_nl.py:455-465  (_parse_app_open)
  [b1482ea46475566a]   STRU  build_focus  L=18 N=2 saved=18 sim=1.00
      src/nlp2uri/schemes/desktop.py:40-57  (build_focus)
      src/nlp2uri/schemes/desktop.py:102-119  (build_move)
  [f20ea3c3839b0415]   STRU  _compile_resource  L=12 N=2 saved=12 sim=1.00
      src/nlp2uri/systemmap/compile.py:141-152  (_compile_resource)
      src/nlp2uri/systemmap/compile.py:155-166  (_compile_artifact)
  [df71a0ba7463343c]   STRU  _index_artifacts  L=11 N=2 saved=11 sim=1.00
      src/nlp2uri/systemmap/index.py:190-200  (_index_artifacts)
      src/nlp2uri/systemmap/index.py:300-310  (_index_validations)
  [85ffa2defd9f0fa1]   STRU  _windows_window_move_actions  L=10 N=2 saved=10 sim=1.00
      src/nlp2uri/compile.py:450-459  (_windows_window_move_actions)
      src/nlp2uri/compile.py:496-501  (_windows_window_focus_actions)
  [4fac14ef046e2d2c]   STRU  _mentions_no_submit  L=9 N=2 saved=9 sim=1.00
      src/nlp2uri/parse_nl.py:145-153  (_mentions_no_submit)
      src/nlp2uri/parse_nl.py:156-164  (_mentions_require_plugin)
  [78c31a47ae2d1c13]   EXAC  to_dict  L=8 N=2 saved=8 sim=1.00
      src/nlp2uri/systemmap/getv_uri.py:105-112  (to_dict)
      src/nlp2uri/systemmap/resolve.py:22-29  (to_dict)
  [a5e2055bcecafecc]   STRU  _macos_window_move_actions  L=7 N=2 saved=7 sim=1.00
      src/nlp2uri/compile.py:441-447  (_macos_window_move_actions)
      src/nlp2uri/compile.py:491-493  (_macos_window_focus_actions)
  [1079b0e4b2d5a43f]   EXAC  probe  L=6 N=2 saved=6 sim=1.00
      src/nlp2uri/cqrs/drivers/resource_probe.py:30-35  (probe)
      src/nlp2uri/cqrs/drivers/runtime_curl.py:29-34  (probe)
  [02add39e2c61e448]   EXAC  _ir_field  L=4 N=2 saved=4 sim=1.00
      src/nlp2uri/systemmap/export.py:21-24  (_ir_field)
      src/nlp2uri/systemmap/index.py:90-93  (_ir_field)
  [22e18df0ee19a21c]   STRU  koruide_missing_message  L=4 N=2 saved=4 sim=1.00
      src/nlp2uri/control_execute.py:29-32  (koruide_missing_message)
      src/nlp2uri/systemmap/load.py:26-32  (env2llm_missing_message)
  [3d6c0029f92cde72]   STRU  uri_for_schedule  L=4 N=2 saved=4 sim=1.00
      src/nlp2uri/systemmap/uri.py:79-82  (uri_for_schedule)
      src/nlp2uri/systemmap/uri.py:85-88  (uri_for_generated_service)
  [7320e91881d35948]   EXAC  _query_params  L=3 N=2 saved=3 sim=1.00
      src/nlp2uri/compile.py:72-74  (_query_params)
      src/nlp2uri/control_compile.py:18-20  (_query_params)
  [ff8711d5a6139426]   STRU  uri_for_conversation  L=3 N=2 saved=3 sim=1.00
      src/nlp2uri/systemmap/uri.py:63-65  (uri_for_conversation)
      src/nlp2uri/systemmap/uri.py:68-70  (uri_for_process)

REFACTOR[15] (ranked by priority):
  [1] ○ extract_function   → src/nlp2uri/systemmap/utils/_index_resources.py
      WHY: 4 occurrences of 11-line block across 1 files — saves 33 lines
      FILES: src/nlp2uri/systemmap/index.py
  [2] ○ extract_function   → src/nlp2uri/utils/_parse_ide_status.py
      WHY: 3 occurrences of 11-line block across 1 files — saves 22 lines
      FILES: src/nlp2uri/parse_nl.py
  [3] ○ extract_function   → src/nlp2uri/schemes/utils/build_focus.py
      WHY: 2 occurrences of 18-line block across 1 files — saves 18 lines
      FILES: src/nlp2uri/schemes/desktop.py
  [4] ○ extract_function   → src/nlp2uri/systemmap/utils/_compile_resource.py
      WHY: 2 occurrences of 12-line block across 1 files — saves 12 lines
      FILES: src/nlp2uri/systemmap/compile.py
  [5] ○ extract_function   → src/nlp2uri/systemmap/utils/_index_artifacts.py
      WHY: 2 occurrences of 11-line block across 1 files — saves 11 lines
      FILES: src/nlp2uri/systemmap/index.py
  [6] ○ extract_function   → src/nlp2uri/utils/_windows_window_move_actions.py
      WHY: 2 occurrences of 10-line block across 1 files — saves 10 lines
      FILES: src/nlp2uri/compile.py
  [7] ○ extract_function   → src/nlp2uri/utils/_mentions_no_submit.py
      WHY: 2 occurrences of 9-line block across 1 files — saves 9 lines
      FILES: src/nlp2uri/parse_nl.py
  [8] ○ extract_function   → src/nlp2uri/systemmap/utils/to_dict.py
      WHY: 2 occurrences of 8-line block across 2 files — saves 8 lines
      FILES: src/nlp2uri/systemmap/getv_uri.py, src/nlp2uri/systemmap/resolve.py
  [9] ○ extract_function   → src/nlp2uri/utils/_macos_window_move_actions.py
      WHY: 2 occurrences of 7-line block across 1 files — saves 7 lines
      FILES: src/nlp2uri/compile.py
  [10] ○ extract_function   → src/nlp2uri/cqrs/drivers/utils/probe.py
      WHY: 2 occurrences of 6-line block across 2 files — saves 6 lines
      FILES: src/nlp2uri/cqrs/drivers/resource_probe.py, src/nlp2uri/cqrs/drivers/runtime_curl.py
  [11] ○ extract_function   → src/nlp2uri/systemmap/utils/_ir_field.py
      WHY: 2 occurrences of 4-line block across 2 files — saves 4 lines
      FILES: src/nlp2uri/systemmap/export.py, src/nlp2uri/systemmap/index.py
  [12] ○ extract_function   → src/nlp2uri/utils/koruide_missing_message.py
      WHY: 2 occurrences of 4-line block across 2 files — saves 4 lines
      FILES: src/nlp2uri/control_execute.py, src/nlp2uri/systemmap/load.py
  [13] ○ extract_function   → src/nlp2uri/systemmap/utils/uri_for_schedule.py
      WHY: 2 occurrences of 4-line block across 1 files — saves 4 lines
      FILES: src/nlp2uri/systemmap/uri.py
  [14] ○ extract_function   → src/nlp2uri/utils/_query_params.py
      WHY: 2 occurrences of 3-line block across 2 files — saves 3 lines
      FILES: src/nlp2uri/compile.py, src/nlp2uri/control_compile.py
  [15] ○ extract_function   → src/nlp2uri/systemmap/utils/uri_for_conversation.py
      WHY: 2 occurrences of 3-line block across 1 files — saves 3 lines
      FILES: src/nlp2uri/systemmap/uri.py

QUICK_WINS[10] (low risk, high savings — do first):
  [1] extract_function   saved=33L  → src/nlp2uri/systemmap/utils/_index_resources.py
      FILES: index.py
  [2] extract_function   saved=22L  → src/nlp2uri/utils/_parse_ide_status.py
      FILES: parse_nl.py
  [3] extract_function   saved=18L  → src/nlp2uri/schemes/utils/build_focus.py
      FILES: desktop.py
  [4] extract_function   saved=12L  → src/nlp2uri/systemmap/utils/_compile_resource.py
      FILES: compile.py
  [5] extract_function   saved=11L  → src/nlp2uri/systemmap/utils/_index_artifacts.py
      FILES: index.py
  [6] extract_function   saved=10L  → src/nlp2uri/utils/_windows_window_move_actions.py
      FILES: compile.py
  [7] extract_function   saved=9L  → src/nlp2uri/utils/_mentions_no_submit.py
      FILES: parse_nl.py
  [8] extract_function   saved=8L  → src/nlp2uri/systemmap/utils/to_dict.py
      FILES: getv_uri.py, resolve.py
  [9] extract_function   saved=7L  → src/nlp2uri/utils/_macos_window_move_actions.py
      FILES: compile.py
  [10] extract_function   saved=6L  → src/nlp2uri/cqrs/drivers/utils/probe.py
      FILES: resource_probe.py, runtime_curl.py

EFFORT_ESTIMATE (total ≈ 5.1h):
  medium _index_resources                    saved=33L  ~66min
  medium _parse_ide_status                   saved=22L  ~44min
  medium build_focus                         saved=18L  ~36min
  easy   _compile_resource                   saved=12L  ~24min
  easy   _index_artifacts                    saved=11L  ~22min
  easy   _windows_window_move_actions        saved=10L  ~20min
  easy   _mentions_no_submit                 saved=9L  ~18min
  easy   to_dict                             saved=8L  ~16min
  easy   _macos_window_move_actions          saved=7L  ~14min
  easy   probe                               saved=6L  ~12min
  ... +5 more (~36min)

METRICS-TARGET:
  dup_groups:  15 → 0
  saved_lines: 154 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 443 func | 67f | 2026-06-07
# generated in 0.00s

NEXT[8] (ranked by impact):
  [1] !! SPLIT           src/nlp2uri/compile.py
      WHY: 650L, 0 classes, max CC=18
      EFFORT: ~4h  IMPACT: 11700

  [2] !! SPLIT           src/nlp2uri/parse_nl.py
      WHY: 540L, 0 classes, max CC=7
      EFFORT: ~4h  IMPACT: 3780

  [3] !  SPLIT-FUNC      compile_uri_to_actions  CC=18  fan=20
      WHY: CC=18 exceeds 15
      EFFORT: ~1h  IMPACT: 360

  [4] !! SPLIT-FUNC      compile_uri_to_control_plan  CC=25  fan=14
      WHY: CC=25 exceeds 15
      EFFORT: ~1h  IMPACT: 350

  [5] !  SPLIT-FUNC      build_uri  CC=19  fan=17
      WHY: CC=19 exceeds 15
      EFFORT: ~1h  IMPACT: 323

  [6] !  SPLIT-FUNC      build_koru_ide_uri_index  CC=22  fan=14
      WHY: CC=22 exceeds 15
      EFFORT: ~1h  IMPACT: 308

  [7] !  SPLIT-FUNC      _match_command_entry  CC=16  fan=13
      WHY: CC=16 exceeds 15
      EFFORT: ~1h  IMPACT: 208

  [8] !! SPLIT           planfile.yaml
      WHY: 1319L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[3]:
  ⚠ Splitting planfile.yaml may break 0 import paths
  ⚠ Splitting src/nlp2uri/compile.py may break 54 import paths
  ⚠ Splitting src/nlp2uri/parse_nl.py may break 30 import paths

METRICS-TARGET:
  CC̄:          3.5 → ≤2.4
  max-CC:      25 → ≤12
  god-modules: 4 → 0
  high-CC(≥15): 6 → ≤3
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
  prev CC̄=3.3 → now CC̄=3.5
```

## Intent

Natural language to URI resolution and cross-platform local URI execution
