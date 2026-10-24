# Learnings: historywright

Procedural lessons for [README.md](README.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first, by meaning (`evergreen.py search "<the lesson>" --kinds learnings` finds near-duplicates in every registered unit): add / update / retire / none. Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

### L-012 · 2026-10-24 · Caching a page needed a dummy quote, and 1795 OCR spells "shot" as "fhot"
- Trigger: extending the sawmill pack (sawmill-3d/history) for a wide illustration, 2026-10-24. `hw.py verify url` checks a link without storing the body, so the only way to put Evans 1795 and Fairbairn 1864 into the page store for reading was `hw.py verify quote --url U --quote <any word>`. Then searches of the Evans OCR for "shot", "sufficient" and "distance" found nothing: the 1795 printing uses the long s, which the OCR reads as "f" ("fhot", "fufficient dif-").
- Hypothesis: a reading step disguised as a check gets skipped or done with curl, which leaves the page out of the fetch log; and a researcher searching pre-1800 OCR with modern spellings concludes that a source is silent when it is not.
- Rule: read pages with `hw.py fetch <url> [--find "<word>"]` (page store, fetch log, text file); `--find` also tries each term with every non-final s as "f" and as "ſ". Search pre-1800 OCR in long-s spellings before calling a source silent.
- Evidence: the sawmill pack's sources.json, s1 (Evans 1795 OCR: "fufficient dif-", "underfhot", "tale-race") and s14 (Fairbairn 1864); class Fetch in tests/test_hw.py.
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-24

### L-011 · 2026-10-24 · A water-powered machine's pack must say where the water comes from and goes
- Trigger: the sawmill pack (sawmill-3d/history) was extended on 2026-10-24 for a wide picture of the mill in its landscape. Its Mechanism section (from `pack init --mechanism`) covered the drive chain inside the mill and said nothing about the dam, races, gate or where the water meets the wheel, and image models' commonest error was water pouring from the wheel's hub. A "Scene: the water path in a wide picture" section had to be researched and written by hand.
- Hypothesis: the drive chain starts at the wheel, so a template that asks for it stops there; a picture wider than the wheel is checked against nothing, and the model falls back on a fountain-like jet from the axle or a trough over an undershot wheel.
- Rule: `pack init --mechanism` writes a "Water path (water-powered machines)" subsection: source, head race or flume, gate, where the water meets the wheel for its type, turning direction, tail race, and the prohibitions (no water from the hub or axle; no trough ending above an undershot wheel; the wheel sits in its race), each a `<fill: ...>` placeholder that validate-pack fails on until it is replaced with cited facts or the subsection is deleted.
- Evidence: the sawmill pack's anachronism.md ("Scene: the water path in a wide picture") and answer.md section 4, from Evans 1795 (forebay slanted under an undershot wheel, gate near the floats, tail-race fall, dam a sufficient distance above the mill, waste in the canal bank) and Fairbairn 1864 (water applied near the bottom, rushing under the shuttle, tail-race in the direction of revolution, weir sluice in a wing wall); test_water_path_placeholders_fail_until_filled.
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-24

### L-010 · 2026-10-23 · A machine's pack needs a Mechanism section: what drives what, and where each part must sit
- Trigger: a pack for a water-powered sash sawmill (1790-1840) feeding 3D and image work. The answer held every fact (flutter wheel on the crank shaft, pitman up through the floor, sash between fender posts), but the anachronism template only asked what did not exist yet; the drive chain and a list of placements a picture must never break (blade outside the building, wheel with no shaft into it, floating gears) had to be written by hand.
- Hypothesis: for a machine the likeliest error in a picture or model is not a date but a part in the wrong place or connected to nothing; a prose answer does not say where each part sits, so nothing downstream can check it.
- Rule: `pack init --mechanism` sets `historywright.mechanism: true` and gives anachronism.md the "Mechanism: what drives what, and where it must sit" section (numbered links from the power source to the tool, then what a picture must never show); `validate-pack` fails when the flag is set and the section is missing or has no items. Example: skills/historywright-pack/references/mechanism-example.md.
- Evidence: the sawmill pack built 2026-10-23 (its anachronism.md, Mechanism and Prohibitions sections); test_mechanism_section_required_when_flagged.
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-23

### L-009 · 2026-10-23 · validate-pack passed an unedited template
- Trigger: on the sawmill pack (2026-10-23), validate-pack was found to accept the files `pack init` writes: answer.md with `<answer with inline citations [s1]>` still in it passes, because the template already has a Confidence line, a "Sources agree" note and the AI-researched line; anachronism.md's three empty `- ` lines counted as three checklist items. On a fresh pack it also crashed (KeyError 'warnings') instead of reporting the empty sources.json.
- Hypothesis: checks that look for required markers are satisfied by a template that contains those markers; the template is the one input every pack starts from, so the validator has to recognise it.
- Rule: validate-pack fails on any template placeholder left in answer.md and on empty list items in anachronism.md, and counts only filled items towards the three; check_sources returns `warnings` on every path.
- Evidence: the sawmill pack, 2026-10-23; test_validate_fails_on_unedited_templates.
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-23

### L-008 · 2026-10-23 · pack add-ref recorded a non-commercial image in a commercial pack instead of refusing it
- Trigger: building the sawmill pack (2026-10-23), add-ref only set `nc: true` on a non-commercial image whatever the pack's licence, so the rule "never put a non-commercial image in a commercial pack" was enforced only later by validate-pack, after the file was downloaded and both indexes written.
- Hypothesis: a rule that the writer does not enforce gets broken and then needs cleanup by hand in two files; refusing at the door is cheaper than detecting afterwards.
- Rule: add-ref reads the manifest first and refuses (`ok: false`, a clear error, nothing written) a non-commercial licence when `historywright.commercial` is true; validate-pack keeps its check for hand-edited indexes.
- Evidence: the sawmill pack, 2026-10-23; test_add_ref_refuses_nc_image_in_commercial_pack.
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-23

### L-007 · 2026-10-23 · The non-commercial licence check matched "nc" inside words
- Trigger: on the sawmill pack (2026-10-23), the regex `(nc|non-?commercial)` flagged "CC BY 4.0 licence" (li-c-e-n-c-e) and a French "...de France" credit as non-commercial, which would mark open images `nc: true` and block them from commercial packs.
- Hypothesis: an unanchored two-letter pattern matches inside ordinary English and French words; licence strings say NC as a separate token (CC BY-NC, BY-NC-SA).
- Rule: NC_LICENCES is `\bnc\b` or `\bnon[- ]?commercial`; a new licence string gets a test case both ways.
- Evidence: the sawmill pack, 2026-10-23; test_nc_licence_regex_is_anchored.
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-23

### L-005 · 2026-10-17 · A research skill's A/B must grant the research tools to both arms
- Trigger: the first `evergreen.py worth --ab` run scored 48% with the skill against 33% without (verdict CUT). Most with-arm failures ended "requires approval": the runner's default outcome tools are Skill, Read, Glob, Grep and Write, so hw.py, WebFetch and WebSearch were blocked; the skill then refused to answer from memory, as its rules say, while the without arm answered from memory in 3 to 5 seconds.
- Hypothesis: the default tool grant fits skills that edit files, not skills whose whole job is fetching sources; a blocked with arm measures the permission gate, and the harness's environment check does not look for "requires approval" in the answer.
- Rule: every value case of this plugin lists `"tools": ["Bash", "PowerShell", "WebFetch", "WebSearch", "Edit"]` so both arms can research; read any A/B with many "requires approval" answers as an environment run, not a verdict.
- Evidence: the run-1 transcripts (kangxi-with-3, menelik-with-1, microsoft-with-2, misattributed-quote-with-1/2/3) and the re-run in TESTS.md.
- Scope: skill (evals); worth raising with the evergreen plugin (environment_fault could match PERMISSION_REFUSED in the answer)
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-17

### L-004 · 2026-10-17 · Some servers refuse a User-Agent that names python-urllib
- Trigger: `hw.py probe` got 403 from the OpenHistoricalMap Overpass status page while the registry builder's curl got 200; the only difference was hw.py's agent ending in "python-urllib". SEC EDGAR, the other way round, refuses library-style agents and wants "name email".
- Hypothesis: bot filters match library names in the agent string; an agent that names the tool, its repository and a contact passes.
- Rule: the agent is `historywright/<version> (<repo>; <contact>)` with no library name; a registry entry with `"ua": "plain"` gets `historywright <contact>` (SEC).
- Evidence: the probe on 2026-10-17: ohm 403, then ok after the change; `hw.py src edgar` answers with the plain agent.
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-17

### L-005 · 2026-10-18 · "Who ruled X exactly N years ago" in early South Asia has several answers that depend on an era's start year
- Trigger: "who ruled India exactly 2,000 years ago" (AD 26). The era outline went straight from the Maurya to the Gupta, so it gave no route for 185 BCE to 320 CE; Gondophares' accession (Takht-i-Bahi: year 26 of his reign = year 103 of an era) falls in AD 21 or AD 32 depending on whether the Azes era began 58/57 or 47/46 BCE.
- Hypothesis: early Indian kings are dated by inscriptions in regional eras, and the start years of those eras are disputed; one date question becomes two or three answers, and "India" was not one realm.
- Rule: answer by region (north-west, Mathura, Deccan, south), compute each era reading in code, and give each reading's answer with the scholar who holds it.
- Evidence: Cribb 2017 (zenodo 3492002) and Falk and Bennett 2009 (Acta Orientalia 70), both read 2026-10-18; eras.md South Asia now lists the kingdoms between Maurya and Gupta (C-20261018-10).
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-18

### L-004 · 2026-10-18 · A wrong year in Crossref is not a blended reference; Brill PDFs sit behind a bot check
- Trigger: `hw.py doi 10.5617/ao.5339 --year 2009` said "blended or wrong reference" because Crossref gives 1970 for Falk and Bennett, while the PDF's masthead prints "Acta Orientalia 2009: 70". OpenAlex repeats the 1970. Separately, an OpenAlex `oa_url` on brill.com returned an AWS WAF "Human Verification" page instead of the PDF.
- Hypothesis: some journals deposited back issues with a placeholder year; registry metadata is not the printed record. Brill guards downloads against scripts.
- Rule: when title and author match and only the year differs, read the year printed on the work before rejecting it (`match_record` now says so); treat a brill.com download as unreadable and look for another copy.
- Evidence: the 2026-10-18 India question; DoiMatch tests.
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-18

### L-003 · 2026-10-17 · British Old Style dates before 1752 need the January-start year
- Trigger: the method reference first gave George Washington's birth as "11 February 1731 O.S." and fed 1731 to the converter, which would give 22 February 1731, a year early.
- Hypothesis: before 1752 the English legal year began on 25 March, so a date between 1 January and 24 March carries the previous year's number; modern conversion needs the January-start year.
- Rule: hw.py reads every year as starting 1 January; for a British (or colonial) date in January to 24 March before 1752, pass the next year and let `--country GB` print the dual year (1731/32).
- Evidence: `hw.py cal date "1732-02-11 O.S." --country GB` gives 22 February 1732 and dual year 1731/32; test_os_ns_and_dual_year.
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-17

### L-002 · 2026-10-17 · Print UTF-8 explicitly: Windows consoles default to cp1252
- Trigger: printing DILA era names (康熙) from Python on Windows raised UnicodeEncodeError ('charmap' codec).
- Hypothesis: Python's stdout on a Windows console uses the ANSI code page unless PYTHONIOENCODING or reconfigure says otherwise; history output is full of CJK, Greek and diacritics.
- Rule: hw.py calls `sys.stdout.reconfigure(encoding="utf-8")` before printing (`utf8_stdout`); ad hoc scripts set PYTHONIOENCODING=utf-8.
- Evidence: the 2026-10-17 build session; every hw.py command prints CJK on Windows since.
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-17

### L-001 · 2026-10-17 · Python 3.13+ refuses some archive certificates that curl accepts
- Trigger: `hw.py cal setup` could not download DILA's zip: "CERTIFICATE_VERIFY_FAILED ... Missing Subject Key Identifier", while curl fetched it.
- Hypothesis: Python 3.13 turned on X.509 strict verification by default; older academic hosts serve certificates without the key identifier extension.
- Rule: on that error only, retry once with `VERIFY_X509_STRICT` cleared (chain and hostname still checked), and keep a mirror of the same data (DILA's GitHub copy) as the fallback.
- Evidence: R-20261017-27; the second `hw.py cal setup --force` built the table from the zip.
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-17
