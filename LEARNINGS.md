# Learnings: historywright

Procedural lessons for [README.md](README.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first, by meaning (`evergreen.py search "<the lesson>" --kinds learnings` finds near-duplicates in every registered unit): add / update / retire / none. Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

### L-004 · 2026-10-17 · Some servers refuse a User-Agent that names python-urllib
- Trigger: `hw.py probe` got 403 from the OpenHistoricalMap Overpass status page while the registry builder's curl got 200; the only difference was hw.py's agent ending in "python-urllib". SEC EDGAR, the other way round, refuses library-style agents and wants "name email".
- Hypothesis: bot filters match library names in the agent string; an agent that names the tool, its repository and a contact passes.
- Rule: the agent is `historywright/<version> (<repo>; <contact>)` with no library name; a registry entry with `"ua": "plain"` gets `historywright <contact>` (SEC).
- Evidence: the probe on 2026-10-17: ohm 403, then ok after the change; `hw.py src edgar` answers with the plain agent.
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-17

### L-003 · 2026-10-17 · British Old Style dates before 1752 need the January-start year
- Trigger: the method reference first gave George Washington's birth as "11 February 1731 O.S." and fed 1731 to the converter, which would give 22 February 1731, a year early.
- Hypothesis: before 1752 the English legal year began on 25 March, so a date between 1 January and 24 March carries the previous year's number; modern conversion needs the January-start year.
- Rule: hw.py reads every year as starting 1 January; for a British (or colonial) date in January to 24 March before 1752, pass the next year and let `--country GB` print the dual year (1731/32).
- Evidence: `hw.py cal date "1732-02-11 O.S." --country GB` gives 22 February 1732 and dual year 1731/32; test_os_ns_and_dual_year.
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-17

### L-002 · 2026-10-17 · Print UTF-8 explicitly: Windows consoles default to cp1252
- Trigger: printing DILA era names (康熙) from Python on Windows raised UnicodeEncodeError ('charmap' codec).
- Hypothesis: Python's stdout on a Windows console uses the ANSI code page unless PYTHONIOENCODING or reconfigure says otherwise; history output is full of CJK, Greek and diacritics.
- Rule: hw.py calls `sys.stdout.reconfigure(encoding="utf-8")` before printing (`utf8_stdout`); ad hoc scripts set PYTHONIOENCODING=utf-8.
- Evidence: the 2026-10-17 build session; every hw.py command prints CJK on Windows since.
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-17

### L-001 · 2026-10-17 · Python 3.13+ refuses some archive certificates that curl accepts
- Trigger: `hw.py cal setup` could not download DILA's zip: "CERTIFICATE_VERIFY_FAILED ... Missing Subject Key Identifier", while curl fetched it.
- Hypothesis: Python 3.13 turned on X.509 strict verification by default; older academic hosts serve certificates without the key identifier extension.
- Rule: on that error only, retry once with `VERIFY_X509_STRICT` cleared (chain and hostname still checked), and keep a mirror of the same data (DILA's GitHub copy) as the fallback.
- Evidence: R-20261017-27; the second `hw.py cal setup --force` built the table from the zip.
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-17
