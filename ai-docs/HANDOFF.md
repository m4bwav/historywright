# historywright handoff

Updated 2026-11-01 (leftovers session).

## State

- Public: https://github.com/m4bwav/historywright (main). Three skills, hw.py (six stdlib modules), 85-source
  registry, 46 offline tests, CI green on three systems with Python 3.9 and 3.14.
- Released: v0.1.0, v0.2.0 and **v0.3.0 on 2026-10-24** (pack fixes, loc-habs, Water path, `hw.py fetch`):
  https://github.com/m4bwav/historywright/releases/tag/v0.3.0. Unreleased: C-20261101-1 (Commons images only, notes).
- 0.2.0 = CHANGELOG C-20261018-5 to -10: project home, Roman and Hijri dates, Wayback collapse, PDF quotes,
  `place search --source ohm`, Seshat CC BY-SA, doi "only the year differs", South Asia era outline 185 BCE-320 CE.
- Wiki still at 0.2.0, not updated for 0.3.0 (wiki commit 9b024ba; live 12 pages, 0 failures). Procedure and verifier:
  [notes/2026-10-18-github-wiki.md](notes/2026-10-18-github-wiki.md); the verifier defaults to v0.2.0.
- Installed: historywright@mark-local (check the version with `claude plugin list`).
- Cache: two live answers in `~/.historywright/cache` (who ruled India in AD 26; what happened to India's records).
  Move them aside before eval runs.
- Keys stay in `~/.historywright/config.json` (OpenAlex, WHG). Never in the repository.
- Owner rulings: [decisions/2026-10-18-owner-rulings-live-calls-and-tag.md](decisions/2026-10-18-owner-rulings-live-calls-and-tag.md),
  [decisions/2026-10-18-step5-rulings.md](decisions/2026-10-18-step5-rulings.md).

## Waiting for Mark

- Any directory submission (on hold since 2026-10-17).
- A DPLA key (free, by email) if DPLA should become a search source; not requested.

## Next

1. Wiki to 0.3.0 (procedure in notes/2026-10-18-github-wiki.md; point the verifier at v0.3.0).
2. South Asia depth (L-005): the Deccan and Tamil answers for AD 26 went unverified because the SOAS and UW
   theses would not download. Find a readable scholarly source on Satavahana chronology and add it to the registry or eras.md.
   Done 2026-11-01: the 403 hosts (R-20261101-1: Gallica and QDL stay walled, DPLA needs a key, HathiTrust ok),
   two-column PDF note in cli.md, Commons filetype filter.
3. Optional: `evergreen.py worth --ab` on the 11 value cases for a fresh baseline after 0.2.0.
4. Evergreen refresh due 2026-11-16.
5. Gaps found on the sawmill pack (2026-10-23), not yet built, one line each:
   - Long-s OCR: `hw.py fetch --find` tries long-s spellings (0.3.0); `verify quote` itself still does not fold s/f.
   - IIIF: LoC, Gallica and many museums serve images through IIIF; `pack add-ref` could take a IIIF manifest or image service and pick a size.
   - Internet Archive plates: book plates (Evans 1795 Plates XI-XIV) have no per-plate URL; add a route from an IA item and page number to a page image for `add-ref`.
   - EDTF intervals: period ranges such as 1790/1840 and open ends need checks and examples in entities.json and timeline.json.
   - Drawing-measured claims: values read off a measured drawing (sheet N, scaled) have no quote to verify; sources.json needs a claim kind for them (locator plus "measured from sheet").

## Read first

1. [next-session-prompt.md](next-session-prompt.md).
2. [log.md](log.md) (the 2026-10-18 entries) and the decisions folder.
3. [../AGENTS.md](../AGENTS.md) for the repository rules, [../README.md](../README.md) for the overview.
