# ModelGate — Production AI Inference Gateway

> **Project type:** Semester-long production AI infrastructure project  
> **Primary language:** Python  
> **Initial framework:** FastAPI  
> **Long-term direction:** Backend engineering + DevOps + MLOps + AI infrastructure  
> **Course:** INF345  
> **Core principle:** Start extremely small, then improve the same project throughout the semester instead of rebuilding it.

---

## 1. Project in One Sentence

**ModelGate is a production-oriented AI inference gateway that gives applications one stable HTTP API for talking to AI models, while gradually adding routing, reliability, rate limiting, caching, observability, evaluation, cost tracking, containerization, and Kubernetes deployment.**

The project starts as a very small HTTP service and grows into a realistic piece of AI infrastructure.

---

# 2. The Main Idea

Applications that use Large Language Models often call model providers directly:

```text
Application
    |
    v
OpenAI / Anthropic / Ollama / another model
```

This is easy at first, but it creates problems as the system grows.

For example:

- What happens if the model provider is down?
- What if one team sends too many requests?
- What if API costs become too high?
- What if the same request is repeated many times?
- What if a cheaper model could answer a simple request?
- What if a model change makes quality worse?
- How do we measure latency?
- How do we know which provider is failing?
- How do we inspect requests in production?
- How do we deploy multiple instances?
- How do we safely roll out model changes?
- How do we keep application code independent from model vendors?

ModelGate sits between applications and AI providers.

```text
Application
    |
    v
+----------------+
|   ModelGate    |
+----------------+
    |
    +-----------------+-----------------+
    |                 |                 |
    v                 v                 v
 Local Model        OpenAI          Anthropic
```

The application talks only to ModelGate.

ModelGate decides what should happen behind the scenes.

That means application code can remain stable even when the AI infrastructure changes.

---

# 3. Why This Project Exists

The goal is **not** to build another chatbot.

The goal is to learn what happens around AI models when they are used in real production systems.

The project is designed to develop skills in:

- backend engineering
- API design
- asynchronous programming
- testing
- Git workflows
- CI/CD
- Docker
- Docker Compose
- databases
- Redis
- caching
- distributed systems
- reliability engineering
- observability
- monitoring
- security
- secrets management
- load testing
- Kubernetes
- MLOps
- model serving
- model routing
- AI evaluation
- cost optimization
- production debugging

The AI model itself is only one part of the system.

The main engineering challenge is making the surrounding infrastructure reliable, observable, testable, scalable, and maintainable.

---

# 4. Why It Fits INF345

INF345 is not asking for a huge application immediately.

The course is designed around gradually taking the **same repository** from a small local service toward production deployment.

The expected progression is approximately:

```text
Small HTTP service
        |
        v
Tests
        |
        v
CI/CD
        |
        v
Docker
        |
        v
Deployment
        |
        v
Kubernetes
        |
        v
Production concerns
```

ModelGate naturally follows the same path:

```text
Tiny AI Gateway
        |
        v
Tests
        |
        v
CI/CD
        |
        v
Docker
        |
        v
Real model providers
        |
        v
Redis / PostgreSQL
        |
        v
Observability
        |
        v
Kubernetes
        |
        v
Production AI infrastructure
```

Nothing has to be thrown away.

Every future addition extends the same project.

---

# 5. The Most Important Rule

## Do not build the final system immediately.

The final architecture may eventually include:

- FastAPI
- PostgreSQL
- Redis
- OpenTelemetry
- Prometheus
- Grafana
- multiple model providers
- semantic caching
- model routing
- background workers
- CI/CD
- Docker
- Kubernetes

But **Week 3 should contain almost none of that**.

The point is to grow the architecture gradually.

A good project history should look like this:

```text
v0.1  Basic HTTP API
v0.2  Provider abstraction
v0.3  Real local model
v0.4  Request logging
v0.5  Persistent storage
v0.6  Rate limiting
v0.7  Caching
v0.8  Intelligent routing
v0.9  Reliability and fallbacks
v0.10 Observability
v0.11 Evaluation pipeline
v0.12 Production deployment
v1.0  Kubernetes-ready AI gateway
```

The development history is part of the value of the project.

---

# 6. Week 3 Scope — The Project Starts Here

For the first milestone, ModelGate should be intentionally simple.

The project only needs a small FastAPI HTTP service.

## Week 3 architecture

```text
Client
   |
   v
+-----------+
| FastAPI   |
| ModelGate |
+-----------+
   |
   v
Mock Provider
```

There is no real LLM requirement yet.

There is no database.

There is no Redis.

There is no authentication.

There are no API keys.

There is no Docker requirement yet unless the course later asks for it.

There is no frontend.

There is no Kubernetes.

---

# 7. Week 3 API

The initial service can expose four endpoints.

## 7.1 `GET /`

Purpose:

- prove the service is running
- provide simple service metadata

Example response:

```json
{
  "service": "ModelGate",
  "version": "0.1.0",
  "description": "AI model gateway"
}
```

---

## 7.2 `GET /healthz`

Purpose:

- provide a very fast health check
- satisfy the INF345 contract
- later become useful for Docker and Kubernetes health probes

Example response:

```json
{
  "status": "ok"
}
```

