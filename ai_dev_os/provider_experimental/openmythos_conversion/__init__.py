from __future__ import annotations

from dataclasses import dataclass

OPENMYTHOS_HF_IMPLEMENTATION_REPO = "maidacundo/open-mythos-hf"
OPENMYTHOS_HF_WEIGHTS_REPO = "maidacundo/open-mythos-140m"
OPENMYTHOS_EXPERIMENTAL_MODEL = "openmythos-exp"
OPENMYTHOS_GGUF_ARTIFACT = "openmythos-q4_k_m.gguf"
OPENMYTHOS_MODEFILE = "Modelfile.openmythos-exp"
OPENMYTHOS_CONVERSION_DEPENDENCIES = (
    "transformers>=4.40,<5",
    "safetensors>=0.4,<1",
    "huggingface_hub>=0.23,<1",
)
OPENMYTHOS_CONVERSION_TOOLING = (
    "llama.cpp convert_hf_to_gguf.py",
    "llama.cpp llama-quantize",
)


@dataclass(frozen=True)
class GGUFCompatibilityFrame:
    direct_hf_repo: str
    weighted_hf_repo: str
    direct_ollama_result: str
    weighted_ollama_result: str
    gguf_repository_found: bool
    llama_cpp_compatible: bool
    compatibility_result: str


@dataclass(frozen=True)
class ExperimentalModelValidationFrame:
    validation_active: bool
    tokenizer_integrity: str
    forward_pass_stability: str
    compact_prompt_inference: str
    hf_native_weights_repo: str
    adjacent_runtime_retrieval_only: bool
    compact_prompts_only: bool
    max_prompt_chars: int


@dataclass(frozen=True)
class ExperimentalQuantizationFrame:
    quantization_active: bool
    preferred_quantization: str
    rtx3080_10gb_target: bool
    expected_artifact: str
    artifact_scope: str
    modelfile_name: str
    num_ctx: int
    temperature: float


@dataclass(frozen=True)
class ExperimentalFallbackFrame:
    fallback_active: bool
    fallback_route: str
    rollback_safe_fallback: bool
    no_hidden_provider_switching: bool
    no_production_routing_change: bool
    fallback_reason: str


@dataclass(frozen=True)
class OpenMythosConversionFrame:
    conversion_active: bool
    local_patch_only: bool
    isolated_dependencies_only: bool
    stable_runtime_dependencies_unchanged: bool
    dependencies: tuple[str, ...]
    conversion_tooling: tuple[str, ...]
    conversion_result: str
    gguf_artifact_result: str
    ollama_model_name: str
    modelfile_template: str
    no_architecture_authority: bool
    no_governance_authority: bool
    no_anti_explosion_authority: bool
    no_autonomous_execution_authority: bool


@dataclass(frozen=True)
class OpenMythosConversionRuntimeFrame:
    compatibility: GGUFCompatibilityFrame
    validation: ExperimentalModelValidationFrame
    quantization: ExperimentalQuantizationFrame
    fallback: ExperimentalFallbackFrame
    conversion: OpenMythosConversionFrame


class OpenMythosConversionRuntime:
    def evaluate(
        self,
        *,
        direct_ollama_result: str = "failed:repository_not_gguf_or_llama_cpp_compatible",
        weighted_ollama_result: str = "failed:repository_not_gguf_or_llama_cpp_compatible",
        gguf_repository_found: bool = False,
        conversion_result: str = "guarded:not_converted_custom_open_mythos_architecture",
    ) -> OpenMythosConversionRuntimeFrame:
        compatibility = GGUFCompatibilityFrame(
            direct_hf_repo=OPENMYTHOS_HF_IMPLEMENTATION_REPO,
            weighted_hf_repo=OPENMYTHOS_HF_WEIGHTS_REPO,
            direct_ollama_result=direct_ollama_result,
            weighted_ollama_result=weighted_ollama_result,
            gguf_repository_found=gguf_repository_found,
            llama_cpp_compatible=False,
            compatibility_result="requires_conversion_fallback",
        )
        validation = ExperimentalModelValidationFrame(
            validation_active=True,
            tokenizer_integrity="tokenizer_json_available_in_hf_weights_repo",
            forward_pass_stability="not_executed_until_conversion_supported",
            compact_prompt_inference="not_executed_until_gguf_artifact_exists",
            hf_native_weights_repo=OPENMYTHOS_HF_WEIGHTS_REPO,
            adjacent_runtime_retrieval_only=True,
            compact_prompts_only=True,
            max_prompt_chars=1200,
        )
        quantization = ExperimentalQuantizationFrame(
            quantization_active=True,
            preferred_quantization="Q4_K_M",
            rtx3080_10gb_target=True,
            expected_artifact=OPENMYTHOS_GGUF_ARTIFACT,
            artifact_scope="experimental_local_only",
            modelfile_name=OPENMYTHOS_MODEFILE,
            num_ctx=4096,
            temperature=0.7,
        )
        fallback = ExperimentalFallbackFrame(
            fallback_active=True,
            fallback_route="qwen2.5-coder:7b",
            rollback_safe_fallback=True,
            no_hidden_provider_switching=True,
            no_production_routing_change=True,
            fallback_reason="openmythos_gguf_unavailable",
        )
        conversion = OpenMythosConversionFrame(
            conversion_active=True,
            local_patch_only=True,
            isolated_dependencies_only=True,
            stable_runtime_dependencies_unchanged=True,
            dependencies=OPENMYTHOS_CONVERSION_DEPENDENCIES,
            conversion_tooling=OPENMYTHOS_CONVERSION_TOOLING,
            conversion_result=conversion_result,
            gguf_artifact_result="not_created_until_compatible_conversion_succeeds",
            ollama_model_name=OPENMYTHOS_EXPERIMENTAL_MODEL,
            modelfile_template=OPENMYTHOS_MODEFILE,
            no_architecture_authority=True,
            no_governance_authority=True,
            no_anti_explosion_authority=True,
            no_autonomous_execution_authority=True,
        )
        return OpenMythosConversionRuntimeFrame(
            compatibility=compatibility,
            validation=validation,
            quantization=quantization,
            fallback=fallback,
            conversion=conversion,
        )


__all__ = [
    "GGUFCompatibilityFrame",
    "OPENMYTHOS_CONVERSION_DEPENDENCIES",
    "OPENMYTHOS_CONVERSION_TOOLING",
    "OPENMYTHOS_EXPERIMENTAL_MODEL",
    "OPENMYTHOS_GGUF_ARTIFACT",
    "OPENMYTHOS_HF_IMPLEMENTATION_REPO",
    "OPENMYTHOS_HF_WEIGHTS_REPO",
    "OPENMYTHOS_MODEFILE",
    "ExperimentalFallbackFrame",
    "ExperimentalModelValidationFrame",
    "ExperimentalQuantizationFrame",
    "OpenMythosConversionFrame",
    "OpenMythosConversionRuntime",
    "OpenMythosConversionRuntimeFrame",
]
