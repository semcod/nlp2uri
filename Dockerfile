FROM python:3.12-slim-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        xdg-utils \
        desktop-file-utils \
        wmctrl \
        scrot \
        bash \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -e ".[dev]" \
    && chmod +x examples/run-e2e.sh \
        examples/resolve/nl-to-uri/e2e.sh \
        examples/execute/dry-run/e2e.sh \
        examples/mcp/tool-handoff/e2e.sh \
        examples/integrators/rest-api/e2e.sh \
        examples/integrators/mcp-stdio/e2e.sh \
        examples/integrators/shell-export/e2e.sh \
        scripts/testapp-handler.sh

ENV NLP2URI_CAPTURE_DIR=/tmp/nlp2uri-captures
ENV NLP2URI_INTEGRATION=1

CMD ["bash", "examples/run-e2e.sh"]
