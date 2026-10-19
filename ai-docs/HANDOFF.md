# historywright handoff

Updated 2026-10-18 (end of the Step 4 session).

## State

- Public: https://github.com/m4bwav/historywright (main). Three skills, hw.py (five stdlib modules), 85-source
  registry, 38 offline tests, CI green on three systems with Python 3.9 and 3.14.
- Released: v0.1.0 on 2026-10-18 (tag at 6d06bb0), https://github.com/m4bwav/historywright/releases/tag/v0.1.0.
  Main is ahead: project-scoped home (PR #9), Roman day counts, Hijri months, AH labels, circa, Wayback collapse
  (PR #10). CHANGELOG "unreleased: C-20261018-5 onward".
- Wiki live, pages run against v0.1.0 (wiki commit 17a9717). Update procedure and verifier:
  [notes/2026-10-18-github-wiki.md](notes/2026-10-18-github-wiki.md).
- Evals: the three action cases with a project-home fixture, 9/9 with, 1/9 without (T-20261018-3). The probe
  found nothing to trim. TESTS.md has the record.
- Owner rulings 2026-10-18: live keyless calls allowed while no terms are broken and no ban risked (paces tightened,
  PR #7; wikiwright L-160 adopted); v0.1.0 yes.
  [decisions/2026-10-18-owner-rulings-live-calls-and-tag.md](decisions/2026-10-18-owner-rulings-live-calls-and-tag.md),
  small rulings in [decisions/2026-10-18-step4-rulings.md](decisions/2026-10-18-step4-rulings.md).
- Keys stay in `~/.historywright/config.json` (OpenAlex, WHG). Never in the repository.
- The installed copy (historywright@mark-local) has not been reinstalled since PR #9 and #10.

## Waiting for Mark

- A 0.2.0 tag for the unreleased changes on main (his go-ahead, as for 0.1.0).
- Any directory submission (on hold since 2026-10-17).

## Next

1. Reinstall historywright@mark-local from main.
2. Open items: quote checks on PDFs (OpenAlex often links only PDFs), OHM queries in `hw.py place`, WHG v3 docs,
   the Seshat licence page, polywright-references reading `refs/index.json` notes, the evergreen plugin issue
   (its A/B environment check could match "requires approval"; it also says "the skill never fired" for
   action-validate-pack, whose with runs pass on the hw.py trace).
3. Optional: `evergreen.py worth --ab` on all 11 value cases with the project home, for a full fresh baseline.
4. After any packaged change, and at each release: the wiki's update procedure, on Windows then WSL, one after
   the other (never at once: each has its own pace file).

## Read first

1. [next-session-prompt.md](next-session-prompt.md).
2. [log.md](log.md) (the 2026-10-18 entries) and the decisions folder.
3. [../AGENTS.md](../AGENTS.md) for the repository rules, [../README.md](../README.md) for the overview.
