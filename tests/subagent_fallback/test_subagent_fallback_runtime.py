from __future__ import annotations

from ai_dev_os.subagent_execution import SubagentExecutionRuntime


def test_tc_subagentexec_11_fallback_handles_vram_cuda_context_and_timeout() -> None:
    frame = SubagentExecutionRuntime().evaluate()

    assert frame.subagent_fallback_active is True
    assert frame.fallback.vram_instability_handled is True
    assert frame.fallback.cuda_failure_handled is True
    assert frame.fallback.context_instability_handled is True
    assert frame.fallback.provider_timeout_handled is True
    assert frame.fallback.delegated_execution_failure_handled is True
    assert frame.fallback.active_fallback_provider == "ollama:qwen2.5-coder:7b"


def test_tc_subagentexec_12_fallback_is_downgrade_safe_and_non_recursive() -> None:
    frame = SubagentExecutionRuntime().evaluate()

    assert frame.fallback.downgrade_safe_fallback is True
    assert frame.fallback.no_recursive_retry_loop is True
    assert "14b_gpu_degraded_to_7b_local" in frame.fallback.compact_provider_switch_summaries
    assert "checkpoint_before_retry" in frame.fallback.rollback_safe_continuation_hints


def test_tc_subagentexec_13_checkpoint_and_rollback_are_safe() -> None:
    frame = SubagentExecutionRuntime().evaluate()

    assert "before_delegation" in frame.checkpoint.validation_checkpoints
    assert frame.rollback.rollback_state == "ROLLBACK_SAFE"
    assert frame.rollback.autonomous_merge_prevented is True
    assert frame.rollback.autonomous_repository_rewrite_prevented is True
    assert frame.rollback.hidden_rollback_automation_prevented is True
    assert frame.health.rollback_safe is True


def test_tc_subagentexec_14_capability_metadata_preserves_model_boundaries() -> None:
    frame = SubagentExecutionRuntime().evaluate()

    assert frame.capability.qwen_coding is True
    assert frame.capability.qwen_governance is False
    assert frame.capability.qwen_architecture is False
    assert frame.capability.gemma_summaries is True
    assert frame.capability.gemma_governance_summaries is True
    assert frame.capability.gemma_coding == "limited"
    assert frame.capability.fallback_available is True
