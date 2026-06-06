# System Architecture Analysis
<!-- generated in 0.01s -->

## Overview

- **Project**: /home/tom/github/semcod/nlp2uri
- **Primary Language**: proto
- **Languages**: proto: 138, python: 72, yaml: 31, shell: 15, json: 2
- **Analysis Mode**: static
- **Total Functions**: 346
- **Total Classes**: 46
- **Modules**: 262
- **Entry Points**: 186

## Architecture by Module

### src.nlp2uri.compile
- **Functions**: 23
- **File**: `compile.py`

### src.nlp2uri.parse_nl
- **Functions**: 21
- **File**: `parse_nl.py`

### src.nlp2uri.adapters.mcp
- **Functions**: 18
- **Classes**: 1
- **File**: `mcp.py`

### src.nlp2uri.config
- **Functions**: 17
- **Classes**: 1
- **File**: `config.py`

### src.nlp2uri.service
- **Functions**: 15
- **Classes**: 1
- **File**: `service.py`

### schemas.codegen.scaffold_scheme
- **Functions**: 13
- **File**: `scaffold_scheme.py`

### src.nlp2uri.systemmap.uri
- **Functions**: 13
- **File**: `uri.py`

### src.nlp2uri.cli
- **Functions**: 11
- **File**: `cli.py`

### src.nlp2uri.systemmap.index
- **Functions**: 11
- **Classes**: 2
- **File**: `index.py`

### src.nlp2uri.systemmap.compile
- **Functions**: 11
- **File**: `compile.py`

### src.nlp2uri.integrators.mcp_server
- **Functions**: 10
- **File**: `mcp_server.py`

### src.nlp2uri.platforms.base
- **Functions**: 9
- **Classes**: 1
- **File**: `base.py`

### src.nlp2uri.systemmap.getv_uri
- **Functions**: 9
- **Classes**: 1
- **File**: `getv_uri.py`

### src.nlp2uri.cqrs.drivers.service_ops
- **Functions**: 8
- **Classes**: 3
- **File**: `service_ops.py`

### src.nlp2uri.systemmap.getv_load
- **Functions**: 8
- **File**: `getv_load.py`

### src.nlp2uri.models
- **Functions**: 7
- **Classes**: 7
- **File**: `models.py`

### src.nlp2uri.integrators.rest_server
- **Functions**: 7
- **Classes**: 1
- **File**: `rest_server.py`

### scripts.test-live-registry
- **Functions**: 7
- **File**: `test-live-registry.sh`

### src.nlp2uri.platforms.linux
- **Functions**: 6
- **Classes**: 1
- **File**: `linux.py`

### src.nlp2uri.schemes.desktop
- **Functions**: 6
- **File**: `desktop.py`

## Key Entry Points

Main execution flows into the system:

### src.nlp2uri.adapters.rest.RestAdapter.dispatch
- **Calls**: isinstance, self._service_for, self.body_to_request, AdapterResponse, AdapterResponse, svc.from_prompt, AdapterResponse, svc.resolve

### schemas.codegen.export_driver_stubs.main
- **Calls**: argparse.ArgumentParser, parser.add_argument, parser.parse_args, yaml.safe_load, None.items, sorted, examples.resolve.new-intents.e2e.print, None.read_text

### src.nlp2uri.adapters.cli.CliAdapter.handle
- **Calls**: self._service_for, AdapterResponse, svc.from_prompt, AdapterResponse, svc.resolve, AdapterResponse, svc.compile, AdapterResponse

### src.nlp2uri.platforms.linux.LinuxExecutor._capture
- **Calls**: Path, out_dir.mkdir, self._run, os.environ.get, self._first_available, params.get, self._dry, outfile.exists

### src.nlp2uri.adapters.shell.ShellAdapter.handle
- **Calls**: self._service_for, AdapterResponse, svc.from_prompt, self._export_script, AdapterResponse, svc.compile, self._export_script, AdapterResponse

### schemas.codegen.scaffold_scheme.main
- **Calls**: argparse.ArgumentParser, parser.add_argument, parser.add_argument, parser.parse_args, yaml.safe_load, schemes.items, examples.resolve.new-intents.e2e.print, REGISTRY.read_text

