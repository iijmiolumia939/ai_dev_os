# Migration Checklist

Use this checklist for every consumer rollout.

- Confirm release version `0.1.0a3` and GitHub tag `0.1.0-alpha.3`.
- Run `python -m ai_dev_os.cli release-readiness --json`.
- Run `python -m ai_dev_os.runtime_audit`.
- Confirm VSCode extension setup and VSIX build verification.
- Confirm session lifecycle setup and human-confirmed rollover.
- Confirm workspace persistence setup uses local-only persistence rules.
- Confirm retrieval scaling integration is summary-only.
- Confirm governance runtime integration is local-first.
- Confirm rollback procedure is available before changing consumer repository configuration.
- Confirm migration checklist results are reviewed by a human before rollout.

Do not run hidden migration, automatic consumer mutation, or generated artifact commits.
