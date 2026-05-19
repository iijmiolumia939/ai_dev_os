# Session Boundary Enforcement

対象: NFR-COST-12, NFR-ARCH-15, FR-SESSIONBOUNDARY-01, FR-SESSIONBOUNDARY-02, FR-SESSIONBOUNDARY-03, FR-SESSIONBOUNDARY-04, FR-SESSIONBOUNDARY-05, TC-SESSIONBOUNDARY-01, TC-SESSIONBOUNDARY-02, TC-SESSIONBOUNDARY-03, TC-SESSIONBOUNDARY-04, TC-SESSIONBOUNDARY-05.

AI_DEV_OS は session boundary を governance primitive として扱います。目的は stale session continuation を防ぐことであり、AI response blocking や Chat UI 自動操作ではありません。

## Runtime

- `session_generation`: session continuity を generation metadata で表現する。full session history replay は禁止する。
- `stale_session_detection`: rollover recommendation 後の継続、stale continuity reuse、architecture topic accumulation、giant continuity accumulation、session age、generation mismatch を検出する。
- `boundary_enforcement`: `ACTIVE`, `WARNING`, `ROLLOVER_REQUIRED`, `STALE_BLOCKED` の state を返す。
- `rollover_state`: handoff/export/clipboard/confirmation/new session の lifecycle を保持する。
- `handoff_confirmation`: human-confirmed rollover の完了条件を扱う。

## Boundary

`STALE_BLOCKED` は governance state であり、AI の応答を強制遮断しません。許可される動作は compact continuity export、copy-ready prompt generation、new session seed generation、人間による確認です。
