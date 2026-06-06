#!/usr/bin/env bash
# Generate protobuf stubs, OpenAPI, driver skeletons, MCP schemas from uri_cqrs_es.v1
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$(cd "$ROOT/.." && pwd)"
GEN_PY="$REPO/generated/python"
GEN_OAPI="$REPO/generated/openapi"
GEN_MCP="$REPO/generated/mcp"
GEN_DRV="$REPO/generated/python/drivers"

SCHEME=""
FORCE_SCAFFOLD=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --scheme) SCHEME="$2"; shift 2 ;;
    --scaffold-force) FORCE_SCAFFOLD=1; shift ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

cd "$ROOT"

# 1. Scaffold per-scheme proto tree from registry.yaml
SCAFFOLD_ARGS=()
if [[ -n "$SCHEME" ]]; then
  SCAFFOLD_ARGS+=(--scheme "$SCHEME")
fi
if [[ "$FORCE_SCAFFOLD" == 1 ]]; then
  SCAFFOLD_ARGS+=(--force)
fi
python3 "$ROOT/codegen/scaffold_scheme.py" "${SCAFFOLD_ARGS[@]}"
python3 "$ROOT/codegen/fix_proto_imports.py"

# 2. buf generate (protobuf → Python gRPC) when buf is available
mkdir -p "$GEN_PY" "$GEN_OAPI" "$GEN_MCP" "$GEN_DRV"

if command -v buf >/dev/null 2>&1; then
  echo "==> buf generate"
  buf dep update 2>/dev/null || true
  buf generate
else
  echo "WARN: buf not installed — skip protobuf codegen (brew install bufbuild/buf/buf)" >&2
fi

# 3. MCP tool JSON schemas from registry
python3 "$ROOT/codegen/export_mcp_schemas.py" ${SCHEME:+--scheme "$SCHEME"}

# 4. Driver skeletons per scheme × target
python3 "$ROOT/codegen/export_driver_stubs.py" ${SCHEME:+--scheme "$SCHEME"}

echo "OK: generated → $REPO/generated/"
