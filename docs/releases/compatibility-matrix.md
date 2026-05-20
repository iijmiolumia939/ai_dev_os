# Compatibility Matrix

Release: `0.1.0-alpha.3`  
Python package version: `0.1.0a3`  
GitHub prerelease tag: `0.1.0-alpha.3`

## Python Versions

- Supported: Python 3.11.
- Supported: Python 3.12.
- CI validation covers Windows, macOS, and Linux on both supported Python versions.
- Consumer repositories should pin AI_DEV_OS as an alpha dependency and keep their own runtime pins explicit.

## VSCode Versions

- Extension engine range: VSCode `^1.90.0`.
- Extension compatibility is validated by TypeScript compile and VSIX packaging checks.
- The extension is a local governance surface only; it does not automate chat UI or remote services.

## Platform Support

- Windows: supported and used for local rollout validation.
- macOS: supported through CI matrix.
- Linux: supported through CI matrix.

## Optional Dependency Boundaries

- Base install has no required provider SDK dependency.
- Optional extras remain isolated: `routing`, `telemetry`, `scientific`, `coding`, `full`, and `all`.
- Provider simulation must remain mock-first and must not require real provider credentials.

## Consumer Repository Expectations

- AITuber: use AI_DEV_OS for governance, session lifecycle, runtime audit, and release readiness only.
- Cat simulator: use bounded governance and retrieval scaling without automatic source mutation.
- Standalone governance repos: use release audit and compatibility docs as local release gates.
- Experimental repos: treat all APIs as alpha and keep rollout human-confirmed.

## Bounded Persistence Requirements

- Persistence must remain local-first.
- Continuity exports must be summary-only.
- Retention windows must use bounded oldest-first cleanup.
- No hidden persistence, hidden migration, generated audit leakage, or automatic consumer mutation is allowed.
