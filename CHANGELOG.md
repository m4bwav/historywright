# Changelog: historywright

Every change to [README.md](README.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

## Releases

- 0.1.0 (unreleased): first version, below.

## Changes

### C-20261018-1 · 2026-10-18 · HW_RECORD no longer writes key values into fixtures
- because: found while writing the wiki (ai-docs/notes/2026-10-18-github-wiki.md): `_record` wrote the raw URL as the fixture pattern, and `tests/check_skills.py` exempts `tests/fixtures/`, so a recording with a URL key (Smithsonian's `api_key`) would have committed it
- files: skills/historywright/scripts/hw_net.py (`record_pattern`, `_record`), tests/test_hw.py (test_record_pattern_hides_keys)
- The pattern is built from the redacted URL, with each hidden value matching any value on replay.

### C-20261017-1 · 2026-10-17 · Created: three skills, hw.py, the registry, the pack contract
- because: user request (Step 2 kickoff, ai-docs/next-session-prompt.md); R-20261017-1 to -27; L-001 to L-003
- files: skills/historywright (SKILL.md; references/method.md, answer-format.md, dates.md, cli.md; scripts/hw.py, hw_net.py, hw_dates.py, hw_sources.py, hw_check.py), skills/historywright-sources (SKILL.md; references/registry.json, eras.md, recipes.md), skills/historywright-pack (SKILL.md; references/contract.md), evals/evals.json, tests/, scripts/budget.py, README.md, RESEARCH.md
- Initial version, tier `moderate`, interval 30 days, one unit shared by the three skills (ai-docs/decisions/2026-10-17-step2-build.md). Every guard in the skills cites its `R-` finding. hw.py reads Wikidata's full statements, maps a Wikipedia sentence to its footnotes, searches gazetteers, OpenAlex, Crossref and any registry source, does dates with integer JDN arithmetic (DILA tables for East Asian eras), verifies URLs, quotes, DOIs, QIDs and source independence, and builds and validates packs.
