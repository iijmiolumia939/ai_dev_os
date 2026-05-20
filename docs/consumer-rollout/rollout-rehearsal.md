# Consumer Rollout Rehearsal

対象ID: FR-ROLLOUT-01, FR-ROLLOUT-02, FR-ROLLOUT-03, FR-ROLLOUT-04, FR-ROLLOUT-05, NFR-ROLLOUT-01, NFR-ARCH-25, NFR-COST-22, TC-ROLLOUT-01, TC-ROLLOUT-02, TC-ROLLOUT-03, TC-ROLLOUT-04, TC-ROLLOUT-05

AI_DEV_OS consumer rollout rehearsal は、実 consumer repository に対して AI_DEV_OS を自動導入する機能ではない。目的は、導入前に bounded governance platform として運用可能かを summary-only に検証すること。

## Rehearsal Scope

Dry-run audit は以下を読むだけにする。

- AI_DEV_OS install state
- VSCode extension state
- session lifecycle compatibility
- workspace persistence compatibility
- governance runtime compatibility
- runtime graph compatibility
- bounded persistence compatibility
- rollback path existence

## Human-Confirmed Boundary

Rehearsal は以下を行わない。

- automatic migration
- workspace rewrite
- hidden mutation
- auto governance enforcement
- Chat UI operation

## Rollback-Safe Output

`ConsumerRolloutAuditFrame` は `rollout_ready`、`migration_friction`、`governance_readiness`、`rollback_ready`、`bounded_rollout_confirmed` の bounded summary を返す。実 rollback は行わず、rollback path の存在と orphaned state risk だけを dry-run で示す。

## AITuber Rehearsal

ローカルで sibling `AITuber` repository が存在する場合、`python -m ai_dev_os.runtime_audit` は consumer rollout section で AITuber を read-only に観測する。CI では deterministic temp consumer tests により同じ contract を検証する。
