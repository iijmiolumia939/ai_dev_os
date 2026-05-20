# Governance Drift Detection

対象: NFR-COST-16, NFR-ARCH-19, NFR-OBS-02, FR-GOVTREND-01, FR-GOVTREND-02, FR-GOVTREND-03, FR-GOVTREND-04, FR-GOVTREND-05, TC-GOVTREND-01, TC-GOVTREND-02, TC-GOVTREND-03, TC-GOVTREND-04, TC-GOVTREND-05.

Governance drift detection は bounded rolling window の先頭と末尾の summary signals を比較し、governance pressure drift、persistence accumulation drift、stale continuity drift、architecture contamination drift、checkpoint debt drift、prompt mode drift を deterministic に検出します。

## Output

- drift detected
- dominant drift
- drift direction
- drift velocity
- stabilization recommendation

Recommendation は観測 signal であり、自律的な response blocking、forced session shutdown、repo mutation は実行しません。
