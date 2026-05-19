# Session Orchestrator Guide

Addresses: NFR-COST-06, NFR-ARCH-09, FR-SESSION-CLI-01 through FR-SESSION-CLI-05, TC-SESSION-CLI-01 through TC-SESSION-CLI-05.

Session Orchestrator automates the human steps around bounded Chat sessions. It does not operate the ChatGPT or Copilot UI. It produces deterministic decisions, compact continuity bundles, and copy-ready prompts that a human can paste into a new session.

## Runtime Surfaces

- Sprint start automation generates a compact continuity bundle and sprint start prompt.
- Sprint close automation checks whether commit, push, remote verification, and next-session bundle preparation are still required.
- Prompt pack generation creates copy-ready prompts for sprint start, sprint close, architecture isolation, patch-only work, session rollover, and remote verification.
- Session decision combines rollover, stale context, cache awareness, architecture isolation, provider telemetry, and retrieval scaling signals.
- Continuity export renders compact bundles as markdown, JSON, plain text, or copy-ready prompt text.

## Non Goals

- No Copilot UI automation.
- No network dependency.
- No real provider calls.
- No full transcript replay.
- No generated telemetry artifacts.
