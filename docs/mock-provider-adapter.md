# Mock Provider Adapter

The mock provider adapter validates provider routing, fallback, latency, failure, and cost behavior without calling paid provider SDKs. It is deterministic and local-only.

## Simulated Scenarios

- `success`
- `timeout`
- `rate_limit`
- `provider_error`
- `high_latency`
- `cost_spike`
- `degraded_response`

## Governance Boundary

The mock provider never owns orchestration. Budget runtime, GPT-5.5 guard, council throttling, diff-only enforcement, retrieval scaling, and runtime audit remain the controlling governance layers.

## Non-Goals

- No OpenAI, LiteLLM, Langfuse, DVC, HTTP, or network calls.
- No randomized provider behavior.
- No generated telemetry artifact committed to git.