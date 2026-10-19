# historywright handoff

Updated 2026-10-18 (end of the Step 5 session).

## State

- Public: https://github.com/m4bwav/historywright (main). Three skills, hw.py (six stdlib modules, `hw_pdf.py`
  new), 85-source registry, 43 offline tests, CI green on three systems with Python 3.9 and 3.14.
- Released: v0.1.0 on 2026-10-18 (tag at 6d06bb0). Main is ahead with CHANGELOG C-20261018-5 to -9: project
  home, Roman and Hijri dates, Wayback collapse, PDF quote checks (PR #12), `place search --source ohm`
  (PR #13), Seshat as CC BY-SA 4.0 (PR #14).
- Wiki pages run against v0.1.0. Versions-and-Upgrading lists every unreleased change (wiki commit baff65f).
  Update procedure and verifier: [notes/2026-10-18-github-wiki.md](notes/2026-10-18-github-wiki.md).
- Installed: historywright@mark-local reinstalled from main after the merges (still says 0.1.0).
- Evals: action cases 9/9 with the project-home fixture (T-20261018-3). Not re-run this session: no change
  altered what a skill triggers on or decides.
- Owner rulings: live keyless calls fine while no terms are broken and no ban risked
  ([decisions/2026-10-18-owner-rulings-live-calls-and-tag.md](decisions/2026-10-18-owner-rulings-live-calls-and-tag.md)).
  Small rulings: [decisions/2026-10-18-step5-rulings.md](decisions/2026-10-18-step5-rulings.md).
- Keys stay in `~/.historywright/config.json` (OpenAlex, WHG). Never in the repository.
- Elsewhere: polywright PR #22 merged (references skill reads a pack's refs/index.json); evergreen issues
  m4bwav/evergreen-protocol#28 and #29 filed (A/B harness), not fixed.

## Waiting for Mark

- A 0.2.0 tag for the unreleased changes (asked 2026-10-18, no answer yet).
- Any directory submission (on hold since 2026-10-17).

## Next

1. If Mark says yes to 0.2.0: bump `.claude-plugin/plugin.json` and `VERSION` in hw_net.py in a PR, merge, tag
   `v0.2.0`, check the release workflow, then the wiki update procedure against the tag (Commands gains
   `--source ohm`; How-Claims-Are-Checked gains PDFs; a Releases row; empty "On main, not yet released").
2. Open items left: the Gallica, DPLA, QDL and HathiTrust 403s with hw.py's honest User-Agent (RESEARCH open
   questions); two-column PDFs read in stream order (a quote across columns can miss).
3. Optional: `evergreen.py worth --ab` on all 11 value cases with the project home, for a fresh baseline.
4. Wiki runs on Windows then WSL, one after the other (each has its own pace file).

## Read first

1. [next-session-prompt.md](next-session-prompt.md).
2. [log.md](log.md) (the 2026-10-18 entries) and the decisions folder.
3. [../AGENTS.md](../AGENTS.md) for the repository rules, [../README.md](../README.md) for the overview.
