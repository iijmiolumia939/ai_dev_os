# Bounded Governance History

対象: NFR-COST-16, NFR-ARCH-19, NFR-OBS-02, FR-GOVTREND-01, FR-GOVTREND-02, FR-GOVTREND-03, FR-GOVTREND-04, FR-GOVTREND-05, TC-GOVTREND-01, TC-GOVTREND-02, TC-GOVTREND-03, TC-GOVTREND-04, TC-GOVTREND-05.

Bounded governance history は local-only observability のための bounded compact trend summary です。AI_DEV_OS は full governance history を保存せず、dashboard delta は前回 snapshot と current snapshot の差分だけを表示します。

## Non-goals

- no hidden history growth
- no raw runtime replay
- no cloud sync
- no autonomous enforcement
- no autonomous repo control

VSCode extension の trend indicator と dashboard delta view は rate-limited notifications を使い、trend spam を避けます。表示状態は `IMPROVING`, `STABLE`, `DEGRADING`, `OSCILLATING` に限定されます。