Requirements:

- HTTP 200
- non-empty response
- no dependency on a database
- should answer very quickly
- should continue working even if optional external systems are unavailable

This endpoint should remain simple for the whole project.

---

## 7.3 `GET /v1/models`

Purpose:

Return the models currently available through the gateway.

In Week 3 they can be fake models.

Example:

```json
{
  "models": [
    {
      "id": "mock-small",
      "provider": "mock"
    },
    {
      "id": "mock-large",
      "provider": "mock"
    }
  ]
}
```

Later this endpoint can return real model information.

---

## 7.4 `POST /v1/chat`

Purpose:

Provide the first stable inference interface.

Example request:

```json
{
  "model": "mock-small",
  "message": "Hello"
}
```

Example response:

```json
{
  "model": "mock-small",
  "provider": "mock",
  "response": "Mock response: Hello"
}
```

For Week 3 the response can be generated without any real AI model.

The important part is establishing the HTTP contract.

---

# 8. Why Use a Mock Provider First?

Starting with a mock provider is deliberate.

A mock provider might do something as simple as:

```text
Input:
"Hello"

Output:
"Mock response: Hello"
```

This gives several advantages:

- no API key
- no internet dependency
- no external failures
- no cost
- deterministic tests
- fast tests
- easy debugging
- easier INF345 grading
- no credentials accidentally committed to Git

Most importantly, it lets the project establish a stable interface before integrating real models.

Later:

```text
MockProvider
```

can be replaced or joined by:

```text
OllamaProvider
OpenAIProvider
AnthropicProvider
```

without changing the external API.

---

# 9. Initial Provider Abstraction

A later early milestone should introduce a provider interface.

Conceptually:

```python
class ModelProvider:
    async def generate(self, request):
        ...
```

Implementations:

```text
ModelProvider
    |
    +-- MockProvider
    |
    +-- OllamaProvider
    |
    +-- OpenAIProvider
    |
    +-- AnthropicProvider
```

This is important because ModelGate should not be tightly coupled to one AI provider.

The gateway should depend on a common interface.

Individual providers should contain provider-specific code.

---

# 10. Stable Interface Principle

One of the main engineering lessons of this project is:

> **The implementation may change while the external contract stays stable.**

For example, this endpoint:

```text
POST /v1/chat
```

might initially call:

```text
MockProvider
```

then later:

```text
Ollama
```

then:

```text
OpenAI
```

then eventually:

```text
Router
   |
   +-- Qwen
   +-- OpenAI
   +-- Anthropic
```

But applications using ModelGate should not need major changes.

That is the role of the gateway.

---

# 11. Suggested Initial Repository Structure

A simple starting structure:

```text
modelgate/
|
+-- app/
|   +-- __init__.py
|   +-- main.py
|   +-- schemas.py
|   +-- providers/
|       +-- __init__.py
|       +-- mock.py
|
+-- tests/
|   +-- test_health.py
|   +-- test_models.py
|   +-- test_chat.py
|
+-- scripts/
|   +-- run.sh
|   +-- test.sh
|
+-- requirements.txt
+-- README.md
+-- .gitignore
```

Do not create many unnecessary layers in Week 3.

The project structure should grow only when complexity actually requires it.

---

# 12. INF345 Week 3 Contract

The project must satisfy the course contract.

## `scripts/run.sh`

Responsibilities:

- start the service
- use `$PORT`
- default to port `8080`

Example concept:

```bash
#!/usr/bin/env bash
set -euo pipefail

export PORT="${PORT:-8080}"

python3 -m app.main
```

If using Uvicorn directly:

```bash
uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8080}"
```

The exact implementation can vary, but `$PORT` must be respected.

---

## `scripts/test.sh`

Responsibilities:

- run the real test suite
- return exit code `0` on success
- print the normalized summary required by the course

Example final line:

```text
TESTS: 5/5
```

The tests must genuinely depend on the application.

They must not be fake tests that only print success.

---

# 13. Initial Test Cases

At least the following tests should exist.

## Test 1 — Root endpoint

```text
GET /
```

Expected:

```text
HTTP 200
```

---

## Test 2 — Health endpoint

```text
GET /healthz
```

Expected:

```text
HTTP 200
```

and a non-empty body.

---

## Test 3 — List models

```text
GET /v1/models
```

Expected:

- HTTP 200
- model list exists
- at least one mock model exists

---

## Test 4 — Chat request

```text
POST /v1/chat
```

Expected:

- HTTP 200
- returned model matches request
- response is non-empty

---

## Test 5 — Invalid model

Request:

```json
{
  "model": "does-not-exist",
  "message": "Hello"
}
```

Expected:

```text
HTTP 400 or 404
```

The exact status should be chosen once and then kept consistent.

---

# 14. Git Strategy

The repository should demonstrate real development.

Do not create the entire project in one commit.

A reasonable early history:

```text
Initial project structure

Add FastAPI application

Add health endpoint

Add mock model provider

Add model listing endpoint

Add chat endpoint

Add API tests

Add run and test scripts

Document project setup
```

Use branches for meaningful changes.

Example:

```text
main
 |
 +-- feature/health-endpoint
 |
 +-- feature/mock-provider
 |
 +-- feature/chat-api
```

