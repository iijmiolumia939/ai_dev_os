from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SprintMetadataFrame:
    sprint_id: str
    active_fr_tc: tuple[str, ...]
    affected_runtimes: tuple[str, ...]
    roadmap_stage: str
    active_risks: tuple[str, ...]
    architecture_flags: tuple[str, ...]
    continuity_state: str
    validation_status: str
    schema_supported: bool


class SprintMetadataPolicy:
    def from_file(self, path: str | Path) -> SprintMetadataFrame:
        return self.from_mapping(self._parse_simple_yaml(Path(path).read_text(encoding="utf-8")))

    def from_mapping(self, data: dict[str, object]) -> SprintMetadataFrame:
        return SprintMetadataFrame(
            sprint_id=str(data.get("sprint_id", data.get("sprint", "next"))),
            active_fr_tc=self._tuple(data.get("active_fr_tc", ())),
            affected_runtimes=self._tuple(data.get("affected_runtimes", ())),
            roadmap_stage=str(data.get("roadmap_stage", "unknown")),
            active_risks=self._tuple(data.get("active_risks", ())),
            architecture_flags=self._tuple(data.get("architecture_flags", ())),
            continuity_state=str(data.get("continuity_state", "compact")),
            validation_status=str(data.get("validation_status", "unknown")),
            schema_supported=True,
        )

    def default(
        self, *, sprint_id: str = "next", project_name: str = "project"
    ) -> SprintMetadataFrame:
        return self.from_mapping(
            {
                "sprint_id": sprint_id,
                "active_fr_tc": ("FR-REPOINTEL-01", "TC-REPOINTEL-01"),
                "affected_runtimes": ("repository_intelligence", "session_orchestrator"),
                "roadmap_stage": f"{project_name}: repository intelligence",
                "active_risks": ("manual summary drift",),
                "architecture_flags": ("read-only workspace collector",),
                "continuity_state": "compact",
                "validation_status": "pending",
            }
        )

    def _parse_simple_yaml(self, text: str) -> dict[str, object]:
        data: dict[str, object] = {}
        current_key = ""
        for raw_line in text.splitlines():
            line = raw_line.rstrip()
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if line.startswith("  - ") and current_key:
                values = list(data.get(current_key, ()))
                values.append(line[4:].strip().strip("\"'"))
                data[current_key] = tuple(values)
                continue
            if ":" in line:
                key, value = line.split(":", 1)
                current_key = key.strip()
                stripped = value.strip()
                if stripped.startswith("[") and stripped.endswith("]"):
                    data[current_key] = tuple(
                        part.strip().strip("\"'")
                        for part in stripped[1:-1].split(",")
                        if part.strip()
                    )
                elif stripped:
                    data[current_key] = stripped.strip("\"'")
                else:
                    data[current_key] = ()
        return data

    def _tuple(self, value: object) -> tuple[str, ...]:
        if isinstance(value, tuple):
            return tuple(str(item) for item in value)
        if isinstance(value, list):
            return tuple(str(item) for item in value)
        if isinstance(value, str):
            return (value,) if value else ()
        return ()
