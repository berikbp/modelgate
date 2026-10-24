# Build dependencies in a separate stage.
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app
ENV UV_LINK_MODE=copy \
    UV_NO_PROGRESS=1

RUN python -m pip install --no-cache-dir uv

# Dependency manifests go first so Docker can cache installed packages.
COPY pyproject.toml uv.lock .python-version README.md ./
RUN uv sync --frozen --no-install-project --no-dev

# The final stage contains Python, installed packages, and application code only.
FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app
ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1

COPY --from=builder /app/.venv /app/.venv
COPY app/ ./app/

USER 10001:10001

EXPOSE 8080
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port \"${PORT:-8080}\""]
