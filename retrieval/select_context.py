from __future__ import annotations

from retrieval.relevance_score import score_path, tokenize


def select_context(manifest: dict[str, object], query: str, limit: int = 12) -> dict[str, object]:
    terms = tokenize(query)
    entries = list(manifest.get("entries", []))
    ranked = sorted(
        entries, key=lambda entry: score_path(str(entry.get("path", "")), terms), reverse=True
    )
    return {
        "version": 1,
        "entries": ranked[:limit],
        "policy": "retrieval-first; no full repository context",
    }
