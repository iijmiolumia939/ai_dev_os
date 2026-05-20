from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.runtime_graph.contract_surface import RuntimeContractSurfaceFrame


@dataclass(frozen=True)
class RuntimeContractOverlapFrame:
    contract_overlap_detected: bool
    duplicated_contract_groups: tuple[str, ...]
    oversized_contract_surface: bool
    contract_fragmentation_pressure: str
    contract_simplification_recommended: bool
    summary_only: bool
    full_signature_export_used: bool
    raw_ast_export_used: bool


class RuntimeContractOverlapPolicy:
    def detect(
        self,
        contract_surface: RuntimeContractSurfaceFrame,
        *,
        max_groups: int = 8,
    ) -> RuntimeContractOverlapFrame:
        groups = tuple(
            group
            for group in (
                _group("frames", contract_surface.exported_frames),
                _group("policies", contract_surface.exported_policies),
                _group("contracts", contract_surface.exported_contracts),
                _group("public_apis", contract_surface.public_runtime_apis),
                _group("integrations", contract_surface.optional_integrations),
            )
            if group
        )[:max_groups]
        oversized = contract_surface.oversized_runtime_detected or (
            contract_surface.contract_surface_size > 72
        )
        pressure = "high" if oversized else "medium" if len(groups) >= 3 else "low"
        return RuntimeContractOverlapFrame(
            contract_overlap_detected=bool(groups),
            duplicated_contract_groups=groups,
            oversized_contract_surface=oversized,
            contract_fragmentation_pressure=pressure,
            contract_simplification_recommended=oversized or len(groups) >= 3,
            summary_only=True,
            full_signature_export_used=False,
            raw_ast_export_used=False,
        )


def _group(label: str, values: tuple[str, ...]) -> str:
    if len(values) < 2:
        return ""
    prefix_count: dict[str, int] = {}
    for value in values:
        prefix = value.split(":", 1)[0].split(".", 1)[0]
        prefix_count[prefix] = prefix_count.get(prefix, 0) + 1
    repeated = tuple(sorted(key for key, count in prefix_count.items() if count > 1))
    if repeated:
        return f"{label}:{','.join(repeated[:4])}"
    return f"{label}:broad_surface"
