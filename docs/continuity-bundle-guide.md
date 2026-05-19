# Continuity Bundle Guide

Continuity bundles preserve bounded continuity between sessions. They are local summaries for the next session, not memory expansion or full history replay.

## Include

- active FR and TC IDs;
- current sprint summary;
- affected runtimes;
- active risks;
- current roadmap;
- current architectural constraints;
- current governance state.

## Exclude

- full sprint history;
- giant markdown;
- stale open questions;
- obsolete ADRs;
- unrelated runtimes;
- vendor assets;
- full repository tree.

## Token Budget

The bundle must expose a token estimate. If the bundle exceeds the budget, it is compacted to summary-only continuity. Under high pressure, summary-only continuity is mandatory.
