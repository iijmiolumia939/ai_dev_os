# Workspace Snapshot Runtime

Addresses: NFR-COST-08, NFR-ARCH-11, FR-WORKSPACE-01 through FR-WORKSPACE-05, TC-WORKSPACE-01 through TC-WORKSPACE-05.

Workspace Snapshot provides bounded workspace cognition without workspace mutation. It summarizes repositories, dirty state, rollout status, known failures, and architecture hotspots for sprint rollover and continuity planning.

## Runtime Boundaries

- Read-only git metadata only.
- No full repository indexing.
- No full file tree export.
- No network or provider dependency.
- Summary-only continuity.

## CLI

```powershell
python -m ai_dev_os.cli workspace-snapshot --workspace . --json
python -m ai_dev_os.cli architecture-hotspots --workspace . --copy-ready
```
