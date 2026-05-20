# Contract Overlap

対象: NFR-ARCH-22, NFR-COST-19, NFR-OBS-05, FR-RUNTIMESIMPLIFY-01, FR-RUNTIMESIMPLIFY-02, FR-RUNTIMESIMPLIFY-03, FR-RUNTIMESIMPLIFY-04, FR-RUNTIMESIMPLIFY-05, TC-RUNTIMESIMPLIFY-01, TC-RUNTIMESIMPLIFY-02, TC-RUNTIMESIMPLIFY-03, TC-RUNTIMESIMPLIFY-04, TC-RUNTIMESIMPLIFY-05.

Contract overlap runtime は exported frames、exported policies、exported contracts、public APIs、duplicated integration surfaces を compact metadata だけで観測します。

## Non Goals

- full signature export は行わない。
- raw AST export は行わない。
- public API の全展開は行わない。
- runtime implementation details をコピーしない。

## Signals

- `contract_overlap_detected`
- `duplicated_contract_groups`
- `oversized_contract_surface`
- `contract_fragmentation_pressure`
- `contract_simplification_recommended`

これらは runtime graph の contract surface summary から算出されます。recommendation は human-confirmed only であり、自動 contract rewrite は禁止です。