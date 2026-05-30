# Validation Evidence Runtime

Refs: NFR-COST-15, NFR-ARCH-18, NFR-OBS-01, FR-GOVHEALTH-01, FR-GOVHEALTH-02, FR-GOVHEALTH-03, FR-GOVHEALTH-04, FR-GOVHEALTH-05, TC-GOVHEALTH-01, TC-GOVHEALTH-02, TC-GOVHEALTH-03, TC-GOVHEALTH-04, TC-GOVHEALTH-05.

`ValidationEvidenceRuntime` is the canonical bounded validation-evidence surface for the governance stack. It is deterministic and local-only. It does not call providers, access the filesystem, execute processes, mutate git state, or perform autonomous execution.

## Inputs

- `pytest_passed`
- `ruff_passed`
- `audit_passed`
- `diff_check_passed`
- `unresolved_validation_issues`
- `unresolved_audit_issues`

Release-check booleans may be omitted. Omitted booleans are preserved as `None` so the runtime can distinguish missing release evidence from explicit pass or fail outcomes.

## Outputs

- `validation_evidence.status`
- `validation_evidence.validation_passed`
- `validation_evidence.reasons`
- `retained_evidence_history`
- `evicted_evidence_history`

## Deterministic Mapping

`FAILED`

- any of `pytest_passed`, `ruff_passed`, `audit_passed`, or `diff_check_passed` is `False`
- `validation_passed = False`

`PASSED`

- all validation booleans are `True`
- `unresolved_validation_issues == 0`
- `unresolved_audit_issues == 0`
- `validation_passed = True`

`PASSED_WITH_WARNINGS`

- at least one release-check boolean is omitted
  or all validation booleans are `True` and at least one unresolved validation or audit issue remains
- `validation_passed = True`

Negative unresolved issue counts are rejected with `ValueError`.

## Reasons

Reasons are bounded, ordered, and deterministic. Active tokens include:

- `PYTEST_FAILED`
- `RUFF_FAILED`
- `AUDIT_FAILED`
- `DIFF_CHECK_FAILED`
- `PYTEST_NOT_PROVIDED`
- `RUFF_NOT_PROVIDED`
- `AUDIT_NOT_PROVIDED`
- `DIFF_CHECK_NOT_PROVIDED`
- `RELEASE_CHECK_INPUTS_INCOMPLETE`
- `UNRESOLVED_VALIDATION_ISSUES`
- `UNRESOLVED_AUDIT_ISSUES`
- `VALIDATION_COMPLETE`

- `MAX_VALIDATION_EVIDENCE_REASONS = 7`

## History

- `MAX_EVIDENCE_HISTORY_RETENTION = 4`
- history retention uses oldest-first deterministic eviction
- the runtime exposes `retained_evidence_history` and `evicted_evidence_history`

## Runtime Audit

`python -m ai_dev_os.runtime_audit` projects the canonical surface at:

- `report.validation_evidence.status`
- `report.validation_evidence.validation_passed`
- `report.validation_evidence.reasons`

`run_runtime_enforcement_audit(release_check_inputs=...)` is the explicit release-check input surface for projecting release results into the audit. When no release-check inputs are provided, `runtime_audit` emits `PASSED_WITH_WARNINGS` instead of a release-ready `PASSED`.

The canonical validation surface is also reused by `report.repository_readiness`, so repository-readiness evaluation preserves the same validation booleans, omitted release checks, and unresolved issue counts.
