# Copilot Session Rollover Workflow

Session rollover is a human-in-the-loop workflow. AI_DEV_OS prepares the bounded continuity material; the user pastes it into Copilot Chat or Agent Mode.

## Recommended Flow

1. Run `python -m ai_dev_os.cli should-rollover --project aituber --json`.
2. If rollover is recommended, run `python -m ai_dev_os.cli continuity-export --project aituber --copy-ready`.
3. Start a fresh Copilot session.
4. Paste the copy-ready bundle or sprint start prompt.
5. Keep the session scoped to one sprint objective.
6. Close the sprint with `python -m ai_dev_os.cli sprint-close --sprint 42 --project aituber --json`.

## Architecture Work

If the output recommends an architecture session, start a separate architecture-only session. Do not mix redesign context with routine patch work.

## Cost Control

This workflow prevents hidden token burn by avoiding full sprint history, raw memory, generated artifacts, and old review context in the next session.
