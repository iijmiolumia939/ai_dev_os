# Atomic Prompting Guide

Addresses: NFR-COST-04, FR-COPILOT-USAGE-01, TC-COPILOT-USAGE-01.

Atomic prompting means one prompt has one objective and one bounded work surface. It reduces output length, repair loops, and repeated context loading.

## Accepted Shape

A prompt is accepted when it names:

- one objective;
- one changed area or file group;
- one expected output shape;
- the relevant requirement or test ID when available.

Example shape:

```text
Implement FR-COPILOT-USAGE-01 in ai_dev_os/copilot_usage/atomic_prompting and add the matching TC-COPILOT-USAGE-01 test.
```

## Split Shape

Split the prompt when it mixes unrelated objectives, such as architecture review, implementation, documentation, and final review in one request.

Recommended sequence:

1. Decide the architecture boundary.
2. Implement the scoped patch.
3. Run focused tests.
4. Review the resulting diff.

## Blocked Shape

The runtime blocks or rejects prompts that request a full repository review, full repository rewrite, or unbounded inspection. These requests should be converted into retrieval-first bundles with active files, active requirements, and a small task objective.
