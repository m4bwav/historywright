# Kickoff: historywright Step 6 (0.2.0 when Mark says, then the remaining open items)

Written 2026-10-18 at the end of the Step 5 session. Paste this into a fresh session started in the folder that
holds this repository (the historywright clone).

## Where things stand

- v0.1.0 released 2026-10-18 (tag at 6d06bb0). Main is ahead with CHANGELOG C-20261018-5 to -9: project home,
  Roman and Hijri dates, Wayback collapse, PDF quote checks (`hw_pdf.py`), `place search --source ohm`, Seshat
  as CC BY-SA 4.0.
- Step 5 merged PRs #12, #13 and #14 here and polywright PR #22, and filed evergreen-protocol #28 and #29.
  Rulings 1 to 5 are in `ai-docs/decisions/2026-10-18-step5-rulings.md`.
- The wiki describes 0.1.0; Versions-and-Upgrading lists every unreleased change.
- Mark was asked about a 0.2.0 tag on 2026-10-18 and has not answered.

## Read first

1. `ai-docs/HANDOFF.md`, then `ai-docs/log.md` (the 2026-10-18 entries).
2. `ai-docs/decisions/2026-10-18-step5-rulings.md` and `2026-10-18-owner-rulings-live-calls-and-tag.md`.
3. `AGENTS.md`, `TESTS.md`, `LEARNINGS.md`.
4. The owner's rules: the vault user PROFILE (`everlast.py vault where` prints the vault), section "Code and repos".

## Next steps, in order

0. **Ask Mark in your first message, then carry on:** is it time for a 0.2.0 tag (C-20261018-5 to -9)? If yes:
   bump `.claude-plugin/plugin.json` and `VERSION` in hw_net.py in a PR, merge, tag `v0.2.0`, check the release
   workflow, reinstall historywright@mark-local, then run the wiki update procedure against the tag
   (`ai-docs/notes/2026-10-18-github-wiki.md`): Commands gains `--source ohm`, How-Claims-Are-Checked gains PDFs,
   add a Releases row and empty "On main, not yet released".
1. Open items (HANDOFF "Next" 2): test whether the Gallica, DPLA, QDL and HathiTrust 403s clear with hw.py's
   own User-Agent (one request each, after reading each site's terms); record results as `R-` entries and update
   the registry. Two-column PDFs: consider a pdftotext-only note in cli.md rather than a column-aware reader.
2. Optional: `evergreen.py worth --ab` on all 11 value cases with the project-home fixture.

## Rules

- Commit with `git -c user.email=156112+m4bwav@users.noreply.github.com`. No AI attribution anywhere.
- Every change goes through a pull request; merge it yourself once CI passes (this repo uses merge commits),
  unless it changes the release workflow or a public API.
- Run `python tests/check_skills.py`, `python tests/test_hw.py` and `python scripts/budget.py` before every
  commit, and stage files by name, not with `git add -A`.
- Every SKILL.md edit gets a CHANGELOG entry and keeps the description under 700 characters.
- hw.py stays standard library (pdftotext is optional and found on PATH), one JSON object per command, LF
  endings (`write_text` helper), tested offline.
- The repository is public: no absolute paths from this machine, no names, no keys in any file, ai-docs included.
- The Bash tool's hook refuses heredocs holding a doubled backslash: put such scripts in a scratch .py file, or
  use the Edit tool.
- `claude plugin update` sees no change while the version stays 0.1.0: reinstall with `uninstall` then `install`.
- Other plugins' clones (polywright) may hold another session's uncommitted work: use a git worktree from
  `origin/main` for any change there.
- Eval runs: the action cases carry the `project-home` fixture; check `~/.historywright/cache` is empty after a
  run, and move any entry aside.
- Never index or walk AppData. Kill processes only by PID.

## When to stop and ask

- Before any release tag and any directory submission: Mark's go-ahead.
- Before signing up for or paying for any source, installing a large dependency, or requesting a key for anyone.
- Before any new live source or a faster pace: read that source's published terms and limits first (Mark's
  condition on live calls), and slow any host that answers 429.

Decide small design rulings yourself, record each in `ai-docs/decisions/`, and flag it in one line.

## Last paragraph (keep it in every rewrite)

At each milestone, and before you finish, write what you learned to the repo's `ai-docs/`: the log, a HANDOFF of 50 lines at most, and decisions and research notes. Then rewrite this file, `ai-docs/next-session-prompt.md`, as the prompt for the next fresh session: what to read first, the next step and its limits, the rules, and when to stop. End the new prompt with this same paragraph, and paste it in your final message.
