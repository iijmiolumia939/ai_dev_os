# Cache Aware Session Policy

Addresses: NFR-COST-04, FR-COPILOT-USAGE-05, TC-COPILOT-USAGE-05.

The default usage rule is one task per session. The exception is when task continuity is high and repeated instructions are likely to benefit from cache reuse.

## Recommendations

- `continue_session`: small context, high continuity, useful cache reuse.
- `compact_before_continue`: large context, high continuity, useful cache reuse.
- `fork_session`: large or stale context with partial continuity.
- `new_session`: task boundary crossed or a new objective begins.

The policy balances bounded-context discipline with cache reuse instead of always clearing or always continuing the session.
