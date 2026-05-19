from __future__ import annotations

from dataclasses import dataclass

EXCLUDED_CONTEXT_KEYS = {
    "full_sprint_history",
    "giant_markdown",
    "stale_oq",
    "obsolete_adr",
    "unrelated_runtime",
    "vendor_assets",
    "full_repository_tree",
}


@dataclass(frozen=True)
class ContinuityBundleSource:
    active_fr_tc: tuple[str, ...]
    current_sprint_summary: str
    affected_runtimes: tuple[str, ...]
    active_risks: tuple[str, ...]
    current_roadmap: tuple[str, ...]
    current_architectural_constraints: tuple[str, ...]
    current_governance_state: dict[str, str]
    extra_context: dict[str, str] | None = None


@dataclass(frozen=True)
class ContinuityBundleFrame:
    active_fr_tc: tuple[str, ...]
    current_sprint_summary: str
    affected_runtimes: tuple[str, ...]
    active_risks: tuple[str, ...]
    current_roadmap: tuple[str, ...]
    current_architectural_constraints: tuple[str, ...]
    current_governance_state: dict[str, str]
    excluded_context: tuple[str, ...]
    bundle_token_estimate: int
    token_reduction_estimate: int
    summary_only: bool


class ContinuityBundlePolicy:
    def __init__(self, *, token_budget: int = 2_400) -> None:
        self.token_budget = token_budget

    def build(
        self,
        source: ContinuityBundleSource,
        *,
        summary_only: bool = False,
    ) -> ContinuityBundleFrame:
        extra_context = source.extra_context or {}
        excluded = tuple(key for key in extra_context if key in EXCLUDED_CONTEXT_KEYS)
        included_extra = {
            key: value for key, value in extra_context.items() if key not in EXCLUDED_CONTEXT_KEYS
        }
        summary = self._compact_text(source.current_sprint_summary, 900 if summary_only else 1_500)
        roadmap = self._limit_tuple(source.current_roadmap, 3 if summary_only else 5)
        risks = self._limit_tuple(source.active_risks, 3 if summary_only else 5)
        constraints = self._limit_tuple(
            source.current_architectural_constraints,
            4 if summary_only else 6,
        )
        frame = ContinuityBundleFrame(
            active_fr_tc=self._limit_tuple(source.active_fr_tc, 10),
            current_sprint_summary=summary,
            affected_runtimes=self._limit_tuple(source.affected_runtimes, 8),
            active_risks=risks,
            current_roadmap=roadmap,
            current_architectural_constraints=constraints,
            current_governance_state=dict(source.current_governance_state),
            excluded_context=excluded,
            bundle_token_estimate=0,
            token_reduction_estimate=sum(
                self._estimate_tokens(value) for value in extra_context.values()
            ),
            summary_only=summary_only,
        )
        token_estimate = self._estimate_frame_tokens(frame) + sum(
            self._estimate_tokens(value) for value in included_extra.values()
        )
        if token_estimate > self.token_budget:
            summary = self._trim_to_budget(summary, max(120, self.token_budget // 3))
            frame = ContinuityBundleFrame(
                active_fr_tc=frame.active_fr_tc,
                current_sprint_summary=summary,
                affected_runtimes=frame.affected_runtimes,
                active_risks=frame.active_risks,
                current_roadmap=frame.current_roadmap,
                current_architectural_constraints=frame.current_architectural_constraints,
                current_governance_state=frame.current_governance_state,
                excluded_context=frame.excluded_context,
                bundle_token_estimate=0,
                token_reduction_estimate=frame.token_reduction_estimate,
                summary_only=True,
            )
            token_estimate = self._estimate_frame_tokens(frame)
        return ContinuityBundleFrame(
            active_fr_tc=frame.active_fr_tc,
            current_sprint_summary=frame.current_sprint_summary,
            affected_runtimes=frame.affected_runtimes,
            active_risks=frame.active_risks,
            current_roadmap=frame.current_roadmap,
            current_architectural_constraints=frame.current_architectural_constraints,
            current_governance_state=frame.current_governance_state,
            excluded_context=frame.excluded_context,
            bundle_token_estimate=min(token_estimate, self.token_budget),
            token_reduction_estimate=frame.token_reduction_estimate,
            summary_only=frame.summary_only,
        )

    def _compact_text(self, text: str, max_chars: int) -> str:
        return text if len(text) <= max_chars else text[: max_chars - 3].rstrip() + "..."

    def _trim_to_budget(self, text: str, token_budget: int) -> str:
        max_chars = token_budget * 4
        return self._compact_text(text, max_chars)

    def _limit_tuple(self, values: tuple[str, ...], limit: int) -> tuple[str, ...]:
        return tuple(value for value in values if value)[:limit]

    def _estimate_frame_tokens(self, frame: ContinuityBundleFrame) -> int:
        return self._estimate_tokens(
            " ".join(
                (
                    " ".join(frame.active_fr_tc),
                    frame.current_sprint_summary,
                    " ".join(frame.affected_runtimes),
                    " ".join(frame.active_risks),
                    " ".join(frame.current_roadmap),
                    " ".join(frame.current_architectural_constraints),
                    " ".join(
                        f"{key}:{value}" for key, value in frame.current_governance_state.items()
                    ),
                )
            )
        )

    def _estimate_tokens(self, text: str) -> int:
        return max(1, len(text) // 4) if text else 0
