from __future__ import annotations

from adapters.aituber.binding import build_aituber_contract, build_aituber_runtime_binding
from compatibility import default_matrix
from versioning import validate_compatibility


def test_aituber_adapter_contract_is_compatible() -> None:
    contract = build_aituber_contract()
    report = validate_compatibility(contract, os_version="0.1.0", matrix=default_matrix())

    assert report.compatible is True
    assert contract.adapter.name == "aituber"
    assert "embodiment" in report.extensions


def test_aituber_runtime_binding_points_to_shared_runtime() -> None:
    binding = build_aituber_runtime_binding()

    assert binding.retrieval.startswith("retrieval.")
    assert binding.governance.startswith("governance.")
    assert binding.telemetry.startswith("telemetry.")
    assert binding.integrations.startswith("integrations.")
