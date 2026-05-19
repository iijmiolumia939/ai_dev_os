# Retrieval Scaling Guide

Retrieval scaling keeps continuity useful while bounding token usage and model cost.

## Operating Model

1. Build a bounded memory tree from summaries only.
2. Compact large context before routing.
3. Preserve active requirements, changed files, active artifacts, relevant entries, and retrieval policy.
4. Rank continuity summaries deterministically by weight, priority, and title.
5. Apply budget pressure and token pressure together.
6. Downgrade Tier2 eligibility when pressure is high.
7. Prefer summary-only and fallback modes under critical pressure.

## Validation Metrics

The retrieval scaling tests report before and after token counts through `RetrievalScalingFrame.before_tokens` and `RetrievalScalingFrame.after_tokens`. A valid scaling result prevents token explosion, preserves continuity summaries, and keeps retrieval deterministic.

## Rollback Safety

The runtime is a pure deterministic layer. It does not ingest background memory, mutate identity, call providers, or own orchestration. If retrieval scaling produces unexpected results, consumers can roll back by disabling the package-level retrieval scaling call and falling back to existing `select_context` and `prune` behavior.