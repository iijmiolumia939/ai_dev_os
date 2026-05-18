from __future__ import annotations


def tokenize(value: str) -> set[str]:
    return {part.lower() for part in value.replace("-", "_").replace("/", "_").split("_") if part}


def score_path(path: str, query_terms: set[str]) -> int:
    normalized = path.replace("\\", "/").lower()
    return sum(3 for term in query_terms if term in normalized)
