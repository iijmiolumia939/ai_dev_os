from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AuditDeltaFrame:
    runtime_audit_delta_mode: bool
    unchanged_audit_section_suppression: bool
    compact_audit_delta_summary: tuple[str, ...]
    expandable_audit_details: tuple[str, ...]
    repeated_validation_replay_suppression: bool
    estimated_avoided_validation_tokens: int
    summary_only: bool
    deterministic: bool


class AuditDeltaPolicy:
    def summarize(
        self,
        *,
        changed_sections: tuple[str, ...],
        unchanged_sections: tuple[str, ...],
        repeated_validations: tuple[str, ...] = (),
    ) -> AuditDeltaFrame:
        changed = tuple(dict.fromkeys(sorted(changed_sections)))
        unchanged = tuple(dict.fromkeys(sorted(unchanged_sections)))
        repeated = tuple(dict.fromkeys(sorted(repeated_validations)))
        return AuditDeltaFrame(
            runtime_audit_delta_mode=True,
            unchanged_audit_section_suppression=bool(unchanged),
            compact_audit_delta_summary=tuple(f"audit:{section}" for section in changed),
            expandable_audit_details=tuple(f"unchanged:{section}" for section in unchanged)
            + tuple(f"validation:{item}" for item in repeated),
            repeated_validation_replay_suppression=bool(repeated),
            estimated_avoided_validation_tokens=len(unchanged) * 260 + len(repeated) * 380,
            summary_only=True,
            deterministic=True,
        )
