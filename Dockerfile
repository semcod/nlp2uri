FROM python:3.12-slim-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        xdg-utils \
        desktop-file-utils \
        wmctrl \
        scrot \
        bash \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -e ".[dev]" \
    && chmod +x examples/run_all.sh scripts/testapp-handler.sh

ENV NLP2URI_CAPTURE_DIR=/tmp/nlp2uri-captures
ENV NLP2URI_INTEGRATION=1

CMD ["bash", "examples/run_all.sh"]
