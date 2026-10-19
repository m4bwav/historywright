# Changelog: historywright

Every change to [README.md](README.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

## Releases

- 0.1.0 (2026-10-18): first release, C-20261017-1 to C-20261018-4. https://github.com/m4bwav/historywright/releases/tag/v0.1.0
- unreleased: C-20261018-5 onward.

## Changes

### C-20261018-5 · 2026-10-18 · Project-scoped home: a .historywright folder in the working directory keeps its own cache
- because: T-20261018-1 and T-20261017-5 (eval runs shared the real cache, so an earlier run's entry ended a later run at Step 0); next-session prompt Step 1
- files: skills/historywright/scripts/hw_net.py (`home_source`, `home`, `user_home`, `config_path`, pace file), skills/historywright/scripts/hw.py (DILA table, `doctor`, `keys`, help), skills/historywright/references/cli.md (lead paragraph), README.md (Privacy), tests/test_hw.py (test_project_home), evals/evals.json and evals/fixtures/project-home (the three action cases)
- Home is `HW_HOME`, else `./.historywright` when it exists, else `~/.historywright`; keys, the DILA table and the pace file stay in the user home (the pace stays per host across projects) unless the project folder has its own config.json; `doctor` reports `home_from` and `config`.

### C-20261018-4 · 2026-10-18 · Keyless request paces held under each source's public limit
- because: R-20261018-1 (the owner's ruling on live keyless calls: no broken terms, no ban risk)
- files: skills/historywright-sources/references/registry.json (pace_s of wikidata, wikipedia, commons, openalex, crossref, internet-archive), skills/historywright/scripts/hw_net.py (DEFAULT_PACE)
- Wikimedia 0.35 s, OpenAlex 0.15 s, Crossref 0.2 s, archive.org 4 s; no other behaviour changes.

### C-20261018-3 · 2026-10-18 · Docs: the registry holds 85 sources; the README's Caesar lines are a summary; cli.md exit 2 and the missing options
- because: found while writing the wiki (ai-docs/notes/2026-10-18-github-wiki.md, inaccuracies 1 to 3)
- files: README.md (The skills; What a run looks like), .claude-plugin/plugin.json (description), skills/historywright-sources/SKILL.md (Files), skills/historywright/references/cli.md (lead paragraph; table rows wd search, wp refs, cache, verify quote, pack init, keys)
- "about 60 sources" became 85 (`hw.py lint`); the README says the four Caesar lines summarise the JSON; cli.md names the argparse exit 2 and lists `--lang`, `--limit`, `--max-age`, `--refetch`, `--name`, `--no-browser` and `keys status --offline`.

### C-20261018-2 · 2026-10-18 · cal date: suffix AUC and AH, AH years as their own range, refusals instead of silent misreadings
- because: found while writing the wiki (ai-docs/notes/2026-10-18-github-wiki.md): `cal date "709 AUC"` answered AD 709 (it is 45 BC), `"AH 1300"` gave the days of 1882 rather than those of AH 1300, and `"1 Muharram 1 AH"` and `"Ides of March 44 BC"` were misread with no warning
- files: skills/historywright/scripts/hw_dates.py (`parse_date`, `ah_year_range`), skills/historywright/scripts/hw.py (`cal date`), skills/historywright/references/dates.md (rows Kalends, AUC, Islamic), tests/test_hw.py (two tests)
- `709 AUC` and `1300 AH` read as the prefix forms; a year-only AH date covers its own 354 or 355 days, with an EDTF interval; AUC or AH in a form the parser cannot read, and Kalends, Nones or Ides, are refused with the form to use; other words the parser skips are listed in `notes`.

### C-20261018-1 · 2026-10-18 · HW_RECORD no longer writes key values into fixtures
- because: found while writing the wiki (ai-docs/notes/2026-10-18-github-wiki.md): `_record` wrote the raw URL as the fixture pattern, and `tests/check_skills.py` exempts `tests/fixtures/`, so a recording with a URL key (Smithsonian's `api_key`) would have committed it
- files: skills/historywright/scripts/hw_net.py (`record_pattern`, `_record`), tests/test_hw.py (test_record_pattern_hides_keys)
- The pattern is built from the redacted URL, with each hidden value matching any value on replay.

### C-20261017-1 · 2026-10-17 · Created: three skills, hw.py, the registry, the pack contract
- because: user request (Step 2 kickoff, ai-docs/next-session-prompt.md); R-20261017-1 to -27; L-001 to L-003
- files: skills/historywright (SKILL.md; references/method.md, answer-format.md, dates.md, cli.md; scripts/hw.py, hw_net.py, hw_dates.py, hw_sources.py, hw_check.py), skills/historywright-sources (SKILL.md; references/registry.json, eras.md, recipes.md), skills/historywright-pack (SKILL.md; references/contract.md), evals/evals.json, tests/, scripts/budget.py, README.md, RESEARCH.md
- Initial version, tier `moderate`, interval 30 days, one unit shared by the three skills (ai-docs/decisions/2026-10-17-step2-build.md). Every guard in the skills cites its `R-` finding. hw.py reads Wikidata's full statements, maps a Wikipedia sentence to its footnotes, searches gazetteers, OpenAlex, Crossref and any registry source, does dates with integer JDN arithmetic (DILA tables for East Asian eras), verifies URLs, quotes, DOIs, QIDs and source independence, and builds and validates packs.
