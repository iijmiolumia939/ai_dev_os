from __future__ import annotations

from release import ReleaseChecklist, validate_release
from versioning import ChangeKind, classify_change


def test_semantic_versioning_classification() -> None:
    assert classify_change(breaking_runtime=True, new_capability=False) is ChangeKind.MAJOR
    assert classify_change(breaking_runtime=False, new_capability=True) is ChangeKind.MINOR
    assert classify_change(breaking_runtime=False, new_capability=False) is ChangeKind.PATCH


def test_release_governance_blocks_unsafe_release() -> None:
    safe, failures = validate_release(
        ReleaseChecklist(
            governance_validation=True,
            cost_governance_validation=True,
            extension_validation=True,
            compatibility_validation=False,
            package_build_validation=True,
            readme_rendering_validation=True,
            twine_validation=True,
        )
    )

    assert safe is False
    assert failures == ("compatibility_validation",)
