# historywright handoff

Updated 2026-11-02 (v0.6.0 session).

## State

- Public: https://github.com/m4bwav/historywright (main). Three skills, hw.py (six stdlib modules), 85-source
  registry (96 sources), 63 offline tests, CI green on three systems with Python 3.9 and 3.14.
- Released: v0.1.0, v0.2.0, v0.3.0 (2026-10-24: pack fixes, loc-habs) and **v0.4.0 on 2026-11-01** (`hw.py fetch`,
  Water path, Commons filter; the v0.3.0 tag had missed PR #21, L-013): https://github.com/m4bwav/historywright/releases/tag/v0.4.0.
  **v0.5.0 on 2026-11-01** (long-s quotes, EDTF interval checks, measured claims, IIIF/IA add-ref; C-20261101-3 to -8):
  https://github.com/m4bwav/historywright/releases/tag/v0.5.0.
  **v0.5.1 on 2026-11-01** (IA `stream/` text URLs read from `download/`, C-20261101-9 and -10):
  https://github.com/m4bwav/historywright/releases/tag/v0.5.1.
  **v0.6.0 on 2026-11-02** (`hw.py src dpla`, keyed; C-20261102-1 and -2):
  https://github.com/m4bwav/historywright/releases/tag/v0.6.0. Installed copy updated to 0.6.0.
- 0.2.0 = CHANGELOG C-20261018-5 to -10: project home, Roman and Hijri dates, Wayback collapse, PDF quotes,
  `place search --source ohm`, Seshat CC BY-SA, doi "only the year differs", South Asia era outline 185 BCE-320 CE.
- Wiki at 0.5.1 (behind the 0.6.0 release) (wiki commit 366ce61; live 12 pages, 0 failures). Procedure and verifier:
  [notes/2026-10-18-github-wiki.md](notes/2026-10-18-github-wiki.md); the verifier defaults to v0.5.1 (1c55b31). Dated skip markers: two
  verify-quote outputs (LacusCurtius down, SSL); drop them when it answers. The Wayback marker was dropped later on
  2026-11-01 (wiki f9be70e).
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

1. Wiki to 0.6.0: add `src dpla` and the DPLA key row, re-run the verifier on Windows and WSL
   ([notes/2026-10-18-github-wiki.md](notes/2026-10-18-github-wiki.md)), point its default at v0.6.0 (1288691).
2. Optional: `evergreen.py worth --ab` on the 11 value cases (last after 0.2.0; paid).
3. Evergreen refresh due 2026-11-16.
4. Small follow-up: drop the two LacusCurtius skip markers when the site answers (TLS failure as of 2026-11-01).
   Nothing unreleased on main.

## Read first

1. [next-session-prompt.md](next-session-prompt.md).
2. [log.md](log.md) (the 2026-10-18 entries) and the decisions folder.
3. [../AGENTS.md](../AGENTS.md) for the repository rules, [../README.md](../README.md) for the overview.
