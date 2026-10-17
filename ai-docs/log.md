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
