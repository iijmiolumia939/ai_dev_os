# Governance Pressure Model

対象: NFR-COST-15, NFR-ARCH-18, NFR-OBS-01, FR-GOVHEALTH-01, FR-GOVHEALTH-02, FR-GOVHEALTH-03, FR-GOVHEALTH-04, FR-GOVHEALTH-05, TC-GOVHEALTH-01, TC-GOVHEALTH-02, TC-GOVHEALTH-03, TC-GOVHEALTH-04, TC-GOVHEALTH-05.

Governance pressure model は retrieval, persistence, session, architecture, provider, continuity, checkpoint, stale context pressure を deterministic に集約します。

## Bounded Output

- aggregate pressure
- dominant pressure
- pressure direction
- pressure trend
- bounded operation recommendation

Recommendation は人間に見せる signal です。AI_DEV_OS は hidden action を実行せず、repository mutation や session shutdown を自律実行しません。
