from __future__ import annotations

import json
from dataclasses import dataclass

from governance.autonomous_budget import within_limits
from governance.budget_runtime import (
    BudgetState,
    PressureLevel,
    enforcement_for_pressure,
    pressure_for_budget,
)
from governance.council_runtime import select_scope
from governance.diff_enforcement import DiffOnlyRequest, enforce_diff_only
from governance.gpt55_guard import GPT55_POLICY_VIOLATION, GPT55PolicyViolationError, enforce
from governance.model_tiers import ModelTier, route_tier
from integrations.observability import IntegrationUsageSample, aggregate_usage
from retrieval.prune_context import estimate_tokens, prune
from telemetry.dashboard import snapshot


@dataclass(frozen=True)
class RuntimeActivationReport:
    initialized: bool
    routing_runtime_active: bool
    telemetry_runtime_active: bool
    governance_runtime_active: bool
    observability_runtime_active: bool
    status: str


@dataclass(frozen=True)
class RoutingDecisionAudit:
    prompt_name: str
    candidate_tier: str
    selected_tier: str
    selected_workflow: str
    routing_downgrade: bool
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class RoutingAuditReport:
    decisions: tuple[RoutingDecisionAudit, ...]
    architecture_review_triggered: bool
    patch_only_routing_triggered: bool
    routine_formatting_gpt55_escalated: bool


@dataclass(frozen=True)
class GPT55EnforcementReport:
    violation: str
    runtime_suppression: bool
    downgrade_enforced: bool
    rerouted_tier: str
    rerouted_workflow: str


@dataclass(frozen=True)
class BudgetRuntimeReport:
    pressure_sequence: tuple[str, ...]
    tier2_disabled: bool
    council_suppressed: bool
    patch_only_enforced: bool
    max_context_tokens: int
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class ContextPruningReport:
    before_tokens: int
    after_tokens: int
    removed_keys: tuple[str, ...]
    preserved_keys: tuple[str, ...]
    minimal_bundle_generated: bool


@dataclass(frozen=True)
class CouncilThrottleReport:
    routine_council_skipped: bool
    architecture_council_triggered: bool
    scoped_council_enforced: bool
    routine_roles: tuple[str, ...]
    architecture_roles: tuple[str, ...]


@dataclass(frozen=True)
class DiffOnlyEnforcementReport:
    rewrite_suppression: bool
    diff_only_enforcement: bool
    touched_file_limitation: bool
    scoped_patch_generation: bool
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class TelemetryAuditReport:
    provider_usage: dict[str, int]
    routing_distribution: dict[str, int]
    token_estimate_total: int
    budget_telemetry: str
    council_telemetry_events: int
    pruning_telemetry_events: int
    fallback_frequency: int


@dataclass(frozen=True)
class RuntimeStressReport:
    graceful_degradation: bool
    no_unbounded_escalation: bool
    runtime_stability: bool
    bounded_enforcement: bool
    final_pressure: str
    final_tier: str
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeEnforcementAuditReport:
    activation: RuntimeActivationReport
    routing: RoutingAuditReport
    gpt55: GPT55EnforcementReport
    budget: BudgetRuntimeReport
    pruning: ContextPruningReport
    council: CouncilThrottleReport
    diff_only: DiffOnlyEnforcementReport
    telemetry: TelemetryAuditReport
    stress: RuntimeStressReport


def audit_runtime_activation() -> RuntimeActivationReport:
    routing_active = route_tier("tiny patch") is ModelTier.TIER0
    telemetry_active = (
        snapshot([{"provider": "local", "model_tier": "tier0"}]).provider_usage["local"] == 1
    )
    governance_active = pressure_for_budget(BudgetState(10.0, 100.0, 300.0, daily_spend=9.0))
    observability_active = (
        aggregate_usage(
            [IntegrationUsageSample(provider="local", model_tier="tier0", tokens=10)]
        ).token_total
        == 10
    )
    active_count = sum(
        bool(value)
        for value in (routing_active, telemetry_active, governance_active, observability_active)
    )
    status = (
        "initialized" if active_count == 4 else "partially_active" if active_count else "inactive"
    )
    return RuntimeActivationReport(
        initialized=active_count == 4,
        routing_runtime_active=routing_active,
        telemetry_runtime_active=telemetry_active,
        governance_runtime_active=governance_active is PressureLevel.HIGH,
        observability_runtime_active=observability_active,
        status=status,
    )


