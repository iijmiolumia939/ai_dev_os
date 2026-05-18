# Contributing

AI Development OS changes must preserve reusability.

Before submitting changes:
- keep project-specific behavior in `adapters/` or `extensions/`
- avoid hardcoded repository paths
- keep provider SDKs optional
- add or update governance gates for new boundaries
- run `python -m ruff check .`, `python -m black --check .`, and `python -m pytest`

For behavior changes, add tests under `tests/` and document migration impact.