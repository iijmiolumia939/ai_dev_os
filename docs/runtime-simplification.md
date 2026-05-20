# Runtime Simplification

対象: NFR-ARCH-22, NFR-COST-19, NFR-OBS-05, FR-RUNTIMESIMPLIFY-01, FR-RUNTIMESIMPLIFY-02, FR-RUNTIMESIMPLIFY-03, FR-RUNTIMESIMPLIFY-04, FR-RUNTIMESIMPLIFY-05, TC-RUNTIMESIMPLIFY-01, TC-RUNTIMESIMPLIFY-02, TC-RUNTIMESIMPLIFY-03, TC-RUNTIMESIMPLIFY-04, TC-RUNTIMESIMPLIFY-05.

Runtime simplification は AI_DEV_OS の runtime explosion、contract fragmentation、governance duplication を human-guided に整理するための bounded observability runtime です。目的は自動自己改変ではなく、summary-only overlap analysis と deterministic merge candidates を人間が確認できる形で出すことです。

## Boundary

- automatic runtime merge は行わない。
- file rewrite や dynamic code transformation は行わない。
- AST replay、full source analysis、dynamic tracing は行わない。
- hidden contract injection は行わない。
- local-only architecture cognition と summary-only recommendation に限定する。

## Frames

- `RuntimeOverlapFrame`: responsibility overlap と simplification pressure を出す。
- `RuntimeMergeCandidateFrame`: merge candidates、merge risk、rollback-safe possibility、human review requirement を出す。
- `RuntimeSimplificationRecommendationFrame`: runtime merges、contract reductions、boundary tightening、isolation、governance consolidation を human-readable にまとめる。

VSCode extension は runtime overlap、contract overlap、merge candidates を compact tree view と rate-limited warning として表示します。自動 refactor や chat UI control は行いません。