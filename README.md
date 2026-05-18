# AI Development Operating System

(AI-native Software Engineering Runtime)

AI Development Operating System is a reusable runtime for building AI-native software projects under usage-based billing constraints. It provides retrieval-first context assembly, local-first execution, runtime-enforced governance, telemetry, provider integrations, diff-only workflows, and project bootstrap templates.

This repository is not tied to AITuber, CatSimulator, Unity, MuJoCo, or any single domain. Project-specific behavior belongs in adapters or extensions.

## Release Status

`0.1.0-alpha.1` is the first alpha release line. Public APIs are intentionally small, extension interfaces are still evolving, and governance runtime policies are experimental. Treat this release as suitable for pilot consumer repositories, not as a stable long-term API contract.

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