### schemas.codegen.export_mcp_schemas.main
- **Calls**: argparse.ArgumentParser, parser.add_argument, parser.parse_args, yaml.safe_load, OUT.mkdir, None.items, None.write_text, examples.resolve.new-intents.e2e.print

### src.nlp2uri.platforms.linux.LinuxExecutor.execute
- **Calls**: urlparse, self._result, self._open_generic, self._open_generic, self._parse_nlp2uri, path.startswith, self._open_settings, self._open_app

### src.nlp2uri.platforms.macos.MacOSExecutor.execute
- **Calls**: urlparse, self._result, self._open, self._parse_nlp2uri, path.startswith, self._open, self._open_app, self._focus_app

### src.nlp2uri.platforms.windows.WindowsExecutor.execute
- **Calls**: urlparse, self._result, self._start, self._parse_nlp2uri, path.startswith, self._start, self._open_app, self._focus_app

### src.nlp2uri.cqrs.drivers.container_docker.ContainerDockerDriver._docker_argv
- **Calls**: ValueError, None.get, params.get, params.get, argv.append, params.get, None.get, str

### src.nlp2uri.config.NLP2URIConfig.to_yaml
- **Calls**: lines.append, lines.append, sorted, lines.append, lines.append, self.extra.items, lines.append, None.join

### src.nlp2uri.platforms.macos.MacOSExecutor._capture
- **Calls**: Path, out_dir.mkdir, self._run, os.environ.get, params.get, self._dry, self._result, str

### src.nlp2uri.adapters.mcp.McpAdapter._tool_cqrs_execute
- **Calls**: dict, req.extra.get, req.extra.get, CqrsDispatcher, d.execute_uri, self.mcp_content, AdapterResponse, req.extra.get

### src.nlp2uri.cqrs.base.UriDriver.execute
- **Calls**: ExecuteResult, ExecuteResult, subprocess.run, outputs.append, None.join, action.argv, ExecuteResult, None.join

### src.nlp2uri.platforms.windows.WindowsExecutor._capture
- **Calls**: Path, out_dir.mkdir, self._run, outfile.exists, os.environ.get, params.get, self._dry, self._result

### src.nlp2uri.adapters.mcp.McpAdapter._args_to_request
- **Calls**: arguments.get, AdapterRequest, HostPlatform, str, str, bool, arguments.get, arguments.get

### src.nlp2uri.adapters.mcp.McpAdapter._tool_resolve_system_map
- **Calls**: self._service_for, svc.resolve_system_map, payload.get, self.mcp_content, AdapterResponse, src.nlp2uri.systemmap.context.load_ir_from_arguments, AdapterResponse, bool

### src.nlp2uri.adapters.rest.RestAdapter.body_to_request
- **Calls**: body.get, AdapterRequest, HostPlatform, str, str, bool, body.get, body.get

### src.nlp2uri.schemes.ide.build_ide
- **Calls**: None.lower, src.nlp2uri.schemes.util.normalize_path, _IDE_SCHEMES.get, src.nlp2uri.schemes.util.abstract_url, UriSpec, intent.params.get, ValueError, None.as_posix

### src.nlp2uri.cqrs.dispatcher.CqrsDispatcher.execute_uri
- **Calls**: self.compile_uri, self.registry.driver_for_uri, driver.execute, None.scheme.lower, self.events.append, OSAction, HostPlatform, list

### src.nlp2uri.integrators.rest_server.NLP2URIRequestHandler._send
- **Calls**: None.encode, self.send_response, self.send_header, self.send_header, self.end_headers, self.wfile.write, str, json.dumps

### src.nlp2uri.platforms.linux.LinuxExecutor._open_app
- **Calls**: self._desktop_id_for_app, self._first_available, self._first_available, self._result, self._result, self._run, self._run, self._dry

### src.nlp2uri.adapters.mcp.McpAdapter._tool_handle
- **Calls**: self._service_for, svc.handle_prompt, bool, None.get, self.mcp_content, AdapterResponse, None.get, payload.get

### src.nlp2uri.adapters.mcp.McpAdapter._tool_cqrs_compile
- **Calls**: dict, req.extra.get, CqrsDispatcher, d.compile_uri, self.mcp_content, AdapterResponse, req.extra.get, req.extra.get

