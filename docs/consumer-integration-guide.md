# Consumer Integration Guide

Consumers depend on AI Development OS through stable contracts, adapters, and optional extensions. Project-specific logic must stay in the consumer project or adapter layer.

Recommended flow:
1. Select an adapter contract.
2. Validate compatibility against the compatibility matrix.
3. Bind governance, retrieval, telemetry, and integrations through shared APIs.
4. Keep domain runtime outside `core/`.