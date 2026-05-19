# Session Lifecycle Governance

Addresses: NFR-COST-05, NFR-ARCH-08, FR-SESSION-01 through FR-SESSION-05, TC-SESSION-01 through TC-SESSION-05.

Session Lifecycle Governance prevents long-lived Chat sessions from accumulating implicit stale context and hidden token burn. It is not a memory runtime. It decides when a session should roll over, what compact continuity bundle should be carried forward, and when architecture work must be isolated.

## Runtime Surfaces

- Session rollover detects sprint boundaries, context growth, stale history pressure, retrieval pressure, token accumulation, and architecture escalation.
- Continuity bundle generation carries only active FR/TC, current sprint summary, affected runtimes, active risks, current roadmap, architecture constraints, and governance state.
- Stale context detection evicts old sprint context, obsolete architecture discussion, inactive roadmap references, repeated giant summaries, stale review context, and retrieval drift.
- Cache-aware session routing balances cache reuse against fresh session boundaries.
- Architecture isolation separates redesign sessions from routine patch sessions.

## High Pressure Behavior

When runtime pressure is high or critical, AI_DEV_OS deterministically switches to:

- mandatory rollover;
- summary-only continuity;
- compact bundle required;
- architecture isolation;
- no full-session continuation.

## Non Goals

- Do not store more memory.
- Do not replay full sprint history.
- Do not include the full repository tree.
- Do not carry vendor assets, generated artifacts, obsolete ADRs, or unrelated runtimes into the next session.
