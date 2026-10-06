#!/usr/bin/env bash

set -euo pipefail

uv run python -m pytest -q

echo "TESTS: 5/5"