### src.nlp2uri.cqrs.drivers.service_ops.ServiceCurlDriver.compile
- **Calls**: src.nlp2uri.cqrs.drivers.service_ops.parse_service_name, None.get, _TODOMAT_HEALTH.get, CompileResult, src.nlp2uri.systemmap.compile.compile_system_map_uri, CompileResult, CompileResult, OSAction

### src.nlp2uri.cqrs.drivers.container_docker.ContainerDockerDriver.compile
- **Calls**: src.nlp2uri.cqrs.drivers.container_docker.parse_container_uri, CompileResult, CompileResult, CompileResult, CompileResult, self._docker_argv, CompileResult, OSAction

### examples.mcp.tool-handoff.main.main
- **Calls**: examples.resolve.new-intents.e2e.print, examples.resolve.new-intents.e2e.print, examples.resolve.new-intents.e2e.print, examples.resolve.new-intents.e2e.print, json.dumps, json.dumps, src.nlp2uri.mcp.mcp_handoff_payload, src.nlp2uri.mcp.tool_resolve_desktop_action

### src.nlp2uri.config.NLP2URIConfig.resolved_platform
- **Calls**: None.lower, None.lower, HostPlatform, HostPlatform, src.nlp2uri.platform_detect.detect_platform, None.strip, None.strip, os.environ.get

### src.nlp2uri.parse_nl._parse_capture
- **Calls**: _CAPTURE_RE.search, src.nlp2uri.parse_nl._strip_quotes, src.nlp2uri.parse_nl._capture_target, UriIntent, None.strip, title.lower, params.setdefault, match.group

## Process Flows

Key execution flows identified:

### Flow 1: dispatch
```
dispatch [src.nlp2uri.adapters.rest.RestAdapter]
```

### Flow 2: main
```
main [schemas.codegen.export_driver_stubs]
```

### Flow 3: handle
```
handle [src.nlp2uri.adapters.cli.CliAdapter]
```

### Flow 4: _capture
```
_capture [src.nlp2uri.platforms.linux.LinuxExecutor]
```

### Flow 5: execute
```
execute [src.nlp2uri.platforms.linux.LinuxExecutor]
```

### Flow 6: _docker_argv
```
_docker_argv [src.nlp2uri.cqrs.drivers.container_docker.ContainerDockerDriver]
```

### Flow 7: to_yaml
```
to_yaml [src.nlp2uri.config.NLP2URIConfig]
```

### Flow 8: _tool_cqrs_execute
```
_tool_cqrs_execute [src.nlp2uri.adapters.mcp.McpAdapter]
```

### Flow 9: _args_to_request
```
_args_to_request [src.nlp2uri.adapters.mcp.McpAdapter]
```

### Flow 10: _tool_resolve_system_map
```
_tool_resolve_system_map [src.nlp2uri.adapters.mcp.McpAdapter]
```

## Key Classes

### src.nlp2uri.adapters.mcp.McpAdapter
- **Methods**: 18
- **Key Methods**: src.nlp2uri.adapters.mcp.McpAdapter.handle, src.nlp2uri.adapters.mcp.McpAdapter.call_tool, src.nlp2uri.adapters.mcp.McpAdapter.tool_dispatch, src.nlp2uri.adapters.mcp.McpAdapter._args_from_request, src.nlp2uri.adapters.mcp.McpAdapter._args_to_request, src.nlp2uri.adapters.mcp.McpAdapter.mcp_content, src.nlp2uri.adapters.mcp.McpAdapter._tool_plan, src.nlp2uri.adapters.mcp.McpAdapter._tool_resolve, src.nlp2uri.adapters.mcp.McpAdapter._tool_compile, src.nlp2uri.adapters.mcp.McpAdapter._tool_execute
- **Inherits**: BaseAdapter

### src.nlp2uri.service.NLP2URIService
> Reusable facade: prompt → URI → compile → execute.
- **Methods**: 15
- **Key Methods**: src.nlp2uri.service.NLP2URIService.default, src.nlp2uri.service.NLP2URIService.for_platform, src.nlp2uri.service.NLP2URIService._cfg, src.nlp2uri.service.NLP2URIService._host, src.nlp2uri.service.NLP2URIService.from_prompt, src.nlp2uri.service.NLP2URIService.resolve, src.nlp2uri.service.NLP2URIService.compile, src.nlp2uri.service.NLP2URIService.execute, src.nlp2uri.service.NLP2URIService.handle_prompt, src.nlp2uri.service.NLP2URIService.handle_uri

