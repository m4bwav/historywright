# historywright creation pass, 2026-10-17

The evergreen creation pass (PROTOCOL §8) for historywright, run before any skill text. Seven `evergreen-researcher` passes ran in parallel, in creation mode: four on the subject track (because the source list is large), one each on tooling, practice and testing. Their verbatim reports are in [2026-10-17-creation-pass/](2026-10-17-creation-pass/); the `R-` entries are in [../../RESEARCH.md](../../RESEARCH.md). This file is the synthesis: what the build in Step 2 should rest on.

Cost: searches 211 (11 refused by the shared budget) · fetches 245 · tool calls 477.

A caveat on coverage. The seven passes shared one WebSearch budget of about 200 per turn, and it ran out partway through. The tooling pass got only 4 searches and made up for it with 73 direct fetches of the MCP registry, the skills.sh search API, GitHub's API and the Anthropic catalog. The subject passes left a few items unchecked; each pass's report lists them under Open questions. Live API calls were the most decisive evidence throughout, and the build should keep using them (see `hw.py probe` below).

## 1. Where the answers live

### What changed in the last year (the reasons model memory of these APIs is wrong)

- **Wikimedia rate limits** (enforced since 2026-03-12): 10 requests a minute for an unidentified client, 200 for a client with a User-Agent that names the tool and a contact, concurrency 3 at most, Retry-After honoured. The API Portal at api.wikimedia.org was retired in June 2026; use `en.wikipedia.org/api/rest_v1/` and `w/api.php`.
- **Wikidata Query Service split** (2025-05-09, legacy endpoint gone in early 2026): `query.wikidata.org` holds the main graph; scholarly articles are at `query-scholarly.wikidata.org`.
- **OpenAlex** (2026-02-13): API keys and a daily dollar budget; the `mailto` polite pool is gone. Keyless still works at a tenth of the budget, and a free key is needed to page past page 1.
- **Crossref** (2025-12-01): new limits; polite pool 10 single-DOI requests a second, concurrency 3.
- **The Met** retired its v1 search on 2026-10-01; use `v1.1/search`.
- **Rijksmuseum** removed its key API; the new Linked Art search needs no key.
- **Getty** retired its XML services (final sets 2026-01-30); SPARQL and N-Triples remain.
- **Chronicling America** is reachable only through the loc.gov JSON API (since 2025-08-04), at 20 requests a minute.
- **HathiTrust** Data API retired 2024-07-17 (the Bibliographic API works); **JSTOR** Constellate shut 2025-07-01; **Trove** v2 retired 2024-09; **NARA** v1 retired 2023-09.
- **ctext.org** API now needs an institutional subscription and a registered IP, and its terms say scrapers may be fed corrupted data.
- **World Historical Gazetteer** needs a token, a real User-Agent, and has a 5,000-a-day quota; CHGIS records are not redistributable through it.
- **Bot walls** (Anubis and 403s) now block many heritage sites to scripts: Trove, EDH, papyri.info, Gallica pages, QDL, DPLA, CBDB, Britannica, GatesNotes. The documented JSON APIs mostly still answer.

### Ranked sources

Tier: 1 primary or expert-curated, 2 curated reference or aggregator, 3 crowd-sourced tertiary. "Key" means a free sign-up; "PAID" means a subscription. Full tables with endpoints are in the four subject reports.

