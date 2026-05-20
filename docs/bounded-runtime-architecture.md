# Bounded Runtime Architecture

対象: NFR-ARCH-21, NFR-COST-18, NFR-OBS-04, FR-RUNTIMEGRAPH-01, FR-RUNTIMEGRAPH-02, FR-RUNTIMEGRAPH-03, FR-RUNTIMEGRAPH-04, FR-RUNTIMEGRAPH-05, TC-RUNTIMEGRAPH-01, TC-RUNTIMEGRAPH-02, TC-RUNTIMEGRAPH-03, TC-RUNTIMEGRAPH-04, TC-RUNTIMEGRAPH-05.

AI_DEV_OS は governance、retrieval、persistence、session orchestration、provider simulation、VSCode integration、workspace cognition に分割されています。bounded runtime architecture は、この分割を full visualization platform にせず、fixed-size observability と local-only cognition で維持します。

## Runtime Clusters

- governance
- retrieval
- persistence
- orchestration
- provider
- vscode
- cognition
- adapters

`RuntimeClusterFrame` は cluster size、oversized clusters、cross-cluster pressure、merge candidates、isolation candidates を summary-only で保持します。

## Architecture Pressure

`ArchitecturePressureFrame` は runtime count pressure、dependency density pressure、contract surface pressure、cross-boundary pressure、orchestration pressure、persistence complexity pressure を統合します。

`bounded_architecture_maintained` が true である条件は、bounded edge limit、summary-only discovery、no signature replay、no AST export が守られていることです。