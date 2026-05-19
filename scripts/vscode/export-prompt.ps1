param(
    [string]$Workspace = ".",
    [switch]$Json,
    [switch]$CopyReady
)

$arguments = @("-m", "ai_dev_os.cli", "export-prompt", "--workspace", $Workspace)
if ($Json) { $arguments += "--json" }
if ($CopyReady) { $arguments += "--copy-ready" }
python @arguments
