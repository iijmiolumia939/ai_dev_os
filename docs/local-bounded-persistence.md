# Local Bounded Persistence

対象: NFR-COST-13, NFR-ARCH-16, NFR-SEC-03, FR-PERSISTENCE-01, FR-PERSISTENCE-02, FR-PERSISTENCE-03, FR-PERSISTENCE-04, FR-PERSISTENCE-05, TC-PERSISTENCE-01, TC-PERSISTENCE-02, TC-PERSISTENCE-03, TC-PERSISTENCE-04, TC-PERSISTENCE-05.

Local bounded persistence は永続メモリではありません。目的は VSCode restart、workspace reopen、session interruption 後に、bounded continuity recovery を可能にすることです。

## Files

- `.ai-dev-os/session-boundary.json`
- `.ai-dev-os/rollover-state.json`
- `.ai-dev-os/continuity-index.json`
- `.ai-dev-os/prompt-mode-state.json`
- `.ai-dev-os/checkpoints/`

これらは workspace-local only であり、Git commit 対象ではありません。

## Cleanup

`PersistenceCleanupPolicy` は obsolete continuity bundle、stale session generation、expired rollover state、duplicated compact export、inactive sprint checkpoint を deterministic に cleanup します。cleanup は summary metadata に対してのみ実行され、raw export replay は行いません。
