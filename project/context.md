# System Architecture Analysis
<!-- generated in 0.00s -->

## Overview

- **Project**: /home/tom/github/semcod/nlp2uri
- **Primary Language**: python
- **Languages**: python: 45, shell: 12, yaml: 6, json: 2, yml: 1
- **Analysis Mode**: static
- **Total Functions**: 238
- **Total Classes**: 24
- **Modules**: 68
- **Entry Points**: 124

## Architecture by Module

### src.nlp2uri.compile
- **Functions**: 23
- **File**: `compile.py`

### src.nlp2uri.parse_nl
- **Functions**: 21
- **File**: `parse_nl.py`

### src.nlp2uri.config
- **Functions**: 17
- **Classes**: 1
- **File**: `config.py`

### src.nlp2uri.systemmap.uri
- **Functions**: 13
- **File**: `uri.py`

### src.nlp2uri.adapters.mcp
- **Functions**: 13
- **Classes**: 1
- **File**: `mcp.py`

### src.nlp2uri.service
- **Functions**: 12
- **Classes**: 1
- **File**: `service.py`

### src.nlp2uri.systemmap.compile
- **Functions**: 11
- **File**: `compile.py`

### src.nlp2uri.cli
- **Functions**: 11
- **File**: `cli.py`

### src.nlp2uri.systemmap.index
- **Functions**: 11
- **Classes**: 2
- **File**: `index.py`

### src.nlp2uri.integrators.mcp_server
- **Functions**: 10
- **File**: `mcp_server.py`

### src.nlp2uri.platforms.base
- **Functions**: 9
- **Classes**: 1
- **File**: `base.py`

### src.nlp2uri.integrators.rest_server
- **Functions**: 7
- **Classes**: 1
- **File**: `rest_server.py`

### src.nlp2uri.models
- **Functions**: 7
- **Classes**: 7
- **File**: `models.py`

### src.nlp2uri.platforms.linux
- **Functions**: 6
- **Classes**: 1
- **File**: `linux.py`

### src.nlp2uri.schemes.desktop
- **Functions**: 6
- **File**: `desktop.py`

### src.nlp2uri.mcp
- **Functions**: 5
- **File**: `mcp.py`

### src.nlp2uri.platforms.macos
- **Functions**: 5
- **Classes**: 1
- **File**: `macos.py`

### src.nlp2uri.platforms.windows
- **Functions**: 5
- **Classes**: 1
- **File**: `windows.py`

### src.nlp2uri.adapters.base
- **Functions**: 5
- **Classes**: 3
- **File**: `base.py`

### src.nlp2uri.schemes.util
- **Functions**: 5
- **File**: `util.py`

## Key Entry Points

Main execution flows into the system:

### src.nlp2uri.adapters.rest.RestAdapter.dispatch
- **Calls**: isinstance, self._service_for, self.body_to_request, AdapterResponse, AdapterResponse, svc.from_prompt, AdapterResponse, svc.resolve

### src.nlp2uri.adapters.cli.CliAdapter.handle
- **Calls**: self._service_for, AdapterResponse, svc.from_prompt, AdapterResponse, svc.resolve, AdapterResponse, svc.compile, AdapterResponse

### src.nlp2uri.platforms.linux.LinuxExecutor._capture
- **Calls**: Path, out_dir.mkdir, self._run, os.environ.get, self._first_available, params.get, self._dry, outfile.exists

### src.nlp2uri.adapters.shell.ShellAdapter.handle
- **Calls**: self._service_for, AdapterResponse, svc.from_prompt, self._export_script, AdapterResponse, svc.compile, self._export_script, AdapterResponse

### src.nlp2uri.platforms.linux.LinuxExecutor.execute
- **Calls**: urlparse, self._result, self._open_generic, self._open_generic, self._parse_nlp2uri, path.startswith, self._open_settings, self._open_app

### src.nlp2uri.platforms.macos.MacOSExecutor.execute
- **Calls**: urlparse, self._result, self._open, self._parse_nlp2uri, path.startswith, self._open, self._open_app, self._focus_app

### src.nlp2uri.platforms.windows.WindowsExecutor.execute
- **Calls**: urlparse, self._result, self._start, self._parse_nlp2uri, path.startswith, self._start, self._open_app, self._focus_app

