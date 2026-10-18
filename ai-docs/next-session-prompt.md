# Kickoff: historywright after the build (Step 3: wiki, eval follow-ups, polish)

Written 2026-10-17 at the end of the Step 2 build session. Paste this into a fresh session started in the folder
that holds this repository (the historywright clone).

## Where things stand

- historywright is built, public and installed: https://github.com/m4bwav/historywright, installed locally as
  historywright@mark-local 0.1.0. Three skills (`historywright`, `historywright-sources`, `historywright-pack`),
  hw.py (five stdlib modules), an 85-source registry, the era outline, the pack contract, 31 offline tests, CI
  green on Linux, macOS and Windows with Python 3.9 and 3.14. No tag, no release.
- Evals (TESTS.md, T-20261017-2 to -4): triggers 15 of 15, decoys 9 of 9; the with/without A/B on 11 value cases
  scored 82% with the skill against 39% without (+42 points, noise margin 22, cost 3.1x), harness verdict TRIM. All
  eight outcome cases pass 3 of 3 with the skill. With a clean cache, action-wikidata-full-statements passed 3/3 with the skill and 0/3 without (T-20261017-5).
- The first A/B (CUT) measured the harness: the runner's default tools blocked shell and web, and eval runs shared
  the user's real cache (L-005, and the cache note in TESTS.md). Value cases now grant Bash, PowerShell,
  WebFetch, WebSearch and Edit; the eval-written cache entries were moved to
  `~/.historywright/cache-from-evals-2026-10-17/`.
- Keys: OpenAlex and WHG are live in `~/.historywright/config.json`. Read them from there; never copy them
  anywhere else. `tests/check_skills.py` fails on key-like strings, home paths and AI credit lines.

## Read first

1. `ai-docs/HANDOFF.md`, then `ai-docs/log.md` (the 2026-10-17 Step 2 entry).
2. `ai-docs/decisions/2026-10-17-step2-build.md` (nine build rulings).
3. `AGENTS.md` (repository rules), `README.md`, `TESTS.md`, `LEARNINGS.md` (L-001 to L-005).
4. The owner's rules: the vault user PROFILE (`<vault>/user/PROFILE.md`, section "Code and repos";
   `everlast.py vault where` prints the vault). The owner's private notes for this project are in the vault's
   `projects/historywright/private/`.

## Next steps, in order

0. **Uncommitted work from the last session** (it ran out of session time): branch `docs/evals-banner` was pushed with the banner (`.github/images/banner.jpg`, seed 505), the eval fixes (tools field, `_skill`, regexes, exported `evals/cases/`), TESTS.md T-2 to T-5, LEARNINGS L-005, the log, HANDOFF and this prompt. Open a PR from it (`gh pr create`), let CI pass, merge it yourself. Also owed: `evergreen.py tested . --passed ... --failed ...` to record the suite in evergreen.json, and the action-cache-entry A/B (its run never started; clear `~/.historywright/cache` first).

1. **Wiki.** Ask Mark whether he has saved the first wiki page at https://github.com/m4bwav/historywright/wiki
   (GitHub creates the wiki repository only then; `git ls-remote https://github.com/m4bwav/historywright.wiki.git`
   tells). Then run the wikiwright skill on the repository. If he has not, ask once and move on.
2. **Evals follow-up.** Isolate the cache for eval runs: give hw.py a project-scoped home (for example a
   `.historywright/` folder in the working directory that `HW_HOME` lookups prefer) or run the action cases under
   `claude plugin eval` in WSL2 with `HW_HOME` set. Then re-run the action cases. Run `evergreen.py worth
   skills/historywright --probe` for trim candidates (TRIM verdict); trim only what the probe shows the model
   already knows, then re-run the A/B on the with arm only (`--append`, arms with).
3. **Open items** (README and HANDOFF list them): quote checks on PDFs (OpenAlex often links PDFs only), OHM
   queries in `hw.py place`, WHG v3 docs, the Seshat licence page, polywright-references reading
   `refs/index.json` notes, an `evergreen` plugin issue (its A/B environment check could match "requires approval").
4. Keep every change in a pull request; merge it yourself once CI passes (Mark's merge-by-default rule), unless it
   changes the release workflow or a public API, which waits for him.

## Rules

- Commit with `git -c user.email=156112+m4bwav@users.noreply.github.com`. No AI attribution anywhere.
- Research beats recall: a changed endpoint, limit, licence or gold answer needs an `R-` entry with its source.
- hw.py stays standard library, one JSON object per command, LF endings (`write_text` helper), tested offline.
- Never index or walk AppData. Kill processes only by PID. Parallel researchers share about 200 WebSearch calls a
  turn: cap each.

## When to stop and ask

- Before the first release tag (v0.1.0) and any directory submission: Mark's go-ahead.
- Before signing up for or paying for any source, installing a large dependency, or requesting a key for anyone.

Decide small design rulings yourself, record each in `ai-docs/decisions/`, and flag it in one line.

## Last paragraph (keep it in every rewrite)

At each milestone, and before you finish, write what you learned to the repo's `ai-docs/`: the log, a HANDOFF of 50 lines at most, and decisions and research notes. Then rewrite this file, `ai-docs/next-session-prompt.md`, as the prompt for the next fresh session: what to read first, the next step and its limits, the rules, and when to stop. End the new prompt with this same paragraph, and paste it in your final message.
