#!/usr/bin/env bash

set -euo pipefail

PORT="${PORT:-8080}"

exec uv run uvicorn app.main:app\
    --host 0.0.0.0 --port "$PORT" --reload --reload-dir app --reload-dir scripts
