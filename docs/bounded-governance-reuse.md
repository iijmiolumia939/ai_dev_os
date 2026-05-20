# Bounded Governance Reuse

Governance Core の目的は runtime explosion を抑えながら、duplicated governance warning と bounded retention drift を観測可能にすることです。

## Dashboard Signals

VSCode extension は次の command と view を提供します。

- `aiDevOs.showGovernanceCore`
- `aiDevOs.showSharedPrimitives`
- `aiDevOs.showPrimitiveReuse`
- `aiDevOs.showBoundedRetention`
- `aiDevOs.showCompactExportStatus`
- `aiDevOsSharedPrimitives`
- `aiDevOsPrimitiveReuse`
- `aiDevOsBoundedRetention`

これらは local summary を表示するだけで、自動 refactor、外部送信、隠れた状態変更は行いません。