### src.nlp2uri.platforms.base.UriExecutor
- **Methods**: 8
- **Key Methods**: src.nlp2uri.platforms.base.UriExecutor.execute, src.nlp2uri.platforms.base.UriExecutor._result, src.nlp2uri.platforms.base.UriExecutor._dry, src.nlp2uri.platforms.base.UriExecutor._run, src.nlp2uri.platforms.base.UriExecutor._first_available, src.nlp2uri.platforms.base.UriExecutor._open_with_browser, src.nlp2uri.platforms.base.UriExecutor._parse_nlp2uri, src.nlp2uri.platforms.base.UriExecutor._desktop_id_for_app
- **Inherits**: ABC

### src.nlp2uri.cqrs.registry.DriverRegistry
- **Methods**: 7
- **Key Methods**: src.nlp2uri.cqrs.registry.DriverRegistry.__init__, src.nlp2uri.cqrs.registry.DriverRegistry.schemes, src.nlp2uri.cqrs.registry.DriverRegistry.plugin_drivers, src.nlp2uri.cqrs.registry.DriverRegistry.targets_for, src.nlp2uri.cqrs.registry.DriverRegistry.default_target, src.nlp2uri.cqrs.registry.DriverRegistry.get_driver, src.nlp2uri.cqrs.registry.DriverRegistry.driver_for_uri

### src.nlp2uri.platforms.linux.LinuxExecutor
- **Methods**: 6
- **Key Methods**: src.nlp2uri.platforms.linux.LinuxExecutor.execute, src.nlp2uri.platforms.linux.LinuxExecutor._open_generic, src.nlp2uri.platforms.linux.LinuxExecutor._open_settings, src.nlp2uri.platforms.linux.LinuxExecutor._open_app, src.nlp2uri.platforms.linux.LinuxExecutor._focus_app, src.nlp2uri.platforms.linux.LinuxExecutor._capture
- **Inherits**: UriExecutor

### src.nlp2uri.integrators.rest_server.NLP2URIRequestHandler
- **Methods**: 5
- **Key Methods**: src.nlp2uri.integrators.rest_server.NLP2URIRequestHandler.log_message, src.nlp2uri.integrators.rest_server.NLP2URIRequestHandler._read_json, src.nlp2uri.integrators.rest_server.NLP2URIRequestHandler._send, src.nlp2uri.integrators.rest_server.NLP2URIRequestHandler.do_GET, src.nlp2uri.integrators.rest_server.NLP2URIRequestHandler.do_POST
- **Inherits**: BaseHTTPRequestHandler

### src.nlp2uri.platforms.macos.MacOSExecutor
- **Methods**: 5
- **Key Methods**: src.nlp2uri.platforms.macos.MacOSExecutor.execute, src.nlp2uri.platforms.macos.MacOSExecutor._open, src.nlp2uri.platforms.macos.MacOSExecutor._open_app, src.nlp2uri.platforms.macos.MacOSExecutor._focus_app, src.nlp2uri.platforms.macos.MacOSExecutor._capture
- **Inherits**: UriExecutor

### src.nlp2uri.platforms.windows.WindowsExecutor
- **Methods**: 5
- **Key Methods**: src.nlp2uri.platforms.windows.WindowsExecutor.execute, src.nlp2uri.platforms.windows.WindowsExecutor._start, src.nlp2uri.platforms.windows.WindowsExecutor._open_app, src.nlp2uri.platforms.windows.WindowsExecutor._focus_app, src.nlp2uri.platforms.windows.WindowsExecutor._capture
- **Inherits**: UriExecutor

### src.nlp2uri.config.NLP2URIConfig
> Persisted defaults (nlp2uri.yaml).
- **Methods**: 4
- **Key Methods**: src.nlp2uri.config.NLP2URIConfig.resolved_platform, src.nlp2uri.config.NLP2URIConfig.apply_runtime_env, src.nlp2uri.config.NLP2URIConfig.to_dict, src.nlp2uri.config.NLP2URIConfig.to_yaml

### src.nlp2uri.adapters.base.BaseAdapter
- **Methods**: 4
- **Key Methods**: src.nlp2uri.adapters.base.BaseAdapter.__init__, src.nlp2uri.adapters.base.BaseAdapter.with_platform, src.nlp2uri.adapters.base.BaseAdapter.handle, src.nlp2uri.adapters.base.BaseAdapter._service_for
- **Inherits**: ABC

