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

