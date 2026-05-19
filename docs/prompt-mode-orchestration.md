# Prompt Mode Orchestration

Addresses: NFR-COST-10, NFR-ARCH-13, FR-PROMPTMODE-01 through FR-PROMPTMODE-05, TC-PROMPTMODE-01 through TC-PROMPTMODE-05.

Prompt Mode Orchestration selects the minimum sufficient reasoning mode, prompt shape, context depth, and review intensity for the current session.

## Principles

- Default mode is `bounded_implementation`.
- Architecture work uses isolated profiles only when required.
- Routine patch work does not force an architecture council.
- Full historical continuity is excluded.
- Retrieval budget is explicit and bounded.

## CLI

```powershell
python -m ai_dev_os.cli session-mode --workspace . --json
python -m ai_dev_os.cli reasoning-profile --workspace . --copy-ready
```
