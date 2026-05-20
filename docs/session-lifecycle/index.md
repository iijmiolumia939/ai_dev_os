# Session Lifecycle Release Guide

Release: `0.1.0-alpha.3`

## Rollover Workflow

Run `should-rollover` and `session-boundary-handoff`. Rollover is advisory until a human confirms it.

## Continuity Bundle Workflow

Use `continuity-export --copy-ready` to produce compact context. Do not replay full sprint history.

## Stale Session Workflow

Use stale session warnings to stop hidden context drift. Stale state should trigger a reviewed handoff, not automatic mutation.

## Compact Context Workflow

Keep active requirements, affected runtimes, current risks, and next prompt seed. Exclude old sprint logs, generated artifacts, and raw memory.

## Governance Incident Workflow

Treat governance incidents as alpha signals. Review them manually and connect them to release readiness only after validation.

## Bounded Persistence Workflow

Use local-only persistence, retention windows, checkpoint rotation, and persistence cleanup. Generated reports and bundles must remain ignored unless a human explicitly promotes them to docs.
