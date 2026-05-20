# VSCode Extension Version Mismatch

対象ID: FR-PRESENCE-02, FR-PRESENCE-05, NFR-OBS-03, NFR-COST-17, TC-PRESENCE-02, TC-PRESENCE-05

AI_DEV_OS extension visibility は repo version と installed VSIX version の差分を deterministic に検出する。

## 検出対象

- repo package version
- installed extension version
- stale install
- missing reinstall
- duplicate install
- missing commands
- missing tree views
- stale activation events
- stale manifest

## 実例

今回の visibility 問題は次の状態で検出できる。

```text
repo      = 0.1.0-alpha.3
installed = 0.1.0
```

この場合、`ExtensionVersionFrame` は `version_match=false`、`stale_extension_detected=true`、`reinstall_recommended=true` を返す。

## Human-Confirmed Boundary

Version mismatch detection は reinstall を推奨するだけで、自動インストールや自動 UI 操作はしない。人間が VSIX を確認して再インストールする。

## Bounded Visibility

`StaleExtensionFrame` は missing capability の summary だけを返す。manifest 全体の replay や extension host log の永続保存は行わない。
