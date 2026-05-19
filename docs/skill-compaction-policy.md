# Skill Compaction Policy

Addresses: NFR-ARCH-07, FR-COPILOT-USAGE-03, TC-COPILOT-USAGE-03.

Skill compaction prevents AGENTS.md, copilot instructions, and skill files from becoming an always-loaded context bundle.

## Required Shape

Each skill must provide a compact index entry:

```text
skill-name: when to use this skill
```

A skill without a When to Use rule is excluded from the compact index until it is scoped.

## Suppression Rules

- Do not load every skill by default.
- Do not dump full skill bodies into the prompt context.
- Suppress duplicated skill descriptions.
- Warn on long instructions that should be split or indexed.
- Exclude skills whose When to Use rule does not match the active task.
