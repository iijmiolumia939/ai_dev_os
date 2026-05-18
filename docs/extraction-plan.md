# AI Development OS Extraction Plan

対象ID: NFR-COST-01, FR-ARCH-04, TC-OS-01, TC-OS-02, TC-OS-03

`ai-dev-os/` は、project 固有 runtime から分離された reusable AI-native software engineering operating system である。

## Shared Runtime Boundaries

COMMON:
- retrieval-first context assembly
- checkpoint compression and loading
- model tier routing
- budget governance
- telemetry and usage reports
- council throttling
- diff-only workflow
- provider integrations
- governance gates

PROJECT-SPECIFIC:
- embodiment runtime
- avatar and renderer protocol
- social presence and narrative runtime
- simulation physics
- biological locomotion
- domain scientific models

## Migration Sequencing

1. Extract shared runtime scaffold into `ai-dev-os/`.
2. Add adapter layer for existing projects.
3. Keep existing project runtime untouched while validating shared gates.
4. Bootstrap new projects from templates.
5. Move CI/governance to shared policy once adapters are stable.

## Compatibility Guarantees

- Additive migration only.
- Existing project paths remain valid.
- Shared runtime does not import project runtime.
- Project adapters may import shared runtime, but shared runtime may not import adapters.
- Provider SDKs remain optional and isolated.