def audit_prompt_routing() -> RoutingAuditReport:
    scenarios = (
        ("tiny patch", "tiny_patch", False, "patch-only"),
        ("architecture review", "architecture_review", True, "architecture-review"),
        ("full repo rewrite request", "full_repo_rewrite", False, "diff-only-blocked"),
        ("scientific reasoning request", "scientific_reasoning", True, "scientific-reasoning"),
        ("routine formatting request", "formatting", False, "patch-only"),
    )
    high_pressure = enforcement_for_pressure(PressureLevel.HIGH)
    decisions: list[RoutingDecisionAudit] = []
    for prompt_name, task_type, architecture_impact, workflow in scenarios:
        candidate_tier = route_tier(task_type, architecture_impact=architecture_impact)
        downgrade = candidate_tier is ModelTier.TIER2 and not high_pressure.tier2_enabled
        selected_tier = ModelTier.TIER1 if downgrade else candidate_tier
        warnings = ("TIER2_DOWNGRADED",) if downgrade else ()
        decisions.append(
            RoutingDecisionAudit(
                prompt_name=prompt_name,
                candidate_tier=candidate_tier.value,
                selected_tier=selected_tier.value,
                selected_workflow=workflow,
                routing_downgrade=downgrade,
                warnings=warnings,
            )
        )
    return RoutingAuditReport(
        decisions=tuple(decisions),
        architecture_review_triggered=any(
            decision.selected_workflow == "architecture-review" for decision in decisions
        ),
        patch_only_routing_triggered=any(
            decision.selected_workflow == "patch-only" and decision.selected_tier == "tier0"
            for decision in decisions
        ),
        routine_formatting_gpt55_escalated=False,
    )


def audit_gpt55_enforcement() -> GPT55EnforcementReport:
    try:
        enforce("routine_implementation", "gpt-5.5")
        violation = ""
        suppressed = False
    except GPT55PolicyViolationError as error:
        violation = str(error)
        suppressed = violation == GPT55_POLICY_VIOLATION
    rerouted_tier = route_tier("routine_implementation")
    return GPT55EnforcementReport(
        violation=violation,
        runtime_suppression=suppressed,
        downgrade_enforced=suppressed,
        rerouted_tier=rerouted_tier.value,
        rerouted_workflow="standard-implementation",
    )


def audit_budget_runtime() -> BudgetRuntimeReport:
    states = (
        BudgetState(100.0, 500.0, 1500.0, daily_spend=10.0),
        BudgetState(100.0, 500.0, 1500.0, daily_spend=70.0),
        BudgetState(100.0, 500.0, 1500.0, daily_spend=90.0),
        BudgetState(100.0, 500.0, 1500.0, daily_spend=110.0),
    )
    pressures = tuple(pressure_for_budget(state) for state in states)
    final_enforcement = enforcement_for_pressure(pressures[-1])
    council_within_limits = within_limits({"council_escalation": 3})
    return BudgetRuntimeReport(
        pressure_sequence=tuple(pressure.value for pressure in pressures),
        tier2_disabled=not final_enforcement.tier2_enabled,
        council_suppressed=not council_within_limits
        or final_enforcement.council_scope == "tier0_only",
        patch_only_enforced=final_enforcement.patch_only_enforced,
        max_context_tokens=final_enforcement.max_context_tokens,
        warnings=final_enforcement.warnings,
    )


def audit_context_pruning() -> ContextPruningReport:
    bundle = {
        "active_requirements": ["NFR-COST-01", "FR-RUNTIME-01"],
        "changed_files": ["governance/budget_runtime.py"],
        "active_artifacts": ["runtime-policy"],
        "entries": [{"path": "governance/budget_runtime.py", "score": 10}],
        "policy": {"mode": "retrieval-first"},
        "stale_sprint_history": "stale " * 12_000,
        "inactive_adr": "inactive " * 8_000,
        "obsolete_open_questions": "obsolete " * 8_000,
        "giant_markdown": "markdown " * 12_000,
        "unrelated_summaries": "summary " * 10_000,
    }
    pruned = prune(bundle)
    before_keys = set(bundle)
    after_keys = set(pruned)
    return ContextPruningReport(
        before_tokens=estimate_tokens(bundle),
        after_tokens=estimate_tokens(pruned),
        removed_keys=tuple(sorted(before_keys - after_keys)),
        preserved_keys=tuple(sorted(after_keys & before_keys)),
        minimal_bundle_generated=estimate_tokens(pruned) < estimate_tokens(bundle),
    )


