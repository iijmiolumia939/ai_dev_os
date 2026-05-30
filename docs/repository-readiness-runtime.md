# Repository Readiness Runtime

Refs: NFR-COST-15, NFR-ARCH-18, NFR-OBS-01, FR-GOVHEALTH-01, FR-GOVHEALTH-02, FR-GOVHEALTH-03, FR-GOVHEALTH-04, FR-GOVHEALTH-05, TC-GOVHEALTH-01, TC-GOVHEALTH-02, TC-GOVHEALTH-03, TC-GOVHEALTH-04, TC-GOVHEALTH-05.

`RepositoryReadinessRuntime` is the canonical bounded repository-readiness surface for the governance stack. It is deterministic and local-only. It does not call providers, mutate the filesystem, mutate git state, or perform autonomous execution.

## Inputs

- `merge_readiness.status`
- `merge_readiness.recommendation`
- `validation_evidence`

The runtime also accepts explicit validation inputs instead of a `validation_evidence` frame:

- `pytest_passed`
- `ruff_passed`
- `diff_check_passed`
- `audit_passed`
- `unresolved_validation_issues`
- `unresolved_audit_issues`

## Outputs

- `repository_readiness.status`
- `repository_readiness.recommendation`
- `repository_readiness.reasons`
- `repository_readiness.merge_status`
- `repository_readiness.merge_recommendation`
- `repository_readiness.pytest_passed`
- `repository_readiness.ruff_passed`
- `repository_readiness.diff_check_passed`
- `repository_readiness.audit_passed`
- `repository_readiness.unresolved_validation_issues`
- `repository_readiness.unresolved_audit_issues`
- `retained_repository_history`
- `evicted_repository_history`

Validation booleans may be `None` when upstream validation evidence records omitted release-check inputs.

## Deterministic Mapping

`READY`

- `merge_readiness.status == READY`
- `validation_evidence.status == PASSED`
- recommendation: `MERGE_CANDIDATE`

`READY_WITH_WARNINGS`

- merge readiness is not `NOT_READY`
- validation evidence is not `FAILED`
- at least one warning-level condition remains, including incomplete validation evidence
- recommendation: `REVIEW_BEFORE_MERGE`

`NOT_READY`

- `merge_readiness.status == NOT_READY`
  or `validation_evidence.status == FAILED`
- recommendation: `DO_NOT_MERGE`

If no explicit `validation_evidence` frame is provided, the runtime synthesizes one from the explicit validation inputs. If both are provided, inconsistent values are rejected with `ValueError`.

## Reasons

For `READY`, active tokens include:

- `MERGE_READY_CONFIRMED`
- `PYTEST_PASSED`
- `RUFF_PASSED`
- `DIFF_CHECK_PASSED`
- `AUDIT_PASSED`
- `NO_UNRESOLVED_VALIDATION_ISSUES`
- `NO_UNRESOLVED_AUDIT_ISSUES`

For `READY_WITH_WARNINGS`, active tokens include:

- `MERGE_READY_WITH_WARNINGS`
- `VALIDATION_EVIDENCE_INCOMPLETE`
- `UNRESOLVED_VALIDATION_ISSUES`
- `UNRESOLVED_AUDIT_ISSUES`

For `NOT_READY`, active tokens include:

- `MERGE_NOT_READY`
- `PYTEST_FAILED`
- `RUFF_FAILED`
- `DIFF_CHECK_FAILED`
- `AUDIT_FAILED`

Fallback token:

- `REPOSITORY_REVIEW_REQUIRED`

- `MAX_REPOSITORY_REASONS = 8`

## History

- `MAX_REPOSITORY_HISTORY_RETENTION = 4`
- history retention uses oldest-first deterministic eviction
- the runtime exposes `retained_repository_history` and `evicted_repository_history`

## Runtime Audit

`python -m ai_dev_os.runtime_audit` projects the canonical surface at:

- `report.repository_readiness.status`
- `report.repository_readiness.recommendation`
- `report.repository_readiness.reasons`
- `report.repository_readiness.merge_status`
- `report.repository_readiness.merge_recommendation`

The repository-readiness audit report preserves the merge-readiness status and recommendation while reusing the canonical validation-evidence surface for validation fields.

If `runtime_audit` is executed without explicit release-check inputs, repository readiness remains bounded at `READY_WITH_WARNINGS` or below; it does not infer a release-ready `READY` state from synthetic validation passes.
