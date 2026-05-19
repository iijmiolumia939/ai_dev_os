from __future__ import annotations

from dataclasses import dataclass

from ai_dev_os.session_boundary.session_generation import SessionGenerationFrame


@dataclass(frozen=True)
class StaleSessionFrame:
    rollover_recommended_but_ignored: bool
    stale_continuity_reuse: bool
    architecture_topic_accumulation: bool
    giant_continuity_accumulation: bool
    excessive_session_age: bool
    stale_generation_mismatch: bool
    stale_session_detected: bool
    boundary_violation_risk: str
    rollover_required: bool
    forced_compaction_recommended: bool
    new_session_required: bool


class StaleSessionDetectionPolicy:
    def detect(
        self,
        *,
        generation: SessionGenerationFrame,
        rollover_recommended: bool,
        handoff_generated: bool,
        new_session_started: bool,
        continuity_generation: int,
        architecture_topic_count: int = 0,
        continuity_token_estimate: int = 0,
        session_age: int = 0,
        stale_continuity_reuse: bool = False,
    ) -> StaleSessionFrame:
        ignored = rollover_recommended and handoff_generated and not new_session_started
        architecture_accumulation = architecture_topic_count >= 3
        giant_continuity = continuity_token_estimate >= 12_000
        excessive_age = session_age >= 6
        generation_mismatch = continuity_generation < generation.active_generation
        detected = any(
            (
                ignored,
                stale_continuity_reuse,
                architecture_accumulation,
                giant_continuity,
                excessive_age,
                generation_mismatch,
            )
        )
        high_risk = ignored or generation_mismatch or giant_continuity
        risk = "high" if high_risk else "medium" if detected else "low"
        return StaleSessionFrame(
            rollover_recommended_but_ignored=ignored,
            stale_continuity_reuse=stale_continuity_reuse,
            architecture_topic_accumulation=architecture_accumulation,
            giant_continuity_accumulation=giant_continuity,
            excessive_session_age=excessive_age,
            stale_generation_mismatch=generation_mismatch,
            stale_session_detected=detected,
            boundary_violation_risk=risk,
            rollover_required=detected or rollover_recommended,
            forced_compaction_recommended=detected,
            new_session_required=high_risk,
        )
