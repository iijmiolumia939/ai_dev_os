# Release Readiness

`0.1.0-alpha.3` adds deterministic release readiness checks for pilot consumer rollout.

## Checks

- Runtime audit active.
- Canonical validation evidence projected before repository readiness.
- Governance core active.
- Bounded retention active.
- Session lifecycle active.
- VSCode extension buildable.
- Provider simulation isolated.
- No telemetry in the extension source.
- No hidden persistence beyond local bounded stores.
- No artifact leakage through tracked release files.

## Commands

```powershell
python -m ai_dev_os.cli release-readiness --json
python -m ai_dev_os.cli release-readiness --copy-ready
python -m ai_dev_os.runtime_audit
```

Rollout remains human-confirmed and rollback-safe.
