# Governance Trace Runtime

Refs: NFR-COST-15, NFR-ARCH-18, NFR-OBS-01, FR-GOVHEALTH-01, FR-GOVHEALTH-02, FR-GOVHEALTH-03, FR-GOVHEALTH-04, FR-GOVHEALTH-05, TC-GOVHEALTH-01, TC-GOVHEALTH-02, TC-GOVHEALTH-03, TC-GOVHEALTH-04, TC-GOVHEALTH-05.

`GovernanceTraceRuntime` is the canonical bounded governance-trace surface for the governance stack. It is deterministic, read-only, and local-only. It does not call providers, access the filesystem, execute processes, mutate git state, or perform autonomous execution.

## Inputs

- `observation_review.readiness_score`
- `observation_review.risk_level`
- `observation_review.continuation.continuation_stability`
- `operator_review.status`
- `operator_review.priority`
- `merge_readiness.status`
- `merge_readiness.recommendation`
- `validation_evidence.status`
- `validation_evidence.validation_passed`
- `repository_readiness.status`
- `repository_readiness.recommendation`

## Outputs

- `governance_trace.status`
- `governance_trace.root_cause`
- `governance_trace.trace_chain`
- `governance_trace.repository_status`
- `governance_trace.repository_recommendation`
- `governance_trace.merge_status`
- `governance_trace.merge_recommendation`
- `governance_trace.operator_status`
- `governance_trace.operator_priority`
- `governance_trace.validation_status`
- `governance_trace.validation_passed`
- `governance_trace.risk_level`
- `governance_trace.readiness_score`
- `governance_trace.continuation_stability`
- `retained_trace_history`
- `evicted_trace_history`

## Deterministic Mapping

`TRACE_AVAILABLE`

- all upstream statuses are supported
- `observation_review.readiness_score` is bounded in `0..100`
- `observation_review.continuation.continuation_stability` is one of `STABLE`, `GUARDED`, `UNSTABLE`
- `trace_chain` length is exactly `5`

`TRACE_INCOMPLETE`

- any upstream status falls outside the supported bounded set
- `observation_review.readiness_score` is outside `0..100`
- continuation stability is unsupported
- the bounded trace chain cannot be completed

## Root Cause Resolution

When `status == TRACE_INCOMPLETE`, the runtime returns the first active incomplete reason:

- `REPOSITORY_TRACE_INCOMPLETE`
- `MERGE_TRACE_INCOMPLETE`
- `OPERATOR_TRACE_INCOMPLETE`
- `VALIDATION_TRACE_INCOMPLETE`
- `RISK_TRACE_INCOMPLETE`
- `CONTINUATION_TRACE_INCOMPLETE`
- `READINESS_TRACE_INCOMPLETE`
- fallback: `TRACE_CHAIN_INCOMPLETE`

When `repository_readiness.status == READY`, the runtime returns:

- `GOVERNANCE_HEALTHY`

When `repository_readiness.status == READY_WITH_WARNINGS`, the runtime returns the first active warning reason:

- `VALIDATION_STATUS_PASSED_WITH_WARNINGS`
- `MERGE_READY_WITH_WARNINGS`
- `OPERATOR_STATUS_ATTENTION`
- `CONTINUATION_STABILITY_GUARDED`
- `RISK_LEVEL_MODERATE`
- `READINESS_BELOW_READY_THRESHOLD`

When `repository_readiness.status == NOT_READY`, the runtime returns the first active blocker reason:

- `VALIDATION_STATUS_FAILED`
- `OPERATOR_STATUS_CRITICAL`
- `RISK_LEVEL_CRITICAL`
- `OPERATOR_STATUS_REVIEW_REQUIRED`
- `CONTINUATION_UNSTABLE`
- `RISK_LEVEL_HIGH`
- `MERGE_NOT_READY`
- `READINESS_BELOW_READY_THRESHOLD`

## Trace Chain

The bounded `trace_chain` is always produced in this order:

- `REPOSITORY_<repository_readiness.status>`
- `MERGE_<merge_readiness.status>`
- `OPERATOR_STATUS_<operator_review.status>`
- `RISK_LEVEL_<observation_review.risk_level>`
- `READINESS_SCORE_<observation_review.readiness_score>`

- `MAX_TRACE_CHAIN_LENGTH = 5`

## History

- `MAX_TRACE_HISTORY_RETENTION = 4`
- history retention uses oldest-first deterministic eviction
- the runtime exposes `retained_trace_history` and `evicted_trace_history`

## Runtime Audit

`python -m ai_dev_os.runtime_audit` projects the canonical surface at:

- `report.governance_trace.status`
- `report.governance_trace.root_cause`
- `report.governance_trace.trace_chain`
- `report.governance_trace.repository_status`
- `report.governance_trace.merge_status`
- `report.governance_trace.validation_status`

The governance trace audit report is read-only and preserves the upstream repository, merge, operator, validation, and observation values it explains.
