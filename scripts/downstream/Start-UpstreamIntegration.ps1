$ErrorActionPreference = 'Stop'
$repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
$branch = (& git -C $repo branch --show-current)
if ($LASTEXITCODE -ne 0 -or $branch -ne 'custom') { throw 'Start from the development checkout on custom.' }
$changes = (& git -C $repo status --porcelain)
if ($LASTEXITCODE -ne 0 -or $changes) { throw 'Commit or preserve development changes first.' }
$upstream = (& git -C $repo remote get-url upstream)
if ($LASTEXITCODE -ne 0 -or $upstream -ne 'https://github.com/NousResearch/hermes-agent.git') {
    throw 'upstream must point to the official Hermes repository.'
}
& git -C $repo fetch upstream main
if ($LASTEXITCODE -ne 0) { throw 'Upstream fetch failed.' }
& git -C $repo merge-base --is-ancestor upstream/main custom
if ($LASTEXITCODE -eq 0) { Write-Host 'custom already includes the fetched upstream main.'; exit 0 }
if ($LASTEXITCODE -ne 1) { throw 'Could not compare upstream with custom.' }
$integration = 'integration/upstream-' + [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')
& git -C $repo switch -c $integration
if ($LASTEXITCODE -ne 0) { throw 'Could not create the integration branch.' }
& git -C $repo merge --no-ff upstream/main -m "Merge upstream main into $integration"
if ($LASTEXITCODE -ne 0) {
    throw 'Merge stopped. Resolve conflicts on this integration branch, or run git merge --abort. custom has not moved.'
}
Write-Host "Prepared $integration. Build and test it before merging it into custom."
