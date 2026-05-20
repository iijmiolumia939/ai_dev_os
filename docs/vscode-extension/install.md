# VSCode Extension Install

The AI_DEV_OS extension is a local governance UI for session handoff, persistence status, runtime graph, simplification, governance trends, and governance core primitives.

## Build Verification

```powershell
Set-Location extensions/ai-dev-os-vscode
npm ci
npm run compile
npx @vscode/vsce package --pre-release --out ai-dev-os-vscode-0.1.0-alpha.3.vsix
```

## Release Checks

- VSIX build verification must pass before release.
- Extension compile verification must pass before release.
- `.vscodeignore` must exclude source, logs, generated output, temporary files, and VSIX artifacts.
- The extension must not use hidden network dependency or hidden telemetry.
- Bounded local persistence is the only supported persistence model.
