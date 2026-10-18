# historywright handoff

Updated 2026-10-17 (end of the Step 2 build session).

## State

- Built and public: https://github.com/m4bwav/historywright (main). Three skills, hw.py (five stdlib modules),
  an 85-source registry, the era outline, the pack contract, 31 offline tests, CI green on three operating
  systems. Installed locally as historywright@mark-local 0.1.0. Not tagged or released.
- Evergreen: one plugin-level unit at the repository root (tier moderate, next due 2026-11-16), registered in the
  catalog. Test results: [../TESTS.md](../TESTS.md).
- ai-docs registered with everlast (mode repo, sync push). The owner's key-setup record is in the vault's private
  sidecar (`projects/historywright/private/keys-setup.md`).
- Keys stay in `~/.historywright/config.json` (OpenAlex, WHG). Never in the repository; `tests/check_skills.py`
  fails on key-like strings.

## Waiting for Mark

- The wiki: GitHub creates the wiki repository only when its first page is saved in the browser. Then run
  wikiwright on the repository.
- The v0.1.0 tag and release (the release workflow is ready), and any directory submission.

## Next

1. Wiki (after Mark's click): wikiwright.
2. Action cases under `claude plugin eval` in WSL2, so the cache case is graded on the file in `$HW_HOME`
   (on native Windows the A/B grades it on the `cache put` call).
3. Tune any value case the A/B left failing (TESTS.md lists them).
4. Open items: quote checks on PDFs (OpenAlex often links only PDFs), OHM queries in `hw.py place`, WHG v3 docs,
   the Seshat licence page, polywright-references reading `refs/index.json` notes.

## Read first

1. [next-session-prompt.md](next-session-prompt.md).
2. [decisions/2026-10-17-step2-build.md](decisions/2026-10-17-step2-build.md) and [log.md](log.md).
3. [../AGENTS.md](../AGENTS.md) for the repository rules, [../README.md](../README.md) for the overview.
