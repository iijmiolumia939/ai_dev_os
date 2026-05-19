# Repository Intelligence

Addresses: NFR-COST-07, NFR-ARCH-10, FR-REPOINTEL-01 through FR-REPOINTEL-05, TC-REPOINTEL-01 through TC-REPOINTEL-05.

Repository Intelligence collects workspace-local metadata for sprint orchestration. It is deterministic and read-only. It does not require GitHub API access, provider SDKs, or network calls.

## Collectors

- Git collector: branch, HEAD, ahead/behind, changed runtime paths, tests, and governance paths.
- Sprint metadata: `sprint.yml` schema support for active FR/TC, affected runtimes, risks, roadmap, architecture flags, continuity state, and validation status.
- Runtime discovery: runtime packages, tests, governance, adapters, renderers, experimental, and stale runtimes.
- Validation collector: aggregates existing validation summaries without running commands.
- CI context: stores lightweight CI status and known failure context, including Unity license failure detection.

## Goal

The runtime reduces manual sprint summaries and improves continuity bundle generation, prompt packs, and rollover recommendations without mutating the repository.