### src.nlp2uri.config.NLP2URIConfig.to_yaml
- **Calls**: lines.append, lines.append, sorted, lines.append, lines.append, self.extra.items, lines.append, None.join

### src.nlp2uri.platforms.macos.MacOSExecutor._capture
- **Calls**: Path, out_dir.mkdir, self._run, os.environ.get, params.get, self._dry, self._result, str

### src.nlp2uri.platforms.windows.WindowsExecutor._capture
- **Calls**: Path, out_dir.mkdir, self._run, outfile.exists, os.environ.get, params.get, self._dry, self._result

### src.nlp2uri.adapters.rest.RestAdapter.body_to_request
- **Calls**: body.get, AdapterRequest, HostPlatform, str, str, bool, body.get, body.get

### src.nlp2uri.schemes.ide.build_ide
- **Calls**: None.lower, src.nlp2uri.schemes.util.normalize_path, _IDE_SCHEMES.get, src.nlp2uri.schemes.util.abstract_url, UriSpec, intent.params.get, ValueError, None.as_posix

### src.nlp2uri.adapters.mcp.McpAdapter._args_to_request
- **Calls**: arguments.get, AdapterRequest, HostPlatform, str, str, bool, arguments.get, arguments.get

### src.nlp2uri.adapters.mcp.McpAdapter._tool_resolve_system_map
- **Calls**: self._service_for, svc.resolve_system_map, payload.get, self.mcp_content, AdapterResponse, src.nlp2uri.systemmap.context.load_ir_from_arguments, AdapterResponse, bool

### src.nlp2uri.integrators.rest_server.NLP2URIRequestHandler._send
- **Calls**: None.encode, self.send_response, self.send_header, self.send_header, self.end_headers, self.wfile.write, str, json.dumps

### src.nlp2uri.platforms.linux.LinuxExecutor._open_app
- **Calls**: self._desktop_id_for_app, self._first_available, self._first_available, self._result, self._result, self._run, self._run, self._dry

### src.nlp2uri.adapters.mcp.McpAdapter._tool_handle
- **Calls**: self._service_for, svc.handle_prompt, bool, None.get, self.mcp_content, AdapterResponse, None.get, payload.get

### examples.mcp.tool-handoff.main.main
- **Calls**: examples.resolve.new-intents.e2e.print, examples.resolve.new-intents.e2e.print, examples.resolve.new-intents.e2e.print, examples.resolve.new-intents.e2e.print, json.dumps, json.dumps, src.nlp2uri.mcp.mcp_handoff_payload, src.nlp2uri.mcp.tool_resolve_desktop_action

### src.nlp2uri.config.NLP2URIConfig.resolved_platform
- **Calls**: None.lower, None.lower, HostPlatform, HostPlatform, src.nlp2uri.platform_detect.detect_platform, None.strip, None.strip, os.environ.get

### src.nlp2uri.integrators.rest_server.NLP2URIRequestHandler.do_POST
- **Calls**: RestAdapter.match_route, self.adapter.dispatch, self._send, self._send, self._read_json, response.to_dict, urlparse, self._send

### src.nlp2uri.platforms.linux.LinuxExecutor._focus_app
- **Calls**: self._first_available, self._first_available, self._open_app, self._result, self._run, self._run, self._dry, self._dry

### src.nlp2uri.schemes.desktop.build_settings
- **Calls**: intent.params.get, UriSpec, _NATIVE_SETTINGS.get, _WINDOWS_SETTINGS_PANELS.get, _MACOS_SETTINGS_PANELS.get, src.nlp2uri.schemes.util.abstract_url, uri.split, uri.split

### src.nlp2uri.parse_nl._parse_capture
- **Calls**: _CAPTURE_RE.search, src.nlp2uri.parse_nl._strip_quotes, src.nlp2uri.parse_nl._capture_target, UriIntent, None.strip, title.lower, params.setdefault, match.group

### examples.execute.dry-run.main.main
- **Calls**: src.nlp2uri.resolve.nlp2uri, src.nlp2uri.compile.compile_uri_to_actions, examples.resolve.new-intents.e2e.print, examples.resolve.new-intents.e2e.print, examples.resolve.new-intents.e2e.print, examples.resolve.new-intents.e2e.print, action.argv

### src.nlp2uri.integrators.rest_server.NLP2URIRequestHandler.do_GET
- **Calls**: RestAdapter.match_route, self.adapter.dispatch, self._send, self._send, AdapterRequest, response.to_dict, urlparse