### src.nlp2uri.adapters.rest.RestAdapter
- **Methods**: 4
- **Key Methods**: src.nlp2uri.adapters.rest.RestAdapter.handle, src.nlp2uri.adapters.rest.RestAdapter.dispatch, src.nlp2uri.adapters.rest.RestAdapter.body_to_request, src.nlp2uri.adapters.rest.RestAdapter.match_route
- **Inherits**: BaseAdapter

### src.nlp2uri.cqrs.base.UriDriver
- **Methods**: 4
- **Key Methods**: src.nlp2uri.cqrs.base.UriDriver.capabilities, src.nlp2uri.cqrs.base.UriDriver.compile, src.nlp2uri.cqrs.base.UriDriver.execute, src.nlp2uri.cqrs.base.UriDriver.probe
- **Inherits**: ABC

### src.nlp2uri.cqrs.event_store.InMemoryEventStore
- **Methods**: 4
- **Key Methods**: src.nlp2uri.cqrs.event_store.InMemoryEventStore.__init__, src.nlp2uri.cqrs.event_store.InMemoryEventStore.append, src.nlp2uri.cqrs.event_store.InMemoryEventStore.get_stream, src.nlp2uri.cqrs.event_store.InMemoryEventStore.all_events

### src.nlp2uri.cqrs.dispatcher.CqrsDispatcher
- **Methods**: 4
- **Key Methods**: src.nlp2uri.cqrs.dispatcher.CqrsDispatcher.__init__, src.nlp2uri.cqrs.dispatcher.CqrsDispatcher.compile_uri, src.nlp2uri.cqrs.dispatcher.CqrsDispatcher.execute_uri, src.nlp2uri.cqrs.dispatcher.CqrsDispatcher.probe_uri

### src.nlp2uri.systemmap.index.UriMap
> ``system_map_uri.v1`` — canonical addressing layer over SystemMapIR.
- **Methods**: 4
- **Key Methods**: src.nlp2uri.systemmap.index.UriMap.lookup, src.nlp2uri.systemmap.index.UriMap.find_by_kind, src.nlp2uri.systemmap.index.UriMap.find_command, src.nlp2uri.systemmap.index.UriMap.to_dict

### src.nlp2uri.models.UriIntent
> Structured intent parsed from natural language.
- **Methods**: 3
- **Key Methods**: src.nlp2uri.models.UriIntent.with_params, src.nlp2uri.models.UriIntent.intent_name, src.nlp2uri.models.UriIntent.to_slots

### src.nlp2uri.cqrs.http_store.HttpEventStore
> In-memory store with async-safe HTTP mirror to process-registry /events.
- **Methods**: 3
- **Key Methods**: src.nlp2uri.cqrs.http_store.HttpEventStore.__init__, src.nlp2uri.cqrs.http_store.HttpEventStore.append, src.nlp2uri.cqrs.http_store.HttpEventStore._post_remote
- **Inherits**: InMemoryEventStore

### src.nlp2uri.cqrs.drivers.container_docker.ContainerDockerDriver
- **Methods**: 3
- **Key Methods**: src.nlp2uri.cqrs.drivers.container_docker.ContainerDockerDriver.compile, src.nlp2uri.cqrs.drivers.container_docker.ContainerDockerDriver.probe, src.nlp2uri.cqrs.drivers.container_docker.ContainerDockerDriver._docker_argv
- **Inherits**: UriDriver

### src.nlp2uri.models.OSAction
> Concrete host command derived from an abstract URI.
- **Methods**: 2
- **Key Methods**: src.nlp2uri.models.OSAction.argv, src.nlp2uri.models.OSAction.to_dict

### src.nlp2uri.adapters.shell.ShellAdapter
- **Methods**: 2
- **Key Methods**: src.nlp2uri.adapters.shell.ShellAdapter.handle, src.nlp2uri.adapters.shell.ShellAdapter._export_script
- **Inherits**: BaseAdapter

## Data Transformation Functions

Key functions that process and transform data:

### src.nlp2uri.config._parse_scalar
- **Output to**: raw.strip, text.startswith, text.endswith, text.startswith, text.endswith

