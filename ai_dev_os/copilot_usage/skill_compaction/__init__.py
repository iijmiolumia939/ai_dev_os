from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SkillInstruction:
    name: str
    description: str
    content: str
    when_to_use: str = ""
    always_loaded: bool = False


@dataclass(frozen=True)
class InstructionCompactReport:
    compact_skill_index: tuple[str, ...]
    missing_when_to_use: tuple[str, ...]
    excluded_instructions: tuple[str, ...]
    long_instruction_warnings: tuple[str, ...]
    repeated_instruction_suppressed: tuple[str, ...]
    blocked_patterns: tuple[str, ...]
    estimated_avoided_tokens: int


class SkillCompactionPolicy:
    def __init__(self, *, long_instruction_tokens: int = 1_200) -> None:
        self.long_instruction_tokens = long_instruction_tokens

    def evaluate(
        self,
        instructions: tuple[SkillInstruction, ...],
        *,
        active_task: str = "",
    ) -> InstructionCompactReport:
        compact_index: list[str] = []
        missing_when_to_use: list[str] = []
        excluded: list[str] = []
        long_warnings: list[str] = []
        repeated: list[str] = []
        blocked: list[str] = []
        seen_descriptions: set[str] = set()
        active_terms = self._terms(active_task)

        if instructions and all(instruction.always_loaded for instruction in instructions):
            blocked.append("every_skill_always_loaded")

        for instruction in instructions:
            description_key = " ".join(instruction.description.lower().split())
            if description_key in seen_descriptions:
                repeated.append(instruction.name)
                continue
            seen_descriptions.add(description_key)

            if not instruction.when_to_use.strip():
                missing_when_to_use.append(instruction.name)
                excluded.append(instruction.name)
                continue
            if self._estimate_tokens(instruction.content) > self.long_instruction_tokens:
                long_warnings.append(instruction.name)
            if not self._is_relevant(instruction, active_terms):
                excluded.append(instruction.name)
                continue
            compact_index.append(self._compact_entry(instruction))

        if any(self._looks_like_full_dump(instruction.content) for instruction in instructions):
            blocked.append("full_instruction_dump")
        if repeated:
            blocked.append("duplicated_skill_descriptions")

        removed_tokens = sum(
            self._estimate_tokens(instruction.content)
            for instruction in instructions
            if instruction.name in set(excluded + repeated)
        )
        return InstructionCompactReport(
            compact_skill_index=tuple(compact_index),
            missing_when_to_use=tuple(missing_when_to_use),
            excluded_instructions=tuple(dict.fromkeys(excluded)),
            long_instruction_warnings=tuple(long_warnings),
            repeated_instruction_suppressed=tuple(repeated),
            blocked_patterns=tuple(dict.fromkeys(blocked)),
            estimated_avoided_tokens=removed_tokens,
        )

    def _compact_entry(self, instruction: SkillInstruction) -> str:
        when = instruction.when_to_use.strip().splitlines()[0]
        return f"{instruction.name}: {when}"

    def _is_relevant(self, instruction: SkillInstruction, active_terms: set[str]) -> bool:
        if not active_terms:
            return not instruction.always_loaded
        instruction_terms = self._terms(f"{instruction.name} {instruction.when_to_use}")
        return bool(active_terms & instruction_terms)

    def _looks_like_full_dump(self, content: str) -> bool:
        return self._estimate_tokens(content) > self.long_instruction_tokens * 3

    def _terms(self, text: str) -> set[str]:
        return {
            term
            for term in text.lower().replace("/", " ").replace("-", " ").split()
            if len(term) > 3
        }

    def _estimate_tokens(self, text: str) -> int:
        return max(1, len(text) // 4) if text else 0
