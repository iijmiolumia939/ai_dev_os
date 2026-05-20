from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CheckpointRotationFrame:
    active_checkpoints: tuple[str, ...]
    archived_checkpoints: tuple[str, ...]
    expired_checkpoints: tuple[str, ...]
    generation_rotation: tuple[str, ...]
    checkpoint_compaction: bool
    rotation_required: bool


class CheckpointRotationPolicy:
    def rotate(
        self,
        *,
        checkpoints: tuple[str, ...],
        max_active: int = 3,
        max_archived: int = 5,
    ) -> CheckpointRotationFrame:
        unique = tuple(dict.fromkeys(checkpoints))
        active = unique[:max_active]
        archived = unique[max_active : max_active + max_archived]
        expired = unique[max_active + max_archived :]
        return CheckpointRotationFrame(
            active_checkpoints=active,
            archived_checkpoints=archived,
            expired_checkpoints=expired,
            generation_rotation=active + archived,
            checkpoint_compaction=bool(expired),
            rotation_required=bool(expired),
        )
