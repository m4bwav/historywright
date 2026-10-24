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

## 2026-10-18 · Step 3: PRs merged, evals recorded, wiki published, three hw.py bugs fixed

- PR #1 (the previous session's branch `docs/evals-banner`: banner, eval fixes, T-2 to T-5) merged after CI. Added on the way: `tests/check_skills.py` skips the git-ignored `evals/cases/results/`, whose runner output holds local paths (28 false failures locally, none in CI).
- action-cache-entry A/B (T-20261018-1): with the skill 3/3, without 0/3, $2.14. The real cache was empty; the eval's entry moved to `~/.historywright/cache-from-evals-2026-10-18/`. Measured baselines filled into all 11 value cases; `evergreen.py tested . --passed 19 --failed 0`. PR #2.
- Wiki: Mark had saved the first page (`ls-remote` showed `master`). wikiwright wrote 12 pages verified against main at 29bc397 on Windows and WSL Ubuntu; wiki commit 5f89b34, `live` 12 pages 0 failures. Details, the update procedure and the doc inaccuracies: [notes/2026-10-18-github-wiki.md](notes/2026-10-18-github-wiki.md).
- Bugs found while writing it, fixed before pinning: `HW_RECORD` wrote key values into fixture patterns (PR #3, `record_pattern`); `cal date` misread `709 AUC`, `1300 AH`, `AH 1300` (days of 1882), `1 Muharram 1 AH` and Roman day counts with no warning (PR #4; 34 tests). CHANGELOG C-20261018-1 and -2.
- Rulings: [decisions/2026-10-18-session-rulings.md](decisions/2026-10-18-session-rulings.md). The live-API verification departs from wikiwright's L-122; recorded there as L-160 `live-public-sources` (wikiwright PR #20, merged), waiting for Mark.
- Doc errors the wiki found, fixed in PR #5 (C-20261018-3): README, plugin.json and the sources skill said "about 60 sources" (85 is right); the README presented its Caesar summary as literal output; cli.md missed the exit 2 case and seven options.
- Not done: Step 2 of the kickoff (eval cache isolation, `worth --probe`, trim) and Step 3 (open items). Next prompt rewritten.
## [2026-10-18] index | rebuilt (8 entries)

## 2026-10-18 · Step 4 session: owner rulings, paces, v0.1.0 released

- Mark's rulings ([decisions/2026-10-18-owner-rulings-live-calls-and-tag.md](decisions/2026-10-18-owner-rulings-live-calls-and-tag.md)): the wiki verifier may keep calling keyless public APIs live "if this doesn't break terms or will result in them banning us"; the v0.1.0 tag, yes.
- Checked the condition against the recorded limits. Wikimedia's 0.3 s pace was exactly its 200/min, Crossref's 0.1 s was double the public pool's 5/s (the verifier sends no mailto), OpenAlex keyless sat at its 10/s cap, and the Wayback availability API answered 429 on every verifier run at 0.5 s. PR #7 set 0.35 s, 0.2 s, 0.15 s and 4 s (R-20261018-1, C-20261018-4); merged after CI.
- wikiwright PR #21: L-160 `live-public-sources` adopted with the owner's condition (check each source's limit and User-Agent rule; slow any host that answered 429); merged.
- Tagged v0.1.0 on main at 6d06bb0; the release workflow passed and published historywright-0.1.0.zip (94,510 bytes): https://github.com/m4bwav/historywright/releases/tag/v0.1.0
- Step 1, project-scoped home (PR #9, C-20261018-5): `HW_HOME`, else `./.historywright` when it exists, else `~/.historywright`; keys, the DILA table and the pace file stay in the user home. The first A/B (T-20261018-2, with 7/9) showed agents `cd` into the skill folder, so the run folder's fixture was never seen and the real cache got an entry (moved aside); SKILL.md now says to run hw.py by full path from the working folder and `doctor` warns (`cwd_in_skill_folder`). Re-run T-20261018-3: with 9/9, without 1/9, real cache stayed empty.
- Step 2, trim: `worth --probe` named 0 of 22 anchors without the skill, so nothing was trimmed (decisions/2026-10-18-step4-rulings.md). The TRIM verdict is cost (2.77x).
- Step 3 (PR #10, C-20261018-6, R-20261018-2): `cal date` reads Kalends/Nones/Ides (inclusive, Julian) and Hijri month names, labels AH dates in AH, writes circa as EDTF `~`; `src wayback` uses `collapse=digest` (live test: six identical 1996 captures became six different ones). 38 offline tests.
- Wiki: re-run against v0.1.0 on Windows and WSL (3 expected changes; the Wayback check now answers at the 4 s pace, so `likely_hallucinated` shows live); release row, zip install and an unreleased list added; wiki commit 17a9717, `live` 12 pages, 0 failures. The verifier now defaults to the v0.1.0 commit.
- Snag: the Bash tool's hook refuses heredocs with doubled backslashes; regex-heavy edits went through the Edit tool.

## 2026-10-18 · Step 5 session: reinstall, PDF quotes, OHM places, Seshat licence, two evergreen issues

- Asked Mark about a 0.2.0 tag in the first message; no answer this session, so no tag.
- Reinstalled historywright@mark-local from main (twice: at the start and after the merges; the version is still 0.1.0, so `uninstall` then `install`, since `update` sees no new version). `doctor` from a project folder: `home_from: project`, no todo, `pdftotext: true`.
- PR #12 (C-20261018-7): quote checks read PDFs. New `hw_pdf.py` (pdftotext when on PATH, else a stdlib reader for Flate, object streams, ToUnicode). Unreadable PDFs answer `found: null`, and for PDF text a 20+ letter quote may match with spacing ignored (drop caps). Live trial on arXiv, govinfo and PLOS PDFs: [notes/2026-10-18-pdf-quotes.md](notes/2026-10-18-pdf-quotes.md).
- PR #13 (C-20261018-8, R-20261018-3): `place search --source ohm`. OHM publishes no API limit, so the general Overpass rules apply: exact name matches, one attempt, a 5 s pace, and a 30 s wait after a 429. Dates are astronomical years, and a negative `--year` means BC. Live: Kingdom of Prussia 1800, Roman Republic 44 BC.
- PR #14 (C-20261018-9, R-20261018-4): Seshat's current terms are CC BY-SA 4.0 with commercial use allowed (the registry said BY-NC-SA). The WHG docs were re-read and the limits are unchanged.
- polywright PR #22 (merged): polywright-references starts from a pack's `refs/index.json` (object date, nc flag, anachronism.md).
- evergreen issues: m4bwav/evergreen-protocol#28 (approval refusals are graded rather than left out as environment faults), #29 (`skill_fired` counts only Skill calls, so a with arm that runs the plugin's script gets "never fired").
- Wiki: Versions-and-Upgrading lists the three new unreleased changes (wiki commit baff65f). The other pages wait for the release run.
- Rulings: [decisions/2026-10-18-step5-rulings.md](decisions/2026-10-18-step5-rulings.md) (1 to 5).
- Snag: the Bash hook refused a heredoc holding regex backslashes; the fixture builder went into a scratch .py file instead.

## 2026-10-18 · Step 6 session: two live questions, 0.2.0 released

- Mark asked "who ruled India exactly 2k years ago?" and said to release after recording improvements (the go-ahead for 0.2.0).
- Answer (AD 26, cached in `~/.historywright/cache`): no single ruler. North-west: Gondophares, year 6 of his reign if the Takht-i-Bahi era (year 103 = his year 26) is the Vikrama era (Cribb 2017); on Falk and Bennett's Azes era start of 47/46 BC (Acta Orientalia 70, 2009) he took the throne c. AD 32, after AD 26. Kujula Kadphises later (c. AD 50-90, Cribb). The Deccan (Satavahanas) and the south were not verified in this run: the SOAS and UW theses would not download.
- Follow-up question: what happened to India's records? Read Stein's Rajatarangini introduction (1900: Kalhana's eleven earlier chronicles are lost, and none like it survive elsewhere in India), Prinsep's 1837 Sanchi note in JASB (the pillar script had been "the wonder of the learned" until he read it), and Raverty's Tabakat-i-Nasiri (the Bihar fortress that "was a college", with its books). Cached.
- Improvements (PR #16, C-20261018-10, L-004, L-005): `match_record` says "only the year differs" when title and author match (Crossref gives 1970 for Falk and Bennett 2009); eras.md South Asia covers 185 BCE to 320 CE and warns that the eras are disputed. 46 offline tests.
- Released 0.2.0: plugin.json and VERSION bumped in PR #16, merged after six green CI jobs, tag v0.2.0 at f890f1c, release workflow green, `historywright-0.2.0.zip`: https://github.com/m4bwav/historywright/releases/tag/v0.2.0. historywright@mark-local reinstalled.
- Snag: the first `git tag -a` push was refused with GH007 because an annotated tag carries the tagger's email. Re-tagged with `-c user.email=<no-reply>`.
- Snag: brill.com `oa_url` downloads return an AWS WAF human-verification page (L-004).
- Wiki: the verifier was re-run on Windows and WSL against f890f1c. The 9 changed sections are all expected (the released features). Pages updated to 0.2.0 by a subagent (wiki commit 9b024ba): outputs 55 checked, 0 missing; check 0 errors; live 12 pages, 0 failures. Four blocks were run by hand and marked skip (two refusals, one OHM call, one doi year-only example). The PDF paragraph is written from the code and tests; no PDF quote was run for it. The saved verifier outputs and the default commit now point at v0.2.0.
- Vault: the `user/ENVIRONMENTS.md` line about annotated tags is written but not committed. The vault's `.git/index.lock` (18:49) belonged to another process, and it was left alone.

## 2026-10-21 · Art sources from artwright; AIC header fix

- Applied artwright's reviewed proposal (its ruling R6: art fact questions route through this registry): ten link-out entries (getty-provenance, museo-egizio, artnet-pdb, artprice, mutualart, invaluable, liveauctioneers, sothebys-results, christies-results, art-sales-index), the registry now holds 95 sources.
- `artic` was broken: the API answers 403 (Cloudflare) without an `AIC-User-Agent` header. The search block now sends one (access `ua-required`), and `hw.py probe` sends a source's search headers, with an offline test. Live `hw.py src artic helmet` returned 10 results after the fix.
- Research R-20261021-1, change C-20261021-1 (unreleased). Not in this PR: Interpol, Art Loss Register, Lost Art, Proveana, IFAR and the Art Basel/UBS report (the proposal's "left out" list; each needs one direct request first); the optional `met` note on artistPrefix.

## 2026-10-23 · Pack fixes from the sawmill pack

- A water-powered sash sawmill pack (1790-1840) for 3D work showed seven gaps; built in branch pack-mechanism-fixes: the NC licence regex anchored (L-007), add-ref refuses NC images in commercial packs (L-008), validate-pack fails on unedited templates (L-009) and no longer crashes on a fresh pack, add-ref keeps the accession tail and never overwrites, `src loc-habs` (R-20261023-1, checked live), and the Mechanism section with `pack init --mechanism` (L-010, example in skills/historywright-pack/references/mechanism-example.md). Step 2 of the pack skill now says to read pages through `verify quote` from the start.
- Version 0.3.0 in plugin.json and hw_net.VERSION (C-20261023-1 to -3); not tagged.
- Learning ids start at L-007: another session's uncommitted edit on main adds L-006.
- Gaps left for later are listed in HANDOFF.md, Next 5.
