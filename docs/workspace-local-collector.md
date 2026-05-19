# Workspace Local Collector

Workspace-local collectors read repository metadata and never mutate it.

## Read-only Rules

- No commit.
- No push.
- No checkout.
- No branch creation.
- No remote API requirement.
- No provider call.

The Git collector may run read-only git commands such as `status` and `rev-parse`. Validation collector aggregates existing summaries instead of executing validation commands.

## CLI

```powershell
python -m ai_dev_os.cli repo-intel --repo-path . --json
python -m ai_dev_os.cli runtime-map --repo-path . --json
python -m ai_dev_os.cli validation-summary --repo-path . --json
python -m ai_dev_os.cli ci-context --repo-path . --json
```
