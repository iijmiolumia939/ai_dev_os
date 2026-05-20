# VSCode Extension Setup

対象: NFR-COST-12, NFR-COST-13, NFR-ARCH-15, NFR-ARCH-16, NFR-SEC-03, FR-SESSIONBOUNDARY-01, FR-SESSIONBOUNDARY-02, FR-SESSIONBOUNDARY-03, FR-SESSIONBOUNDARY-04, FR-SESSIONBOUNDARY-05, FR-PERSISTENCE-01, FR-PERSISTENCE-02, FR-PERSISTENCE-03, FR-PERSISTENCE-04, FR-PERSISTENCE-05, TC-SESSIONBOUNDARY-01, TC-SESSIONBOUNDARY-02, TC-SESSIONBOUNDARY-03, TC-SESSIONBOUNDARY-04, TC-SESSIONBOUNDARY-05, TC-PERSISTENCE-01, TC-PERSISTENCE-02, TC-PERSISTENCE-03, TC-PERSISTENCE-04, TC-PERSISTENCE-05.

`extensions/ai-dev-os-vscode` は AI_DEV_OS の human-confirmed governance IDE layer です。Copilot Chat、ChatGPT、AgentChat、VSCode UI を自動操作しません。telemetry、remote publish、background prompt injection、autonomous chat control は行いません。

## Build

```powershell
Set-Location extensions/ai-dev-os-vscode
npm install
npm run compile
vsce package
```

`npm run compile` は `out/extension.js` を生成します。VSIX には runtime に必要な `out/` と manifest を含め、`.ai-dev-os/`、logs、cache、telemetry、temporary files、source maps、local checkpoints は含めません。

## Install From VSIX

1. VSCode の Extensions view を開く。
2. `...` menu から `Install from VSIX...` を選択する。
3. `extensions/ai-dev-os-vscode/ai-dev-os-vscode-0.1.0.vsix` を選択する。
4. `Reload Window` を実行する。
5. Command Palette で `AI_DEV_OS:` commands が表示されることを確認する。

## Extension Development Host

1. VSCode で AI_DEV_OS repository root を開く。
2. `extensions/ai-dev-os-vscode` を extension project として開くか、同ディレクトリを対象にした launch configuration を使う。
3. F5 で Extension Development Host を起動する。
4. startup exception が出ないことを確認する。
5. Explorer view に `AI_DEV_OS Session Boundary`、`AI_DEV_OS Governance Dashboard`、`AI_DEV_OS Governance Trends` が表示されることを確認する。
6. status bar に governance health と governance trend が表示されることを確認する。

## Runtime Commands

Command Palette から次を確認する。

- `AI_DEV_OS: Session Audit`
- `AI_DEV_OS: Generate Handoff`
- `AI_DEV_OS: Show Governance Dashboard`
- `AI_DEV_OS: Show Governance Trends`
- `AI_DEV_OS: Restore Session State`
- `AI_DEV_OS: Show Governance Pressure`
- `AI_DEV_OS: Show Governance Risks`
- `AI_DEV_OS: Compact Governance Context`

これらは local summary state を表示または更新するだけです。hidden automation や remote publish は行いません。

## Workspace Persistence

`.ai-dev-os/` は workspace-local only で、`.gitignore` により commit 対象外です。extension は startup 時に次を summary-only として読み取れます。

- `.ai-dev-os/session-boundary.json`
- `.ai-dev-os/rollover-state.json`
- `.ai-dev-os/continuity-index.json`
- `.ai-dev-os/checkpoints/`
- `.ai-dev-os/schema/`

stale session、rollover pending、retention pressure、schema migration、checkpoint pressure は warning と dashboard state として表示します。自動 cleanup や rollover は command 実行時だけ行います。