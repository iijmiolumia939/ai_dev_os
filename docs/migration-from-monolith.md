# Migration From Monolith

1. Extract shared runtime without deleting project code.
2. Add adapters at project boundaries.
3. Move prompts, retrieval, telemetry, and governance to shared runtime.
4. Keep domain logic in project code or extensions.
5. Enable shared CI gates once the adapter boundary is stable.