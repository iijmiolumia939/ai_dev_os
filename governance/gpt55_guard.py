from __future__ import annotations

GPT55_POLICY_VIOLATION = "GPT55_POLICY_VIOLATION"
ALLOWED_TASKS = {
    "architecture_redesign",
    "adversary_review",
    "scientific_reasoning",
    "governance_review",
}


class GPT55PolicyViolationError(RuntimeError):
    pass


def enforce(task_type: str, model_name: str) -> None:
    normalized_model = model_name.lower().replace(" ", "-")
    normalized_task = task_type.lower().replace("-", "_").replace(" ", "_")
    if normalized_model.startswith("gpt-5.5") and normalized_task not in ALLOWED_TASKS:
        raise GPT55PolicyViolationError(GPT55_POLICY_VIOLATION)
