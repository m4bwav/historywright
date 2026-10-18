# Kickoff: historywright Step 4 (eval cache isolation, trim, small hw.py follow-ups)

Written 2026-10-18 at the end of the Step 3 session. Paste this into a fresh session started in the folder that
holds this repository (the historywright clone).

## Where things stand

- historywright is public and installed: https://github.com/m4bwav/historywright, historywright@mark-local 0.1.0
  (reinstalled from main on 2026-10-18). No tag, no release.
- The wiki is live (12 pages, wiki commit 5f89b34), verified against main at 29bc397 on Windows and WSL Ubuntu.
  Its note, `ai-docs/notes/2026-10-18-github-wiki.md`, holds the update procedure, the verifier and its outputs.
- Evals: all 19 cases have passed with the skill; measured baselines are in `evals/evals.json`. The A/B verdict
  was TRIM (82% with, 39% without, cost 3.1x).
- Step 3 merged PR #1 to #5, including two hw.py fixes found by the wiki: `HW_RECORD` no longer writes key
  values into fixtures, and `cal date` no longer misreads `709 AUC`, `1300 AH`, AH years, Hijri months or Roman
  day counts.
- Keys: OpenAlex and WHG are live in `~/.historywright/config.json`. Read them from there; never copy them
  anywhere else.

## Read first

1. `ai-docs/HANDOFF.md`, then `ai-docs/log.md` (the 2026-10-18 entry).
2. `ai-docs/decisions/2026-10-18-session-rulings.md` (six rulings) and `2026-10-17-step2-build.md`.
3. `AGENTS.md`, `TESTS.md`, `LEARNINGS.md` (L-001 to L-005).
4. The owner's rules: the vault user PROFILE (`everlast.py vault where` prints the vault), section "Code and repos".

## Next steps, in order

0. **Ask Mark two things in your first message, then carry on:** may the wiki verifier keep calling keyless
   public APIs live (wikiwright L-160 `live-public-sources`, which departs from its L-122)? And is it time for the
   v0.1.0 tag? Record his answers in `ai-docs/decisions/`. If he refuses L-160, re-verify the wiki against
   fixtures recorded once and labelled as recorded (the note's update procedure), and set L-160's status.
1. **Eval cache isolation.** Eval runs share the real `~/.historywright/cache`, so an earlier run's entry ends a
   later run at Step 0. Give hw.py a project-scoped home: `HW_HOME` first, then a `.historywright/` folder in the
   working directory when it exists, then `~/.historywright`. Test it offline, say it in cli.md and `doctor`,
   and have the eval cases create the folder. Then re-run the three action cases (`evergreen.py worth ... --ab
   --case "action-*"`), and record the results in TESTS.md.
2. **Trim.** `evergreen.py worth skills/historywright --probe` for what the model already knows; trim only that
   from SKILL.md, then re-run the A/B on the with arm only (`--append --arm with`). Every SKILL.md edit gets a
   CHANGELOG entry and keeps the description under 700 characters.
3. **Small hw.py follow-ups** (HANDOFF "Next" 2): Wayback capture repeats in `src wayback`, the AH `read_as`
   label, circa as EDTF `~`, and parsing Kalends, Nones, Ides and Hijri month names. Each with a test.
4. **Open items** (HANDOFF "Next" 3), as time allows.
5. After any change to a packaged file, run the wiki's update procedure (the note), on Windows and in WSL.

## Rules

- Commit with `git -c user.email=156112+m4bwav@users.noreply.github.com`. No AI attribution anywhere.
- Every change goes through a pull request; merge it yourself once CI passes (squash or merge as the repo's
  history shows; this repo uses merge commits), unless it changes the release workflow or a public API.
- Run `python tests/check_skills.py`, `python tests/test_hw.py` and `python scripts/budget.py` before every
  commit, and stage files by name, not with `git add -A` (Step 3 pushed a failing commit that way).
- Research beats recall: a changed endpoint, limit, licence or gold answer needs an `R-` entry with its source.
- hw.py stays standard library, one JSON object per command, LF endings (`write_text` helper), tested offline.
- The repository is public: no absolute paths from this machine, no names, no keys in any file, ai-docs included.
- Never index or walk AppData. Kill processes only by PID. Eval runs write to the real cache until step 1 lands:
  move `~/.historywright/cache` aside before an action case and put it back after.

## When to stop and ask

- Before the first release tag (v0.1.0) and any directory submission: Mark's go-ahead.
- Before signing up for or paying for any source, installing a large dependency, or requesting a key for anyone.

Decide small design rulings yourself, record each in `ai-docs/decisions/`, and flag it in one line.

## Last paragraph (keep it in every rewrite)

At each milestone, and before you finish, write what you learned to the repo's `ai-docs/`: the log, a HANDOFF of 50 lines at most, and decisions and research notes. Then rewrite this file, `ai-docs/next-session-prompt.md`, as the prompt for the next fresh session: what to read first, the next step and its limits, the rules, and when to stop. End the new prompt with this same paragraph, and paste it in your final message.
