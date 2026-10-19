# Kickoff: historywright Step 5 (reinstall, open items, 0.2.0 when Mark says)

Written 2026-10-18 at the end of the Step 4 session. Paste this into a fresh session started in the folder that
holds this repository (the historywright clone).

## Where things stand

- v0.1.0 released 2026-10-18 (tag at 6d06bb0). Main is ahead with PR #9 (project-scoped `.historywright/` home)
  and PR #10 (Kalends/Nones/Ides, Hijri month names, AH labels, circa as EDTF `~`, Wayback `collapse=digest`).
- The wiki describes 0.1.0 (wiki commit 17a9717) and lists the unreleased changes on Versions-and-Upgrading.
- Mark's rulings: live keyless API calls are fine while they break no source's terms and risk no ban; paces sit
  under each documented public limit (R-20261018-1). wikiwright L-160 is adopted with that condition.
- Evals: action cases 9/9 with the skill using a project-home fixture (T-20261018-3). The probe found nothing to
  trim.

## Read first

1. `ai-docs/HANDOFF.md`, then `ai-docs/log.md` (the 2026-10-18 entries).
2. `ai-docs/decisions/2026-10-18-owner-rulings-live-calls-and-tag.md` and `2026-10-18-step4-rulings.md`.
3. `AGENTS.md`, `TESTS.md`, `LEARNINGS.md`.
4. The owner's rules: the vault user PROFILE (`everlast.py vault where` prints the vault), section "Code and repos".

## Next steps, in order

0. **Ask Mark in your first message, then carry on:** is it time for a 0.2.0 tag for the unreleased changes
   (CHANGELOG C-20261018-5 and -6)? If yes: bump `.claude-plugin/plugin.json` and `VERSION` in hw_net.py in a PR,
   merge, tag `v0.2.0`, check the release workflow, then run the wiki update procedure against the new tag (the
   note), adding a Releases row and emptying "On main, not yet released".
1. Reinstall historywright@mark-local from main and run `hw.py doctor` from a project folder.
2. Open items (HANDOFF "Next" 2), each with a test where it changes hw.py and an `R-` entry where it rests on a
   changed endpoint, limit or licence.
3. Before any new live source or a faster pace: check that source's published terms and limits first (Mark's
   condition on live calls). Slow any host that answers 429.

## Rules

- Commit with `git -c user.email=156112+m4bwav@users.noreply.github.com`. No AI attribution anywhere.
- Every change goes through a pull request; merge it yourself once CI passes (this repo uses merge commits),
  unless it changes the release workflow or a public API.
- Run `python tests/check_skills.py`, `python tests/test_hw.py` and `python scripts/budget.py` before every
  commit, and stage files by name, not with `git add -A`.
- Every SKILL.md edit gets a CHANGELOG entry and keeps the description under 700 characters.
- hw.py stays standard library, one JSON object per command, LF endings (`write_text` helper), tested offline.
- The repository is public: no absolute paths from this machine, no names, no keys in any file, ai-docs included.
- The Bash tool's hook refuses heredocs holding a doubled backslash: make regex edits with the Edit tool.
- Eval runs: the action cases carry the `project-home` fixture; still check `~/.historywright/cache` is empty
  after a run, and move any entry aside.
- Never index or walk AppData. Kill processes only by PID.

## When to stop and ask

- Before any release tag and any directory submission: Mark's go-ahead.
- Before signing up for or paying for any source, installing a large dependency, or requesting a key for anyone.

Decide small design rulings yourself, record each in `ai-docs/decisions/`, and flag it in one line.

## Last paragraph (keep it in every rewrite)

At each milestone, and before you finish, write what you learned to the repo's `ai-docs/`: the log, a HANDOFF of 50 lines at most, and decisions and research notes. Then rewrite this file, `ai-docs/next-session-prompt.md`, as the prompt for the next fresh session: what to read first, the next step and its limits, the rules, and when to stop. End the new prompt with this same paragraph, and paste it in your final message.
