# Changelog

## 0.1.0-alpha.3

- Added deterministic release readiness audit for 0.1.0-alpha.3 prerelease rollout.
- Added consumer rollout docs for AITuber, cat simulator, standalone governance repos, and experimental repos.
- Added compatibility matrix and runtime governance freeze docs with explicit alpha boundary language.
- Added CLI commands for `release-readiness`, `consumer-rollout-check`, `extension-readiness`, and `governance-freeze-status` with `--json` and `--copy-ready` support.
- Added runtime audit `release_readiness` section for bounded release confirmation and rollout confusion reduction estimates.
- Prepared VSCode extension release docs and package metadata for prerelease VSIX verification.
- Maintained human-confirmed rollout, local-only persistence, no hidden automation, and rollback-safe migration boundaries.

## 0.1.0-alpha.2

- Added runtime enforcement audit as a release governance asset.
- Added governance observability reports for activation, routing, GPT-5.5 suppression, budget pressure, pruning, council throttling, diff-only enforcement, telemetry, and stress degradation.
- Added deterministic downgrade validation for Tier2 candidate routing under budget pressure.
- Added diff-only enforcement for full rewrite, giant rewrite, and untouched-file rewrite suppression.
- Added runtime stress validation for graceful degradation and bounded enforcement.
- Promoted `python -m ai_dev_os.runtime_audit` to a CI release gate.

## 0.1.0

- Initial standalone extraction of AI Development Operating System.
- Added reusable governance, retrieval, telemetry, integrations, prompts, bootstrap, templates, adapters, extensions, and gates.