Open and merge pull requests.

This will also help satisfy the course repository-quality requirements.

---

# 15. Real Model Integration

After the basic API is stable, add the first real provider.

The best first real provider is probably a local model through Ollama or another local inference server.

Architecture:

```text
Client
   |
   v
ModelGate
   |
   v
Ollama
   |
   v
Qwen / Llama / another local model
```

Why local first:

- no paid API required
- fewer secret-management problems
- easier experimentation
- useful for learning model serving
- can work with models already available locally

The mock provider should remain available for tests.

---

# 16. Multi-Provider Architecture

Later:

```text
                   +----------------+
                   |   ModelGate    |
                   +-------+--------+
                           |
              +------------+------------+
              |            |            |
              v            v            v
           Ollama        OpenAI      Anthropic
```

A provider registry can map model names to providers.

Example concept:

```text
qwen-local
    -> OllamaProvider

gpt-model
    -> OpenAIProvider

claude-model
    -> AnthropicProvider
```

The gateway should normalize provider-specific responses into one common response format.

---

# 17. Request and Response Normalization

Providers use different request structures.

ModelGate should eventually define its own canonical request schema.

Example:

```json
{
  "model": "qwen-local",
  "messages": [
    {
      "role": "user",
      "content": "Explain distributed systems."
    }
  ],
  "temperature": 0.2,
  "max_tokens": 500
}
```

And a normalized response:

```json
{
  "id": "req_123",
  "model_requested": "qwen-local",
  "model_served": "qwen-local",
  "provider": "ollama",
  "output": "A distributed system...",
  "usage": {
    "input_tokens": 8,
    "output_tokens": 91
  },
  "latency_ms": 734
}
```

The provider adapter translates between this format and provider-specific formats.

---

# 18. Persistent Request Logging

Eventually every request should receive a unique request ID.

Store metadata such as:

```text
request_id
timestamp
provider
requested_model
served_model
input_tokens
output_tokens
latency
status
error_type
cache_hit
fallback_used
estimated_cost
```

Do not blindly store sensitive prompts.

Production logging should distinguish:

- operational metadata
- optional content logging
- personally identifiable information
- secrets

The system should be designed so content logging can be disabled.

---

# 19. PostgreSQL

When persistence becomes necessary, introduce PostgreSQL.

Possible stored entities:

```text
teams
api_keys
requests
providers
model_configs
usage_records
budgets
routing_rules
evaluation_runs
```

Architecture:

```text
ModelGate
   |
   +-- LLM Providers
   |
   +-- PostgreSQL
```

Use migrations instead of manually changing production schemas.

Possible future tooling:

```text
SQLAlchemy
Alembic
```

---

# 20. Redis

Redis can support several production features.

Possible uses:

```text
rate limiting
cache
temporary state
distributed locks
request counters
provider health state
```

Do not introduce Redis before there is a reason.

---

# 21. Rate Limiting

One future feature is controlling how many requests a client or team may send.

Example plans:

```text
Free team:
10 requests/minute

Standard team:
100 requests/minute

Internal service:
1000 requests/minute
```

A distributed implementation can use Redis.

Later the gateway can enforce:

```text
requests/minute
tokens/minute
concurrent requests
daily usage
monthly budget
```

Typical response when limited:

```text
HTTP 429 Too Many Requests
```

Possible header:

```text
Retry-After
```

---

# 22. Authentication

Later clients should authenticate to the gateway.

For example:

```text
Authorization: Bearer <MODEL_GATE_API_KEY>
```

The gateway can map the key to:

```text
team
permissions
allowed models
rate limits
budget
```

Never store raw production API keys if avoidable.

Store hashes where appropriate.

Secrets must never be committed to Git.

---

# 23. Cost Tracking

Cloud AI models can cost money per token.

ModelGate can calculate approximate request cost.

Example:

```text
Input tokens:  500
Output tokens: 200

Input cost:    ...
Output cost:   ...

Total request cost: ...
```

Useful metrics:

```text
cost per request
cost per team
cost per model
cost per day
cost per month
cost per successful request
```

Eventually the gateway can enforce budgets.

Example:

```text
Team monthly budget = $50

Current usage = $49.80

New expensive request
        |
        v
budget check
        |
        v
deny or route to cheaper model
```

---

# 24. Intelligent Model Routing

Initially the user chooses a model.

Later ModelGate can choose automatically.

Example:

```text
Incoming request
       |
       v
Complexity classifier
   /       |       \
  /        |        \
simple   medium    complex
  |        |          |
  v        v          v
small    medium      large
model     model       model
```

Example:

```text
"Translate hello into Spanish."

-> small local model
```

Example:

```text
"Compare two distributed database architectures and
analyze consistency, fault tolerance, and failure modes."

-> stronger model
```

The routing system can optimize multiple objectives:

```text
quality
latency
cost
availability
privacy
context length
```

---

# 25. Routing Policies

Routing should eventually be configurable rather than hardcoded.

Example configuration:

```yaml
routing:
  simple:
    primary: qwen-local
    fallback: gpt-small

  medium:
    primary: gpt-small
    fallback: claude-medium

  complex:
    primary: gpt-large
    fallback: claude-large
```

