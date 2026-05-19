# VSCode Session Handoff

対象: NFR-COST-11, NFR-ARCH-14, FR-VSCODE-01, FR-VSCODE-02, FR-VSCODE-03, FR-VSCODE-04, FR-VSCODE-05, TC-VSCODE-01, TC-VSCODE-02, TC-VSCODE-03, TC-VSCODE-04, TC-VSCODE-05.

AI_DEV_OS の VSCode integration は、session rollover が必要なときに compact continuity bundle と copy-ready prompt を生成する local runtime です。Copilot、ChatGPT、AgentChat の UI を自動操作しません。新 session 作成、貼り付け、送信は人間が確認して行います。

## Runtime Boundary

- stale context detection と rollover recommendation を行う。
- continuity bundle は summary-only / bounded context として生成する。
- prompt export は `prompt.txt`, `continuation.md`, `compact_bundle.json` の形式を持つ。
- clipboard runtime は利用可能なローカル clipboard にコピーし、失敗時は export fallback を使う。
- network、browser automation、Chat UI automation は runtime boundary 外です。

## Commands

```powershell
python -m ai_dev_os.cli handoff-session --workspace . --json
python -m ai_dev_os.cli export-prompt --workspace . --copy-ready
python -m ai_dev_os.cli copy-prompt --workspace . --json
python -m ai_dev_os.cli session-pressure --workspace . --json
python -m ai_dev_os.cli vscode-state --workspace . --json
```

VSCode task は `.vscode/tasks.json` に定義されています。`AI_DEV_OS: Generate Handoff` は copy-ready prompt を terminal に出力し、ユーザーが必要な session に貼り付けます。
