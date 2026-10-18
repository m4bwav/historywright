---
kind: decision
status: active
date: 2026-10-18
title: Step 3 session rulings (wiki, eval records, date parser)
tags: [wiki, evals, hw.py, dates]
---

# Step 3 session rulings (2026-10-18)

Small rulings made during the Step 3 session, per the kickoff's "decide small rulings yourself, record each, flag it". Each can be reversed.

1. **Refuse, don't parse, Roman day counts and Islamic month names.** `cal date` now rejects "Ides of March 44 BC" and "1 Muharram 1 AH" with the form to use, rather than gaining a Kalends/Nones/Ides converter and a Hijri month table. Refusing removes the silent misreading at once; parsing them is a feature for later, with tests. Other unread words are kept as before but listed in `notes` ("ignored words: c.").
2. **A year-only AH date covers its own days.** `AH 1300` gives JDN 2408762 to 2409116 and EDTF `1882-11-12/1883-11-01`, not the days of 1882. `read_as` still shows the Western year the AH year begins in, as before, so the change does not alter that field's meaning.
3. **The wiki documents main at a pinned commit.** There is no release, so the verifier downloads the repository zip at 29bc397 from codeload.github.com, as polywright's downloads its release zip. After the first release, switch it to the release zip.
4. **The wiki verifier calls keyless public APIs live.** The pages show what Wikidata, Wikipedia, Pleiades, CHGIS, OpenAlex, Crossref and the Wayback Machine returned on 2026-10-18, from a fresh home folder with no keys and no contact. This departs from wikiwright's L-122, so wikiwright records it as L-160 `live-public-sources`, which waits for the owner's ruling.
5. **Measured baselines go into `evals/evals.json`.** Each value case's `baseline` now reads "without the skill N of 3 passed (T-..., date, sonnet)", from T-20261017-4, -5 and T-20261018-1, so `evergreen.py worth` stops reading them as never run.
6. **Eval runs and the real cache.** For the action-cache-entry A/B the real `~/.historywright/cache` was moved aside (it was empty), and the one entry the eval wrote went to `~/.historywright/cache-from-evals-2026-10-18/`. The proper fix (a project-scoped home for eval runs) is still the next session's Step 2.
