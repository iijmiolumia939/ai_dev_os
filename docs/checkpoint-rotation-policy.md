# Checkpoint Rotation Policy

対象: NFR-COST-14, NFR-ARCH-17, NFR-SEC-04, FR-RETENTION-01, FR-RETENTION-02, FR-RETENTION-03, FR-RETENTION-04, FR-RETENTION-05, TC-RETENTION-01, TC-RETENTION-02, TC-RETENTION-03, TC-RETENTION-04, TC-RETENTION-05.

Checkpoint rotation policy は checkpoint generations を bounded に保ち、checkpoint explosion を防ぐ runtime です。

## Rotation Output

- active checkpoints
- archived checkpoints
- expired checkpoints
- generation rotation
- checkpoint compaction

Rotation は active と archived の上限を超えた checkpoint を expired として返します。workspace-local `.ai-dev-os/checkpoints/` の summary-only metadata を対象とし、full workspace snapshot や raw transcript は保存しません。
