from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.runtime_graph.runtime_discovery import RuntimeDiscoveryFrame


@dataclass(frozen=True)
class RuntimeContractSurfaceFrame:
    exported_frames: tuple[str, ...]
    exported_policies: tuple[str, ...]
    exported_contracts: tuple[str, ...]
    public_runtime_apis: tuple[str, ...]
    optional_integrations: tuple[str, ...]
    contract_surface_size: int
    runtime_api_pressure: str
    contract_expansion_detected: bool
    oversized_runtime_detected: bool
    simplification_recommended: bool
    full_signature_replay_used: bool
    raw_ast_export_used: bool


class RuntimeContractSurfacePolicy:
    def summarize(
        self,
        discovery: RuntimeDiscoveryFrame,
        *,
        max_contract_surface: int = 64,
    ) -> RuntimeContractSurfaceFrame:
        frames = tuple(
            f"{record.runtime_name}:Frame"
            for record in discovery.runtimes
            if record.runtime_contract_count > 0
        )[:max_contract_surface]
        policies = tuple(
            f"{record.runtime_name}:Policy"
            for record in discovery.runtimes
            if record.runtime_category != "other"
        )[:max_contract_surface]
        contracts = tuple(
            f"{record.runtime_name}:{record.runtime_category}" for record in discovery.runtimes
        )[:max_contract_surface]
        apis = tuple(f"{record.runtime_name}.summary" for record in discovery.runtimes)[
            :max_contract_surface
        ]
        optional = tuple(
            record.runtime_name
            for record in discovery.runtimes
            if record.runtime_category in {"provider", "adapters", "vscode"}
        )[:8]
        size = sum(record.runtime_contract_count for record in discovery.runtimes)
        oversized = any(record.runtime_contract_count > 10 for record in discovery.runtimes)
        pressure = "high" if size > 72 else "medium" if size > 36 else "low"
        expansion = size > max_contract_surface
        return RuntimeContractSurfaceFrame(
            exported_frames=frames,
            exported_policies=policies,
            exported_contracts=contracts,
            public_runtime_apis=apis,
            optional_integrations=optional,
            contract_surface_size=size,
            runtime_api_pressure=pressure,
            contract_expansion_detected=expansion,
            oversized_runtime_detected=oversized,
            simplification_recommended=expansion or oversized or pressure == "high",
            full_signature_replay_used=False,
            raw_ast_export_used=False,
        )
