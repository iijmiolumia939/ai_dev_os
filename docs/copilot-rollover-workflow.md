# Copilot Rollover Workflow

対象: NFR-COST-11, NFR-ARCH-14, FR-VSCODE-01, FR-VSCODE-02, FR-VSCODE-04, TC-VSCODE-01, TC-VSCODE-04, TC-VSCODE-05.

この workflow は Copilot / AgentChat session の context pressure が高いときに、manual rollover を短く安全にするためのものです。AI_DEV_OS は recommendation と compact prompt generation だけを行い、Copilot UI の起動、session 作成、貼り付け、送信は行いません。

## Steps

1. `AI_DEV_OS: Session Audit` で rollover pressure を確認する。
2. `AI_DEV_OS: Generate Handoff` で compact handoff prompt を生成する。
3. 新しい Copilot / AgentChat session を人間が作成する。
4. 出力された prompt を人間が確認して貼り付ける。
5. 新 session は compact continuity bundle だけを使い、full history replay を行わない。

## Governance

- stale topics は continuity bundle から除外される。
- repository subset と prompt mode が明示される。
- architecture isolation が必要な場合は handoff summary に反映される。
- notification は rate limited で、spam を発生させない。
