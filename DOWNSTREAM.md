# Personal Hermes maintenance

Fork: https://github.com/DeputyFifeofMayberry/hermes-agent

`origin` is the personal fork; `upstream` is NousResearch/hermes-agent.
`main` is an unchanged upstream mirror. `custom` is the tested personal version.
The development checkout is separate from the installed checkout under
`%LOCALAPPDATA%\hermes\hermes-agent`. Develop and resolve merges in the development
checkout; install only commits already pushed to `origin/custom`.

## Update the installed version

```powershell
hermes update --branch custom
```

Or run `scripts/downstream/Update-PersonalHermes.ps1` from the development
checkout. Add `-Check` to check availability without applying an update.
The helper refuses a dirty installed checkout, a different origin, or a different
branch. Hermes still performs its normal backups and completion steps.

The existing updater defaults to `main`, even when `custom` is checked out.
`updates.auto_switch_parked_branch` is disabled in the current user configuration
to protect this branch. Use the explicit command above; a plain `hermes update`
or an update button that omits the branch is not the personal update route.
Do not select the official stable/canary feed for this custom source installation.

## Bring in developer updates

Start with a clean development checkout on `custom`:

```powershell
git switch custom
.\scripts\downstream\Start-UpstreamIntegration.ps1
```

The helper fetches official `main` and merges it into a new integration branch.
It leaves `custom` unchanged. A conflict stops there: resolve it and commit the
merge, or use `git merge --abort`. Git cannot promise zero overlapping edits;
this workflow keeps conflicts away from the installed version.

Review the merge and run the relevant Python tests through
`scripts/run_tests.sh`, plus the web/desktop builds. Reuse Hermes's PM-managed
Node/npm toolchain (activate this checkout first). Then promote the exact tested
integration branch, replacing the placeholder below:

```powershell
git switch custom
git merge --ff-only integration/upstream-YYYYMMDD-HHMMSS
git push origin custom
```

Keep the upstream mirror current separately, without custom commits or force pushes:

```powershell
git switch main
git merge --ff-only upstream/main
git push origin main
git switch custom
```

Then update the installed version with `hermes update --branch custom`.
Run one integration at a time and finish it before beginning another.

## Add fork features later

Create `feature/<name>` from `custom` for each chosen feature. Prefer an existing
plugin, extension, or configuration hook where possible. Otherwise, add the
other fork as a named remote, inspect its changes against its common upstream
ancestor, and cherry-pick only the feature commits and required dependencies.
Record the source commit and retain its attribution/license. Test that feature
branch, merge it into `custom`, and push. Avoid merging an entire unrelated fork:
it may carry old upstream changes, different dependencies, and platform assumptions.
Git recognizes shared commits, but rewritten/squashed feature commits may need
manual reconciliation when upstream eventually adds the same functionality.

## Vite policy

This personal version pins Vite **8.3.2** in `web`, `apps/desktop`, and
`apps/bootstrap-installer`, with the root lockfile regenerated. The root PostCSS
override is **8.5.28**, satisfying Vite's dependency requirement.

Updates install from the committed lockfile, so a global Vite installation is
unnecessary. Future personal updates retain the pin until deliberately changed.
When an upstream merge touches these manifests or the lockfile, reconcile the
manifests first, retain the chosen compatible Vite version, regenerate the root
lockfile with the managed npm, and build/test again. Do not blindly accept one
side of the lockfile or resolve it by deleting dependencies.

For later Vite releases, query `npm view vite version`, update all three exact
pins together, review any required dependency/Node changes, regenerate the lock,
and test on an integration branch. Promote the upgrade only after it passes.
The setup does not silently adopt every newly published package during updates.
