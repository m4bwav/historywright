# Kickoff: historywright Step 7 (open items after 0.2.0)

Written 2026-10-18 at the end of the Step 6 session. Paste this into a fresh session started in the folder that
holds this repository (the historywright clone).

## Where things stand

- v0.2.0 released 2026-10-18 (tag at f890f1c, zip on the release page); the wiki describes 0.2.0 (9b024ba).
- Step 6 answered two live questions (India in AD 26, and the fate of India's records). The lessons became PR #16:
  doi "only the year differs" and the South Asia era outline (L-004, L-005, C-20261018-10).
- Nothing waits for Mark except directory submissions (on hold).

## Read first

1. `ai-docs/HANDOFF.md`, then `ai-docs/log.md` (the 2026-10-18 entries).
2. `AGENTS.md`, `TESTS.md`, `LEARNINGS.md` (L-004, L-005 new).
3. The owner's rules: the vault user PROFILE (`everlast.py vault where` prints the vault), section "Code and repos".

## Next steps, in order

1. The 403s: test whether Gallica, DPLA, QDL and HathiTrust answer hw.py's own User-Agent (one request each,
   after reading each site's terms); record `R-` entries and update the registry. Note in cli.md that two-column
   PDFs read in stream order.
2. South Asia depth (L-005): find a readable scholarly source on Satavahana and early Tamil chronology; add it
   to the registry or eras.md and note what it settles.
3. Optional: `evergreen.py worth --ab` on the 11 value cases (move `~/.historywright/cache` entries aside first).
4. The next release only when Mark says; then the same procedure as 0.2.0 (bump plugin.json and VERSION in a PR,
   tag with the no-reply email, check the release workflow, reinstall, wiki procedure).

## Rules

- Commit and tag with `git -c user.email=156112+m4bwav@users.noreply.github.com` (an annotated tag with the global address is refused, GH007). No AI attribution anywhere.
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
