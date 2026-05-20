from __future__ import annotations

from dataclasses import dataclass

REPEATED_PATTERNS = (
    "validation pass",
    "clean worktree",
    "ci success",
    "artifact cleanup",
    "rollout summary",
)


@dataclass(frozen=True)
class SummarySection:
    title: str
    body: str
    unchanged: bool = False


@dataclass(frozen=True)
class SummaryDeduplicationFrame:
    repeated_summary_detected: bool
    duplicate_section_collapse: bool
    unchanged_section_suppression: bool
    compact_references: tuple[str, ...]
    retained_sections: tuple[SummarySection, ...]
    suppressed_sections: tuple[str, ...]
    estimated_avoided_repeated_tokens: int
    deterministic: bool
    expandable: bool


class SummaryDeduplicationPolicy:
    def deduplicate(self, sections: tuple[SummarySection, ...]) -> SummaryDeduplicationFrame:
        seen: set[str] = set()
        retained: list[SummarySection] = []
        suppressed: list[str] = []
        compact_refs: list[str] = []
        repeated_detected = False
        avoided = 0

        for section in sections:
            key = _normalized_key(section)
            repeated = key in seen or any(pattern in key for pattern in REPEATED_PATTERNS)
            if section.unchanged or key in seen:
                suppressed.append(section.title)
                compact_refs.append(f"{section.title}: unchanged")
                avoided += _token_estimate(section.body)
                repeated_detected = repeated_detected or repeated
                continue
            if repeated:
                compact_refs.append(f"{section.title}: compact-ref")
                avoided += max(1, _token_estimate(section.body) // 2)
                repeated_detected = True
            retained.append(section)
            seen.add(key)

        return SummaryDeduplicationFrame(
            repeated_summary_detected=repeated_detected,
            duplicate_section_collapse=bool(suppressed),
            unchanged_section_suppression=any(section.unchanged for section in sections),
            compact_references=tuple(compact_refs),
            retained_sections=tuple(retained),
            suppressed_sections=tuple(suppressed),
            estimated_avoided_repeated_tokens=avoided,
            deterministic=True,
            expandable=True,
        )


def _normalized_key(section: SummarySection) -> str:
    body = " ".join(section.body.lower().split())
    title = " ".join(section.title.lower().split())
    return f"{title}:{body}"


def _token_estimate(text: str) -> int:
    return max(1, len(text.split()))
