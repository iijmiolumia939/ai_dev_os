# Clipboard Continuity Export

対象: NFR-COST-11, FR-VSCODE-03, FR-VSCODE-05, TC-VSCODE-02, TC-VSCODE-03, TC-VSCODE-05.

Clipboard runtime は local-only の copy-ready prompt delivery layer です。clipboard が利用できない場合や copy に失敗した場合は、bounded prompt export に fallback します。テストは実 clipboard に依存せず、失敗 path を deterministic に検証します。

## Export Shape

- `prompt.txt`: 次 session に貼り付ける prompt。
- `continuation.md`: compact continuity の人間向け markdown。
- `compact_bundle.json`: structured summary-only bundle。

export bundle には full transcript、full repository dump、generated artifact、Chat UI state を含めません。

## Safety Boundary

- network call は行わない。
- browser / Playwright / Selenium / VSCode Chat UI automation は行わない。
- clipboard は local OS capability として扱い、失敗時は file export に fallback する。
- session handoff は human-confirmed であり、送信操作は人間が実行する。
