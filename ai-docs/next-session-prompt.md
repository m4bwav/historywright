# Kickoff: historywright open items (after 0.4.0)

Rewritten 2026-11-01. Paste this into a fresh session started in the folder that holds this repository (the
historywright clone). If the clone's main is behind or dirty, work in a git worktree from `origin/main`.

## Load state

1. `ai-docs/HANDOFF.md` (state and the Next list), then `ai-docs/log.md` (newest entries).
2. `AGENTS.md`, `TESTS.md`, `LEARNINGS.md`.
3. The owner's rules: the vault user PROFILE (`everlast.py vault where` prints the vault), section "Code and repos".

## Waiting on Mark

- Directory submissions (on hold). A DPLA key (not requested; ask first).

## Order of work

Take HANDOFF's Next list top to bottom: South Asia depth (a readable scholarly source on Satavahana chronology),
then the sawmill-pack gaps (one PR per gap, each with a test), the optional A/B, and the evergreen refresh when due
(2026-11-16). Tag and release yourself once the version is bumped in a PR and CI passes; before tagging, check every
CHANGELOG entry in the range is in the tag commit (L-013). After a release, bring the wiki to it
(notes/2026-10-18-github-wiki.md).

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

- Before any directory submission or registry publishing: Mark's go-ahead. Tags and GitHub releases do not need it.
- Before signing up for or paying for any source, installing a large dependency, or requesting a key for anyone.
- Before any new live source or a faster pace: read that source's published terms and limits first (Mark's
  condition on live calls), and slow any host that answers 429.

Decide small design rulings yourself, record each in `ai-docs/decisions/`, and flag it in one line.

## Last paragraph (keep it in every rewrite)

At each milestone, and before you finish, write what you learned to the repo's `ai-docs/`: the log, a HANDOFF of 50 lines at most, and decisions and research notes. Then rewrite this file, `ai-docs/next-session-prompt.md`, as the prompt for the next fresh session: what to read first, the next step and its limits, the rules, and when to stop. End the new prompt with this same paragraph, and paste it in your final message.
