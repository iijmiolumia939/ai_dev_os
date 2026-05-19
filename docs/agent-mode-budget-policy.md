# Agent Mode Budget Policy

Addresses: NFR-COST-04, FR-COPILOT-USAGE-04, TC-COPILOT-USAGE-04.

Agent Mode is useful but can create repeated model calls through tool execution, repair loops, validation retries, and context refreshes. AI_DEV_OS treats those loops as a budgeted runtime surface.

## Guarded Counters

- max tool calls;
- max repair loops;
- max validation retries;
- max context refreshes;
- max architecture escalations.

## High Pressure Behavior

When pressure is high or critical, the guard switches to:

- patch-only mode;
- no Tier2;
- no council expansion;
- stop and report.

The guard does not execute tools. It produces a deterministic report that orchestration layers can enforce.
