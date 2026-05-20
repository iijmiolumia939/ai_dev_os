from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderCapability:
    provider_class: str
    architecture_safe: bool
    implementation_safe: bool
    compact_summary_safe: bool
    deterministic_metadata_only: bool
    recommended_for: tuple[str, ...]


@dataclass(frozen=True)
class ProviderCapabilityMatrixFrame:
    recommended_provider_class: str
    capabilities: tuple[ProviderCapability, ...]
    architecture_safe_provider_classification: bool
    implementation_safe_provider_classification: bool
    compact_summary_safe_provider_classification: bool
    deterministic_provider_metadata_only: bool
    provider_neutral: bool
    local_only: bool
    summary_only: bool


class ProviderCapabilityMatrixPolicy:
    def classify(
        self,
        *,
        cognition_tier: str,
        architecture_sensitive: bool = False,
        implementation_patch: bool = False,
        compact_summary: bool = False,
    ) -> ProviderCapabilityMatrixFrame:
        normalized = cognition_tier.upper()
        if compact_summary or implementation_patch or normalized == "LOW":
            recommended = "LOW"
        elif architecture_sensitive or normalized == "HIGH":
            recommended = "HIGH"
        else:
            recommended = "MEDIUM"
        capabilities = (
            ProviderCapability(
                "LOW",
                architecture_safe=False,
                implementation_safe=True,
                compact_summary_safe=True,
                deterministic_metadata_only=True,
                recommended_for=("compact_summary", "repetitive_task", "local_patch"),
            ),
            ProviderCapability(
                "MEDIUM",
                architecture_safe=False,
                implementation_safe=True,
                compact_summary_safe=True,
                deterministic_metadata_only=True,
                recommended_for=("implementation", "bounded_review", "adapter_wiring"),
            ),
            ProviderCapability(
                "HIGH",
                architecture_safe=True,
                implementation_safe=True,
                compact_summary_safe=False,
                deterministic_metadata_only=True,
                recommended_for=("architecture", "governance", "high_risk_boundary"),
            ),
        )
        return ProviderCapabilityMatrixFrame(
            recommended_provider_class=recommended,
            capabilities=capabilities,
            architecture_safe_provider_classification=True,
            implementation_safe_provider_classification=True,
            compact_summary_safe_provider_classification=True,
            deterministic_provider_metadata_only=all(
                capability.deterministic_metadata_only for capability in capabilities
            ),
            provider_neutral=True,
            local_only=True,
            summary_only=True,
        )