Later this can be stored in PostgreSQL or another configuration system.

---

# 26. Semantic Caching

Traditional caching compares exact keys.

But AI requests can be semantically equivalent.

Example:

```text
"What is Python?"
```

and:

```text
"Explain Python to me."
```

may mean nearly the same thing.

A semantic cache can:

1. embed the incoming prompt
2. search previous cached prompts
3. calculate similarity
4. return a cached result if similarity is high enough
5. otherwise call the real model
6. store the new result

Architecture:

```text
Request
   |
   v
Semantic Cache
   |
   +-- HIT --> cached response
   |
   +-- MISS
         |
         v
        LLM
         |
         v
      response
         |
         v
    store cache
```

---

# 27. Cache Correctness

Caching LLM responses is dangerous if implemented carelessly.

A cache key may need to consider:

```text
user prompt
system prompt
model
temperature
max tokens
tool configuration
provider
prompt version
```

Two requests with the same user text should not necessarily share a response.

---

# 28. Cache Expiration

Cached responses should have a TTL.

Example:

```text
stable programming question:
24 hours

time-sensitive question:
5 minutes

current news:
do not cache
```

Later, ModelGate can classify requests and choose cache policies automatically.

---

# 29. Reliability Engineering

AI providers can fail.

Production systems must expect failure.

ModelGate should eventually implement:

```text
timeouts
retries
exponential backoff
health checks
fallback routing
circuit breakers
graceful degradation
```

---

# 30. Timeouts

Every external request needs a timeout.

Bad:

```text
call model
wait forever
```

Better:

```text
call model
   |
   +-- response before timeout -> continue
   |
   +-- timeout -> retry/fallback/error
```

Timeout configuration should be explicit.

---

# 31. Retries

Some failures are temporary.

Examples:

```text
network timeout
HTTP 429
temporary HTTP 5xx
```

Retries should be bounded.

Example:

```text
attempt 1
   |
 failure
   |
wait 0.5s
   |
attempt 2
   |
 failure
   |
wait 1s
   |
attempt 3
```

Do not retry every error.

Authentication failures normally should not be retried.

---

# 32. Fallback Providers

Example:

```text
Request
   |
   v
OpenAI
   |
 timeout
   |
   v
retry
   |
 failure
   |
   v
Anthropic fallback
   |
   v
response
```

The final response should contain metadata indicating which model actually served the request.

---

# 33. Circuit Breaker

Repeatedly sending requests to a failing provider wastes time.

A circuit breaker has approximately three states:

```text
CLOSED
normal traffic allowed

OPEN
provider considered unhealthy
traffic blocked

HALF-OPEN
send a test request
```

Example:

```text
Provider fails repeatedly
        |
        v
Circuit opens
        |
        v
Requests use fallback
        |
        v
Cooldown
        |
        v
Test request
   /          \
success       fail
  |             |
  v             v
close        open again
```

---

# 34. Health Checks

The gateway can eventually track provider health.

Possible state:

```text
healthy
degraded
down
```

Possible measurements:

```text
recent error rate
P95 latency
P99 latency
timeout count
rate-limit count
successful health requests
```

---

# 35. Observability

One of the most important goals is learning how to understand a system after deployment.

Observability consists mainly of:

```text
logs
metrics
traces
```

All three should eventually exist.

---

# 36. Structured Logging

Do not rely only on:

```python
print("something broke")
```

Use structured logs.

Example:

```json
{
  "event": "inference_completed",
  "request_id": "req_42",
  "provider": "ollama",
  "model": "qwen",
  "latency_ms": 713,
  "status": "success"
}
```

Structured logs are easier to search and analyze.

---

# 37. Metrics

Prometheus can eventually collect metrics such as:

```text
modelgate_requests_total
modelgate_request_duration_seconds
modelgate_provider_errors_total
modelgate_tokens_input_total
modelgate_tokens_output_total
modelgate_cache_hits_total
modelgate_cache_misses_total
modelgate_fallbacks_total
modelgate_cost_usd_total
```

---

# 38. Latency Percentiles

Average latency is not enough.

Track:

```text
P50
P95
P99
```

Example:

```text
P50 = 400 ms
P95 = 1200 ms
P99 = 3100 ms
```

This shows how bad the slowest requests are.

---

# 39. Distributed Tracing

OpenTelemetry can show the full path of one request.

Example:

```text
POST /v1/chat                   900 ms
|
+-- authenticate                 2 ms
|
+-- rate_limit_check             1 ms
|
+-- semantic_cache_lookup       12 ms
|
+-- model_routing                2 ms
|
+-- provider_request           850 ms
|
+-- usage_logging               18 ms
```

This makes debugging production latency much easier.

---

# 40. Grafana

Grafana can visualize metrics.

Possible dashboards:

## Operations dashboard

```text
requests/sec
error rate
provider health
fallback rate
circuit breaker state
```

## Performance dashboard

```text
P50 latency
P95 latency
P99 latency
tokens/sec
cache hit rate
```

## Cost dashboard

```text
cost/day
cost/team
cost/model
budget utilization
estimated savings
```

---

# 41. AI Evaluation

Normal software tests are not enough for AI.

Traditional assertion:

```text
2 + 2 == 4
```

