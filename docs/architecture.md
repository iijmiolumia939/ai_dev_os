# Architecture

AI Development OS uses clean boundaries between shared runtime, project adapters, and reusable extensions.

Shared runtime owns governance, retrieval, telemetry, checkpointing, integrations, prompts, and bootstrap. Adapters connect the runtime to project code. Extensions provide reusable domain layers without binding the OS to a single project.