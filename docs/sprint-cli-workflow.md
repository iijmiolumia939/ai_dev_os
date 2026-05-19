# Sprint CLI Workflow

The CLI reduces sprint lifecycle work to deterministic local commands and copy-ready output.

## Start A Sprint

```powershell
python -m ai_dev_os.cli sprint-start --sprint 42 --project aituber --copy-ready
```

Paste the generated prompt into a fresh Chat or Agent session when rollover is recommended.

## Close A Sprint

```powershell
python -m ai_dev_os.cli sprint-close --sprint 41 --project aituber --json
```

Use the output to verify whether commit, push, remote CI, and next-session bundle preparation remain open.

## Export Continuity

```powershell
python -m ai_dev_os.cli continuity-export --project aituber --copy-ready
```

The export excludes full history, old sprint logs, stale roadmap entries, vendor assets, raw memory, and generated artifacts.

## Decide Rollover

```powershell
python -m ai_dev_os.cli should-rollover --project aituber --json
python -m ai_dev_os.cli session-audit --project aituber --json
```

Use the decision to choose between continuing, compacting, forking, or opening an architecture session.