### src.nlp2uri.platforms.base.UriExecutor._parse_nlp2uri
- **Calls**: urlparse, None.join, parse_qs, ValueError, parsed.path.lstrip, unquote, raw.items

### src.nlp2uri.platforms.base.UriExecutor._desktop_id_for_app
- **Calls**: None.removesuffix, Path, base.glob, name.lower, base.is_dir, None.is_file, entry.name.lower

### src.nlp2uri.cli.main
- **Calls**: None.parse_args, src.nlp2uri.config.ensure_config, src.nlp2uri.cli._run_execute, src.nlp2uri.cli._run_config, src.nlp2uri.cli._run_shell, src.nlp2uri.cli._run_adapter_command, src.nlp2uri.cli._build_parser

### src.nlp2uri.parse_nl._parse_settings_panel
- **Calls**: _SETTINGS_PANEL_RE.search, UriIntent, match.group, match.group, match.group, match.group, src.nlp2uri.parse_nl._normalize_panel

### src.nlp2uri.parse_nl._parse_open_prefix
- **Calls**: UriIntent, lowered.startswith, lowered.startswith, None.strip, src.nlp2uri.parse_nl._normalize_app_name, remainder.split, len

## Process Flows

Key execution flows identified:

### Flow 1: dispatch
```
dispatch [src.nlp2uri.adapters.rest.RestAdapter]
```

### Flow 2: handle
```
handle [src.nlp2uri.adapters.cli.CliAdapter]
```

### Flow 3: _capture
```
_capture [src.nlp2uri.platforms.linux.LinuxExecutor]
```

### Flow 4: execute
```
execute [src.nlp2uri.platforms.linux.LinuxExecutor]
```

### Flow 5: to_yaml
```
to_yaml [src.nlp2uri.config.NLP2URIConfig]
```

### Flow 6: body_to_request
```
body_to_request [src.nlp2uri.adapters.rest.RestAdapter]
```

### Flow 7: build_ide
```
build_ide [src.nlp2uri.schemes.ide]
  └─ →> normalize_path
  └─ →> abstract_url
```

### Flow 8: _args_to_request
```
_args_to_request [src.nlp2uri.adapters.mcp.McpAdapter]
```

### Flow 9: _tool_resolve_system_map
```
_tool_resolve_system_map [src.nlp2uri.adapters.mcp.McpAdapter]
```

### Flow 10: _send
```
_send [src.nlp2uri.integrators.rest_server.NLP2URIRequestHandler]
```

## Key Classes

### src.nlp2uri.adapters.mcp.McpAdapter
- **Methods**: 13
- **Key Methods**: src.nlp2uri.adapters.mcp.McpAdapter.handle, src.nlp2uri.adapters.mcp.McpAdapter.call_tool, src.nlp2uri.adapters.mcp.McpAdapter.tool_dispatch, src.nlp2uri.adapters.mcp.McpAdapter._args_from_request, src.nlp2uri.adapters.mcp.McpAdapter._args_to_request, src.nlp2uri.adapters.mcp.McpAdapter.mcp_content, src.nlp2uri.adapters.mcp.McpAdapter._tool_plan, src.nlp2uri.adapters.mcp.McpAdapter._tool_resolve, src.nlp2uri.adapters.mcp.McpAdapter._tool_compile, src.nlp2uri.adapters.mcp.McpAdapter._tool_execute
- **Inherits**: BaseAdapter

### src.nlp2uri.service.NLP2URIService
> Reusable facade: prompt → URI → compile → execute.
- **Methods**: 12
- **Key Methods**: src.nlp2uri.service.NLP2URIService.default, src.nlp2uri.service.NLP2URIService.for_platform, src.nlp2uri.service.NLP2URIService._cfg, src.nlp2uri.service.NLP2URIService._host, src.nlp2uri.service.NLP2URIService.from_prompt, src.nlp2uri.service.NLP2URIService.resolve, src.nlp2uri.service.NLP2URIService.compile, src.nlp2uri.service.NLP2URIService.execute, src.nlp2uri.service.NLP2URIService.handle_prompt, src.nlp2uri.service.NLP2URIService.handle_uri