| Use | Source | Route | Licence | Access | Tier |
|---|---|---|---|---|---|
| Who, when, with whom; QIDs | Wikidata | `wbgetclaims` or SPARQL `p:/ps:/psv:` with `timePrecision`, `timeCalendarModel`, rank, P1480, P1319, P1326 | CC0 | UA required; 60 s query limit | 3, or 2 where the statement is referenced |
| Routing, QID per title | Wikipedia REST summary, Action API | `/api/rest_v1/page/summary/{title}` gives `wikibase_item` | CC BY-SA | UA, 200/min | 3 (finder, never the cited authority) |
| Ancient places | Pleiades | daily `pleiades-places-latest.json.gz`, `/places/{id}/json` | CC BY 3.0 | none | 1 |
| Chinese places 221 BCE–1911 | CHGIS TGAZ | `chgis.hudci.org/tgaz/placename?n=&yr=&fmt=json` (live-tested) | unstated, not redistributable | none | 1 |
| Places worldwide | World Historical Gazetteer | `/entity/place:{id}/api`, `/reconcile` | per source | Key (token), 5,000/day | 2 |
| Period names to date ranges | PeriodO | `n2t.net/ark:/99152/p0dataset.json` | CC0 | none | 1 |
| Polity borders 3400 BCE–2024 | Cliopatria (Seshat) | one GeoJSON with QIDs | CC BY 4.0 | none | 1 |
| Dated map features | OpenHistoricalMap | planet dumps, Overpass, QLever | mostly CC0 | none | 3 |
| Comparative polity variables | Seshat Polaris-2026 | `seshat-db.com/api/` | CC BY-NC-SA | none | 1 |
| Scholarship | OpenAlex | `api.openalex.org/works?search=` | CC0 | keyless page 1; Key for more | 2 |
| DOI check | Crossref | `api.crossref.org/works/{doi}?mailto=` | open | polite pool | 2 |
| Greek and Latin texts | Perseus TEI on GitHub; LacusCurtius; Attalus | static files and pages | CC BY-SA; PD per page | none | 1 |
| Translated primary texts | Fordham Sourcebooks; Avalon | static pages | copy-permitted | none | 1 to 2 |
| Roman Republic people | DPRR | SPARQL `romanrepublic.ac.uk/rdf` | open | none | 1 |
| Chinese officials | CBDB | SQLite download (June 2026 release) | CC BY-NC-SA | none | 1 |
| Arabic and Persian texts | OpenITI 2025.1.9 | Zenodo bulk | per text | none | 1 |
| US history, newspapers | Library of Congress | `loc.gov/...?fo=json` | mostly PD | 20/min | 1 |
| UK records | TNA Discovery | `discovery.nationalarchives.gov.uk/API/search/records` (live-tested) | OGL | 3,000 per 5 min | 1 |
| Books, scans | Internet Archive | `advancedsearch.php?...&output=json` (live-tested) | per item | none | 1 to 3 |
| Japan | NDL Search, Japan Search | `ndlsearch.ndl.go.jp/api/opensearch` (live-tested) | per provider | no parallel calls | 1 |
| European heritage | Europeana | `record/v2/search.json` (demo key works) | per item | Key | 2 |
| German lives | Deutsche Biographie | Solr beta | CC0 metadata | none | 2 |
| CC0 object images | Met v1.1, Cleveland, Art Institute of Chicago, Getty, Smithsonian, Rijksmuseum | REST | CC0 per record | Smithsonian Key | 1 |
| Company history | SEC EDGAR; Wayback CDX; Federal Register; Computer History Museum oral histories | REST; web | public | EDGAR UA, 10/s | 1 |
| Restricted images | British Museum, Science Museum Group (CC BY-NC-SA), V&A (own terms) | web, dumps | non-commercial | | 1 (flag NC) |
| Dropped | DBpedia (adds nothing over Wikidata), Clio Infra and Maddison (frozen) | | | | |
| PAID or gated, link-out only | ctext API, Scripta Sinica full tier, Trismegistos search, CNKI, eHRAF, JSTOR, IHR/Brepols BBIH, OCD, New Pauly, Encyclopaedia of Islam, Loeb, Transkribus API; NARA (Key by email), Trove (Key and approval) | | | | |

