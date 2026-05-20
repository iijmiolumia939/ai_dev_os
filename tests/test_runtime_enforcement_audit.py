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


def test_runtime_audit_reports_vscode_presence_visibility() -> None:
    report = run_runtime_enforcement_audit()

    assert report.vscode_presence.governance_presence_active is True
    assert report.vscode_presence.version_detection_active is True
    assert report.vscode_presence.runtime_heartbeat_active is True
    assert report.vscode_presence.status_projection_active is True
    assert report.vscode_presence.stale_extension_detection_active is True
    assert report.vscode_presence.bounded_visibility is True
    assert report.vscode_presence.estimated_avoided_invisible_governance_drift > 0
    assert report.vscode_presence.estimated_avoided_stale_extension_confusion > 0
    assert report.vscode_presence.compact_status.startswith("AI_DEV_OS")


def test_runtime_audit_reports_reasoning_routing_cost_controls() -> None:
    report = run_runtime_enforcement_audit()

    assert report.reasoning_routing.reasoning_routing_active is True
    assert report.reasoning_routing.task_complexity_active is True
    assert report.reasoning_routing.escalation_policy_active is True
    assert report.reasoning_routing.cost_budget_policy_active is True
    assert report.reasoning_routing.quality_floor_active is True
    assert report.reasoning_routing.sprint_reasoning_map_active is True
    assert report.reasoning_routing.tier_distribution == {"HIGH": 1, "MEDIUM": 1, "LOW": 2}
    assert report.reasoning_routing.estimated_avoided_premium_burn > 0
    assert report.reasoning_routing.estimated_avoided_unnecessary_escalation > 0
    assert report.reasoning_routing.human_visible_routing is True
    assert report.reasoning_routing.deterministic_reasoning_policy is True
    assert report.reasoning_routing.rollback_safe_routing is True
    assert report.reasoning_routing.provider_neutral_contracts is True
    assert report.reasoning_routing.hidden_escalation_used is False


def test_runtime_audit_reports_output_compression_controls() -> None:
    report = run_runtime_enforcement_audit()

    assert report.output_compression.output_compression_active is True
    assert report.output_compression.summary_deduplication_active is True
    assert report.output_compression.validation_compaction_active is True
    assert report.output_compression.report_density_active is True
    assert report.output_compression.compact_completion_active is True
    assert report.output_compression.expandable_reporting is True
    assert report.output_compression.human_readable is True
    assert report.output_compression.rollback_safe is True
    assert report.output_compression.deterministic_compact_mode is True
    assert report.output_compression.estimated_avoided_completion_tokens > 0
    assert report.output_compression.estimated_avoided_repeated_summaries > 0
    assert report.output_compression.hidden_reporting_used is False
    assert report.output_compression.validation_skipped is False


def test_runtime_audit_reports_retrieval_budget_controls() -> None:
    report = run_runtime_enforcement_audit()

    assert report.retrieval_budget.retrieval_budget_active is True
    assert report.retrieval_budget.retrieval_scope_active is True
    assert report.retrieval_budget.retrieval_radius_active is True
    assert report.retrieval_budget.retrieval_pressure_active is True
    assert report.retrieval_budget.retrieval_compaction_active is True
    assert report.retrieval_budget.repo_wide_retrieval_forbidden is True
    assert report.retrieval_budget.estimated_avoided_hidden_input_tokens > 0
    assert report.retrieval_budget.estimated_avoided_repo_wide_reasoning > 0
    assert report.retrieval_budget.local_only is True
    assert report.retrieval_budget.deterministic is True
    assert report.retrieval_budget.summary_only is True
    assert report.retrieval_budget.no_ast_replay is True
    assert report.retrieval_budget.no_dynamic_tracing is True
    assert report.retrieval_budget.no_hidden_provider_routing is True
    assert report.retrieval_budget.no_automatic_retrieval_escalation is True


def test_runtime_audit_reports_incremental_context_controls() -> None:
    report = run_runtime_enforcement_audit()

    assert report.incremental_context.incremental_context_active is True
    assert report.incremental_context.context_delta_active is True
    assert report.incremental_context.delta_retrieval_active is True
    assert report.incremental_context.continuity_delta_active is True
    assert report.incremental_context.audit_delta_active is True
    assert report.incremental_context.cognition_cache_active is True
    assert report.incremental_context.incremental_pressure_active is True
    assert report.incremental_context.incremental_recommendation_active is True
    assert report.incremental_context.estimated_avoided_repeated_input_tokens > 0
    assert report.incremental_context.estimated_avoided_duplicate_runtime_cognition > 0
    assert report.incremental_context.local_only is True
    assert report.incremental_context.deterministic is True
    assert report.incremental_context.summary_only is True
    assert report.incremental_context.bounded_retention is True
    assert report.incremental_context.no_raw_transcript_persistence is True
    assert report.incremental_context.no_hidden_provider_memory is True
    assert report.incremental_context.no_ast_replay is True
    assert report.incremental_context.no_repo_wide_replay is True
    assert report.incremental_context.no_dynamic_tracing is True
    assert report.incremental_context.no_automatic_context_expansion is True
    assert report.runtime_graph.incremental_context_active is True
    assert report.runtime_simplification.incremental_context_active is True
    assert report.workspace_persistence.incremental_context_active is True
    assert report.governance_health.incremental_context_active is True
    assert report.governance_trends.incremental_context_active is True
