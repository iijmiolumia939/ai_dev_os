# Consumer Migration Guide

## Migration Overview

Use AI Development OS as an external runtime package. Keep consumer-specific policies, prompts, adapters, and extensions in the consumer repository, while shared governance, retrieval, telemetry, and integration contracts come from this platform.

## Prepare an Existing Repository

1. Install the package from the GitHub repository.
2. Run the bootstrap command in a temporary output directory.
3. Compare the generated `prompts/`, `governance/`, `retrieval/`, `telemetry/`, `integrations/`, and `.github/workflows/` surfaces with the existing repository.
4. Copy only the project-specific configuration needed by the consumer repository.
5. Add consumer CI checks that run formatting, linting, tests, governance gates, and bootstrap validation.

## Adapter Integration

Create a consumer adapter that declares the project name, adapter version, supported AI Development OS version, required capabilities, and enabled extensions. Adapter code should translate consumer-specific contracts into shared runtime contracts without importing private core internals.

## Retrieval Integration

Use retrieval-first context assembly for active requirements, changed files, touched interfaces, recent checkpoints, relevant contracts, and open questions. Avoid full repository context as a default operating mode.

## Governance Integration

Use runtime-enforced governance for context budgets, model tier routing, council scope limits, retry limits, review loop limits, and expensive-model restrictions. Governance should block unsafe or unbounded work before model calls are made.

## Telemetry Integration

Write project-tagged usage records and aggregate them into daily or sprint-level summaries. Do not log secrets, credentials, private prompts, raw user data, or provider tokens.

## Release Readiness Checklist

- Consumer adapter contract validates against the compatibility matrix.
- Optional dependencies are installed only for the consumer mode that needs them.
- Bootstrap output is generated in a temporary directory and is not committed accidentally.
- Generated telemetry artifacts and local caches are ignored.
- CI validates install, imports, bootstrap generation, gates, tests, build, and metadata checks.