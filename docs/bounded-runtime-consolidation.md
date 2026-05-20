# Bounded Runtime Consolidation

対象: NFR-ARCH-22, NFR-COST-19, NFR-OBS-05, FR-RUNTIMESIMPLIFY-01, FR-RUNTIMESIMPLIFY-02, FR-RUNTIMESIMPLIFY-03, FR-RUNTIMESIMPLIFY-04, FR-RUNTIMESIMPLIFY-05, TC-RUNTIMESIMPLIFY-01, TC-RUNTIMESIMPLIFY-02, TC-RUNTIMESIMPLIFY-03, TC-RUNTIMESIMPLIFY-04, TC-RUNTIMESIMPLIFY-05.

Bounded runtime consolidation は runtime merge を実行する仕組みではありません。AI_DEV_OS の runtime fragmentation を summary-only に観測し、人間が rollback-safe な consolidation plan を検討できるようにするための architecture cognition layer です。

## Human Confirmation

`RuntimeMergeCandidateFrame` と `RuntimeSimplificationRecommendationFrame` は recommendation-only です。`human_review_required` と `human_confirmed_only` が true のまま保たれ、automatic merge、automatic rewrite、hidden injection は使いません。

## Consolidation Targets

- duplicated governance signals
- duplicated pressure aggregation
- duplicated persistence cleanup and retention logic
- duplicated session lifecycle warnings
- duplicated compact/export surfaces

## Safe Boundary

Consolidation は docs、tests、manual PR review を通じて別 commit で行います。この runtime は候補を示すだけで、source tree を変更しません。