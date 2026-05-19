from __future__ import annotations

from dataclasses import dataclass

ARCHITECTURE_PATTERNS = {
    "architecture_redesign": ("architecture redesign", "architectural redesign", "再設計"),
    "governance_redesign": ("governance redesign", "policy redesign", "ガバナンス再設計"),
    "provider_redesign": ("provider redesign", "provider architecture", "provider 境界"),
    "retrieval_redesign": ("retrieval redesign", "retrieval architecture", "検索設計"),
    "runtime_contract_redesign": ("contract redesign", "runtime contract", "契約再設計"),
    "broad_review_request": ("review everything", "overall review", "全体レビュー", "全部見て"),
}


@dataclass(frozen=True)
class ArchitectureIsolationFrame:
    isolated_session_required: bool
    scoped_architecture_bundle: tuple[str, ...]
    council_required: bool
    fresh_session_required: bool
    detected_patterns: tuple[str, ...]
    warnings: tuple[str, ...]


class ArchitectureIsolationPolicy:
    def evaluate(
        self,
        prompt: str,
        *,
        affected_runtimes: tuple[str, ...] = (),
        routine_patch: bool = False,
    ) -> ArchitectureIsolationFrame:
        normalized = prompt.lower()
        detected: list[str] = []
        for pattern_name, markers in ARCHITECTURE_PATTERNS.items():
            if any(marker in normalized for marker in markers):
                detected.append(pattern_name)
        if routine_patch and detected:
            detected.append("routine_patch_architecture_mixing")

        isolated = bool(detected)
        scoped_bundle = tuple(
            dict.fromkeys(affected_runtimes or self._bundle_from_patterns(detected))
        )
        return ArchitectureIsolationFrame(
            isolated_session_required=isolated,
            scoped_architecture_bundle=scoped_bundle,
            council_required=isolated and "broad_review_request" not in detected,
            fresh_session_required=isolated,
            detected_patterns=tuple(dict.fromkeys(detected)),
            warnings=(
                ("routine_patch_must_not_mix_architecture_context",)
                if routine_patch and isolated
                else ()
            ),
        )

    def _bundle_from_patterns(self, detected: list[str]) -> tuple[str, ...]:
        bundle: list[str] = []
        if "governance_redesign" in detected:
            bundle.append("governance")
        if "provider_redesign" in detected:
            bundle.append("providers")
        if "retrieval_redesign" in detected:
            bundle.append("retrieval")
        if "runtime_contract_redesign" in detected:
            bundle.append("runtime_contracts")
        if "architecture_redesign" in detected and not bundle:
            bundle.append("architecture")
        return tuple(bundle)
