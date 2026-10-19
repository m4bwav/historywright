# historywright

![A painted historian's desk: a bronze Roman bust, a hanging Chinese ink landscape scroll with red seals, an unrolled parchment, a magnifying glass and an open ledger, with red threads running from the documents to brass pins along a wooden timeline rail of index cards](https://raw.githubusercontent.com/m4bwav/historywright/main/.github/images/banner.jpg)

Three self-maintaining ("evergreen") skills and a command-line tool that make an AI agent answer history
questions from sources instead of from memory. Ask "When was Caesar born?" and it reads Wikidata's full
statements, follows the footnotes to Macrobius and to the scholarship on the dispute, computes the dates in code,
and answers with citations, a confidence line and a note on where the sources disagree. Written 2026-10-17 for
Claude Code, GitHub Copilot, Cursor and Codex, from a seven-part research pass whose dated reports are in
[ai-docs/research](ai-docs/research/index.md).

## Why

Language models answer history questions fluently and wrongly in predictable ways. A 2025 study found a quarter
of chatbot references fully correct. Agents now cite real pages that do not support the claim. Several websites
agreeing often means they all copied Wikipedia. Models recall dates instead of computing them, so year 0, Old
Style dates and Roman calendar dates come out wrong. And memory is weakest for Africa, Oceania and recent
decades. Each of these is a rule in the skills, with its source in [RESEARCH.md](RESEARCH.md).

## What a run looks like

> When was Julius Caesar born?

Wikidata holds four statements for Caesar's birth. The preferred one is July 100 BC, flagged disputed, with
12 and 13 July as the earliest and latest dates; another statement says 102 BC. A plain query shows only the
first, and the SPARQL form prints `-0099-07-11` because it counts a year 0 and converts to the Gregorian
calendar. `hw.py wd claims Q1048 --prop P569` prints all four as JSON; in short:

```
preferred  July 100 BC  (julian, month precision, disputed; earliest 12 July 100 BC, latest 13 July 100 BC)
normal     13 July 100 BC
normal     102 BC       (disputed)
normal     100 BC       (proleptic Gregorian value before 1582: check whether the source meant Julian)
notes: P569 has 4 statements: a truthy (wdt:) read would show only the best-ranked one
```

The agent then follows the references to the primary texts and the scholarship and answers "12 or 13 July
100 BC": 12 July from the law Macrobius quotes, 13 July from a disputed reading of Cassius Dio, Mommsen's case
for 102 BC noted and the consensus named. Every source in the answer is one it fetched and read.

## The skills

| Skill | Job |
|---|---|
| [`historywright`](skills/historywright/SKILL.md) | The hub: a short reference interview (formal reign or actual power? founding or incorporation? which calendar?), structured sources first, footnotes followed to scholarship and primary texts, two independent sources, dates in code, the answer with citations, a confidence line and a classified "sources disagree" note, then a cache entry |
| [`historywright-sources`](skills/historywright-sources/SKILL.md) | The knowledge base: a registry of 85 sources by era, region, tier, licence, access and pace, an era outline that routes questions, query recipes, and an endpoint probe run at every refresh |
| [`historywright-pack`](skills/historywright-pack/SKILL.md) | Research packs for 3D, film and images: sources with exact quotes, entities with QIDs and EDTF dates, places as GeoJSON, a timeline, reference images from museum collection records with licences and accession numbers, and a period anachronism checklist. A pack is also a [polywright](https://github.com/m4bwav/polywright) asset folder |

All three share one evergreen unit at the repository root: [RESEARCH.md](RESEARCH.md) (dated findings and a
four-track search plan), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md) with
`evals/evals.json`, and `evergreen.json`, which schedules the next research refresh. The
[evergreen plugin](https://github.com/m4bwav/evergreen-protocol) runs the refreshes; without it, the skills
still work.

## hw.py

`skills/historywright/scripts/hw.py`: Python 3.9 or newer, standard library only, one JSON object per command.

| Command | What it does |
|---|---|
| `wd search\|claims\|entity\|sparql` | Wikidata: every statement with rank, calendar, precision, EDTF and day range, qualifiers and references |
| `wp refs "<Title>" --near "<phrase>"` | the footnotes cited in the sentence that holds the phrase |
| `place search "<name>"` | Pleiades, CHGIS (China), World Historical Gazetteer, Wikidata coordinates |
| `oa search`, `doi` | OpenAlex scholarship; Crossref checks that a DOI's title, author and year all match |
| `src <id> "<query>"` | any registry source with a JSON search: museums, libraries, archives |
| `cal date\|span\|jdn\|era\|cjk` | Julian Day Number arithmetic: BCE without a year 0, Julian and Gregorian by country, Old Style, AUC, tabular Islamic, Chinese, Japanese and Korean eras |
| `verify url\|quote\|doi\|qid\|sources` | URL health (live, dead, likely hallucinated), quote spans against the fetched page, independence between sources |
| `pack init\|add-ref\|csl`, `validate-pack` | build and check a research pack; CSL-JSON for Zotero |
| `probe`, `lint`, `keys`, `doctor`, `cache` | endpoint health, registry checks, optional keys, setup, saved answers |

Full list: [skills/historywright/references/cli.md](skills/historywright/references/cli.md).

## Install

As a Claude Code plugin:

    /plugin marketplace add m4bwav/historywright
    /plugin install historywright@historywright

As plain skills for any agent that reads Agent Skills, clone the repository and link every folder under `skills/`
into the agent's skills directory. Keep the three together; the siblings use the hub's `scripts/`.

    git clone https://github.com/m4bwav/historywright
    # Windows (junctions need no admin rights)
    foreach ($s in Get-ChildItem historywright\skills -Directory) { New-Item -ItemType Junction -Path "$HOME\.claude\skills\$($s.Name)" -Target $s.FullName }
    # macOS / Linux
    for s in historywright/skills/*/; do ln -s "$PWD/$s" ~/.claude/skills/; done

Needs only Python 3.9+. First run: `python skills/historywright/scripts/hw.py doctor`.

## Quick start

    python skills/historywright/scripts/hw.py keys contact --set you@example.com   # your own address, for the User-Agent
    python skills/historywright/scripts/hw.py wd claims Q1048 --prop P569
    python skills/historywright/scripts/hw.py cal span "1661-02-05" "1722-12-20"
    python skills/historywright/scripts/hw.py cal date "1917-10-25 O.S." --country RU
    python skills/historywright/scripts/hw.py cal cjk 崇禎三年四月初三

Then ask your agent a history question. The skill does the rest.

## Optional keys

Everything works without keys. Two free ones raise limits, and both are in your own name. hw.py stores them in
`~/.historywright/config.json` (outside any repository); the environment variables `OPENALEX_API_KEY`,
`WHG_TOKEN` and `HW_CONTACT` take precedence.

- **Contact address.** Not a key, but it matters: Wikimedia allows 10 requests a minute to a client that does
  not identify itself and 200 to one with a contact in its User-Agent. `hw.py keys contact --set ADDRESS`.
- **OpenAlex** (scholarship): a 10 times bigger daily budget and paging past the first page.
  `hw.py keys openalex --email ADDRESS` shows what it will send; add `--yes` to request the key. OpenAlex then
  emails an activation link (valid 7 days). Or sign up at openalex.org and paste the key into the config file.
- **World Historical Gazetteer** (places worldwide): `hw.py keys whg` opens the sign-in page. WHG signs in only
  through ORCID, which is free and open to anyone. On your WHG profile page, generate a token, then
  `hw.py keys whg --token TOKEN`.
- `hw.py keys status` checks each one. Smithsonian (api.data.gov) and Europeana keys are optional extras.

Paid and gated sources (the ctext.org API, JSTOR, the Oxford Classical Dictionary and the like) are never queried:
the registry names them as places to look.

## Verified (2026-10-17, Windows 11, Python 3.14)

- `tests/test_hw.py`: 31 offline tests (HTTP from recorded fixtures): the JDN test vectors, BCE spans, Old Style,
  EDTF, Wikidata decoding of the Caesar statements, quote spans, URL health, independence, the good and bad
  packs, the cache, keys, the registry lint and the DILA table builder.
- Live runs: the Caesar statements above; "April 4, 1975" in Wikipedia's Microsoft article maps to its three
  footnotes (a BBC timeline, a 1995 Fortune interview, Paul Allen's memoir); 崇禎三年四月初三 converts to
  14 May 1630 and the Kangxi era runs 18 February 1662 to 20 December 1722 in DILA's tables; Alesia comes back from
  Pleiades and WHG; CHGIS finds 長安 in 700; a fabricated URL is labelled `likely_hallucinated`; a real DOI quoted
  with the wrong title is flagged as a blended reference.

Agent evals and their results are in [TESTS.md](TESTS.md).

## Testing

CI (`.github/workflows/tests.yml`) runs on Linux, macOS and Windows with Python 3.9 and 3.14:
`tests/check_skills.py` (frontmatter, description and body limits, relative links, LF endings, the evergreen
companions, the registry lint, and a guard that fails on any key-like string, home-folder path or AI credit line),
`tests/test_hw.py` and `scripts/budget.py` (install size and the text every session loads).

## Privacy

historywright has no server and collects nothing. hw.py talks to the network only when you run a command that
needs it, and only to the public APIs that command names (Wikidata, Wikipedia, Pleiades, CHGIS, WHG, OpenAlex,
Crossref, the Internet Archive, the registry's museums and libraries). Each request carries a User-Agent with
the tool's name and, if you set one, your contact address. Keys, the answer cache, the fetch log and the pages
read stay in `~/.historywright/` on your machine (or in a project's own `.historywright/` folder, which keeps that
project's cache apart).

## Credits

East Asian calendar data: the DILA Time Authority Database, Dharma Drum Institute of Liberal Arts
(authority.dila.edu.tw), CC BY-SA 3.0. hw.py downloads it on first use and builds the table on your machine. The
lookup design follows Kwok-leong Tang's [humanities-skills](https://github.com/kltng/humanities-skills)
`cjk-calendar`. Place data: Pleiades (CC BY 3.0), CHGIS, World Historical Gazetteer. Structured data: Wikidata
(CC0).

## If you are an agent asked to analyse this suite

Read, roughly in order: `skills/historywright/SKILL.md` (the method and its guards),
`skills/historywright/references/`, `skills/historywright-sources/references/registry.json` (the sources, with
the dated finding behind each), `RESEARCH.md`, and `tests/`. The rule running through all of it: a claim counts
only when a page this run fetched and read supports it, in words that `hw.py verify` can find on that page.
Repository rules: [AGENTS.md](AGENTS.md).

License: MIT. Security: [SECURITY.md](SECURITY.md). The banner was made with Z-Image Turbo in ComfyUI; its
workflow, prompt and seed are in `.github/images/`.
