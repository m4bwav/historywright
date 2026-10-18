# historywright log

Append-only, newest last.

## 2026-10-17 · Step 1: creation pass

- Checked the installed evergreen: 0.17.0 (evergreen@mark-local), the version the kickoff requires.
- Ran the evergreen creation pass as seven parallel `evergreen-researcher` passes in creation mode: subject A (structured facts, routing articles, places, periods, comparative data), subject B (primary corpora, national libraries and archives, institutions worldwide), subject C (archaeology, scholarship, museums, modern and business history), subject D (method, dating, disputes, gold answers), tooling, practice, testing.
- Saved the seven verbatim reports to `ai-docs/research/2026-10-17-creation-pass/` (extracted from the subagent transcripts with a small script, not retyped). Wrote the synthesis to `ai-docs/research/2026-10-17-creation-pass.md` and 24 `R-` entries to `RESEARCH.md`.
- Cost: searches 211 (11 refused) · fetches 245 · tool calls 477.
- Snag: the passes shared one WebSearch budget of about 200 a turn, and it ran out mid-pass. The tooling pass got only 4 searches and fell back on the MCP registry, skills.sh and GitHub APIs (73 fetches), which worked well. Next time, give each parallel researcher an explicit search cap (about 25 each for seven passes) and tell it to prefer direct API fetches. The open questions left by the budget are listed in RESEARCH.md.
- Gold answers corrected: Caesar is "12 or 13 July 100 BC"; the longest-ruling emperor answer adds Qianlong's de facto rule to 1799 (about 63 years) and the Zhao Tuo caveat. Microsoft is confirmed, but no official page prints 4 April.
- Small rulings recorded in [decisions/2026-10-17-step1-rulings.md](decisions/2026-10-17-step1-rulings.md).
- Stopped after Step 1 as the kickoff says; the summary and three forks went to Mark. Not a git repo yet; nothing published.

## 2026-10-17 · Mark's answers; keys set up

- Mark: keys yes if automatable or easy; CJK download as recommended; no paid sources. Recorded in [decisions/2026-10-17-forks-mark.md](decisions/2026-10-17-forks-mark.md).
- OpenAlex: `POST https://api.openalex.org/api-keys` with the owner's address returned 201 and a key, saved to `~/.historywright/config.json`. `GET /rate-limit` answers `403 key_not_activated` until Mark clicks the "Activate your OpenAlex API key" email (link valid to 2026-10-24). The email had not reached Gmail within a few minutes of the request.
- WHG: sign-in is ORCID-only (the login page says signing in creates the account and needs no academic affiliation), so no automation. Opened https://whgazetteer.org/accounts/login/?next=/profile/ in Mark's browser; the token comes from the Profile page after sign-in.
- DILA licence settled: CC BY-SA 3.0 Unported (COPYING.rst in DILA-edu/Authority-Databases). kltng/calendar_converter has no licence, so build the table from DILA's own 1.34 MB archive instead of using its prebuilt db.
- Wrote [notes/api-keys-setup.md](notes/api-keys-setup.md) for other users: every optional key, how to get it, which steps can be scripted.
- Later the same day: Mark activated the OpenAlex key (`/rate-limit` returned 200, $1 a day) and signed up for ORCID and WHG. His WHG token was saved to `~/.historywright/config.json` (permissions restricted to the owner's account) and tested against `/suggest/entity` (200 with the token, 401 without). Both keys are live. Neither is in any repo file.
## [2026-10-17] index | rebuilt (6 entries)

## 2026-10-17 · Step 2: build, repository, tests

- Built the plugin to synthesis §7 with the changes in [decisions/2026-10-17-step2-build.md](decisions/2026-10-17-step2-build.md): three skills (`historywright`, `-sources`, `-pack`), hw.py as five stdlib modules (wd, wp, place, oa, doi, src, cal, cache, verify, pack, validate-pack, probe, keys, lint, doctor), one plugin-level evergreen unit (`evergreen.py init`, RESEARCH.md kept, registered in the catalog).
- Source registry: 85 sources (53 tier 1, 27 tier 2, 5 tier 3; 22 with a JSON search, 53 link-out), transcribed from the four subject reports by a subagent that live-tested every search and probe; note in [research/2026-10-17-registry-build.md](research/2026-10-17-registry-build.md). `hw.py probe`: 36 of 40 ok on the first run; OHM's 403 was the User-Agent's `python-urllib` suffix (removed, L-004), Getty's ASK probe answers XML (now a SELECT), two 429s were transient.
- Live checks: Caesar's four P569 statements decoded (disputed flag, 12-13 July range, 102 BC); Microsoft's "April 4, 1975" sentence maps to its three footnotes; DILA table built (117,428 months; 崇禎三年四月初三 = 14 May 1630; Kangxi era 18 February 1662 to 20 December 1722); WHG, Pleiades, CHGIS answer; a fabricated URL is labelled `likely_hallucinated`; a real DOI with the wrong title is flagged. R-20261017-25 to -27 and L-001 to L-004 record what the build learned (strict X.509 on DILA's certificate, UTF-8 output on Windows, Old Style year starts, User-Agent filters).
- Fixed during the build: CRLF writes on Windows (a `write_text` helper with `newline="\n"`), charset detection from `<meta>` (LacusCurtius), OpenAlex key moved from the URL to a Bearer header and key parameters redacted from the fetch log (the earlier test lines in the local log were scrubbed).
- End-to-end pack: [notes/2026-10-17-e2e-legionary.md](notes/2026-10-17-e2e-legionary.md); `verify sources` 8 of 8 quotes, `validate-pack` ok, polywright's `pw.py manifest --validate` ok.
- Repository: public https://github.com/m4bwav/historywright (first commit pushed to main), topics, private vulnerability reporting on, CI green on Linux, macOS and Windows with Python 3.9 and 3.14. Installed as historywright@mark-local 0.1.0. ai-docs registered with everlast (mode repo, sync push); the owner's key-setup record moved to the private sidecar.
- Evals: triggers 15 of 15 runs, decoys 9 of 9 quiet (`claude plugin eval`, $2.05). The with/without A/B on the 11 value cases ran with `evergreen.py worth --ab --model sonnet`; results in TESTS.md.
