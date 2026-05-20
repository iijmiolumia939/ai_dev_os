# Schema Evolution Runtime

対象: NFR-COST-14, NFR-ARCH-17, NFR-SEC-04, FR-RETENTION-01, FR-RETENTION-02, FR-RETENTION-03, FR-RETENTION-04, FR-RETENTION-05, TC-RETENTION-01, TC-RETENTION-02, TC-RETENTION-03, TC-RETENTION-04, TC-RETENTION-05.

Schema evolution runtime は workspace-local persistence schema version を管理します。対象は `session-boundary.json`, `rollover-state.json`, `continuity-index.json`, `prompt-mode-state.json`, checkpoint metadata です。

## Migration Boundary

Schema migration は bounded deterministic migration のみを実行します。deprecated key removal、compact migration、incompatible field detection、stale persistence quarantine を扱います。raw persistence replay は禁止です。

Migration failure 時は quarantine mode、restore fallback、compact reset recommendation を返します。cloud sync、telemetry upload、remote memory persistence は使いません。
