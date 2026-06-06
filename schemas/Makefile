.PHONY: scaffold generate proto mcp drivers all

scaffold:
	python3 codegen/scaffold_scheme.py

generate: scaffold mcp drivers

proto:
	@command -v buf >/dev/null || (echo "install buf: https://buf.build/docs/installation" && exit 1)
	buf dep update
	buf generate

mcp:
	python3 codegen/export_mcp_schemas.py

drivers:
	python3 codegen/export_driver_stubs.py

all:
	./codegen/generate.sh

scheme:
	@test -n "$(SCHEME)" || (echo "usage: make scheme SCHEME=command" && exit 1)
	./codegen/generate.sh --scheme $(SCHEME)
