# Shared Runtime Policy

## Stable Interfaces

- `runtime/contracts.py` defines shared request, response, and health contracts.
- `governance/` owns budget, model tier, council, and GPT-5.5 policy.
- `retrieval/` owns context bundle selection and pruning.
- `telemetry/` owns project-tagged usage reports.
- `integrations/` owns optional provider bridges.

## Dependency Isolation

Shared runtime must use the Python standard library unless a dependency is explicitly optional. Provider failures degrade to local fallback and never crash core runtime.

## Reuse Rules

- No project-specific imports in shared runtime.
- No hardcoded absolute paths.
- No cloud-only retrieval.
- No full-file regeneration workflow.
- No full repository context injection.