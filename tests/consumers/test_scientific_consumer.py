from __future__ import annotations

from compatibility import default_matrix
from consumer_contracts import AdapterContract, ConsumerRuntimeContract, ExtensionContract
from versioning import validate_compatibility


def test_scientific_consumer_contract_is_compatible() -> None:
    contract = ConsumerRuntimeContract(
        project_name="ScientificProject",
        adapter=AdapterContract(
            name="scientific",
            version="0.1.0",
            supported_os="0.1.0",
            required_capabilities=("retrieval", "governance", "telemetry"),
        ),
        extensions=(
            ExtensionContract(
                name="scientific",
                version="0.1.0",
                supported_os="0.1.0",
                optional_dependencies=("scientific",),
            ),
        ),
        governance_level="runtime-enforced",
    )

    report = validate_compatibility(contract, os_version="0.1.0", matrix=default_matrix())

    assert report.compatible is True
    assert contract.required_optional_dependencies() == ("scientific",)
