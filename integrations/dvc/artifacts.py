from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ScientificArtifact:
    artifact_id: str
    path: str
    kind: str
    immutable: bool
    dvc_tracked: bool
    simulation_parameters: tuple[str, ...] = ()


def build_artifact_manifest(root: Path) -> dict[str, object]:
    reference_path = root / "extensions" / "scientific" / "formula_registry.json"
    artifacts = [
        ScientificArtifact(
            artifact_id="FORMULA-REF-001",
            path="extensions/scientific/formula_registry.json",
            kind="formula_reference_index",
            immutable=True,
            dvc_tracked=reference_path.exists(),
            simulation_parameters=("mass", "joint_damping", "actuator_gain"),
        )
    ]
    return {
        "version": 1,
        "policy": "version scientific artifacts; do not inject repeated paper context",
        "artifacts": [asdict(artifact) for artifact in artifacts],
    }
