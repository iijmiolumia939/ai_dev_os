from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReportDensityFrame:
    section_count: int
    repeated_token_estimate: int
    unchanged_summary_ratio: float
    verbosity_pressure: str
    compaction_recommendation: bool
    estimated_avoided_completion_tokens: int
    deterministic: bool


class ReportDensityPolicy:
    def audit(
        self,
        sections: tuple[str, ...],
        *,
        unchanged_sections: int = 0,
        repeated_token_estimate: int = 0,
    ) -> ReportDensityFrame:
        section_count = len(sections)
        unchanged_ratio = round(unchanged_sections / max(1, section_count), 4)
        pressure_score = (
            section_count + (repeated_token_estimate // 40) + int(unchanged_ratio * 10)
        )
        if pressure_score >= 12:
            pressure = "HIGH"
        elif pressure_score >= 7:
            pressure = "MEDIUM"
        else:
            pressure = "LOW"
        avoided = max(0, repeated_token_estimate + max(0, section_count - 5) * 20)
        return ReportDensityFrame(
            section_count=section_count,
            repeated_token_estimate=repeated_token_estimate,
            unchanged_summary_ratio=unchanged_ratio,
            verbosity_pressure=pressure,
            compaction_recommendation=pressure in {"MEDIUM", "HIGH"},
            estimated_avoided_completion_tokens=avoided,
            deterministic=True,
        )
