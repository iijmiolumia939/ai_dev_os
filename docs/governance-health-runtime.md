# Governance Health Runtime

Refs: NFR-COST-15, NFR-ARCH-18, NFR-OBS-01, FR-GOVHEALTH-01, FR-GOVHEALTH-02, FR-GOVHEALTH-03, FR-GOVHEALTH-04, FR-GOVHEALTH-05, TC-GOVHEALTH-01, TC-GOVHEALTH-02, TC-GOVHEALTH-03, TC-GOVHEALTH-04, TC-GOVHEALTH-05.

`GovernanceHealthRuntime` is the canonical top-level bounded governance-health surface for the governance stack. It is read-only and local-only. It does not call providers, access the filesystem, execute processes, mutate git state, or perform autonomous execution.

## Inputs

- `observation_review.readiness_score`
- `observation_review.risk_level`
- `operator_review.status`
- `merge_readiness.status`
- `validation_evidence.status`
- `repository_readiness.status`
- `governance_trace.status`
- `governance_trace.root_cause`

## Outputs

- `governance_health.status`
- `governance_health.summary`
- `governance_health.reasons`
- `retained_health_history`
- `evicted_health_history`

## Deterministic Mapping

`HEALTHY`

- `repository_readiness.status == READY`
- `validation_evidence.status == PASSED`
- `merge_readiness.status == READY`
- `governance_trace.status == TRACE_AVAILABLE`
- Summary: `GOVERNANCE_HEALTHY`

`DEGRADED`

- `repository_readiness.status == READY_WITH_WARNINGS`
  or `validation_evidence.status == PASSED_WITH_WARNINGS`
  or `merge_readiness.status == READY_WITH_WARNINGS`
- Summary: `GOVERNANCE_DEGRADED`

`UNHEALTHY`

- `repository_readiness.status == NOT_READY`
  or `validation_evidence.status == FAILED`
  or `merge_readiness.status == NOT_READY`
  or `governance_trace.status == TRACE_INCOMPLETE`
- Summary: `GOVERNANCE_UNHEALTHY`

Unhealthy conditions take precedence over healthy and degraded conditions. If no healthy or unhealthy rule matches, the runtime returns `DEGRADED` as the bounded fallback.

## Reasons

Reasons are bounded and deterministic. Example tokens include:

- `REPOSITORY_READY_WITH_WARNINGS`
- `MERGE_READY_WITH_WARNINGS`
- `VALIDATION_FAILED`
- `TRACE_INCOMPLETE`
- `ROOT_CAUSE_<value>`

## History

- `MAX_HEALTH_HISTORY_RETENTION = 4`
- history retention uses oldest-first deterministic eviction
- the runtime exposes `retained_health_history` and `evicted_health_history`

## Runtime Audit

`python -m ai_dev_os.runtime_audit` now projects the canonical surface at:

- `report.governance_health.governance_health.status`
- `report.governance_health.governance_health.summary`
- `report.governance_health.governance_health.reasons`

The existing `governance_health` audit report remains intact. The canonical surface is added as a nested read-only projection so existing runtime behavior stays unchanged.

When `runtime_audit` is executed without explicit release-check inputs, the projected validation evidence remains `PASSED_WITH_WARNINGS`, which keeps repository readiness and governance health in non-release-ready bounded states.
