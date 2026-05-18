from __future__ import annotations

from governance import PressureLevel
from governance.budget_runtime import enforcement_for_pressure
from governance.model_tiers import ModelTier
from integrations.dvc import build_artifact_manifest
from integrations.litellm import LiteLLMBridge
from integrations.runtime import IntegrationHealth, IntegrationRuntime, IntegrationStatus


def test_litellm_budget_downgrade_and_runtime_fallback(tmp_path) -> None:
    enforcement = enforcement_for_pressure(PressureLevel.HIGH)
    route = LiteLLMBridge().route(ModelTier.TIER2, enforcement)
    runtime = IntegrationRuntime(
        {
            "litellm": IntegrationHealth(
                name="litellm",
                status=IntegrationStatus.OFFLINE,
                provider_available=False,
                offline_fallback="local_stub",
            )
        }
    )

    decision = runtime.route_with_fallback(
        provider="litellm", model=route.model, budget=enforcement
    )

    assert route.tier is ModelTier.TIER1
    assert decision.fallback_used is True
    assert build_artifact_manifest(tmp_path)["artifacts"][0]["artifact_id"] == "FORMULA-REF-001"
