# Windows execution and memory

Use the absolute installed skill path returned by `skill_view`. The shipped
`scripts/research.ps1` selects Hermes's managed Python and binds HERMES_HOME to
this research profile. Invoke it with PowerShell, without Bash command substitution:

```powershell
$skill = 'ABSOLUTE PATH RETURNED BY skill_view'
$run = & (Join-Path $skill 'scripts/research.ps1') create 'short-topic' --query 'Full research question' --mode deep --axis 'Evidence' --axis 'Counterevidence'
& (Join-Path $skill 'scripts/research.ps1') validate $run
& (Join-Path $skill 'scripts/research.ps1') status $run
```

When invoking from `terminal`, use its configured shell's argument syntax. If
the terminal uses cmd.exe, invoke `powershell -NoProfile -ExecutionPolicy Bypass
-File` with the quoted absolute helper path. Do not use `python3`, Bash exports,
or Bash RUN_DIR assignment on native Windows. Keep all run outputs under the
returned absolute run directory and use its `tmp/workspace` as the workdir.

Upstream's secure cleanup relies on POSIX directory descriptors. Both cleanup
inspection and deletion are unavailable on native Windows. Do not call cleanup
here and do not replace it with recursive shell deletion; preserve run files.
Research creation, validation, resumption, and document-gate checks are supported.

Use English for reports unless the user requests another language; include
original-language evidence when it helps answer the question. Link consequential
factual claims to the original source in report prose, in addition to maintaining
the complete source ledger. Report unresolved contradictions and coverage gaps.

If Hindsight is active, retain only checked conclusions worth reusing, with
their source URLs, as-of date, scope, and uncertainty. Hindsight is supplementary
recall; use the run files for progress and recheck dated facts against live sources.
Never claim a memory write succeeded unless the provider confirms it.

Delegation concurrency is an existing runtime setting. Inspect it and respect it;
this installation does not change it. A run budget may end a research session
before convergence; checkpoint and report partial work rather than claim completion.

Scheduling and PDF rendering remain optional and require a specific user request.
