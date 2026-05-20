# Governance Observability

対象: NFR-COST-15, NFR-ARCH-18, NFR-OBS-01, FR-GOVHEALTH-01, FR-GOVHEALTH-02, FR-GOVHEALTH-03, FR-GOVHEALTH-04, FR-GOVHEALTH-05, TC-GOVHEALTH-01, TC-GOVHEALTH-02, TC-GOVHEALTH-03, TC-GOVHEALTH-04, TC-GOVHEALTH-05.

Governance dashboard は human-readable, human-confirmed, bounded observability を提供します。dashboard は summary-only で、raw runtime replay は禁止です。

## Dashboard Fields

- governance health
- pressure summary
- risk summary
- active warnings
- stale session state
- persistence budget state
- checkpoint pressure
- architecture isolation state
- workspace cleanliness
- rollout stability

VSCode extension は status bar、warning notification、dashboard tree view、pressure display を提供します。通知は rate limit され、spam を避けます。表示は観測と確認のためのものであり、hidden automation、cloud sync、telemetry collection、autonomous repo control は行いません。
