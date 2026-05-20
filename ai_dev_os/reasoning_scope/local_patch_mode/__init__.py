from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LocalPatchModeFrame:
    local_runtime_only_reasoning: bool
    file_neighborhood_reasoning: tuple[str, ...]
    adjacent_contract_only_reasoning: tuple[str, ...]
    compact_implementation_cognition: tuple[str, ...]
    no_roadmap_expansion: bool
    adjacent_runtime_only_reasoning_mode: bool
    bounded_cognition_only: bool
    local_only: bool
    deterministic: bool
    summary_only: bool


class LocalPatchModePolicy:
    def scope(
        self,
        *,
        touched_files: tuple[str, ...],
        affected_runtimes: tuple[str, ...],
        adjacent_contracts: tuple[str, ...] = (),
    ) -> LocalPatchModeFrame:
        files = tuple(dict.fromkeys(sorted(touched_files)))[:4]
        runtimes = tuple(dict.fromkeys(sorted(affected_runtimes)))[:2]
        contracts = tuple(dict.fromkeys(sorted(adjacent_contracts)))[:4]
        return LocalPatchModeFrame(
            local_runtime_only_reasoning=True,
            file_neighborhood_reasoning=files,
            adjacent_contract_only_reasoning=contracts,
            compact_implementation_cognition=tuple(f"patch:{runtime}" for runtime in runtimes),
            no_roadmap_expansion=True,
            adjacent_runtime_only_reasoning_mode=True,
            bounded_cognition_only=True,
            local_only=True,
            deterministic=True,
            summary_only=True,
        )