is deterministic.

LLM output can vary.

ModelGate should eventually include an evaluation suite.

Create a **golden dataset** containing test prompts and expected behavior.

Example:

```json
{
  "id": "translation_001",
  "input": "Translate hello into Spanish",
  "expected": "hola"
}
```

More complicated cases can include quality rubrics.

---

# 42. Regression Testing for AI

A future CI pipeline can compare candidate changes against a baseline.

```text
Developer changes:
model
prompt
routing policy
cache policy
provider
       |
       v
GitHub Pull Request
       |
       v
Evaluation suite
       |
       +-- baseline version
       |
       +-- candidate version
       |
       v
Compare quality
       |
       +-- regression -> fail CI
       |
       +-- acceptable -> allow merge
```

This connects software engineering with MLOps.

---

# 43. What Should Be Evaluated?

Possible dimensions:

```text
task accuracy
quality
latency
cost
failure rate
format correctness
hallucination rate
routing correctness
fallback correctness
```

Routing changes should not be evaluated only by cost.

A cheaper system that destroys output quality is not an improvement.

---

# 44. Quality/Cost Tradeoff

One important future metric is something like:

```text
quality achieved per dollar
```

or comparing:

```text
quality
cost
latency
```

across routing strategies.

Example:

| Strategy | Quality | Avg Cost | P95 Latency |
|---|---:|---:|---:|
| strong model only | high | high | medium |
| local model only | medium | low | low |
| smart router | high | medium/low | medium |

Real values must come from experiments, not assumptions.

---

# 45. CI/CD

The repository should eventually use GitHub Actions.

Possible pipeline:

```text
git push
   |
   v
GitHub Actions
   |
   +-- formatting
   |
   +-- linting
   |
   +-- unit tests
   |
   +-- integration tests
   |
   +-- AI evaluation
   |
   +-- Docker build
   |
   +-- security checks
   |
   v
artifact / deployment
```

A model or prompt change should be treated as carefully as a code change.

---

# 46. Docker

When INF345 reaches containerization, ModelGate should be packaged into a Docker image.

Concept:

```text
+-------------------------+
| Docker Container        |
|                         |
| FastAPI                 |
| ModelGate               |
| Python dependencies     |
|                         |
+-------------------------+
```

The container should receive configuration from environment variables.

Examples:

```text
PORT
LOG_LEVEL
DATABASE_URL
REDIS_URL
```

Secrets should not be baked into the image.

---

# 47. Docker Compose

When multiple services are introduced:

```text
docker-compose.yml
```

could eventually run:

```text
modelgate-api
postgres
redis
prometheus
grafana
ollama
```

Example architecture:

```text
                +----------------+
                | ModelGate API  |
                +---+--------+---+
                    |        |
             +------+        +------+
             |                    |
             v                    v
        PostgreSQL              Redis

                Monitoring
                    |
          +---------+---------+
          |                   |
          v                   v
      Prometheus            Grafana
```

---

# 48. Load Testing

Before claiming the system is scalable, test it.

Possible tools:

```text
k6
Locust
wrk
```

Measure:

```text
requests/second
P50 latency
P95 latency
P99 latency
error rate
CPU usage
memory usage
gateway overhead
```

Later simulate:

```text
100 users
500 users
1000 users
provider outage
rate-limit event
Redis failure
slow provider
```

---

# 49. Kubernetes

Kubernetes becomes meaningful once the project has multiple production concerns.

Possible architecture:

```text
                        Internet
                           |
                           v
                       Ingress
                           |
                           v
                    ModelGate Service
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
        Gateway Pod   Gateway Pod   Gateway Pod
             |             |             |
             +-------------+-------------+
                           |
              +------------+------------+
              |                         |
              v                         v
            Redis                   PostgreSQL
              |
              v
        Model Providers
```

---

# 50. Kubernetes Concepts This Project Can Teach

## Deployments

Run multiple ModelGate replicas.

## Services

Provide a stable internal network endpoint.

## Ingress

Expose the API externally.

## ConfigMaps

Store non-secret configuration.

## Secrets

Store API credentials.

## Liveness probes

Use:

```text
GET /healthz
```

## Readiness probes

Later introduce:

```text
GET /readyz
```

which can check whether the instance is ready to serve traffic.

## Resource requests and limits

Control CPU and memory.

## Horizontal Pod Autoscaler

Scale replicas based on traffic or resource usage.

## Rolling deployments

Deploy a new version without taking the entire service offline.

---

# 51. `/healthz` vs `/readyz`

Keep them conceptually separate.

## `/healthz`

Question:

> Is this process alive?

Should be extremely simple.

## `/readyz`

Question:

> Can this instance currently serve requests correctly?

Later readiness may depend on:

```text
configuration loaded
required provider registry available
Redis reachable
database reachable
```

Do not overload `/healthz`.

---

# 52. Graceful Shutdown

When Kubernetes stops a pod, the application should eventually:

1. stop accepting new requests
2. finish active requests where possible
3. close database connections
4. flush telemetry
5. exit cleanly

This is an advanced but important production skill.

---

# 53. Security Goals

The project should eventually include:

```text
authentication
authorization
input validation
secret management
rate limiting
safe logs
dependency scanning
HTTPS at deployment layer
least-privilege credentials
```

