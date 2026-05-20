# Governance Trend Window

対象: NFR-COST-16, NFR-ARCH-19, NFR-OBS-02, FR-GOVTREND-01, FR-GOVTREND-02, FR-GOVTREND-03, FR-GOVTREND-04, FR-GOVTREND-05, TC-GOVTREND-01, TC-GOVTREND-02, TC-GOVTREND-03, TC-GOVTREND-04, TC-GOVTREND-05.

Governance trend window は AI_DEV_OS governance 状態を fixed-size rolling window のみで観測する runtime です。目的は bounded governance trend observability であり、long-term hidden history accumulation ではありません。

## Window Rules

- fixed max window size
- oldest-first eviction
- recent pressure history only
- recent risk history only
- recent health states only
- recent stability states only

Full historical replay は禁止です。window は compact summary のみを保持し、active window size、evicted snapshots、trend window pressure、trend window stability、bounded window maintained を返します。
