param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('create', 'init', 'status', 'validate')]
    [string]$Action,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ResearchArguments
)
$ErrorActionPreference = 'Stop'
$runtime = Get-Content -LiteralPath (Join-Path $PSScriptRoot '../windows-runtime.json') -Raw | ConvertFrom-Json
$previousHome = $env:HERMES_HOME
try {
    $env:HERMES_HOME = $runtime.profile_home
    & $runtime.python -B (Join-Path $PSScriptRoot 'research_state.py') $Action @ResearchArguments
    if ($LASTEXITCODE -ne 0) { throw "Research helper failed with exit code $LASTEXITCODE" }
} finally {
    if ($null -eq $previousHome) { Remove-Item Env:HERMES_HOME -ErrorAction SilentlyContinue }
    else { $env:HERMES_HOME = $previousHome }
}
