# Changelog: historywright

Every change to [README.md](README.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

## Releases

- 0.1.0 (2026-10-18): first release, C-20261017-1 to C-20261018-4. https://github.com/m4bwav/historywright/releases/tag/v0.1.0
- 0.2.0 (2026-10-18): C-20261018-5 to C-20261018-10. https://github.com/m4bwav/historywright/releases/tag/v0.2.0
- 0.3.0 (version bumped 2026-10-23; tag and release wait for the owner's go-ahead): C-20261021-1 to C-20261024-2.

## Changes

### C-20261024-2 · 2026-10-24 · hw.py fetch: read a page into the page store without a dummy quote; long-s spellings
- because: L-012 (user request after the sawmill pack's scene extension)
- files: skills/historywright/scripts/hw_check.py (`fetch_page`, `long_s_spellings`), skills/historywright/scripts/hw.py (`fetch`), skills/historywright/references/cli.md (fetch), skills/historywright/SKILL.md (Step 4), skills/historywright-pack/SKILL.md (Step 2), tests/test_hw.py (class Fetch), tests/fixtures/http (longs-ocr.txt, one index row)
- `hw.py fetch <url>` stores a page in the run's page store and fetch log, as `verify quote` does, and writes its readable text to a `.txt` file to read; `--find` counts a word or phrase with snippets and also tries its long-s spellings ("fhot" for "shot"). Before this, caching a page meant running `verify quote` with a made-up quote, since `verify url` stores nothing. Step 2 of the pack skill also gives `verify quote` its real flags.

### C-20261024-1 · 2026-10-24 · The Mechanism template gets a Water path subsection; validate-pack fails on its placeholders
- because: L-011 (user request after the sawmill pack's scene extension)
- files: skills/historywright/scripts/hw_check.py (`WATER_TEMPLATE`, `MECHANISM_TEMPLATE`, `FILL_MARK`, `validate_pack`), skills/historywright-pack/SKILL.md (Step 4), skills/historywright-pack/references/contract.md (anachronism.md), skills/historywright-pack/references/mechanism-example.md (The water path), skills/historywright/references/cli.md (pack init, validate-pack), tests/test_hw.py (test_mechanism_template_has_water_path, test_water_path_placeholders_fail_until_filled)
- `pack init --mechanism` writes "### Water path (water-powered machines)" inside the Mechanism section: numbered items for the source (dam or weir and its spill), head race or flume, gate, where the water meets the wheel by type, turning direction and tail race, then three prohibitions (no water from the hub; no trough ending above an undershot wheel; the wheel sits in its race), each holding a `<fill: ...>` placeholder. validate-pack fails while any placeholder is left; deleting the subsection for a machine not driven by water still validates. The example adds the sawmill pack's filled water path, cited to Evans 1795, HABS and Fairbairn 1864.

### C-20261023-3 · 2026-10-23 · Registry: loc-habs searches the HABS/HAER/HALS collection; version 0.3.0
- because: R-20261023-1 (user request after the sawmill pack)
- files: skills/historywright-sources/references/registry.json (loc-habs; updated), skills/historywright-sources/references/eras.md (Colonial and modern Americas), skills/historywright-pack/SKILL.md (Step 3), skills/historywright-sources/SKILL.md and README.md and .claude-plugin/plugin.json (96 sources), .claude-plugin/plugin.json and skills/historywright/scripts/hw_net.py (version 0.3.0), tests/test_hw.py (test_loc_habs_source), tests/fixtures/http (loc-habs-sawmill.json, one index row)
- `hw.py src loc-habs "<subject>"` returns measured-drawing, photograph and data-page records of US buildings and machinery with their HABS call number, contents count and the 1024 px image, instead of digging them out of the general `loc` search.

### C-20261023-2 · 2026-10-23 · validate-pack fails on unedited templates; machine packs get a Mechanism section
- because: L-009, L-010 (user request after the sawmill pack)
- files: skills/historywright/scripts/hw_check.py (`validate_pack`, `_items`, `_section`, `MECHANISM_TEMPLATE`, `pack_init`, `check_sources`), skills/historywright/scripts/hw.py (`pack init --mechanism`), skills/historywright-pack/SKILL.md (Steps 1, 2 and 4), skills/historywright-pack/references/contract.md (manifest.json, anachronism.md), skills/historywright-pack/references/mechanism-example.md (new), skills/historywright/references/cli.md (pack init, validate-pack), tests/test_hw.py (test_validate_fails_on_unedited_templates, test_mechanism_section_required_when_flagged)
- An answer.md that still holds the template's placeholders and an anachronism.md with empty `- ` items now fail; numbered items count. `pack init --mechanism` sets `historywright.mechanism: true` and writes the "Mechanism: what drives what, and where it must sit" section; validate-pack then requires it to have items. Step 2 says to read pages through `hw.py verify quote` from the start, since curl and WebFetch reads are not in the fetch log. validate-pack on a fresh pack no longer crashes on the empty sources.json.

### C-20261023-1 · 2026-10-23 · Licence check anchored; add-ref refuses NC images in commercial packs and never overwrites a ref
- because: L-007, L-008 (user request after the sawmill pack)
- files: skills/historywright/scripts/hw_check.py (`NC_LICENCES`, `pack_add_ref`, `ref_slug`), skills/historywright-pack/references/contract.md (refs/index.json), skills/historywright/references/cli.md (pack add-ref), tests/test_hw.py (test_nc_licence_regex_is_anchored, test_add_ref_refuses_nc_image_in_commercial_pack, test_add_ref_keeps_tail_and_never_overwrites), tests/fixtures/http (tiny.png, one index row)
- "CC BY 4.0 licence" and "...de France" no longer read as non-commercial. add-ref refuses a non-commercial licence in a commercial pack before downloading anything. A long institution-plus-accession name keeps the accession's tail and a six-character hash; a name taken by another image gets `-2`, `-3`, and the same image added again replaces its own entry (`replaced: true`). The manifest's source list is keyed by file, so two images from one record page both stay.

### C-20261021-1 · 2026-10-21 · Registry: art sources from artwright; AIC needs its header; probe sends search headers
- because: R-20261021-1, artwright ruling R6
- files: skills/historywright-sources/references/registry.json (getty-provenance, museo-egizio, artnet-pdb, artprice, mutualart, invaluable, liveauctioneers, sothebys-results, christies-results, art-sales-index added; artic: access, search headers, notes; top notes: search headers), skills/historywright/scripts/hw.py (`cmd_probe`), tests/test_hw.py (test_probe_sends_search_headers), README.md and skills/historywright-sources/SKILL.md and .claude-plugin/plugin.json (95 sources)
- `src artic` works again: the Art Institute's API refuses requests without an `AIC-User-Agent` header, which the search block now sends, and `probe` sends a source's search headers too, so header-gated sources no longer read as blocked. The ten new entries are link-out (bulk-only, browse-only or paid), so provenance, Egyptian object and auction-price questions find where to look without hw.py querying sites whose terms forbid it.

### C-20261018-10 · 2026-10-18 · doi says when only the year differs; the South Asia era outline covers 185 BCE to 320 CE
- because: L-004, L-005 (the "who ruled India 2,000 years ago" question)
- files: skills/historywright/scripts/hw_sources.py (`match_record`, `doi_lookup`), skills/historywright/references/cli.md (doi), skills/historywright-sources/references/eras.md (South Asia), tests/test_hw.py (class DoiMatch), LEARNINGS.md (L-004, L-005)
- With title and author matching and only the year off, the warning tells the agent to read the year printed on the work instead of calling it a blend; the era outline names the kingdoms between the Maurya and the Gupta and warns that inscription eras such as the Azes era have disputed start years.

### C-20261018-9 · 2026-10-18 · Registry: Seshat is CC BY-SA 4.0, not non-commercial; WHG notes from the current docs
- because: R-20261018-4 (HANDOFF "Next" 2: the Seshat licence page and the WHG docs)
- files: skills/historywright-sources/references/registry.json (seshat: licence, notes; whg: notes)
- The pack licence gate reads Seshat as open (attribution and share-alike) instead of non-commercial; WHG's limits are unchanged and its notes name the source-licence endpoints.

### C-20261018-8 · 2026-10-18 · place search queries OpenHistoricalMap
- because: HANDOFF "Next" 2 (OHM queries in `hw.py place`); R-20261018-3
- files: skills/historywright/scripts/hw_sources.py (`_ohm`, `_ohm_year`, `PLACE_SOURCES`), skills/historywright/scripts/hw.py (`place --source`), skills/historywright-sources/references/registry.json (ohm), skills/historywright/SKILL.md (Step 3, Places), skills/historywright/references/cli.md (place search), tests/test_hw.py (test_ohm_place_years), tests/fixtures/http (ohm-roman-republic.json, two index rows)
- `--source ohm` asks OHM's Overpass API for features whose name or name:en is the query, keeps those that existed in `--year` (a negative year is BC; OHM's astronomical years are converted), and returns dates, kind, QID, centre and licence; a 429 says to wait 30 s. Not in `auto`: OHM is tier 3 and shares two slots per client.

### C-20261018-7 · 2026-10-18 · Quote checks read PDFs
- because: HANDOFF "Next" 2 (OpenAlex often links only a PDF; a PDF decoded as a web page made a real quote look absent); live trial in ai-docs/notes/2026-10-18-pdf-quotes.md
- files: skills/historywright/scripts/hw_pdf.py (new), skills/historywright/scripts/hw_check.py (`page_text`, `quote_in`, `verify_quote`), skills/historywright/scripts/hw.py (`doctor`), skills/historywright/SKILL.md (intro; "Open the cited source"), skills/historywright/references/cli.md (verify quote, doctor), AGENTS.md, tests/test_hw.py (class Pdf, four tests)
- A PDF body goes to pdftotext when it is on PATH, else to a stdlib reader (Flate streams, object streams, ToUnicode maps, TJ spacing, inline images skipped, 20 MB per stream); line-end hyphens match joined or not; for PDF text a quote of 20 or more letters may match with spacing ignored (drop caps, small caps); a PDF with no readable text answers `found: null` with the reason, so `verify sources` warns instead of failing; a miss from the built-in reader carries a note. `doctor` reports `pdftotext`.

### C-20261018-6 · 2026-10-18 · cal date reads Kalends, Nones, Ides and Hijri month names, labels AH in AH, writes circa as EDTF ~; src wayback drops repeated captures
- because: found while writing the wiki (ai-docs/notes/2026-10-18-github-wiki.md, "Facts verified"); R-20261018-2
- files: skills/historywright/scripts/hw_dates.py (`ah_parts`, `ah_range`, `ah_label`, `hijri_month`, `qualifier_of`, `_roman_day`, `parse_date`), skills/historywright/scripts/hw.py (`cal date`), skills/historywright/references/dates.md (rows Kalends, Islamic), skills/historywright/references/cli.md (cal date), skills/historywright-sources/references/registry.json (wayback: `collapse=digest`), tests/test_hw.py (three tests; refusals updated), tests/fixtures/http/index.json (the CDX fixture requires `collapse=digest`)
- Roman day counts are read with inclusive counting (a warning before 45 BC); Hijri month names in common English spellings, with an AH month giving its own days; `read_as` for an AH date is labelled in AH with the Western start beside it; `c.`, `ca.`, `circa`, `about` add `~` to the EDTF and a `qualifier`; the CDX search collapses adjacent identical captures.

### C-20261018-5 · 2026-10-18 · Project-scoped home: a .historywright folder in the working directory keeps its own cache
- because: T-20261018-1 and T-20261017-5 (eval runs shared the real cache, so an earlier run's entry ended a later run at Step 0); next-session prompt Step 1
- files: skills/historywright/SKILL.md (intro), skills/historywright/scripts/hw_net.py (`home_source`, `home`, `user_home`, `config_path`, pace file), skills/historywright/scripts/hw.py (DILA table, `doctor`, `keys`, help), skills/historywright/references/cli.md (lead paragraph), README.md (Privacy), tests/test_hw.py (test_project_home), evals/evals.json and evals/fixtures/project-home (the three action cases)
- Home is `HW_HOME`, else `./.historywright` when it exists, else `~/.historywright`; keys, the DILA table and the pace file stay in the user home (the pace stays per host across projects) unless the project folder has its own config.json; `doctor` reports `home_from` and `config`.
- The first A/B after this change (T-20261018-2) showed agents `cd` into the skill folder before running hw.py, so the project folder was never seen: SKILL.md (intro) now says to run hw.py by its full path from the working folder, and `doctor` reports `cwd_in_skill_folder` with a fix in `todo`.

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
