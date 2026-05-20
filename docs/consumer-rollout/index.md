# Consumer Rollout

Release: `0.1.0-alpha.3`

Supported pilot consumers: AITuber, cat simulator, standalone governance repos, and experimental repos.

## Install Flow

```powershell
python -m pip install ai-dev-os==0.1.0a3
```

For local source rollout, install from a reviewed checkout:

```powershell
python -m pip install -e .[dev]
```

## VSCode Extension Setup

Build and package the extension from `extensions/ai-dev-os-vscode`, then install the reviewed VSIX manually. The extension stores local governance state only.

## Session Lifecycle Setup

Use `session-audit`, `should-rollover`, `continuity-export`, and `session-boundary-handoff` before long consumer tasks. Rollover must remain human-confirmed rollout.

## Workspace Persistence Setup

Use local workspace persistence and bounded retention only. Do not sync hidden state to remote services.

## Retrieval Scaling Integration

Use retrieval scaling as a summary-only budget signal. Do not pass full repository context by default.

## Governance Runtime Integration

Enable runtime audit, governance core, governance health, governance trends, runtime graph, runtime simplification, provider simulation, and release readiness as local gates.

## Local-Only Persistence Rules

- Keep continuity bundles local.
- Keep generated audit reports ignored.
- Keep consumer migration manual and reviewable.
- Never perform automatic consumer mutation.

See `migration-checklist.md` and `rollback.md` before rollout.
