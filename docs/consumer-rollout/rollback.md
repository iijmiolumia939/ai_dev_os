# Rollback Procedure

Rollback procedure for `0.1.0-alpha.3` consumer pilots:

1. Stop using new AI_DEV_OS commands in the consumer repository.
2. Uninstall or disable the prerelease VSCode extension.
3. Restore the previous dependency pin or editable checkout.
4. Remove only local generated continuity bundles, VSIX files, audit JSON, and temporary build output.
5. Keep source changes staged separately for manual review.
6. Re-run the consumer repository's own validation suite.
7. Document the rollback reason in the consumer issue or release notes.

Rollback is manual and human-confirmed. AI_DEV_OS does not perform automatic rollback mutation.
