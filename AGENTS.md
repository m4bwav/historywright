# Agent rules for historywright

Rules for any AI agent (Claude Code, Copilot, Cursor, Codex, Gemini CLI) working in this repository. `CLAUDE.md`
imports this file and `.github/copilot-instructions.md` points here.

Read [README.md](README.md) first. The three skills live under [skills/](skills/); the hub is
`skills/historywright`, which also holds the CLI (`scripts/hw.py` with its modules `hw_net.py`, `hw_dates.py`,
`hw_sources.py`, `hw_check.py`, `hw_pdf.py`). The source registry and era outline are in
`skills/historywright-sources/references/`. The three skills share one evergreen unit at the repository root:
RESEARCH, CHANGELOG, LEARNINGS, TESTS, `evals/evals.json`, MAINTENANCE and `evergreen.json`.

## Rules

- Evergreen unit in pointer mode: before editing a skill, read `evergreen.json`. If `next_due` has passed or
  `contradiction` is set, say so and refresh after the task (the evergreen plugin's `evergreen-refresh`, otherwise
  MAINTENANCE.md); a refresh runs `hw.py probe` first. Every edit to a SKILL.md or its references gets a
  CHANGELOG entry with its reason (`R-`, `L-` or `T-` ids, or "user request"). Re-run `evals/evals.json`
  (evergreen-test) when a change alters what a skill triggers on, decides or does.
- Research beats recall. Endpoints, limits, licences and access move monthly. Never change a source's route,
  limit, licence or a gold answer from memory: cite the source in RESEARCH.md (an `R-` entry) and log the change.
- `hw.py` stays standard-library Python 3.9+, prints exactly one JSON object per command, fails soft (`ok: false`
  with `error`), and runs on Windows, macOS and Linux. Every new command or option gets a test in
  `tests/test_hw.py` that runs offline (record fixtures with `HW_RECORD=<dir>`, replay with `HW_FIXTURES`).
- Dates are computed by `hw_dates.py` with integer JDN arithmetic, never `datetime` (it stops at year 1).
- The registry (`registry.json`) passes `hw.py lint`. Paid sources are link-out only; keys are written as `{key}`,
  never as values.
- Skills stay under 200 lines, with a description of at most 700 characters (the Agent Skills spec allows 1,024)
  that says what the skill does and names the sibling that owns nearby requests.
- The skills never sign up, pay or request a key without the user's yes, and never invent an email address.
- Before committing, run from the repository root: `python tests/check_skills.py`, `python tests/test_hw.py` and
  `python scripts/budget.py`. CI runs them on three operating systems.
- This is a public repository. Nothing in it names a person other than the author credit and cited authors, a
  private project, a machine, an absolute path on someone's machine, or a credential. API keys live in
  `~/.historywright/config.json` and never enter the repository, its ai-docs, issues or logs;
  `tests/check_skills.py` fails on any key-like string of 40 or more characters outside `tests/fixtures/`.
- Versions: when a packaged file changes, bump `.claude-plugin/plugin.json` and the root CHANGELOG.md's release
  notes, and tag `vX.Y.Z`. The release workflow checks the tag against the manifest, runs the checks, zips the
  skills and publishes a GitHub release.
- Work on `main` through pull requests; delete merged branches.
- No AI attribution anywhere: no Co-Authored-By trailers and no "generated with" lines in commits, pull requests
  or files.

## everlast (session knowledge, load on demand)

- `ai-docs/INDEX.md` lists what past sessions learned here. At the start of a task, scan it and open only the
  entries that match; read `ai-docs/HANDOFF.md` when continuing unfinished work.
- Before finishing a task that hit a dead end, verified a non-obvious command or made a design choice, record it in
  `ai-docs/` and rewrite `HANDOFF.md` when work is left unfinished. Say "nothing to record" when that is true.
- Anything naming a person, an internal host or name, a credential, or an opinion about people goes to the owner's
  private notes, never here.
- Link documents with relative markdown links. Every markdown folder has an index that links its files. No
  wikilinks in the repository.