---

# 54. Secret Management

Never commit real secrets.

Bad:

```text
OPENAI_API_KEY=real-secret
```

in Git.

Use environment variables or secret-management mechanisms.

Local development may use:

```text
.env
```

but it must be ignored:

```text
.env
```

inside `.gitignore`.

Provide:

```text
.env.example
```

with placeholders only.

---

# 55. Error Handling

Responses should eventually use a consistent error structure.

Example:

```json
{
  "error": {
    "code": "MODEL_NOT_FOUND",
    "message": "Requested model does not exist.",
    "request_id": "req_123"
  }
}
```

Possible error categories:

```text
INVALID_REQUEST
MODEL_NOT_FOUND
RATE_LIMITED
AUTHENTICATION_FAILED
PROVIDER_TIMEOUT
PROVIDER_UNAVAILABLE
BUDGET_EXCEEDED
INTERNAL_ERROR
```

---

# 56. API Versioning

Use a version prefix for the main API:

```text
/v1/chat
/v1/models
```

This makes future incompatible API changes easier.

The infrastructure endpoints can remain:

```text
/
/healthz
/readyz
/metrics
```

---

# 57. Streaming

LLMs often return tokens incrementally.

Later ModelGate should support streaming.

Concept:

```text
Client
   |
   v
ModelGate
   |
   v
Provider
   |
 token 1
   |
 token 2
   |
 token 3
   |
   v
Client receives progressively
```

Important production concerns:

```text
client disconnects
provider disconnects
partial responses
timeouts
logging
cache behavior
usage accounting
```

---

# 58. Background Jobs

Some tasks should not block the response.

Examples:

```text
quality evaluation
analytics aggregation
cost reports
slow logging enrichment
cache cleanup
evaluation dataset updates
```

These can eventually use background workers.

Possible architecture:

```text
ModelGate API
    |
    v
Redis Queue
    |
    v
Worker
```

Possible tooling:

```text
Celery
RQ
Arq
```

Only add this if there is a real need.

---

# 59. Future AI Feature Flags

A later advanced feature could support gradual rollout of AI changes.

Example:

```text
Old prompt/model: 90%
New prompt/model: 10%
```

Monitor:

```text
quality
latency
error rate
cost
```

If the new variant performs badly:

```text
automatic rollback
```

This makes model and prompt releases safer.

---

# 60. Shadow Testing

Before showing a new model's response to users:

```text
real request
   |
   +-- production model -> user
   |
   +-- candidate model -> hidden evaluation only
```

This is called a shadow deployment/testing pattern.

It allows ModelGate to compare a candidate model against production traffic without affecting users.

---

# 61. Model Regression Detection

Suppose the project changes:

```text
Qwen version A
        |
        v
Qwen version B
```

Version B might be:

- cheaper
- faster
- smaller

but also worse on some tasks.

ModelGate's evaluation pipeline should detect this before rollout.

---

# 62. Eventual Architecture

A mature architecture might look like:

```text
                            Client
                              |
                              v
                    +-------------------+
                    |     ModelGate     |
                    |      FastAPI      |
                    +---------+---------+
                              |
                       Authentication
                              |
                        Rate Limiter
                           Redis
                              |
                        Request Policy
                              |
                       Semantic Cache
                              |
                         AI Router
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
     Local Models          OpenAI             Anthropic
          |                   |                   |
          +-------------------+-------------------+
                              |
                         Normalization
                              |
                       Usage / Cost Log
                              |
                         PostgreSQL
                              |
             +----------------+----------------+
             |                                 |
             v                                 v
       OpenTelemetry                       Eval Worker
             |
             v
        Prometheus
             |
             v
          Grafana
```

Deployment:

```text
GitHub
   |
   v
GitHub Actions
   |
   +-- tests
   +-- evaluations
   +-- lint
   +-- Docker build
   |
   v
Container Registry
   |
   v
Kubernetes
   |
   +-- ModelGate replicas
   +-- ConfigMaps
   +-- Secrets
   +-- Services
   +-- Ingress
   +-- health probes
   +-- autoscaling
```

---

# 63. What the Project Is NOT

ModelGate is **not** primarily:

- a chatbot UI
- a prompt collection
- a LangChain tutorial
- a wrapper around one OpenAI call
- a frontend project
- a model-training project
- a RAG-only project
- an agent-only project

Those technologies may appear later, but the central project remains:

> **production infrastructure for serving and managing AI inference traffic**

---

# 64. Non-Goals for Early Milestones

Avoid adding these too early:

```text
React frontend
microservices
Kafka
complex authentication
multiple databases
multi-agent system
vector database
Kubernetes
full observability stack
real billing
hundreds of endpoints
```

Early milestones should remain easy to understand.

Complexity should be earned by actual requirements.

---

# 65. Engineering Principles

## 65.1 Keep interfaces stable

Avoid breaking clients every time the internal implementation changes.

## 65.2 Prefer boring solutions first

Start with the simplest thing that works.

## 65.3 Test behavior, not implementation details

Tests should survive internal refactoring.

## 65.4 Configuration should not require code changes

Use environment variables and configuration files appropriately.

## 65.5 Never hide failures

