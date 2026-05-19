# Context Subset Orchestration

Addresses: NFR-COST-09, NFR-ARCH-12, FR-CONTEXTSUBSET-01 through FR-CONTEXTSUBSET-05, TC-CONTEXTSUBSET-01 through TC-CONTEXTSUBSET-05.

Context Subset Orchestration refines workspace, repository, architecture, and sprint continuity into the subset needed by the current session.

## Guarantees

- Full workspace continuation is blocked.
- Repository selection is summary-only.
- Continuity scope is bounded by budget.
- Stale topics are evicted deterministically.
- Session focus prevents architecture drift from contaminating routine implementation.

## CLI

```powershell
python -m ai_dev_os.cli context-subset --workspace . --json
python -m ai_dev_os.cli continuity-scope --workspace . --copy-ready
```
