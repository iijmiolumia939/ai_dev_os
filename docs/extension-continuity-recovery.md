# Extension Continuity Recovery

対象: NFR-COST-13, NFR-ARCH-16, NFR-SEC-03, FR-PERSISTENCE-01, FR-PERSISTENCE-02, FR-PERSISTENCE-03, FR-PERSISTENCE-04, FR-PERSISTENCE-05, TC-PERSISTENCE-01, TC-PERSISTENCE-02, TC-PERSISTENCE-03, TC-PERSISTENCE-04, TC-PERSISTENCE-05.

VSCode extension は startup 時に `.ai-dev-os/session-boundary.json`、`.ai-dev-os/rollover-state.json`、`.ai-dev-os/continuity-index.json` を読み取り、bounded state を復元します。復元対象は pending rollover、stale session warning、compact continuity availability、session generation mismatch の確認に必要な summary-only state だけです。
この persistence は workspace-local だけで動作し、cloud sync や remote memory persistence を使いません。

## Commands

- `AI_DEV_OS: Restore Session State`
- `AI_DEV_OS: Show Persistence State`
- `AI_DEV_OS: Cleanup Stale Persistence`
- `AI_DEV_OS: Export Local Continuity Index`
- `AI_DEV_OS: Reset Local Session State`

## Recovery Boundary

stale persistence は自動再適用しません。extension は警告と recommended action を示し、人間が rollover / cleanup / reset を確認します。UI automation、network dependency、telemetry collection は禁止です。
