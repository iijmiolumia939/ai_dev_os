# Shared Governance Primitives

Shared primitives は duplicated governance logic を compact に再利用するための小さな deterministic API です。

## Migration Targets

- `governance_health`: pressure aggregation。
- `governance_trends`: bounded trend window。
- `persistence_governance`: retention policy。
- `session_lifecycle`: stale context detection と continuity bundle。
- `session_orchestrator`: continuity export。
- `workspace_persistence`: persistence cleanup。
- `context_subset`: stale topic eviction。
- `runtime_graph`: architecture pressure。
- `runtime_simplification`: recommendation export bounds。

## Contract

移行は diff-only です。既存 frame の public fields は維持し、内部の pressure / stale / retention / continuity / export 判定だけを shared primitive に委譲します。
