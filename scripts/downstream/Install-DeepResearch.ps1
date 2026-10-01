param(
    [string]$HermesHome = (Join-Path $env:LOCALAPPDATA 'hermes'),
    [ValidatePattern('^[a-z][a-z0-9-]*$')][string]$Profile = 'research',
    [string]$ArchivePath
)
$ErrorActionPreference = 'Stop'
if ($Profile -eq 'default') { throw 'Use a separate research profile.' }
$integration = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../downstream/deep-research'))
$launcher = Join-Path $HermesHome 'bin/hermes.cmd'
$pin = Get-Content -LiteralPath (Join-Path $integration 'upstream.json') -Raw | ConvertFrom-Json
$runtime = (& $launcher --print-runtime-command --module hermes_cli.main) | ConvertFrom-Json
if ($LASTEXITCODE -ne 0 -or !(Test-Path -LiteralPath $runtime[0])) { throw 'Managed Python resolution failed.' }
$profileHome = Join-Path $HermesHome "profiles/$Profile"
if (!(Test-Path -LiteralPath (Join-Path $profileHome 'config.yaml'))) {
    & $launcher profile create $Profile --clone --no-alias --description 'Deep research with verified sources and resumable reports.'
    if ($LASTEXITCODE -ne 0) { throw 'Profile creation failed.' }
}
if (!$ArchivePath) {
    $cache = Join-Path $profileHome 'cache/deep-research'
    New-Item -ItemType Directory -Path $cache -Force | Out-Null
    $ArchivePath = Join-Path $cache ($pin.commit + '.zip')
    if (!(Test-Path -LiteralPath $ArchivePath)) {
        Invoke-WebRequest -Uri "https://codeload.github.com/Gyu-bot/hermes-deep-research/zip/$($pin.commit)" -OutFile $ArchivePath
    }
}
$destination = Join-Path $profileHome 'skills/research/hermes-deep-research'
& $runtime[0] -B (Join-Path $integration 'install_skill.py') --archive $ArchivePath --destination $destination --python $runtime[0] --profile-home $profileHome
if ($LASTEXITCODE -ne 0) { throw 'Skill installation failed.' }
if (!(Test-Path -LiteralPath (Join-Path $profileHome 'plugins/hindsight/plugin.yaml'))) {
    & $launcher -p $Profile plugins install hindsight --enable
    if ($LASTEXITCODE -ne 0) { throw 'Hindsight dependency setup failed. Run this installer in an interactive terminal.' }
}
$memoryDirectory = Join-Path $profileHome 'hindsight'
New-Item -ItemType Directory -Path $memoryDirectory -Force | Out-Null
$memoryConfig = Join-Path $memoryDirectory 'config.json'
if (!(Test-Path -LiteralPath $memoryConfig)) {
    Copy-Item -LiteralPath (Join-Path $integration 'hindsight-cloud.json') -Destination $memoryConfig
}
$soulPath = Join-Path $profileHome 'SOUL.md'
$soul = if (Test-Path -LiteralPath $soulPath) { Get-Content -LiteralPath $soulPath -Raw } else { '' }
if ($soul -notmatch '(?m)^## Personal deep research defaults$') {
    $instructions = Get-Content -LiteralPath (Join-Path $integration 'profile-instructions.md') -Raw
    [IO.File]::AppendAllText($soulPath, "`n" + $instructions, (New-Object Text.UTF8Encoding($false)))
}
Write-Output "Ready: select the $Profile profile in Hermes, then start a new chat."
Write-Output 'Hindsight Cloud authentication is completed in Settings > Memory & Context.'
