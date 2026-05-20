# Runtime Contract Surface

対象: NFR-ARCH-21, NFR-COST-18, NFR-OBS-04, FR-RUNTIMEGRAPH-01, FR-RUNTIMEGRAPH-02, FR-RUNTIMEGRAPH-03, FR-RUNTIMEGRAPH-04, FR-RUNTIMEGRAPH-05, TC-RUNTIMEGRAPH-01, TC-RUNTIMEGRAPH-02, TC-RUNTIMEGRAPH-03, TC-RUNTIMEGRAPH-04, TC-RUNTIMEGRAPH-05.

Runtime contract surface は public runtime API の膨張を compact に観測するための summary-only runtime です。exported frames、exported policies、exported contracts、public runtime APIs、optional integrations を bounded metadata として扱います。

## Non Goals

- full signature replay は行わない。
- raw AST export は行わない。
- provider call や telemetry upload は行わない。
- runtime implementation details の全列挙は行わない。

## Signals

- `contract_surface_size`
- `runtime_api_pressure`
- `contract_expansion_detected`
- `oversized_runtime_detected`
- `simplification_recommended`

これらは runtime discovery の summary metadata から算出されます。contract pressure が高い場合でも、extension は自動 refactor や autonomous chat control を行わず、人間が確認する warning と dashboard summary だけを出します。