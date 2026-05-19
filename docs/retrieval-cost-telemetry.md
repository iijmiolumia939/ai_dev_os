# Retrieval Cost Telemetry

Retrieval cost telemetry estimates token burn and billing pressure before any paid provider call happens.

## Metrics

- Retrieval context tokens before scaling.
- Compressed context tokens after scaling.
- Prompt and completion token estimates.
- Tier multiplier.
- Fallback and retry penalties.
- Estimated before and after cost.
- Estimated savings ratio.
- Token burn avoided.

## Artifact Policy

Telemetry frames are machine-readable in memory. Generated provider telemetry reports, snapshots, JSONL files, and logs must remain ignored and uncommitted.