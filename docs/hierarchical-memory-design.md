# Hierarchical Memory Design

Hierarchical memory in AI Development OS exists to reduce context cost while preserving continuity. The runtime stores summaries, not raw replay buffers, and retrieves the smallest continuity-safe path needed for the current task.

## Runtime Layers

- `local_summarization`: deterministic Tier0/Tier1 summary compression with token budgets.
- `context_compaction`: stale sprint removal, inactive ADR pruning, obsolete OQ pruning, duplicate suppression, and active artifact preservation.
- `memory_tree`: bounded-depth summary tree for sprint, ADR, checkpoint, architecture, and stale branch summaries.
- `hierarchical_retrieval`: active context plus compressed context plus continuity summary layers.
- `retrieval_scaling`: pressure detection, memory saturation detection, retrieval decay, tier downgrade, summary-only mode, and fallback behavior.

## Safety Rules

- Full repository retrieval is forbidden.
- Raw memory replay is forbidden.
- Tree depth is bounded.
- Active artifacts must be preserved.
- Tier2 summarization is not a routine compression path.
- Outputs must be deterministic.

## Cost Behavior

When retrieval pressure rises, the runtime applies additional compaction, downgrades model tier eligibility, switches toward summary-only context, and enables retrieval fallback mode. This keeps long-term continuity available without allowing token growth to become unbounded.