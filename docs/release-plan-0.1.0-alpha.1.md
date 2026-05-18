# Release Plan: 0.1.0-alpha.1

## Release Scope

This release establishes AI Development OS as a standalone reusable platform for retrieval-first, bounded-context, cost-aware autonomous development. It includes governance runtime primitives, retrieval runtime primitives, telemetry surfaces, optional integration boundaries, consumer contracts, bootstrap generation, compatibility checks, release governance checks, and CI validation.

## Alpha Limitations

- Public APIs are limited to import smoke compatibility and the documented bootstrap command.
- Extension interfaces are experimental and may change before `0.2.0`.
- Governance policy thresholds are experimental and may need calibration in real consumer repositories.
- Provider integrations are abstraction surfaces; optional SDK behavior is not guaranteed in every environment.
- Release automation is validated through GitHub Actions and local install checks, but package publication is still manual.

## Compatibility Guarantees

- Python `3.11` and `3.12` are supported in CI.
- Linux, macOS, and Windows are validated through GitHub Actions.
- Patch releases in the `0.1.x` line should preserve bootstrap command compatibility.
- Consumer-specific logic must remain in `adapters/`, `extensions/`, or consumer repositories.
- Optional provider dependencies must remain isolated from core runtime imports.

## Unsupported APIs

- Direct imports from private module internals are unsupported.
- Extension loader internals are not frozen.
- Provider SDK object shapes are not part of the stable contract.
- Generated scaffold contents may evolve during the alpha line.
- Runtime policy defaults are not yet a long-term compatibility promise.

## Known Risks

- Real consumer repositories may reveal missing adapter lifecycle hooks.
- Optional dependency combinations can still expose provider-specific install issues.
- Governance defaults may be too strict or too permissive for some teams.
- Remote CI validates the repository, not every downstream repository shape.
- The first alpha tag does not imply package index publication.

## Roadmap

1. Validate one production-like consumer repository with the bootstrap workflow.
2. Add adapter certification checks for migration readiness.
3. Stabilize extension interfaces for `0.2.0`.
4. Add release notes and signed artifact policy.
5. Prepare package index publication after repeated remote CI success.