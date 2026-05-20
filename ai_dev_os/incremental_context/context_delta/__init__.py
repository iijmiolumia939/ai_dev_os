from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContextDeltaFrame:
    changed_runtime_summaries: tuple[str, ...]
    changed_contract_summaries: tuple[str, ...]
    changed_governance_summaries: tuple[str, ...]
    changed_session_summaries: tuple[str, ...]
    excluded_unchanged_context: tuple[str, ...]
    unchanged_context_exclusion: bool
    deterministic_delta_scope: bool
    local_only: bool
    summary_only: bool


class ContextDeltaPolicy:
    def summarize(
        self,
        *,
        changed_runtimes: tuple[str, ...],
        all_runtimes: tuple[str, ...],
        changed_contracts: tuple[str, ...] = (),
        changed_governance: tuple[str, ...] = (),
        changed_session: tuple[str, ...] = (),
    ) -> ContextDeltaFrame:
        changed = tuple(dict.fromkeys(sorted(changed_runtimes)))
        all_runtime_names = tuple(dict.fromkeys(sorted(all_runtimes)))
        unchanged = tuple(runtime for runtime in all_runtime_names if runtime not in changed)
        return ContextDeltaFrame(
            changed_runtime_summaries=tuple(f"runtime:{runtime}" for runtime in changed),
            changed_contract_summaries=tuple(
                f"contract:{name}" for name in sorted(set(changed_contracts))
            ),
            changed_governance_summaries=tuple(
                f"governance:{name}" for name in sorted(set(changed_governance))
            ),
            changed_session_summaries=tuple(
                f"session:{name}" for name in sorted(set(changed_session))
            ),
            excluded_unchanged_context=unchanged,
            unchanged_context_exclusion=True,
            deterministic_delta_scope=True,
            local_only=True,
            summary_only=True,
        )
