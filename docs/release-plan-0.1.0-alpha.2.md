# Release Plan: 0.1.0-alpha.2

## Release Scope

This alpha release promotes runtime enforcement audit and observability validation to a release governance asset. The release verifies that AI Development OS does more than expose importable modules: it actively exercises routing, throttling, budgeting, pruning, diff-only enforcement, and telemetry aggregation in deterministic CI.

## Release Notes

- Runtime enforcement audit is available through `python -m ai_dev_os.runtime_audit`.
- Governance observability now reports activation, prompt routing, GPT-5.5 suppression, budget pressure, context pruning, council throttling, diff-only enforcement, telemetry aggregation, and stress behavior.
- Deterministic downgrade validation confirms Tier2 candidates are downgraded when budget pressure disables Tier2.
- Diff-only enforcement suppresses full file regeneration, giant rewrites, and untouched-file rewrites.
- Stress degradation validation confirms critical pressure leads to bounded, patch-only behavior without unbounded escalation.
- CI treats runtime audit execution as a release gate.

## Alpha Limitations

- This remains an alpha release; API freeze is not guaranteed.
- Runtime audit validates deterministic runtime primitives and provider abstraction behavior, not live paid provider API calls.
- Extension interfaces and governance thresholds may change before `0.2.0`.
- Package metadata uses PEP 440 version `0.1.0a2`; the GitHub release tag is `0.1.0-alpha.2`.

## Compatibility Guarantees

- Python `3.11` and `3.12` remain supported in CI.
- Linux, macOS, and Windows CI must pass before release.
- Runtime audit reports are stable enough for release governance checks during the `0.1.x` alpha line.
- Consumer-specific behavior remains isolated from shared runtime packages.

## Release Governance Checks

- Formatting and linting pass.
- Unit and consumer tests pass.
- Architecture, runtime isolation, consumer contamination, extension leak, and optional dependency gates pass.
- Runtime enforcement audit executes in CI.
- Build and `twine check` pass.
- No generated reports, telemetry artifacts, caches, build outputs, or provider secrets are committed.

## Remaining Risks

- Live provider enforcement still needs mock-provider and SDK-adapter smoke coverage.
- Downstream consumer repositories still need their own migration and adapter certification gates.
- Runtime policy defaults are experimental.

## Roadmap

1. Add mock provider adapter tests for routing and throttling without paid API calls.
2. Add adapter certification gates for real consumer repositories.
3. Add machine-readable runtime audit summary output when needed, while keeping generated artifacts out of git.
4. Prepare `0.2.0` interface stabilization for extension and adapter contracts.