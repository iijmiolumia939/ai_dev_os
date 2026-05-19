# Context Diet Policy

Addresses: NFR-COST-04, FR-COPILOT-USAGE-02, TC-COPILOT-USAGE-02.

Context Diet minimizes the material sent to Copilot Chat or Agent Mode. The goal is not to hide useful context; it is to remove context that is expensive, stale, unrelated, or generated.

## Allowed Context

- Active requirement IDs and test IDs.
- Files changed by the current task.
- Small local snippets needed to understand the patch.
- Recent summaries that directly explain the current objective.
- Contract or ADR excerpts only when the task touches that boundary.

## Removed Context

- Full repository context.
- Full file attachments above the local threshold when a smaller snippet is enough.
- Unrelated large files.
- Stale sprint history and obsolete archive notes.
- Vendor assets and generated artifacts.
- Build outputs, caches, logs, and telemetry reports.

## Runtime Output

`ContextDietPolicy` returns:

- `allowed_context`
- `removed_context`
- `token_reduction_estimate`
- `warnings`

The report is deterministic and can be used inside release gates or runtime audit output without network access.
