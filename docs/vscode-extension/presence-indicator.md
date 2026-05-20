# AI_DEV_OS Presence Indicator

対象ID: FR-PRESENCE-01, FR-PRESENCE-04, NFR-OBS-03, NFR-ARCH-20, TC-PRESENCE-01, TC-PRESENCE-04

AI_DEV_OS presence indicator は、VSCode extension と local runtime が動いているかを常時・低ノイズ・bounded に示すための表示である。

## 表示内容

Status bar は compact summary のみを表示する。

```text
AI_DEV_OS ACTIVE GEN:42 LOW_PRESSURE ROLLOVER_OK
```

含める状態は以下に限定する。

- extension active
- runtime audit active
- governance core active
- session boundary active
- workspace persistence active
- runtime graph active
- current session generation
- rollover pending
- stale session detected

## 境界

この表示は governance presence visibility のためのもの。以下は行わない。

- Chat の自動 fork
- prompt の自動送信
- VSCode UI 自動操作
- background mutation
- raw transcript 保存

## Runtime Contract

Python runtime の `GovernancePresenceFrame` は summary-only frame として生成される。raw transcript は含めず、`.ai-dev-os/` の bounded state と extension manifest の存在だけを見る。

VSCode extension 側は `GovernancePresenceStatusBar` と `RuntimeHeartbeatStatusBar` を activation 時に初期化する。通知は stale extension や stale heartbeat の場合だけ rate-limited に出す。