### src.nlp2uri.platforms.base.UriExecutor
- **Methods**: 8
- **Key Methods**: src.nlp2uri.platforms.base.UriExecutor.execute, src.nlp2uri.platforms.base.UriExecutor._result, src.nlp2uri.platforms.base.UriExecutor._dry, src.nlp2uri.platforms.base.UriExecutor._run, src.nlp2uri.platforms.base.UriExecutor._first_available, src.nlp2uri.platforms.base.UriExecutor._open_with_browser, src.nlp2uri.platforms.base.UriExecutor._parse_nlp2uri, src.nlp2uri.platforms.base.UriExecutor._desktop_id_for_app
- **Inherits**: ABC

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

### src.nlp2uri.systemmap.index.UriMap
> ``system_map_uri.v1`` — canonical addressing layer over SystemMapIR.
- **Methods**: 4
- **Key Methods**: src.nlp2uri.systemmap.index.UriMap.lookup, src.nlp2uri.systemmap.index.UriMap.find_by_kind, src.nlp2uri.systemmap.index.UriMap.find_command, src.nlp2uri.systemmap.index.UriMap.to_dict

### src.nlp2uri.models.UriIntent
> Structured intent parsed from natural language.
- **Methods**: 3
- **Key Methods**: src.nlp2uri.models.UriIntent.with_params, src.nlp2uri.models.UriIntent.intent_name, src.nlp2uri.models.UriIntent.to_slots

### src.nlp2uri.adapters.shell.ShellAdapter
- **Methods**: 2
- **Key Methods**: src.nlp2uri.adapters.shell.ShellAdapter.handle, src.nlp2uri.adapters.shell.ShellAdapter._export_script
- **Inherits**: BaseAdapter

### src.nlp2uri.models.OSAction
> Concrete host command derived from an abstract URI.
- **Methods**: 2
- **Key Methods**: src.nlp2uri.models.OSAction.argv, src.nlp2uri.models.OSAction.to_dict

### src.nlp2uri.adapters.base.AdapterResponse
- **Methods**: 1
- **Key Methods**: src.nlp2uri.adapters.base.AdapterResponse.to_dict

### src.nlp2uri.adapters.cli.CliAdapter
- **Methods**: 1
- **Key Methods**: src.nlp2uri.adapters.cli.CliAdapter.handle
- **Inherits**: BaseAdapter

### src.nlp2uri.systemmap.resolve.ResolvedSystemUri
> One NL match against the SystemMap.
- **Methods**: 1
- **Key Methods**: src.nlp2uri.systemmap.resolve.ResolvedSystemUri.to_dict

### src.nlp2uri.systemmap.index.UriMapEntry
> One addressable entity in a SystemMap.
- **Methods**: 1
- **Key Methods**: src.nlp2uri.systemmap.index.UriMapEntry.to_dict

### src.nlp2uri.models.UriSpec
> Resolved abstract URI ready for execution or MCP handoff.
- **Methods**: 1
- **Key Methods**: src.nlp2uri.models.UriSpec.to_dict

### src.nlp2uri.models.NLP2URIResult
> Full compiler output: NL → URI + OS action plan.
- **Methods**: 1
- **Key Methods**: src.nlp2uri.models.NLP2URIResult.to_dict

## Data Transformation Functions

Key functions that process and transform data:

### src.nlp2uri.config._parse_scalar
- **Output to**: raw.strip, text.startswith, text.endswith, text.startswith, text.endswith

### src.nlp2uri.config._parse_simple_yaml
- **Output to**: text.splitlines, line.strip, stripped.split, src.nlp2uri.config._parse_scalar, stripped.startswith

### src.nlp2uri.platforms.base.UriExecutor._parse_nlp2uri
- **Output to**: urlparse, None.join, parse_qs, ValueError, parsed.path.lstrip

### src.nlp2uri.schemes.util.percent_encode_segment
- **Output to**: quote

### src.nlp2uri.systemmap.encode.encode_segment
> Encode a single URI path/authority segment (preserves unreserved).
- **Output to**: quote

### src.nlp2uri.systemmap.encode.encode_path
> Encode a slash-separated path while keeping path separators.
- **Output to**: quote, value.lstrip

### src.nlp2uri.systemmap.uri.uri_for_process
> ``process://{example_id}/policy``.
- **Output to**: src.nlp2uri.systemmap.encode.encode_segment

### src.nlp2uri.systemmap.compile._decode_segment
- **Output to**: unquote

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

## Public API Surface

Functions exposed as public API (no underscore prefix):

