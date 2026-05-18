from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ContinueIndex:
    local_embeddings: bool
    manifest_paths: tuple[str, ...]
    immutable_reference_paths: tuple[str, ...]
    checkpoint_paths: tuple[str, ...]
    cloud_retrieval_enabled: bool = False

    @property
    def local_first(self) -> bool:
        return self.local_embeddings and not self.cloud_retrieval_enabled


def build_local_index(root: Path) -> ContinueIndex:
    manifest_paths = tuple(
        path.relative_to(root).as_posix() for path in (root / "retrieval").glob("*manifest*.json")
    )
    reference_root = root / "extensions" / "scientific"
    immutable_reference_paths = tuple(
        path.relative_to(root).as_posix()
        for path in reference_root.glob("*.json")
        if reference_root.exists()
    )
    checkpoint_root = root / "checkpoints"
    checkpoint_paths = tuple(
        path.relative_to(root).as_posix()
        for path in checkpoint_root.glob("checkpoint-*.json")
        if checkpoint_root.exists()
    )
    return ContinueIndex(
        local_embeddings=True,
        manifest_paths=manifest_paths,
        immutable_reference_paths=immutable_reference_paths,
        checkpoint_paths=checkpoint_paths,
    )
