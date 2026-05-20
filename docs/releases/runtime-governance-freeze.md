# Runtime Governance Freeze

Release: `0.1.0-alpha.3`

This document defines the alpha boundary for release readiness. It is not a stable API contract. API freeze not guaranteed.

## Stabilized Contracts

- Runtime audit top-level report sections remain deterministic and JSON serializable.
- Governance core primitive frames remain summary-only and bounded.
- Session lifecycle handoff, stale session, rollover, and compact bundle frames remain human-confirmed.
- VSCode command identifiers for session, governance, runtime graph, runtime simplification, and governance core remain available for pilot consumers.

## Unstable Contracts

- Internal scoring constants for pressure, risk, stability, and rollout readiness.
- Recommendation text for runtime simplification and consumer rollout.
- Experimental governance incident phrasing and triage labels.
- CLI plain text formatting beyond `--json` and `--copy-ready` output.

## Experimental Runtimes

- Governance incidents.
- Runtime simplification recommendations.
- Consumer rollout readiness scoring.
- Provider cost simulation estimates.

## Bounded API Expectations

- Outputs are summary-only.
- Persistence is local-first.
- Rollout is human-confirmed rollout.
- Migration is rollback-safe and deterministic.
- No hidden automation, hidden migration, or automatic consumer mutation is permitted.

## Alpha Boundary

This release is safe for bounded consumer rollout pilots, not for permanent API integration. Consumers should pin the prerelease and review diffs manually before adoption.
