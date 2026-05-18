from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class UsageRecord:
    project_name: str
    prompt_tokens: int
    output_tokens: int
    cost: float
    model_tier: str
    provider: str


def write_daily_usage(records: list[UsageRecord], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "daily_usage_report.json"
    payload = {
        "projects": sorted({record.project_name for record in records}),
        "prompt_tokens": sum(record.prompt_tokens for record in records),
        "output_tokens": sum(record.output_tokens for record in records),
        "cost": sum(record.cost for record in records),
        "records": [asdict(record) for record in records],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path
