# ModelGate

ModelGate is a small HTTP gateway for AI model inference.

The current version provides a simple FastAPI service with mock AI models. It allows clients to list available models and send a chat request to a selected model.

This project will be gradually extended during the INF345 course with production features such as real model providers, containerization, CI/CD, observability, reliability, and Kubernetes deployment.

## Current Features

- Health check endpoint
- List available mock models
- Send a chat request to a selected mock model
- Configurable server port through the `PORT` environment variable
- Automated API tests

## Run

Start the service with:

```bash
./scripts/run.sh