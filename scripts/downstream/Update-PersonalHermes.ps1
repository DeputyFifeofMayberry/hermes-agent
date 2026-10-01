param([switch]$Check)

$ErrorActionPreference = 'Stop'
$repo = Join-Path $env:LOCALAPPDATA 'hermes\hermes-agent'
$launcher = Join-Path $env:LOCALAPPDATA 'hermes\bin\hermes.cmd'
if (!(Test-Path -LiteralPath $launcher)) { throw "Hermes launcher is missing: $launcher" }
$origin = (& git -C $repo remote get-url origin)
if ($LASTEXITCODE -ne 0) { throw 'Could not read the installed repository.' }
if ($origin.TrimEnd('/').Replace('.git', '') -ne 'https://github.com/DeputyFifeofMayberry/hermes-agent') {
    throw 'The installed origin must be your personal Hermes fork.'
}
$branch = (& git -C $repo branch --show-current)
if ($LASTEXITCODE -ne 0 -or $branch -ne 'custom') { throw 'The installed checkout must be on custom.' }
$changes = (& git -C $repo status --porcelain)
if ($LASTEXITCODE -ne 0 -or $changes) { throw 'Commit or preserve installed source changes before updating.' }
$updateArgs = @('update', '--branch', 'custom')
if ($Check) { $updateArgs += '--check' } else { $updateArgs += '--yes' }
& $launcher @updateArgs
exit $LASTEXITCODE
