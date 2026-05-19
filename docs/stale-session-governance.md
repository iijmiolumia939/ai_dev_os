# Stale Session Governance

対象: NFR-COST-12, NFR-ARCH-15, FR-SESSIONBOUNDARY-01, FR-SESSIONBOUNDARY-02, FR-SESSIONBOUNDARY-03, FR-SESSIONBOUNDARY-04, FR-SESSIONBOUNDARY-05, TC-SESSIONBOUNDARY-01, TC-SESSIONBOUNDARY-02, TC-SESSIONBOUNDARY-03, TC-SESSIONBOUNDARY-04, TC-SESSIONBOUNDARY-05.

Stale session governance は、rollover required の後も同じ session を続けて hidden context drift が増える問題を抑制します。AI_DEV_OS は detection と recommendation を行い、人間が rollover を確認します。UI automation は行いません。

## Detection Signals

- rollover recommended but ignored
- stale continuity reuse
- architecture topic accumulation
- giant continuity accumulation
- excessive session age
- stale generation mismatch

## Enforcement Outcome

- `ACTIVE`: session continuation allowed。
- `WARNING`: compact-only continuation を推奨。
- `ROLLOVER_REQUIRED`: new session seed と handoff export を生成。
- `STALE_BLOCKED`: stale continuation risk が高く、human-confirmed rollover が必要。

## Cost Avoidance

bounded continuity と generation metadata によって、full history replay、giant continuity prompt、stale architecture context の再利用を避けます。Runtime audit は avoided stale continuation tokens と hidden context drift estimate を出力します。
