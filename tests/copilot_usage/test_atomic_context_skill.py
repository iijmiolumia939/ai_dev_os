from __future__ import annotations

from ai_dev_os.copilot_usage.atomic_prompting import AtomicPromptPolicy
from ai_dev_os.copilot_usage.context_diet import ContextDietPolicy, ContextItem
from ai_dev_os.copilot_usage.skill_compaction import SkillCompactionPolicy, SkillInstruction


def test_atomic_prompt_detects_broad_repository_request() -> None:
    report = AtomicPromptPolicy().evaluate(
        "Review the whole repo, decide architecture, implement the fix, and review everything."
    )

    assert report.accepted is False
    assert report.blocked is True
    assert "full_repository_request" in report.detected_patterns
    assert "mixed_architecture_implementation_review_prompt" in report.detected_patterns
    assert report.suggested_split_tasks
    assert report.estimated_avoided_tokens > 0


def test_context_diet_removes_unrelated_files_and_generated_artifacts() -> None:
    report = ContextDietPolicy().evaluate(
        (
            ContextItem("ai_dev_os/copilot_usage/context_diet/__init__.py", 600),
            ContextItem("docs/stale-sprint-history.md", 5_000, related=False, age_days=45),
            ContextItem("Library/vendor/binary.asset", 8_000, related=False),
            ContextItem("build/generated-report.json", 2_500, related=False),
            ContextItem("src/large_unrelated.py", 3_000, related=False),
        )
    )

    assert [item.path for item in report.allowed_context] == [
        "ai_dev_os/copilot_usage/context_diet/__init__.py"
    ]
    assert len(report.removed_context) == 4
    assert report.token_reduction_estimate == 18_500
    assert "unrelated_large_file_removed" in report.warnings
    assert "generated_artifact_removed" in report.warnings


def test_skill_compaction_requires_when_to_use_and_suppresses_duplicates() -> None:
    instructions = (
        SkillInstruction(
            "runtime-python",
            "Python runtime work",
            "Follow deterministic runtime rules." * 40,
            "Use for Python runtime policy work.",
        ),
        SkillInstruction(
            "missing-when-to-use",
            "General coding helper",
            "Always load this long instruction." * 80,
        ),
        SkillInstruction(
            "duplicate-runtime",
            "Python runtime work",
            "Duplicate content." * 80,
            "Use for Python runtime policy work.",
        ),
    )

    report = SkillCompactionPolicy().evaluate(instructions, active_task="Python runtime policy")

    assert report.compact_skill_index == ("runtime-python: Use for Python runtime policy work.",)
    assert report.missing_when_to_use == ("missing-when-to-use",)
    assert report.repeated_instruction_suppressed == ("duplicate-runtime",)
    assert "duplicated_skill_descriptions" in report.blocked_patterns
    assert report.estimated_avoided_tokens > 0
