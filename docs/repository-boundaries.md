# Repository Boundaries

## Common OS

`ai-dev-os/runtime`, `governance`, `retrieval`, `checkpoints`, `telemetry`, `integrations`, `prompts`, `templates`, and `scripts` contain reusable operating-system logic.

These directories must not contain project domain behavior, hardcoded workspace paths, avatar logic, simulation physics, or biological model assumptions.

## Adapters

`ai-dev-os/adapters` bridges project runtime and shared OS runtime. Adapter code is the only place where project-specific identifiers are expected.

## Extensions

`ai-dev-os/extensions` contains reusable domain extension families. Extension code must remain generic inside its domain and avoid binding to a single repository layout.

## Project Runtime

Existing project runtime remains in the host repository until an adapter can replace direct coupling safely.