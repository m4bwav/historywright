# historywright handoff

Updated 2026-11-02 (DPLA probe, 0.6.1 session).

## State

- Public: https://github.com/m4bwav/historywright (main). Three skills, hw.py (six stdlib modules), 85-source
  registry (96 sources), 64 offline tests, CI green on three systems with Python 3.9 and 3.14.
- Released: v0.1.0, v0.2.0, v0.3.0 (2026-10-24: pack fixes, loc-habs) and **v0.4.0 on 2026-11-01** (`hw.py fetch`,
  Water path, Commons filter; the v0.3.0 tag had missed PR #21, L-013): https://github.com/m4bwav/historywright/releases/tag/v0.4.0.
  **v0.5.0 on 2026-11-01** (long-s quotes, EDTF interval checks, measured claims, IIIF/IA add-ref; C-20261101-3 to -8):
  https://github.com/m4bwav/historywright/releases/tag/v0.5.0.
  **v0.5.1 on 2026-11-01** (IA `stream/` text URLs read from `download/`, C-20261101-9 and -10):
  https://github.com/m4bwav/historywright/releases/tag/v0.5.1.
  **v0.6.0 on 2026-11-02** (`hw.py src dpla`, keyed; C-20261102-1 and -2):
  https://github.com/m4bwav/historywright/releases/tag/v0.6.0.
  **v0.6.1 on 2026-11-02** (DPLA probe; C-20261102-3 and -4): https://github.com/m4bwav/historywright/releases/tag/v0.6.1.
  Installed copy updated to 0.6.1.
- 0.2.0 = CHANGELOG C-20261018-5 to -10: project home, Roman and Hijri dates, Wayback collapse, PDF quotes,
  `place search --source ohm`, Seshat CC BY-SA, doi "only the year differs", South Asia era outline 185 BCE-320 CE.
- Wiki at 0.6.1 (wiki commit 3e900dc; live 12 pages, 0 failures). Procedure and verifier:
  [notes/2026-10-18-github-wiki.md](notes/2026-10-18-github-wiki.md); the verifier defaults to v0.6.1 (078613e). No dated
  skip markers left: LacusCurtius answered again on 2026-11-02. `src dpla` on Commands is a keyed hand run (skip marker).
- Installed: historywright@mark-local (check the version with `claude plugin list`).
- Cache: four live answers in `~/.historywright/cache` (two India, crusader Jerusalem 2026-10-23, Deir el-Medina 2026-10-25).
  Move them aside before eval runs.
- Keys stay in `~/.historywright/config.json` (OpenAlex, WHG, DPLA; DPLA saved as a bare string, which `get_key` now reads). Never in the repository.
- Owner rulings: [decisions/2026-10-18-owner-rulings-live-calls-and-tag.md](decisions/2026-10-18-owner-rulings-live-calls-and-tag.md),
  [decisions/2026-10-18-step5-rulings.md](decisions/2026-10-18-step5-rulings.md).

## Waiting for Mark

- Any directory submission (on hold since 2026-10-17).
- None for DPLA: key saved 2026-11-01 (`keys.dpla`).

## Next

1. Optional: `evergreen.py worth --ab` on the 11 value cases (last after 0.2.0; paid).
2. Evergreen refresh due 2026-11-16.
3. No small follow-ups left; `hw.py lint` has no warnings. Nothing unreleased on main. Ideas if time allows: a
   search block for DDB (needs a My DDB key, Mark's call) or Semantic Scholar (keyless pool answers 429).

## Read first

1. [next-session-prompt.md](next-session-prompt.md).
2. [log.md](log.md) (the 2026-10-18 entries) and the decisions folder.
3. [../AGENTS.md](../AGENTS.md) for the repository rules, [../README.md](../README.md) for the overview.
