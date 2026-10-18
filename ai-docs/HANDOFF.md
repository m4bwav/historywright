# historywright handoff

Updated 2026-10-18 (end of the Step 3 session).

## State

- Public: https://github.com/m4bwav/historywright (main). Three skills, hw.py (five stdlib modules), 85-source
  registry, 34 offline tests, CI green on three systems with Python 3.9 and 3.14. Not tagged or released (0.1.0).
- Wiki live: https://github.com/m4bwav/historywright/wiki, 12 pages verified against main at 29bc397 (wiki commit
  5f89b34). How it was made and how to update it: [notes/2026-10-18-github-wiki.md](notes/2026-10-18-github-wiki.md).
- Evals: every case in `evals/evals.json` has passed with the skill (19 of 19, recorded in evergreen.json);
  measured baselines are in each value case. Results: [../TESTS.md](../TESTS.md).
- Merged on 2026-10-18: PR #1 to #5 (banner and eval fixes; eval records; `HW_RECORD` key redaction; `cal date`
  misreadings of AUC, AH and Roman dates; doc fixes). Rulings:
  [decisions/2026-10-18-session-rulings.md](decisions/2026-10-18-session-rulings.md).
- The installed copy (historywright@mark-local 0.1.0) was reinstalled from main at the end of the session.
- Keys stay in `~/.historywright/config.json` (OpenAlex, WHG). Never in the repository.

## Waiting for Mark

- The v0.1.0 tag and release (the workflow is ready), and any directory submission.
- A ruling on wikiwright L-160 `live-public-sources`: the wiki verifier calls keyless public APIs live, which
  departs from wikiwright's L-122. If he refuses, re-verify against recorded fixtures labelled as recorded.

## Next

1. Eval cache isolation: a project-scoped home for eval runs (for example `./.historywright/` preferred when
   present, below `HW_HOME`), then re-run the three action cases; `evergreen.py worth skills/historywright --probe`
   for trim candidates (verdict TRIM), trim only what the probe shows the model knows, re-run the with arm.
2. Small hw.py follow-ups found by the wiki: `src wayback` repeats captures (try CDX `collapse=digest`, with an
   `R-` entry); `read_as` for an AH year shows the Western start year; `c.` is ignored rather than written as
   EDTF `~`; Kalends, Nones, Ides and Hijri month names are refused, not parsed (a feature, with tests).
3. Open items: quote checks on PDFs (OpenAlex often links only PDFs), OHM queries in `hw.py place`, WHG v3 docs,
   the Seshat licence page, polywright-references reading `refs/index.json` notes, the evergreen plugin issue
   (its A/B environment check could match "requires approval").
4. After any packaged change: the wiki's update procedure (the note above), on Windows and WSL.

## Read first

1. [next-session-prompt.md](next-session-prompt.md).
2. [log.md](log.md) (the 2026-10-18 entry) and the decisions folder.
3. [../AGENTS.md](../AGENTS.md) for the repository rules, [../README.md](../README.md) for the overview.