Regional gaps. China is well served (CHGIS, CBDB, Kanripo, the National Library of China's 古籍 reader, CASS journals through NCPSSD after sign-up). India (Abhilekh Patal), Africa (the British Library Endangered Archives Programme, NAAIRS) and Latin America (PARES, Hemeroteca Digital Brasileira) are browse-only with no scriptable API. For those regions the skill has to rely on scholarship (OpenAlex), Wikidata references and Internet Archive scans, and say so in its confidence line.

Wikipedia routing articles. None of the seed articles is a featured or good article; all are actively edited. "Timeline of human prehistory" now redirects to "Timeline of prehistory", and "Outline of the history of China" does not exist (use "Outline of China" and "History of China"). Classes: Human evolution B (Top), History of China B, Periodization C, List of time periods C, Timeline of Chinese history List (Top), List of Chinese monarchs List (Top, 651 editors). Routing only; cite the sources beneath them.

## 2. The method

- **Source hierarchy**: tertiary sources (Wikipedia, Britannica) route and supply citations; follow their footnotes and cite the secondary or primary source. Whether a source is primary depends on the question.
- **Historians' reading** (Wineburg; the Digital Inquiry Group's Historical Thinking Chart): sourcing (who, when, how close, why), contextualisation, corroboration, close reading.
- **Reference interview** (RUSA guidelines): before searching, pin down what the question means (formal reign or actual power, founding or incorporation, which calendar), state the reading chosen, and end with a follow-up offer.
- **Dates**:
  - Julian Day Number as the pivot.
  - Python's `datetime` stops at year 1, so use integer algorithms (Fliegel–Van Flandern).
  - Astronomical years: 1 BC is year 0.
  - Wikidata's JSON uses historical numbering (-0100 is 100 BC), while its RDF and SPARQL use XSD year 0 and convert to Gregorian. A naive SPARQL read of Caesar's birth gives "-0099-07-11".
  - Gregorian adoption differs by country: Catholic states 1582, Britain 1752 (with the year starting 25 March before then), Sweden 1753, Japan 1873, Russia 1918, Greece 1923. Show O.S. and N.S. where they differ.
  - Roman dates before 45 BC are republican-calendar dates with no true solar equivalent.
  - Chinese, Japanese, Korean and Vietnamese era names convert through the DILA Authority Database tables.
  - Islamic dates are tabular before 1924 (Umm al-Qura tables cover only 1924–2077).
