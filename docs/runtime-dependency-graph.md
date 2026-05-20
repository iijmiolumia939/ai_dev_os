# Runtime Dependency Graph

対象: NFR-ARCH-21, NFR-COST-18, NFR-OBS-04, FR-RUNTIMEGRAPH-01, FR-RUNTIMEGRAPH-02, FR-RUNTIMEGRAPH-03, FR-RUNTIMEGRAPH-04, FR-RUNTIMEGRAPH-05, TC-RUNTIMEGRAPH-01, TC-RUNTIMEGRAPH-02, TC-RUNTIMEGRAPH-03, TC-RUNTIMEGRAPH-04, TC-RUNTIMEGRAPH-05.

Runtime dependency graph は AI_DEV_OS の runtime explosion を bounded observability で抑えるための summary-only runtime です。目的は巨大な architecture visualization system ではなく、runtime category、bounded dependency edge、cross-boundary pressure、contract surface pressure を小さく確認することです。

## Boundary

- full repository graph は作らない。
- full AST graph は作らない。
- dynamic runtime tracing は行わない。
- hidden telemetry は使わない。
- local package metadata と deterministic category rules だけを使う。

## Frames

- `RuntimeDiscoveryFrame`: runtime name、category、boundary、contract count、dependency count を列挙する。
- `RuntimeDependencyGraphFrame`: bounded node/edge summary、cross-boundary edges、governance-critical edges、optional edges、isolated groups を保持する。
- `ArchitecturePressureFrame`: runtime count、dependency density、contract surface、cross-boundary、orchestration、persistence complexity を pressure としてまとめる。

## Bounded Graph

`RuntimeDependencyGraphPolicy` は `max_edges` を必ず受け取り、edge count をその上限以下に保ちます。edge はカテゴリ間の固定規則から生成され、source file import graph や AST traversal には依存しません。

## VSCode Integration

VSCode extension は compact tree view と status bar だけを提供します。graph spam を避けるため、oversized runtime warning と cross-boundary warning は rate-limited notification 経由で表示します。