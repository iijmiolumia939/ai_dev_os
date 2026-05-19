# VSCode Rollover Extension

対象: NFR-COST-12, NFR-ARCH-15, FR-SESSIONBOUNDARY-01, FR-SESSIONBOUNDARY-02, FR-SESSIONBOUNDARY-03, FR-SESSIONBOUNDARY-04, FR-SESSIONBOUNDARY-05, TC-SESSIONBOUNDARY-01, TC-SESSIONBOUNDARY-02, TC-SESSIONBOUNDARY-03, TC-SESSIONBOUNDARY-04, TC-SESSIONBOUNDARY-05.

`extensions/ai-dev-os-vscode` は human-confirmed session boundary enforcement のための VSCode extension です。Copilot Chat / ChatGPT / AgentChat UI を自動操作しません。UI automation は禁止です。

## Commands

- `AI_DEV_OS: Session Audit`
- `AI_DEV_OS: Generate Handoff`
- `AI_DEV_OS: Copy Continuity Bundle`
- `AI_DEV_OS: Open New Session Prompt`
- `AI_DEV_OS: Confirm Session Rollover`
- `AI_DEV_OS: Show Session Boundary State`
- `AI_DEV_OS: Compact Current Session`
- `AI_DEV_OS: Show Stale Session Warning`

## Local State

Extension state は VSCode `globalState` に保存されます。保持するのは current session generation、last rollover timestamp、current enforcement state、last exported continuity bundle、stale warning count、pending rollover state です。telemetry 収集と network dependency はありません。

## Handoff Flow

1. local AI_DEV_OS CLI から bounded handoff を生成する。
2. copy-ready prompt を local state に保持する。
3. clipboard command で continuity bundle をコピーする。
4. new session prompt を markdown document として開き、人間が内容を確認する。
5. 人間が新 session へ移行したあと `Confirm Session Rollover` で generation を進める。
