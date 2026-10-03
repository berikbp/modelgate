# ModelGate

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
