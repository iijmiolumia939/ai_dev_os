from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class CognitionCacheFrame:
    bounded_local_only_cognition_fingerprints: tuple[str, ...]
    deterministic_context_fingerprints: tuple[str, ...]
    unchanged_context_skip_recommendation: bool
    no_raw_prompt_persistence: bool
    no_provider_specific_hidden_memory: bool
    bounded_retention: bool
    local_only: bool
    deterministic: bool


class CognitionCachePolicy:
    def fingerprint(
        self,
        *,
        context_summaries: tuple[str, ...],
        previous_fingerprints: tuple[str, ...] = (),
        max_fingerprints: int = 8,
    ) -> CognitionCacheFrame:
        fingerprints = tuple(
            hashlib.sha256(summary.encode("utf-8")).hexdigest()[:16]
            for summary in sorted(set(context_summaries))
        )[:max_fingerprints]
        previous = set(previous_fingerprints)
        unchanged = bool(fingerprints) and all(item in previous for item in fingerprints)
        return CognitionCacheFrame(
            bounded_local_only_cognition_fingerprints=fingerprints,
            deterministic_context_fingerprints=fingerprints,
            unchanged_context_skip_recommendation=unchanged,
            no_raw_prompt_persistence=True,
            no_provider_specific_hidden_memory=True,
            bounded_retention=len(fingerprints) <= max_fingerprints,
            local_only=True,
            deterministic=True,
        )
