# Provider Fallback Policy

Provider fallback simulation validates how AI Development OS behaves when provider health and budget pressure degrade together.

## Fallback Chain

1. Disable Tier2 when budget pressure requires it.
2. Mark Tier1 degraded for rate limits, high latency, or degraded responses.
3. Use local fallback for provider failures or critical pressure.
4. Switch to retrieval-only fallback when context pressure is high.
5. Prefer summary-only fallback when compressed retrieval is available.
6. Enforce patch-only mode under budget pressure.

## Safety Rules

- Fallback simulation must be deterministic.
- No paid provider call is allowed.
- Provider failure must not expand retrieval scope.
- Summary-only fallback must reduce token burn.