- `src.nlp2uri.systemmap.index.build_uri_index` - 52 calls
- `src.nlp2uri.adapters.rest.RestAdapter.dispatch` - 29 calls
- `src.nlp2uri.systemmap.resolve.resolve_prompt_against_system_map` - 23 calls
- `src.nlp2uri.adapters.cli.CliAdapter.handle` - 21 calls
- `src.nlp2uri.adapters.shell.ShellAdapter.handle` - 19 calls
- `src.nlp2uri.systemmap.context.load_ir_from_arguments` - 16 calls
- `src.nlp2uri.runtime.execute_uri` - 15 calls
- `src.nlp2uri.config.config_search_paths` - 15 calls
- `src.nlp2uri.schemes.build.build_uri` - 15 calls
- `src.nlp2uri.compile.compile_uri_to_actions` - 14 calls
- `src.nlp2uri.platforms.linux.LinuxExecutor.execute` - 13 calls
- `src.nlp2uri.integrators.mcp_server.handle_message` - 12 calls
- `src.nlp2uri.integrators.mcp_server.run_stdio` - 12 calls
- `src.nlp2uri.platforms.macos.MacOSExecutor.execute` - 12 calls
- `src.nlp2uri.platforms.windows.WindowsExecutor.execute` - 12 calls
- `src.nlp2uri.config.NLP2URIConfig.to_yaml` - 11 calls
- `src.nlp2uri.adapters.rest.RestAdapter.body_to_request` - 10 calls
- `src.nlp2uri.schemes.ide.build_ide` - 10 calls
- `src.nlp2uri.systemmap.compile.compile_system_map_uri` - 10 calls
- `src.nlp2uri.config.ensure_config` - 9 calls
- `examples.mcp.tool-handoff.main.main` - 8 calls
- `src.nlp2uri.config.NLP2URIConfig.resolved_platform` - 8 calls
- `src.nlp2uri.config.save_config` - 8 calls
- `src.nlp2uri.resolve.nlp2uri` - 8 calls
- `src.nlp2uri.integrators.rest_server.NLP2URIRequestHandler.do_POST` - 8 calls
- `src.nlp2uri.schemes.desktop.build_settings` - 8 calls
- `examples.execute.dry-run.main.main` - 7 calls
- `src.nlp2uri.integrators.rest_server.NLP2URIRequestHandler.do_GET` - 7 calls
- `src.nlp2uri.integrators.rest_server.run_server` - 7 calls
- `src.nlp2uri.systemmap.uri.uri_for_access` - 7 calls
- `src.nlp2uri.cli.main` - 7 calls
- `src.nlp2uri.schemes.file.build_file` - 6 calls
- `src.nlp2uri.parse_nl.parse_text` - 6 calls
- `src.nlp2uri.integrators.rest_server.main` - 5 calls
- `src.nlp2uri.schemes.util.abstract_url` - 5 calls
- `src.nlp2uri.schemes.util.normalize_path` - 5 calls
- `src.nlp2uri.systemmap.fallback.resolve_prompt_with_fallback` - 5 calls
- `src.nlp2uri.schemes.desktop.build_capture` - 5 calls
- `src.nlp2uri.schemes.desktop.build_focus` - 5 calls
- `src.nlp2uri.schemes.desktop.build_app_open` - 5 calls

## System Interactions

How components interact:

```mermaid
graph TD
    dispatch --> isinstance
    dispatch --> _service_for
    dispatch --> body_to_request
    dispatch --> AdapterResponse
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
    execute --> urlparse
    execute --> _result
    execute --> _open_generic
    execute --> _parse_nlp2uri
    execute --> _open
    execute --> startswith
    execute --> _start
    to_yaml --> append
    to_yaml --> sorted
    _capture --> exists
    body_to_request --> get
    body_to_request --> AdapterRequest
    body_to_request --> HostPlatform
    body_to_request --> str
    build_ide --> lower
    build_ide --> normalize_path
```

## Reverse Engineering Guidelines

1. **Entry Points**: Start analysis from the entry points listed above
2. **Core Logic**: Focus on classes with many methods
3. **Data Flow**: Follow data transformation functions
4. **Process Flows**: Use the flow diagrams for execution paths
5. **API Surface**: Public API functions reveal the interface

## Context for LLM

Maintain the identified architectural patterns and public API surface when suggesting changes.