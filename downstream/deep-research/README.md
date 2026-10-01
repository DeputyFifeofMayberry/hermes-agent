# Personal deep research setup

Feature branch: `feature/deep-research`, based on personal `custom` at `5f2087600`.
The app continues to run `custom`; this branch holds the reproducible integration.
Hermes discovers the installed skill in the separate `research` profile, so no
desktop rebuild or application branch switch is needed to use it.

## Plan and implementation

1. Pin the full Gyu-bot package at an immutable commit and verify the archive hash.
2. Clone the default profile into `research` to reuse its configured model and tools.
3. Install the complete runtime skill: license, references, templates, and helpers.
   Keep development tests and README installation examples in the review workspace;
   they are not runtime instructions. The pinned archive preserves all upstream files.
4. Add native PowerShell invocation and English report defaults. Preserve upstream
   research logic; document unsupported Windows cleanup instead of weakening it.
   Add profile instructions to recheck stale extraction against original sources.
5. Prepare Hindsight Cloud with a separate `hermes-research` bank; the user enters
   the API key in Hermes and activates the provider after configuration.
6. Run native Windows unit and helper checks, then a bounded live research check.
7. Publish this feature branch for review before merging it into `custom`.

## Install and use

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/downstream/Install-DeepResearch.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/downstream/Start-DeepResearch.ps1 -Question 'Your specific research question' -Mode deep -BudgetSeconds 900
```

In the desktop app, select **research**, start a new chat, and ask:
“Use hermes-deep-research in deep mode to investigate [question]. Include original
sources, contradictions, limitations, and a Markdown report.”

The helper's default 15-minute run budget is a session ceiling, not a guarantee
of finished research. Continue from the saved run directory to close remaining gaps.
The skill's own deep planning ceiling remains three hours. Concurrency stays at the
existing configured value (10 at setup); neither installer nor skill raises it.

Hindsight: **Settings → Memory & Context**, with settings scoped to **research**:
Cloud; URL `https://api.hindsight.vectorize.io`; bank `hermes-research`; recall `mid`.
Enter the API key using Hermes's secret field, save, select Hindsight, and start a
new session. Built-in memory supports research while Cloud authentication is pending.

## Maintenance and rollback

`upstream.json` pins the reviewed package; normal Hermes updates do not replace this
local skill. Re-running the installer verifies its receipt and preserves local edits.
To upgrade, review a new upstream commit, update its archive hash and adaptations,
preserve the installed package, and run the installer for a fresh destination.
Keep third-party package upgrades separate from upstream Hermes merges.

Switch to the default profile to leave this research setup. No cron jobs are
created. Markdown output needs no PDF dependency; PDF rendering is a separate feature.
Retain reports and checkpoints even if the skill is disabled or removed.

Upstream: https://github.com/Gyu-bot/hermes-deep-research
Copyright 2026 Gyu-bot, MIT. The complete license is installed with the package.

## Verification on October 1, 2026

- Native Windows, Hermes-managed Python 3.14.7: 20 applicable tests passed;
  six POSIX cleanup tests skipped. Two Windows contracts cover PowerShell run
  creation/validation and cleanup refusal with preserved files. The fallback-home
  upstream test was adapted to supply USERPROFILE as well as HOME.
- All PowerShell integration scripts parsed and the actual installer ran twice
  successfully; the second run verified the existing receipt without replacing files.
- Hermes's scanner allowed the installed runtime with zero findings. Development
  fixtures and README clone examples produced caution findings in the full archive;
  they stay in the review workspace rather than the runtime skill directory.
- A bounded live check loaded the installed skill, created a confined run, retrieved
  original sources, and produced a validated report and source ledger. A follow-up
  resumed the same session, replaced stale website extracts with immutable official
  documents, and completed the report. This was a small smoke check, not a benchmark
  of broad research quality or parallel throughput.
- The default profile's config, secrets file, and SOUL remained byte-identical.
  The app remained on `custom`; research concurrency remained 10.
- Hindsight 1.1.0 at catalog commit `eb021da3b2501911e4b57c82b3de1123572a200e`
  and its PM-managed dependencies were installed in the research profile. Cloud
  settings were staged; authentication, activation, and a real memory round-trip
  await the user's key. Built-in memory remains active in the meantime.
- Existing model configuration emitted an auxiliary title-generation HTTP 400;
  the actual research runs succeeded. No model setting was changed to hide it.
