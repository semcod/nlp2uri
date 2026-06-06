#!/usr/bin/env bash
# x-scheme-handler/testapp log sink for Docker integration tests.
set -euo pipefail
LOG_FILE="${NLP2URI_HANDLER_LOG:-/tmp/nlp2uri-handler.log}"
printf '%s\n' "$*" >>"$LOG_FILE"
exit 0