Errors should be observable and diagnosable.

## 65.6 Measure before optimizing

Do not claim caching, routing, or scaling improvements without measurements.

## 65.7 AI quality is a production metric

Latency and uptime are not enough if model output quality becomes worse.

## 65.8 Build gradually

Each milestone should leave the system working.

---

# 66. Possible Development Roadmap

The exact INF345 weeks may differ, so this is a conceptual roadmap rather than a fixed course schedule.

## Milestone A — Minimal Gateway

Build:

```text
GET /
GET /healthz
GET /v1/models
POST /v1/chat
```

Use:

```text
FastAPI
Pydantic
pytest
MockProvider
```

Learn:

```text
HTTP
REST
Python project structure
testing
Git
```

---

## Milestone B — Provider Abstraction

Add:

```text
ModelProvider interface
MockProvider
provider registry
```

Learn:

```text
interfaces
dependency inversion
clean architecture basics
```

---

## Milestone C — Real Local Inference

Add:

```text
OllamaProvider
local Qwen/Llama model
```

Learn:

```text
model serving
timeouts
HTTP clients
async I/O
```

---

## Milestone D — CI/CD

Add:

```text
GitHub Actions
linting
unit tests
integration tests
```

Learn:

```text
automated quality gates
reproducible builds
```

---

## Milestone E — Docker

Add:

```text
Dockerfile
environment configuration
```

Learn:

```text
container images
ports
process management
```

---

## Milestone F — Persistence

Add:

```text
PostgreSQL
request metadata
usage history
migrations
```

Learn:

```text
database design
ORM
schema migration
```

---

## Milestone G — Redis

Add:

```text
rate limiting
basic cache
```

Learn:

```text
distributed state
TTL
atomic operations
```

---

## Milestone H — Multi-Provider Routing

Add:

```text
OpenAIProvider
AnthropicProvider
fallback policy
```

Learn:

```text
provider abstraction
failure handling
routing
```

---

## Milestone I — Intelligent Routing

Add:

```text
request complexity classifier
model selection
quality/cost measurement
```

Learn:

```text
AI systems optimization
model selection
experimentation
```

---

## Milestone J — Reliability

Add:

```text
timeouts
retry
exponential backoff
circuit breaker
provider health
```

Learn:

```text
resilience engineering
failure modes
```

---

## Milestone K — Observability

Add:

```text
structured logs
OpenTelemetry
Prometheus
Grafana
```

Learn:

```text
production debugging
metrics
tracing
monitoring
```

---

## Milestone L — AI Evaluation

Add:

```text
golden dataset
regression evaluation
quality comparison
CI integration
```

Learn:

```text
MLOps
evaluation
AI regression testing
```

---

## Milestone M — Semantic Cache

Add:

```text
embedding-based similarity cache
TTL
invalidation
```

Learn:

```text
embeddings
vector similarity
performance optimization
```

---

## Milestone N — Kubernetes

Add:

```text
Deployment
Service
Ingress
ConfigMap
Secret
liveness probe
readiness probe
autoscaling
```

Learn:

```text
orchestration
production deployment
scaling
```

---

# 67. What Success Looks Like at the End

A strong final ModelGate project should be demonstrably able to:

1. accept AI inference requests over HTTP
2. expose a stable API independent of individual providers
3. support more than one model/provider
4. validate requests and return consistent responses
5. authenticate callers
6. enforce rate limits
7. record usage
8. track cost
9. route requests based on policy
10. retry temporary failures
11. fall back to another provider
12. use circuit breakers
13. cache safe/repeated requests
14. expose metrics
15. produce traces
16. display operational dashboards
17. run automated tests
18. run AI evaluation tests
19. build reproducibly using Docker
20. deploy using Kubernetes
21. survive multiple replicas
22. expose health/readiness endpoints
23. load test the deployment
24. measure performance rather than only describing it

---

# 68. Portfolio Story

A weak description would be:

> I made an API that sends prompts to an LLM.

A much stronger final description would be:

> I built ModelGate, a production-oriented AI inference gateway providing a unified API over local and cloud language models. It supports configurable routing, distributed rate limiting, semantic caching, provider failover, usage/cost tracking, OpenTelemetry tracing, Prometheus metrics, automated model regression evaluation, containerized deployment, and Kubernetes scaling.

The second description communicates production engineering.

Any quantitative claims should come from actual experiments.

Examples of metrics to eventually report:

```text
requests/second
P50 latency
P95 latency
P99 latency
gateway overhead
cache hit rate
cost reduction
fallback recovery time
error rate
evaluation pass rate
routing accuracy
```

---

# 69. Example Final Demo

A strong demo could show:

### Step 1

Send a normal request:

```text
Client -> ModelGate -> local model
```

### Step 2

Show Grafana receiving request metrics.

### Step 3

Send repeated requests and demonstrate cache hits.

### Step 4

Exceed a team's rate limit and receive HTTP 429.

### Step 5

Simulate the primary provider failing.

Show:

```text
primary fails
-> retries
-> circuit breaker
-> fallback provider
-> successful response
```

### Step 6

Change a routing configuration.

Show simple requests moving to a cheaper model.

### Step 7

Run evaluation before deployment.

