from __future__ import annotations

from core import ProjectProfile, RuntimeKind, decide_runtime


def test_shared_runtime_selects_scientific_prompt() -> None:
    decision = decide_runtime(
        ProjectProfile(
            project_name="ScientificProject",
            runtime_type=RuntimeKind.SCIENTIFIC,
            architecture_type="modular",
            governance_level="runtime-enforced",
            scientific_mode=True,
        )
    )

    assert decision.prompt_template == "prompts/scientific-runtime.prompt.md"
    assert decision.local_first is True
