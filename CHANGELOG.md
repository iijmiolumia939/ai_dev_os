# Changelog

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