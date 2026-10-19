---
title: Step 4 small rulings - project home, no trim, date parsing choices
kind: decision
date: 2026-10-18
tags: [hw.py, evals, trim, dates]
summary: "project-scoped home keeps keys, DILA table and pace in the user home; the probe found nothing to trim so SKILL.md was not cut; Roman counts are inclusive and Julian; Hijri names map from common English spellings; circa adds EDTF ~"
---

# Step 4 small rulings (2026-10-18)

Decided in the session, flagged to the owner in one line each.

1. **Project home splits by kind of file.** `./.historywright/` (when it exists) holds the cache, fetch log, page
   store and probe results. Keys, the DILA table and the pace file stay in `~/.historywright` unless that folder
   has its own `config.json`. Why: an eval run must not see an earlier run's answers, but a second copy of the
   1.3 MB DILA download per project is waste, and a pace file per project would let two projects together exceed a
   source's limit (the owner's 2026-10-18 condition on live calls). Only the working directory is checked, not its
   parents, so the choice is predictable.
2. **No trim from the probe.** `evergreen.py worth skills/historywright --probe` (sonnet): without the skill the
   answer named 0 of 22 anchors. It knew the bare date (12 or 13 July 100 BC) and nothing the skill teaches (the
   102 BC dispute, full Wikidata statements, citations, hw.py). The kickoff says to trim only what the probe shows
   the model already knows, so SKILL.md is unchanged and the with-arm re-run was not needed. The earlier TRIM
   verdict came from cost (3.1x); the two redundant outcome cases (misattributed-quote, october-revolution, 3/3
   without the skill) stay as regression checks.
3. **Roman day counts** are counted inclusively and read in the Julian calendar; before 45 BC a count back from
   the Kalends carries a warning (Republican month lengths). English ("the day before the Ides of March") and
   abbreviated Latin ("a.d. III Id. Mar.", "pridie Kal. Apr.") are both read.
4. **Hijri month names** match common English spellings reduced to letters (Rabi' I, Rabi ul-Awwal, Dhu'l-Hijjah,
   Ramazan). A month name implies AH even without "AH". An AH year or month answers with its own days, labelled
   in AH, with the Western start beside it.
5. **Circa** (`c.`, `ca.`, `circa`, `about`, `approx.`) adds `~` to the EDTF (both ends of an interval) and a
   `qualifier` field; "uncertain" stays unsupported in parsing (EDTF `?` only through `edtf_for`).
