# Governance Health Runtime

対象: NFR-COST-15, NFR-ARCH-18, NFR-OBS-01, FR-GOVHEALTH-01, FR-GOVHEALTH-02, FR-GOVHEALTH-03, FR-GOVHEALTH-04, FR-GOVHEALTH-05, TC-GOVHEALTH-01, TC-GOVHEALTH-02, TC-GOVHEALTH-03, TC-GOVHEALTH-04, TC-GOVHEALTH-05.

Governance health runtime は AI_DEV_OS 自体の governance 状態を bounded score と state に変換する summary-only runtime です。目的は governance observability であり、autonomous governance authority ではありません。

## Inputs

- session lifecycle
- stale context pressure
- persistence pressure
- retrieval scaling pressure
- provider simulation pressure
- architecture isolation pressure
- schema migration pressure
- checkpoint rotation pressure
- workspace contamination risk

## Outputs

- governance health score
- governance health state
- governance stability
- governance degradation detected
- governance attention required

状態は `HEALTHY`, `STABLE_WARNING`, `HIGH_PRESSURE`, `CRITICAL_GOVERNANCE` に限定されます。runtime は response blocking、forced session shutdown、autonomous repo mutation、hidden enforcement を実行しません。
