# Copilot Usage Optimization

Addresses: NFR-COST-04, NFR-ARCH-07, FR-COPILOT-USAGE-01 through FR-COPILOT-USAGE-05, TC-COPILOT-USAGE-01 through TC-COPILOT-USAGE-05.

AI_DEV_OS does not try to avoid Copilot. It makes Copilot Chat and Agent Mode cheaper to use by forcing bounded context, atomic tasks, compact instructions, and runtime-visible stop conditions.

## Runtime Policies

- Atomic prompting: one prompt carries one objective. Broad review, full repository, or mixed architecture plus implementation plus review prompts are split or blocked.
- Context diet: only active requirements, changed files, and directly related summaries should enter the prompt context.
- Skill compaction: skills and instructions are indexed by a compact When to Use entry instead of loaded as full dumps.
- Agent mode budget: tool calls, repair loops, validation retries, context refresh, and architecture escalation are capped.
- Session cost policy: one task normally maps to one session, with compaction or fork decisions when cache reuse is still useful.
- Inline first: simple completion, rename, comments, glue code, and local refactors are classified before escalating to Chat or Agent Mode.

## Usage Dashboard Review Workflow

The runtime audit exposes a Copilot usage section. Teams should review provider usage, fallback frequency, avoided tokens, and expensive-mode triggers during normal release governance.

The dashboard review is intentionally policy-level. This package does not call GitHub billing APIs, does not scrape user dashboards, and does not require network access.

## Non Goals

- No real Copilot API calls.
- No provider SDK dependency.
- No uncontrolled RAG or full repository injection.
- No always-loaded skill bundle.
- No unbounded Agent Mode loop.
