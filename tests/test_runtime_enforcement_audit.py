from __future__ import annotations

from ai_dev_os.runtime_audit import run_runtime_enforcement_audit


def test_runtime_activation_and_prompt_routing_are_active() -> None:
    report = run_runtime_enforcement_audit()
    decisions = {decision.prompt_name: decision for decision in report.routing.decisions}

    assert report.activation.status == "initialized"
    assert decisions["tiny patch"].selected_tier == "tier0"
    assert decisions["tiny patch"].selected_workflow == "patch-only"
    assert decisions["architecture review"].candidate_tier == "tier2"
    assert decisions["architecture review"].routing_downgrade is True
    assert decisions["architecture review"].selected_workflow == "architecture-review"
    assert report.routing.routine_formatting_gpt55_escalated is False


def test_runtime_enforces_gpt55_budget_pruning_council_and_diff_only() -> None:
    report = run_runtime_enforcement_audit()

    assert report.gpt55.violation == "GPT55_POLICY_VIOLATION"
    assert report.gpt55.runtime_suppression is True
    assert report.budget.pressure_sequence == ("INFO", "WARNING", "HIGH", "CRITICAL")
    assert report.budget.tier2_disabled is True
    assert report.budget.council_suppressed is True
    assert report.budget.patch_only_enforced is True
    assert "stale_sprint_history" in report.pruning.removed_keys
    assert "inactive_adr" in report.pruning.removed_keys
    assert "obsolete_open_questions" in report.pruning.removed_keys
    assert "active_requirements" in report.pruning.preserved_keys
    assert report.council.routine_council_skipped is True
    assert report.council.architecture_council_triggered is True
    assert report.diff_only.diff_only_enforcement is True
    assert report.diff_only.touched_file_limitation is True


def test_runtime_telemetry_and_stress_audit_are_bounded() -> None:
    report = run_runtime_enforcement_audit()

    assert report.telemetry.provider_usage["local"] == 1
    assert report.telemetry.routing_distribution["tier0"] == 1
    assert report.telemetry.token_estimate_total > 0
    assert report.telemetry.budget_telemetry == "CRITICAL"
    assert report.telemetry.council_telemetry_events == 1
    assert report.telemetry.pruning_telemetry_events >= 3
    assert report.stress.graceful_degradation is True
    assert report.stress.no_unbounded_escalation is True
    assert report.stress.runtime_stability is True
    assert report.stress.bounded_enforcement is True
    assert report.retrieval_scaling.retrieval_pressure in {"HIGH", "CRITICAL"}
    assert report.retrieval_scaling.tier_downgrade is True
    assert report.retrieval_scaling.additional_compaction is True
    assert report.retrieval_scaling.token_explosion_prevented is True
    assert report.retrieval_scaling.after_tokens < report.retrieval_scaling.before_tokens
