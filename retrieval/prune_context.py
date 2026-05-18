from __future__ import annotations

import json

SOFT_LIMIT = 20_000
HARD_LIMIT = 40_000
PRESERVE_KEYS = {"active_requirements", "changed_files", "active_artifacts", "entries", "policy"}


def estimate_tokens(payload: object) -> int:
    return max(1, len(json.dumps(payload, ensure_ascii=False)) // 4)


def prune(bundle: dict[str, object]) -> dict[str, object]:
    if "full_repository_context" in bundle:
        raise ValueError("full repository context is forbidden")
    if estimate_tokens(bundle) <= SOFT_LIMIT:
        return dict(bundle)
    compact = {key: value for key, value in bundle.items() if key in PRESERVE_KEYS}
    compact["context_tokens"] = estimate_tokens(compact)
    if compact["context_tokens"] > HARD_LIMIT:
        compact["entries"] = list(compact.get("entries", []))[:3]
        compact["context_tokens"] = estimate_tokens(compact)
    return compact