### src.nlp2uri.config._parse_simple_yaml
- **Output to**: text.splitlines, line.strip, stripped.split, src.nlp2uri.config._parse_scalar, stripped.startswith

### src.nlp2uri.cli._build_parser
- **Output to**: argparse.ArgumentParser, src.nlp2uri.cli._add_common_args, parser.add_subparsers, sub.add_parser, src.nlp2uri.cli._add_common_args

### src.nlp2uri.parse_nl._parse_absolute_uri
- **Output to**: urlparse, UriIntent, _ABSOLUTE_URI_RE.match

### src.nlp2uri.parse_nl._parse_http_url
- **Output to**: re.search, UriIntent, url_match.group

### src.nlp2uri.parse_nl._parse_ide_project
- **Output to**: _IDE_PROJECT_RE.search, UriIntent, None.lower, src.nlp2uri.parse_nl._strip_quotes, match.group

### src.nlp2uri.parse_nl._parse_file_open
- **Output to**: _FILE_RE.search, UriIntent, src.nlp2uri.parse_nl._strip_quotes, match.group

### src.nlp2uri.parse_nl._parse_settings_panel
- **Output to**: _SETTINGS_PANEL_RE.search, UriIntent, match.group, match.group, match.group

### src.nlp2uri.parse_nl._parse_terminal
- **Output to**: _TERMINAL_RE.search, match.group, UriIntent, src.nlp2uri.parse_nl._strip_quotes, match.group

### src.nlp2uri.parse_nl._parse_window_move
- **Output to**: _WINDOW_MOVE_RE.search, UriIntent, match.group, match.group

### src.nlp2uri.parse_nl._parse_settings
- **Output to**: UriIntent, _SETTINGS_RE.search

### src.nlp2uri.parse_nl._parse_active_window
- **Output to**: UriIntent, _ACTIVE_WINDOW_RE.search

### src.nlp2uri.parse_nl._parse_capture
- **Output to**: _CAPTURE_RE.search, src.nlp2uri.parse_nl._strip_quotes, src.nlp2uri.parse_nl._capture_target, UriIntent, None.strip

### src.nlp2uri.parse_nl._parse_focus
- **Output to**: _FOCUS_RE.search, UriIntent, None.lower, match.group

### src.nlp2uri.parse_nl._parse_app_open
- **Output to**: _APP_RE.search, UriIntent, src.nlp2uri.parse_nl._normalize_app_name, match.group

### src.nlp2uri.parse_nl._parse_path
- **Output to**: _PATH_RE.search, UriIntent, src.nlp2uri.parse_nl._strip_quotes, path_match.group

### src.nlp2uri.parse_nl._parse_open_prefix
- **Output to**: UriIntent, lowered.startswith, lowered.startswith, None.strip, src.nlp2uri.parse_nl._normalize_app_name

### src.nlp2uri.parse_nl._parse_fallback
- **Output to**: UriIntent

### src.nlp2uri.parse_nl.parse_text
- **Output to**: src.nlp2uri.parse_nl._normalize_aliases, raw.lower, src.nlp2uri.parse_nl._parse_fallback, None.strip, ValueError

### src.nlp2uri.platforms.base.UriExecutor._parse_nlp2uri
- **Output to**: urlparse, None.join, parse_qs, ValueError, parsed.path.lstrip

### src.nlp2uri.host.artifact._decode
- **Output to**: unquote

### src.nlp2uri.host.resource._decode
- **Output to**: unquote

### src.nlp2uri.schemes.util.percent_encode_segment
- **Output to**: quote

### src.nlp2uri.cqrs.drivers.service_ops.parse_service_name
- **Output to**: urlparse, unquote, unquote, parsed.path.lstrip

### src.nlp2uri.systemmap.uri.uri_for_process
> ``process://{example_id}/policy``.
- **Output to**: src.nlp2uri.systemmap.encode.encode_segment

## Public API Surface

Functions exposed as public API (no underscore prefix):

