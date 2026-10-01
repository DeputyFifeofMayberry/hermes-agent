param(
    [Parameter(Mandatory = $true)][string]$Question,
    [ValidateSet('quick', 'deep', 'exhaustive')][string]$Mode = 'deep',
    [ValidateRange(60, 21600)][int]$BudgetSeconds = 900,
    [string]$HermesHome = (Join-Path $env:LOCALAPPDATA 'hermes')
)
$ErrorActionPreference = 'Stop'
$launcher = Join-Path $HermesHome 'bin/hermes.cmd'
$prompt = "Use hermes-deep-research in $Mode mode. Question: $Question. Read the Windows execution notes first. Maintain durable checkpoints and original-source citations. Deliver Markdown and sources.json. Respect the $BudgetSeconds second run budget and report partial work if gaps remain."
& $launcher -p research chat --skills hermes-deep-research --run-budget $BudgetSeconds -q $prompt
exit $LASTEXITCODE
