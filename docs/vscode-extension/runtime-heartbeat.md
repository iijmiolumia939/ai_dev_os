# Runtime Heartbeat

対象ID: FR-PRESENCE-03, FR-PRESENCE-04, NFR-OBS-03, NFR-COST-17, TC-PRESENCE-03, TC-PRESENCE-04

Runtime heartbeat は、AI_DEV_OS runtime が最後に正常な bounded state を見せた時刻を compact に示す。

## Heartbeat Sources

Heartbeat は workspace-local な summary file の更新時刻から計算する。

- `.ai-dev-os/session-boundary.json`
- `.ai-dev-os/continuity-index.json`
- `.ai-dev-os/rollover-state.json`
- governance trend runtime source

## 表示

VSCode status bar は以下のような low-noise 表示を使う。

```text
AI_DEV_OS HEARTBEAT ACTIVE
```

詳細 command は `AI_DEV_OS: Show Runtime Heartbeat` で summary JSON を表示する。

## 禁止事項

Runtime heartbeat は full logs を保存しない。Chat session transcript、provider response、raw prompt history は保存しない。heartbeat が stale の場合も、自動 fork や background mutation は行わず、人間へ bounded warning を出すだけにする。
