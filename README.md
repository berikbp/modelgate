# ModelGate

## Overview

ModelGate is a small HTTP gateway for mock AI model inference. Clients can list available models and send a prompt to a selected model. The responses are generated locally; no provider account or API key is needed.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)

## Run

Start the service on the default port, 8080:

```bash
./scripts/run.sh
```

Set `PORT` to listen on another port:

```bash
PORT=9000 ./scripts/run.sh
```

Check that it is running with `curl http://localhost:8080/healthz` (or use your selected port).

## Test

Run the API tests with:

```bash
./scripts/test.sh
```

The script exits with a failure status if a test fails and prints `TESTS: 5/5` when all five tests pass.

## Endpoints

- `GET /` returns a welcome message.
- `GET /healthz` returns the service health status.
- `GET /v1/models` lists the mock models.
- `POST /v1/chat` accepts JSON such as `{"model":"GPT-4","prompt":"Hello"}` and returns a mock response.

## Docker

Build and start the image with a custom port:

```bash
docker build --platform linux/amd64 -t modelgate:dev .
docker run -d --name modelgate -e PORT=9090 -p 9090:9090 modelgate:dev
curl --fail http://localhost:9090/healthz
docker stop modelgate
docker rm modelgate
```

The runtime uses a non-root user and contains only Python, installed dependencies,
and the application. `PORT` defaults to `8080`.

Run the Compose health check and smoke test:

```bash
docker compose up --build --exit-code-from smoke
docker compose down
```

## Container publishing

Pull requests run the API tests. Pushes to `main` also build a Linux amd64 image,
check `/healthz`, and scan for fixable critical vulnerabilities with Trivy. Only
when these checks pass does CI publish the tested image using `GITHUB_TOKEN`:

- `ghcr.io/berikbp/modelgate:<full-commit-sha>`
- `ghcr.io/berikbp/modelgate:latest`

After the first publish, set the GitHub package visibility to Public so anonymous
users and the milestone marker can pull it. The workflow needs permission to
write packages.

Run the official marker after publishing:

```bash
curl -fLsS https://raw.githubusercontent.com/inf345/inf345-week6-lab/main/mark_m3.py -o /tmp/mark_m3.py
python3 /tmp/mark_m3.py --repo https://github.com/berikbp/modelgate
```