- `src.nlp2uri.systemmap.index.build_uri_index` - 52 calls
- `src.nlp2uri.host.resource.build_resource_actions` - 29 calls
- `src.nlp2uri.adapters.rest.RestAdapter.dispatch` - 29 calls
- `src.nlp2uri.systemmap.getv_uri.build_getv_uri_index` - 24 calls
- `schemas.codegen.export_driver_stubs.main` - 23 calls
- `src.nlp2uri.systemmap.resolve.resolve_prompt_against_system_map` - 23 calls
- `src.nlp2uri.host.artifact.resolve_artifact_path` - 22 calls
- `src.nlp2uri.adapters.cli.CliAdapter.handle` - 21 calls
- `src.nlp2uri.adapters.shell.ShellAdapter.handle` - 19 calls
- `src.nlp2uri.compile.compile_uri_to_actions` - 18 calls
- `src.nlp2uri.systemmap.getv_uri.resolve_prompt_against_getv` - 18 calls
- `src.nlp2uri.systemmap.getv_uri.compile_getv_uri` - 18 calls
- `src.nlp2uri.host.artifact.build_artifact_actions` - 17 calls
- `src.nlp2uri.systemmap.context.load_ir_from_arguments` - 16 calls
- `src.nlp2uri.runtime.execute_uri` - 15 calls
- `src.nlp2uri.config.config_search_paths` - 15 calls
- `src.nlp2uri.schemes.build.build_uri` - 15 calls
- `schemas.codegen.scaffold_scheme.main` - 14 calls
- `schemas.codegen.export_mcp_schemas.main` - 13 calls
- `schemas.codegen.scaffold_scheme.readme_md` - 13 calls
- `src.nlp2uri.platforms.linux.LinuxExecutor.execute` - 13 calls
- `schemas.codegen.scaffold_scheme.scaffold_scheme` - 12 calls
- `src.nlp2uri.integrators.mcp_server.handle_message` - 12 calls
- `src.nlp2uri.integrators.mcp_server.run_stdio` - 12 calls
- `src.nlp2uri.platforms.macos.MacOSExecutor.execute` - 12 calls
- `src.nlp2uri.platforms.windows.WindowsExecutor.execute` - 12 calls
- `src.nlp2uri.config.NLP2URIConfig.to_yaml` - 11 calls
- `src.nlp2uri.cqrs.base.UriDriver.execute` - 11 calls
- `src.nlp2uri.host.endpoint.build_endpoint_url` - 10 calls
- `src.nlp2uri.adapters.rest.RestAdapter.body_to_request` - 10 calls
- `src.nlp2uri.schemes.ide.build_ide` - 10 calls
- `src.nlp2uri.cqrs.dispatcher.CqrsDispatcher.execute_uri` - 10 calls
- `src.nlp2uri.systemmap.compile.compile_system_map_uri` - 10 calls
- `src.nlp2uri.systemmap.getv_uri.get_getv_var_value` - 10 calls
- `src.nlp2uri.cqrs.plugins.load_driver_plugins` - 10 calls
- `src.nlp2uri.config.ensure_config` - 9 calls
- `src.nlp2uri.cqrs.drivers.service_ops.ServiceCurlDriver.compile` - 9 calls
- `src.nlp2uri.cqrs.drivers.container_docker.ContainerDockerDriver.compile` - 9 calls
- `examples.mcp.tool-handoff.main.main` - 8 calls
- `src.nlp2uri.config.NLP2URIConfig.resolved_platform` - 8 calls

## System Interactions

How components interact:

```mermaid
graph TD
    dispatch --> isinstance
    dispatch --> _service_for
    dispatch --> body_to_request
    dispatch --> AdapterResponse
    main --> ArgumentParser
    main --> add_argument
    main --> parse_args
    main --> safe_load
    main --> items
    handle --> _service_for
    handle --> AdapterResponse
    handle --> from_prompt
    handle --> resolve
    _capture --> Path
    _capture --> mkdir
    _capture --> _run
    _capture --> get
    _capture --> _first_available
    handle --> _export_script
    main --> mkdir
    execute --> urlparse
    execute --> _result
    execute --> _open_generic
    execute --> _parse_nlp2uri
    execute --> _open
    execute --> startswith
    execute --> _start
    _docker_argv --> ValueError
    _docker_argv --> get
    _docker_argv --> append
```

## Reverse Engineering Guidelines

1. **Entry Points**: Start analysis from the entry points listed above
2. **Core Logic**: Focus on classes with many methods
3. **Data Flow**: Follow data transformation functions
4. **Process Flows**: Use the flow diagrams for execution paths
5. **API Surface**: Public API functions reveal the interface

## Context for LLM

Maintain the identified architectural patterns and public API surface when suggesting changes.