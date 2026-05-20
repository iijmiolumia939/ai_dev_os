# AI Development Operating System

(AI-native Software Engineering Runtime)

AI Development Operating System is a reusable runtime for building AI-native software projects under usage-based billing constraints. It provides retrieval-first context assembly, local-first execution, runtime-enforced governance, telemetry, provider integrations, diff-only workflows, and project bootstrap templates.

This repository is not tied to AITuber, CatSimulator, Unity, MuJoCo, or any single domain. Project-specific behavior belongs in adapters or extensions.

## Release Status

`0.1.0-alpha.3` is the current prerelease line. It stabilizes release readiness, consumer rollout safety, and bounded governance checks for pilot consumer repositories such as AITuber. Python package metadata uses PEP 440 version `0.1.0a3`; the GitHub prerelease tag is `0.1.0-alpha.3`.

This is still an alpha boundary. API freeze is not guaranteed. Rollout must remain human-confirmed, rollback-safe, local-first, and summary-only; AI_DEV_OS does not perform hidden consumer repository mutation.

## Release Readiness

Run the deterministic release checks before consumer rollout:

```powershell
python -m ai_dev_os.cli release-readiness --json
python -m ai_dev_os.cli consumer-rollout-check --copy-ready
python -m ai_dev_os.cli extension-readiness --json
python -m ai_dev_os.cli governance-freeze-status --json
python -m ai_dev_os.runtime_audit
```

Consumer rollout guidance lives in `docs/consumer-rollout/`. Compatibility and alpha governance boundaries live in `docs/releases/`.

## Vision

Create a sustainable software engineering operating system for autonomous AI development that keeps quality, architecture discipline, safety review, and long-term velocity while preventing unbounded context and model-cost growth.

## Architecture

- `core/`: shared contracts and runtime decisions
- `governance/`: budgets, model tiers, GPT-5.5 policy, council scope, autonomous loop limits
- `retrieval/`: manifest generation, relevance scoring, context selection, pruning
- `checkpoints/`: compact sprint state snapshots
- `telemetry/`: project-tagged usage reports and dashboards
- `integrations/`: LiteLLM, Langfuse, aider, Continue, and DVC integration surfaces
- `prompts/`: reusable prompt templates
- `bootstrap/`: project scaffold generation
- `templates/`: reusable project templates
- `adapters/`: project bridge layer
- `extensions/`: reusable domain extension layers

## Usage-Based Billing Motivation

The runtime assumes model calls are metered. It avoids full repository context, giant sprint history, unnecessary expensive models, recursive agent loops, and full-file regeneration. Runtime governance routes routine work to low-cost tiers and reserves expensive reasoning for architecture, adversary, scientific, or governance review.

## Retrieval-First Philosophy

Select only relevant artifacts: active requirements, changed files, touched interfaces, latest checkpoint, relevant contracts, and active open questions. Full repository context is not a valid default.

## Local-First Philosophy

Formatting, linting, retrieval, summarization, bootstrap, checkpointing, and deterministic gates should run locally. Cloud models are reserved for work that needs high-quality reasoning.

## Runtime-Enforced Governance

Governance is code, not a reminder. Budget pressure can disable Tier2 routing, reduce council scope, force patch-only workflows, and block GPT-5.5 for routine tasks.

## Supported Project Types

- scientific projects
- autonomous runtimes
- embodiment runtimes
- simulation projects
- AI services

## Bootstrap Workflow

```powershell
python -m ai_dev_os.bootstrap.init_project --type scientific --name my-scientific-project
```

The scaffold includes prompts, governance, retrieval, telemetry, CI, and integrations.