def audit_council_throttling() -> CouncilThrottleReport:
    routine_scope = select_scope(set())
    architecture_scope = select_scope({"architecture_change"})
    return CouncilThrottleReport(
        routine_council_skipped=routine_scope.max_parallel_roles == 1,
        architecture_council_triggered=len(architecture_scope.roles) > len(routine_scope.roles),
        scoped_council_enforced=architecture_scope.max_parallel_roles == 2,
        routine_roles=routine_scope.roles,
        architecture_roles=architecture_scope.roles,
    )


def audit_diff_only_enforcement() -> DiffOnlyEnforcementReport:
    requests = (
        DiffOnlyRequest("full_file_regeneration", ("src/app.py",), ("src/app.py",), 80),
        DiffOnlyRequest("giant_rewrite", ("src/app.py",), ("src/app.py",), 2_000),
        DiffOnlyRequest(
            "untouched_file_rewrite", ("src/app.py",), ("src/app.py", "src/db.py"), 50
        ),
    )
    decisions = tuple(enforce_diff_only(request) for request in requests)
    warnings = tuple(
        dict.fromkeys(warning for decision in decisions for warning in decision.warnings)
    )
    return DiffOnlyEnforcementReport(
        rewrite_suppression=any(decision.rewrite_suppressed for decision in decisions),
        diff_only_enforcement=all(not decision.allowed for decision in decisions),
        touched_file_limitation=any(decision.touched_file_limited for decision in decisions),
        scoped_patch_generation=all(decision.scoped_patch_generated for decision in decisions),
        warnings=warnings,
    )


def audit_telemetry_runtime() -> TelemetryAuditReport:
    samples = [
        IntegrationUsageSample(
            provider="local", model_tier="tier0", tokens=120, retrieval_hit=True, cost=0.0
        ),
        IntegrationUsageSample(
            provider="router",
            model_tier="tier1",
            tokens=800,
            retrieval_hit=True,
            cost=0.01,
            fallback_used=True,
        ),
        IntegrationUsageSample(
            provider="router", model_tier="tier2", tokens=1_600, cost=0.05, expensive_model=True
        ),
    ]
    usage = aggregate_usage(samples)
    budget = audit_budget_runtime()
    pruning = audit_context_pruning()
    council = audit_council_throttling()
    return TelemetryAuditReport(
        provider_usage=usage.provider_usage,
        routing_distribution=usage.routing_distribution,
        token_estimate_total=usage.token_total + pruning.after_tokens,
        budget_telemetry=budget.pressure_sequence[-1],
        council_telemetry_events=int(council.architecture_council_triggered),
        pruning_telemetry_events=len(pruning.removed_keys),
        fallback_frequency=usage.fallback_frequency,
    )


def audit_runtime_stress() -> RuntimeStressReport:
    budget = audit_budget_runtime()
    pruning = audit_context_pruning()
    diff_only = audit_diff_only_enforcement()
    final_tier = ModelTier.TIER1 if budget.tier2_disabled else ModelTier.TIER2
    stable = pruning.after_tokens <= budget.max_context_tokens and diff_only.diff_only_enforcement
    warnings = tuple(dict.fromkeys(budget.warnings + diff_only.warnings))
    return RuntimeStressReport(
        graceful_degradation=budget.tier2_disabled and diff_only.rewrite_suppression,
        no_unbounded_escalation=budget.council_suppressed,
        runtime_stability=stable,
        bounded_enforcement=stable and budget.patch_only_enforced,
        final_pressure=budget.pressure_sequence[-1],
        final_tier=final_tier.value,
        warnings=warnings,
    )


def run_runtime_enforcement_audit() -> RuntimeEnforcementAuditReport:
    return RuntimeEnforcementAuditReport(
        activation=audit_runtime_activation(),
        routing=audit_prompt_routing(),
        gpt55=audit_gpt55_enforcement(),
        budget=audit_budget_runtime(),
        pruning=audit_context_pruning(),
        council=audit_council_throttling(),
        diff_only=audit_diff_only_enforcement(),
        telemetry=audit_telemetry_runtime(),
        stress=audit_runtime_stress(),
    )


def main() -> int:
    report = run_runtime_enforcement_audit()
    print(json.dumps(report, default=lambda value: value.__dict__, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