- **Machine form**: EDTF (Library of Congress; ISO 8601-2) for uncertain and approximate dates, at levels 0 and 1 in stdlib. A disputed date is a set or a range, never a point. The proposed `entities.json` date object keeps `as_written`, `calendar`, `edtf`, `jdn`, `precision`, `qualifier` (disputed, circa, floruit, tpq, taq), `era_name` and `sources`.
- **Disputes and contested topics**:
  - Attribute each position to named scholars and say which one holds the consensus (Wikipedia's due weight, no false balance).
  - State settled findings as fact.
  - For national narratives, give each side's account with sources from more than one country (Council of Europe multiperspectivity).
- **Classify a conflict before writing the note** (from the CONFLICTS benchmark): an outdated source, a difference of frame (formal reign against actual power), or a genuine scholarly dispute.

## 3. The gold answers, re-verified

- **Caesar, corrected**: born 12 or 13 July 100 BC.
  - 12 July comes from Macrobius (Sat. 1.12.34, quoting Antony's law) and was the official feast. 13 July is inferred from Cassius Dio 47.18, whose reading is itself disputed. Every ancient source implies 100 BC (Suetonius, Jul. 88).
  - Mommsen and others argued for 102 BC (some for 101) from the minimum ages of his offices; Badian (JRS 1959) and Deutsch defend 100 BC, which is the consensus.
  - These are republican-calendar dates.
  - Wikidata holds all of this: the preferred statement is July 100 BC at month precision, flagged disputed, with 12 and 13 July as the earliest and latest dates. A `wdt:` (truthy) query hides the 102 BC statement.
- **Longest-ruling Chinese emperor, corrected**: the Kangxi Emperor has the longest formal reign, 61 years (1661–1722; his era name ran 1662–1722), and was ruled for by regents in his first years.
  - Qianlong formally reigned about 60 years (acceded 1735; his era began 1736). He abdicated on 9 February 1796 so as not to outlast Kangxi, and ruled as Taishang Huang until he died on 7 February 1799, the longest de facto hold on power at about 63 years.
  - Zhao Tuo of Nanyue ruled about 66 years (203–137 BC) but is not counted in the dynastic list. The grader requires neither the regency nor Zhao Tuo.
- **Microsoft, confirmed with a sourcing caveat**: Bill Gates and Paul Allen founded it, styled Micro-Soft, as a partnership on 4 April 1975 in Albuquerque, New Mexico.
  - It moved to Bellevue on 1 January 1979 and was incorporated in Washington on 25 June 1981. The trade name was registered in New Mexico on 26 November 1976.
  - The official sources (the FY2002 10-K, Microsoft's facts page, its 50th-anniversary post of 2025-04-04) give the year and the incorporation date; no official page prints "4 April 1975". The grader must not demand one.

## 4. Tooling

No well-used tool already does historywright's job. The Anthropic official catalog has no history, humanities or Wikidata plugin, skills.sh has no historian skill with real installs, and the MCP registry has nothing for Pleiades, WHG, the Library of Congress or the Internet Archive. What exists to build on or point to:

- **kltng/humanities-skills** (Kwok-leong Tang, 21 skills, active 2026-09): the closest prior art. Its `cjk-calendar` is stdlib Python over a 14 MB SQLite table from the DILA Authority Database (about 220 BCE to 1945, 1,637 eras, regnal years such as 崇禎三年四月初三, sexagenary cycles, JDN pivot). It also has CBDB, CHGIS TGAZ and Wikidata search skills, and ten skills ship `evals/evals.json` in evergreen's shape. Adopt the calendar approach; point to the East Asian skills; use its evals as models. Open question: the DILA data licence (one source says CC BY-SA 3.0).
- **wmde/WikidataMCP**, the official Wikidata MCP at `wd-mcp.wmcloud.org/mcp/` (hybrid vector search, statements with qualifiers and references, SPARQL). It does not handle date precision, calendar model or BCE, which is historywright's niche. Point to it as an optional accelerator. Adopt its companion workflow's rule: discover IDs before writing SPARQL, validate after, never invent a QID.
- **fuzheado/wikipedia-ai-skills** (61 Wikimedia skills with pytest and CI): read `wikimedia-api-access` and `wikidata-reconciliation` before writing hw.py's HTTP layer and QID resolution.
- **54yyyu/zotero-mcp** (5,443 stars, active): the Zotero route. historywright exports sources as CSL-JSON that Zotero imports, and names this for users who keep a Zotero library.
- **google-deepmind/science-skills `literature-search-openalex`** (2,974 installs): the option for heavy scholarly search. hw.py's OpenAlex call stays minimal.
- **lizhuojunx86/chinese-history-mcp**: a pattern to copy. Every claim carries a verbatim quote that is a real substring of the source, plus a review status.
- **The Programming Historian**: "Wikidata for Historical Research" (Hanley, 2026-08) warns about uneven references and P31/P279 inconsistency, and it also skips precision and calendar, which confirms the gap.
- **Out of scope for v1**:
  - Handwriting recognition: Transkribus is paid for API use; Kraken and CHURRO are open, and general VLMs now compete.
  - Research frameworks: GPT Researcher and PaperQA2 are active, and STORM is stale since 2025-09.
- **Python libraries**: convertdate, python-edtf, hijridate, SPARQLWrapper and pywikibot are all replaceable in stdlib for what hw.py needs. Use convertdate and edtf only as test oracles.

## 5. Practice: the lessons that become guards

1. **Never cite what this run did not fetch and read.** Only 26.5% of chatbot-generated references were fully correct across eight models (Cabezas-Clavijo and Sidorenko-Bautista, 2025). The AHA's 2025 principles call an unchecked AI reference in a footnote "never acceptable". Fakes now blend real authors with invented titles (GPTZero found at least 100 in NeurIPS 2025 papers). Guard: a reference appears only if it was retrieved in the run; books and articles are matched on title, author and year together in Crossref, OpenAlex or a catalogue.
2. **A source that exists is not a source that supports.** WikiProject AI Cleanup reports that current models "usually cite real sources but often don't verify that they support the content". "Cited but Not Verified" (2026-05) found live links above 94% but support of 39 to 77%, falling as tool calls grow. Guard: every claim in `sources.json` stores the exact supporting quote, and `hw.py verify` checks it is a substring of the fetched page. A direct quote of a person appears only if its exact words were found in a fetched text naming the speaker.
3. **Wikipedia is a finder, not an authority, and agreement is not independence.** Citogenesis cases (the toaster inventor "Alan MacMasters", 2012–2022, which reached books and a museum) show the press copying Wikipedia and Wikipedia citing it back. Guard: cite the reference beneath the Wikipedia claim after reading it; each source carries `derived_from`; two sources corroborate only if neither is a Wikipedia mirror and they share no `derived_from`.
4. **Do dates in code, never in the model.** Temporal benchmarks (ChronoSense, ChroKnowledge) show models recall dates by memorisation and miss spans. Wikidata's own encodings trap a naive reader (`wdt:` hides disputes; SPARQL shifts BCE years and converts calendars). An "AI Historian" agent that anchored every date to a source sentence scored 86% against 17% for direct prompting on Shiji chronology. Guard: reign lengths, ages, BCE crossings and calendar conversions are computed by `hw.py`; each timeline row carries its source sentence and a range.
5. **Memory is weakest where nobody checks it.** On HiST-LLM (Seshat, NeurIPS 2024) the best model scored 46% (chance 25%), worst for Sub-Saharan Africa, Oceania and recent periods. The language of the prompt changes how a contested event is framed. Guard: lower the default confidence for those regions and look for a regional or non-English scholarly source; on contested topics search in each party's language and name each side.

Three more that shape the packs and the output:

6. **AI history imagery is anachronistic by default.** HistVis (2025) found stereotyped eras and anachronisms across diffusion models; AI "history" videos on YouTube show glazed windows in the 1300s. Guard: pack reference images come only from museum or collection records with an accession number and the object's own date, never from image search or video stills; each pack carries a per-period anachronism checklist from cited sources; generated images are labelled reconstructions.
7. **Agents stop early and do not report it.** Deep Research audits found answers that silently omitted rows, used Statista over the original, and claimed analyses never run (Humphries, 2025; FutureSearch, 2025). Guard: the pack export runs a completeness checklist, each item present or empty with a reason; no count or statistic is claimed without code run in the session.
8. **Never present output as an expert's answer.** r/AskHistorians removes undisclosed AI answers. Guard: answers say they were AI-researched and list their sources.

## 6. Testing

- **Harness**: `claude plugin eval`.
  - Graders: `regex` on the trace or files, `tool_used` with `input_match`, `tool_order`, `file_exists`, `llm`, `baseline`.
  - Mock MCP servers and fixtures make the source answers deterministic.
  - Bash needs an OS sandbox, which on Windows means WSL2; elsewhere use `EG worth --ab`.
  - `hw.py` honours an `HW_HOME` override so the cache case can be graded inside the workspace.
- **Action case**: the trace shows `wbgetclaims` or a `psv:P569` query (not a lone `wdt:P569`) before the answer is written; the cache entry exists with sources and a retrieval date.
- **Verification in `hw.py`**:
  - URL health: HEAD, then GET, then a Wayback check, labelling each URL live, dead, likely hallucinated or unknown (method from arXiv 2604.03173).
  - A DOI check through Crossref or OpenAlex, and a QID check through `wbgetentities`.
  - A quote-span check.
  - `validate-pack`, covering the RFC 7946 GeoJSON rules (lon before lat, closed rings, a swapped-coordinate warning), EDTF level 0 and 1, QID format, and a licence on every reference image.
  - A negative fixture pack that must fail.
- **Grading**:
  - SimpleQA Verified's three-way grade (correct, incorrect, not attempted) for undisputed facts.
  - A dispute rubric from NATCONFQA for disputed ones: every valid answer named, the conflicting pair stated, each side attributed, the reason given.
  - ALCE's definitions of citation recall and precision for the `llm` grader.
- **Cases the research adds**:
  - A non-Western reign (HiST-LLM's weak regions).
  - The October Revolution's Old Style and New Style dates.
  - "Five key books on X" checked against a catalogue.
  - A planted famous misattributed quote.
  - A question whose only online support is Wikipedia mirrors, which must come back unverified.
  - The Caesar answer must not say "99 BC" or "11 July".
- **No benchmark** exists for calendar or disputed-date handling, so those cases are new work. HiST-LLM is the published baseline to cite.

## 7. Proposed layout (for Mark's reply; the research can still move it)

Three skills and a stdlib CLI, the polywright pattern:

- **`historywright`** (hub): answer a question.
  - Intake (a short reference interview: which reading of the question).
  - Route with the era outline.
  - Structured sources first (Wikidata full statements with precision and calendar; places), then follow references to scholarship and primary texts.
  - Corroborate with two independent sources, at least one primary or scholarly.
  - Normalise dates in `hw.py`.
  - Answer with inline citations, a confidence line (what is uncertain, and why), and a "sources disagree" note that classifies the conflict.
  - Write the cache entry.
  - When sources cannot be reached, it says the answer is unverified.
- **`historywright-sources`**: curate the source registry (rank, add, retire, record query recipes, reliability and access notes) and the era outline. This is the evergreen knowledge base. A refresh runs `hw.py probe` against every registry endpoint, because this year's changes were mostly endpoints moving.
- **`historywright-pack`**: export and validate a research pack:
  - `answer.md`, `sources.json` (with quotes), `entities.json` (QIDs, EDTF dates), `places.geojson` (Pleiades, CHGIS, WHG, Cliopatria borders), `timeline.json`;
  - `references/`, with CC0-first museum images and a licence, URL, date, place and accession number for each, plus the anachronism checklist;
  - laid out to polywright's asset contract so `pw.py place` and polywright-references can read it.
- **`hw.py`** commands:
  - `wd` (statements with precision, calendar, rank and qualifiers; SPARQL on both graphs);
  - `wp` (summary, QID, references);
  - `place` (Pleiades, CHGIS, WHG, OHM);
  - `oa` (OpenAlex, optional key);
  - `doi`; `cal` (JDN, Julian/Gregorian, BCE, AUC, tabular Islamic, CJK eras from the DILA table);
  - `cache`; `verify` (URL health, DOI, QID, quote span); `validate-pack`; `probe`; `lint` (registry).
  - One shared fetch layer: a contact User-Agent, a per-host throttle, concurrency 3, Retry-After.
- **Data**:
  - The public repo ships the seed registry (about 60 sources) and a compact era outline.
  - Large tables (DILA, Pleiades dump) download on demand into `~/.historywright/`, which also holds the cache, keys and question history.
  - Size budget: plugin install green under 400 KB, yellow to 1 MB, red above. Era outline green under 12 KB, yellow to 25 KB, red above.
- **Tier**: moderate (60 days), with the scripted probe catching endpoint moves between refreshes.

## 8. Forks for Mark

1. **Free sign-ups.** Everything works keyless at reduced depth. Two free keys would help: an OpenAlex key (more scholarly search per day) and a World Historical Gazetteer token (world places outside the ancient Mediterranean and China). Both are free accounts in Mark's name. Smithsonian (api.data.gov), Europeana and NARA keys are optional extras.
2. **East Asian era conversion.** Recommended: `hw.py cal` downloads the 14 MB DILA table into `~/.historywright/` on first use, with attribution, following kltng's design. The alternatives are to depend on kltng's skill (a third-party install) or to leave CJK eras out of v1.
3. **Paid sources.** None proposed: ctext, JSTOR, eHRAF, the Oxford Classical Dictionary and the rest stay link-out only.
