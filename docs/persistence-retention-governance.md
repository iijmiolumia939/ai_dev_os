# Persistence Retention Governance

対象: NFR-COST-14, NFR-ARCH-17, NFR-SEC-04, FR-RETENTION-01, FR-RETENTION-02, FR-RETENTION-03, FR-RETENTION-04, FR-RETENTION-05, TC-RETENTION-01, TC-RETENTION-02, TC-RETENTION-03, TC-RETENTION-04, TC-RETENTION-05.

Persistence retention governance は workspace-local continuity を bounded に保つための runtime です。目的は persistent AI memory を増やすことではなく、long-running workspace で stale accumulation、schema drift、continuity explosion を防ぐことです。

## Retention Controls

- max checkpoint generations
- max continuity lineage depth
- stale rollover expiration
- inactive sprint retention
- prompt export retention
- compact bundle retention

Retention は deterministic に retained / expired entries を分け、cleanup required、retention pressure、estimated saved storage を返します。unbounded retention は禁止です。
