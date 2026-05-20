# Governance Core

AI_DEV_OS Governance Core は、pressure、stale detection、bounded retention、continuity scope、compact export の重複実装を shared primitives に寄せるための summary-only runtime です。

対象は `TC-GOV-CORE-01` から `TC-GOV-CORE-05` 相当の振る舞いです。runtime は repository を自動変更せず、bounded な frame を返すだけです。

## Runtime

- `ai_dev_os.governance_core.pressure_primitives`: governance pressure の共通集約。
- `ai_dev_os.governance_core.stale_detection`: stale signal の共通分類。
- `ai_dev_os.governance_core.bounded_retention`: oldest-first retention window。
- `ai_dev_os.governance_core.continuity_primitives`: continuity scope と予算の共通制約。
- `ai_dev_os.governance_core.compact_export`: summary-only export 状態。

## Bounds

- network call は行わない。
- full source replay や dynamic tracing は行わない。
- automatic rewrite / merge / cleanup は行わない。
- VSCode extension は local view と command 表示のみを行う。
