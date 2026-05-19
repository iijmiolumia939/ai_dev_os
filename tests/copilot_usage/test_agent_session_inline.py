from __future__ import annotations

from ai_dev_os.copilot_usage.agent_mode_budget import AgentLoopState, AgentModeBudgetGuard
from ai_dev_os.copilot_usage.inline_first import InlineFirstPolicy
from ai_dev_os.copilot_usage.session_policy import SessionCostPolicy, SessionState


def test_agent_mode_budget_stops_loop_expansion_under_pressure() -> None:
    report = AgentModeBudgetGuard().evaluate(
        AgentLoopState(
            tool_calls=24,
            repair_loops=3,
            validation_retries=2,
            context_refreshes=2,
            architecture_escalations=1,
            pressure="HIGH",
        )
    )

    assert report.stop_required is True
    assert report.patch_only_mode is True
    assert report.no_tier2 is True
    assert report.no_council_expansion is True
    assert "high_pressure_stop_and_report" in report.stop_reasons
    assert "max_tool_calls_reached" in report.stop_reasons


def test_cache_aware_session_policy_chooses_compact_and_fork() -> None:
    compact = SessionCostPolicy().evaluate(
        SessionState(
            context_tokens=18_000,
            repeated_instruction_tokens=4_000,
            task_continuity_score=0.85,
            cache_reuse_likelihood=0.8,
            completed_objectives=0,
            new_objectives=1,
        )
    )
    fork = SessionCostPolicy().evaluate(
        SessionState(
            context_tokens=18_000,
            repeated_instruction_tokens=500,
            task_continuity_score=0.2,
            cache_reuse_likelihood=0.2,
            completed_objectives=1,
            new_objectives=2,
        )
    )

    assert compact.compact_before_continue is True
    assert compact.estimated_cache_benefit_tokens == 3_200
    assert compact.estimated_avoided_tokens > 0
    assert fork.new_session_recommended is True
    assert fork.recommendation == "new_session"


def test_inline_first_policy_detects_trivial_tasks() -> None:
    inline = InlineFirstPolicy().evaluate("rename this local variable", touched_files=1)
    local_refactor = InlineFirstPolicy().evaluate(
        "small local refactor extract helper", touched_files=1, estimated_diff_lines=20
    )
    architecture = InlineFirstPolicy().evaluate(
        "architecture review for cross-module runtime boundary", touched_files=4
    )

    assert inline.use_inline_completion is True
    assert inline.classification == "rename"
    assert local_refactor.use_patch_prompt is True
    assert local_refactor.use_agent is False
    assert architecture.use_architecture_review is True
