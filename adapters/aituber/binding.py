from __future__ import annotations

from dataclasses import dataclass

from consumer_contracts import AdapterContract, ConsumerRuntimeContract, ExtensionContract


@dataclass(frozen=True)
class AITuberRuntimeBinding:
    retrieval: str
    governance: str
    telemetry: str
    integrations: str
    adapter: str


def build_aituber_contract(os_version: str = "0.1.0") -> ConsumerRuntimeContract:
    return ConsumerRuntimeContract(
        project_name="AITuber",
        adapter=AdapterContract(
            name="aituber",
            version="0.1.0",
            supported_os=os_version,
            required_capabilities=("retrieval", "governance", "telemetry", "embodiment"),
        ),
        extensions=(
            ExtensionContract(name="embodiment", version="0.1.0", supported_os=os_version),
            ExtensionContract(name="unity", version="0.1.0", supported_os=os_version),
        ),
        governance_level="runtime-enforced",
    )


def build_aituber_runtime_binding() -> AITuberRuntimeBinding:
    return AITuberRuntimeBinding(
        retrieval="retrieval.select_context",
        governance="governance.budget_runtime",
        telemetry="telemetry.runtime",
        integrations="integrations.runtime",
        adapter="adapters.aituber.binding",
    )
