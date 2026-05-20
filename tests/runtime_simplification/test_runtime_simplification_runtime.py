from __future__ import annotations

import inspect

from ai_dev_os.runtime_graph import RuntimeGraphPolicy
from ai_dev_os.runtime_simplification import RuntimeSimplificationPolicy
from ai_dev_os.runtime_simplification.governance_duplication import GovernanceDuplicationPolicy
from ai_dev_os.runtime_simplification.overlap_detection import RuntimeOverlapPolicy


def test_overlap_detection_validation() -> None:
    graph = RuntimeGraphPolicy().evaluate(".")
    frame = RuntimeOverlapPolicy().detect(graph.discovery)

    assert frame.overlap_detected is True
    assert frame.overlap_categories
    assert 0 < frame.overlap_density <= 1
    assert frame.bounded_merge_possible is True
    assert frame.simplification_pressure in {"low", "medium", "high"}
    assert frame.summary_only is True


def test_merge_candidate_validation_is_recommendation_only() -> None:
    simplification = RuntimeSimplificationPolicy().evaluate(".")
    frame = simplification.merge_candidates

    assert frame.merge_candidates
    assert frame.merge_risk in {"low", "medium", "high"}
    assert frame.human_review_required is True
    assert frame.recommendation_only is True
    assert frame.automatic_merge_used is False
    assert simplification.autonomous_mutation_used is False


def test_governance_duplication_validation() -> None:
    graph = RuntimeGraphPolicy().evaluate(".")
    overlap = RuntimeOverlapPolicy().detect(graph.discovery)
    frame = GovernanceDuplicationPolicy().detect(overlap)

    assert frame.governance_duplication_detected is True
    assert frame.duplicated_governance_groups
    assert frame.simplification_priority in {"low", "medium", "high"}
    assert frame.bounded_consolidation_possible is True
    assert frame.summary_only is True


def test_summary_only_recommendation_validation() -> None:
    frame = RuntimeSimplificationPolicy().evaluate(".")

    assert frame.runtime_simplification_active is True
    assert frame.bounded_simplification_analysis is True
    assert frame.local_only_architecture_cognition is True
    assert frame.hidden_contract_injection_used is False
    assert frame.recommendations.summary_only is True
    assert frame.recommendations.human_confirmed_only is True
    assert frame.recommendations.automatic_rewrite_used is False


def test_no_ast_replay_hidden_telemetry_or_autonomous_mutation() -> None:
    import ai_dev_os.runtime_simplification as root
    import ai_dev_os.runtime_simplification.overlap_detection as overlap
    import ai_dev_os.runtime_simplification.runtime_merge_candidates as merge
    import ai_dev_os.runtime_simplification.simplification_recommendations as recommendations

    source = "\n".join(
        inspect.getsource(module).lower() for module in (root, overlap, merge, recommendations)
    )
    forbidden = (
        "requests",
        "http",
        "subprocess",
        "ast.",
        "trace",
        "write_text",
        "unlink(",
        "rename(",
        "git commit",
        "git push",
    )

    assert all(item not in source for item in forbidden)


def test_runtime_audit_reports_runtime_simplification_section() -> None:
    from ai_dev_os.runtime_audit import run_runtime_enforcement_audit

    report = run_runtime_enforcement_audit()

    assert report.runtime_simplification.runtime_overlap_active is True
    assert report.runtime_simplification.contract_overlap_active is True
    assert report.runtime_simplification.runtime_merge_candidates_active is True
    assert report.runtime_simplification.governance_duplication_active is True
    assert report.runtime_simplification.simplification_recommendations_active is True
    assert report.runtime_simplification.estimated_avoided_runtime_fragmentation > 0
    assert report.runtime_simplification.estimated_avoided_governance_duplication > 0
    assert report.runtime_simplification.estimated_avoided_contract_explosion > 0
    assert report.runtime_simplification.autonomous_mutation_used is False
