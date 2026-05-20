# Workspace Persistence

対象: NFR-COST-13, NFR-ARCH-16, NFR-SEC-03, FR-PERSISTENCE-01, FR-PERSISTENCE-02, FR-PERSISTENCE-03, FR-PERSISTENCE-04, FR-PERSISTENCE-05, TC-PERSISTENCE-01, TC-PERSISTENCE-02, TC-PERSISTENCE-03, TC-PERSISTENCE-04, TC-PERSISTENCE-05.

Workspace persistence は bounded AI engineering continuity を workspace-local に保持する runtime です。cloud sync、hidden telemetry、remote memory persistence は行いません。

## Stored State

- current session generation
- rollover state
- compact continuity bundle metadata
- current prompt mode
- session focus
- stale warning state
- repository subset summary
- compact continuity metadata

## Excluded State

- raw transcript
- full prompt history
- provider responses
- full architecture history
- telemetry uploads

`.ai-dev-os/` は `.gitignore` により commit 対象外です。runtime と extension は summary-only JSON を読み書きし、full workspace snapshot を保存しません。
