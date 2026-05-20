from __future__ import annotations

from ai_dev_os.reasoning_scope.reasoning_compaction import ReasoningCompactionPolicy
from ai_dev_os.reasoning_scope.reasoning_depth import ReasoningDepthPolicy


def test_tc_reasoningscope_05_depth_caps_low_medium_high() -> None:
    low = ReasoningDepthPolicy().cap(complexity="LOW", affected_runtimes=("a",))
    medium = ReasoningDepthPolicy().cap(complexity="MEDIUM", affected_runtimes=("a", "b"))
    high = ReasoningDepthPolicy().cap(complexity="HIGH", affected_runtimes=("a", "b", "c"))

    assert low.reasoning_depth_cap == 1
    assert medium.reasoning_depth_cap == 2
    assert high.reasoning_depth_cap == 4
    assert low.maximum_reasoning_neighborhood == 1
    assert medium.maximum_reasoning_neighborhood == 2
    assert high.maximum_reasoning_neighborhood == 4
    assert low.compact_reasoning_recommendation is True
    assert "chain_scope:metadata_only" in high.bounded_chain_scope_metadata


def test_tc_reasoningscope_06_reasoning_compaction_deduplicates_governance() -> None:
    frame = ReasoningCompactionPolicy().compact(
        reasoning_summaries=("summary", "summary", "other"),
        escalation_explanations=("why", "why"),
        governance_reasoning=("b", "a", "a"),
        deep_details=("deep",),
        deep_details_required=False,
    )

    assert frame.compact_reasoning_summaries == ("summary", "other")
    assert frame.compact_escalation_explanations == ("why",)
    assert frame.deduplicated_governance_reasoning == ("a", "b")
    assert frame.expandable_deep_details == ()
    assert frame.summary_only is True