Show a deliberately bad model/prompt change failing the quality gate.

### Step 8

Show multiple ModelGate replicas running in Kubernetes.

This tells one coherent engineering story.

---

# 70. Questions the Project Should Eventually Be Able to Answer

A good production project should let you answer questions like:

### Backend

- Why FastAPI?
- Why async?
- How are requests validated?
- How are errors standardized?
- How does streaming work?

### Architecture

- Why a gateway?
- Why provider adapters?
- Why not call OpenAI directly?
- What happens when providers use different APIs?

### Reliability

- What happens when a provider times out?
- Which errors should be retried?
- When does the circuit breaker open?
- How are fallbacks selected?

### Redis

- Why is rate limiting stored in Redis?
- How do multiple replicas share rate-limit state?
- What happens if Redis fails?

### Database

- Which data belongs in PostgreSQL?
- How are schema migrations managed?
- What information should not be logged?

### AI

- How does routing decide which model to use?
- How do you measure whether routing hurts quality?
- How do you detect model regressions?
- When is semantic caching unsafe?

### Observability

- How do you debug a slow request?
- What are the main metrics?
- Why track P95/P99 instead of only averages?
- How do traces differ from logs?

### DevOps

- How is the Docker image built?
- What runs in CI?
- How are secrets injected?
- How do you reproduce the system locally?

### Kubernetes

- What is a Deployment?
- What is a Service?
- Why does `/healthz` exist?
- Why have `/readyz` separately?
- How does the system scale horizontally?

Being able to answer these from your own project is one of its main educational goals.

---

# 71. Week 3 Checklist

For the first INF345 milestone, focus only on this.

```text
[ ] Public GitHub repository
[ ] Python project
[ ] FastAPI app
[ ] GET /
[ ] GET /healthz
[ ] GET /v1/models
[ ] POST /v1/chat
[ ] mock provider
[ ] PORT environment variable
[ ] default PORT=8080
[ ] scripts/run.sh
[ ] scripts/test.sh
[ ] both scripts executable
[ ] at least 3 genuine tests
[ ] TESTS: n/n output
[ ] .gitignore
[ ] no credentials in Git history
[ ] README
[ ] at least 5 commits
[ ] at least one merged PR
[ ] run teacher's mark_m1.py
[ ] register project in INF345 repository
```

Do not let future features distract from getting this milestone completely correct.

---

# 72. Suggested Registration Description

For the INF345 registration file:

```yaml
repo: https://github.com/YOUR_USERNAME/modelgate
language: python
what: A unified AI model inference gateway that will grow into a production-oriented routing, reliability, observability, and model-serving platform
```

A shorter version:

```yaml
repo: https://github.com/YOUR_USERNAME/modelgate
language: python
what: A unified HTTP gateway for AI model inference
```

---

# 73. Suggested GitHub Repository Description

```text
Production-oriented AI inference gateway for unified model access, routing, reliability, caching, observability, evaluation, and scalable deployment.
```

---

# 74. Project Name

Recommended name:

# ModelGate

Meaning:

```text
Model
  +
Gateway
  =
ModelGate
```

It communicates the main architectural role directly.

Alternative names could be:

```text
InferGate
ModelRouter
AIGateway
InferenceHub
ModelMesh
```

But **ModelGate** is simple and memorable.

---

# 75. Short Project Definition to Remember

If you forget everything else, remember this:

> **ModelGate is the infrastructure layer between an application and AI models.**
>
> Applications send all inference requests to ModelGate instead of talking directly to OpenAI, Anthropic, Ollama, or another provider.
>
> ModelGate gradually becomes responsible for choosing models, controlling traffic, handling failures, caching responses, tracking usage and cost, monitoring performance, evaluating quality, and making AI inference reliable in production.
>
> In INF345, the project begins as a tiny FastAPI service and grows milestone by milestone into a containerized and Kubernetes-deployed production AI system.

---

# 76. The Mental Model

Think of the project like this:

```text
Week 3:

Client
  |
  v
ModelGate
  |
  v
Mock model
```

Later:

```text
Client
  |
  v
ModelGate
  |
  +-- Authentication
  +-- Rate Limiting
  +-- Caching
  +-- Routing
  +-- Reliability
  +-- Evaluation
  +-- Cost Tracking
  +-- Observability
  |
  +-- Local models
  +-- OpenAI
  +-- Anthropic
```

Finally:

```text
                     Production Traffic
                            |
                            v
                        ModelGate
                            |
          +-----------------+-----------------+
          |                 |                 |
          v                 v                 v
       Routing           Reliability      Observability
          |                 |                 |
          +-----------------+-----------------+
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
          Local LLM       Cloud A       Cloud B
                            |
                    Docker + Kubernetes
```

That is the entire project.

---

# 77. Final Guiding Principle

The objective is not to add as many technologies as possible.

The objective is to understand **why each technology becomes necessary**.

The correct sequence is:

```text
simple working system
        |
        v
identify real limitation
        |
        v
introduce one solution
        |
        v
measure whether it helped
        |
        v
test it
        |
        v
document the decision
        |
        v
continue
```

If this principle is followed, ModelGate can become both:

1. a strong INF345 semester project, and
2. a serious production AI engineering portfolio project.

