# Creation pass 2026-10-17: tooling (raw researcher report)

Verbatim report of the evergreen-researcher pass for this track. Synthesis: [../2026-10-17-creation-pass.md](../2026-10-17-creation-pass.md).

## Findings (newest first)

### F1 · 2026-10-16 · 54yyyu/zotero-mcp is the main Zotero MCP server, with nothing close behind
- What: In the MCP registry this is io.github.54yyyu/zotero-mcp v0.15.1, published 2026-10-16. On GitHub it has 5,443 stars, 441 forks and 46 open issues; it was last pushed 2026-10-16 and is MIT-licensed. It reads `zotero.sqlite` directly (local mode), and writes through running Zotero 10+ or the web API. It offers 41 tools by default and 53 in the full set (search, full text, PDF pages, annotations, add by DOI/ISBN), optional semantic search with ChromaDB, a `tests/` directory, and a `zotero-mcp install-skill` command. Other registry entries are much smaller: Combjellyshen/zotero-bridge (2026-02-01), RaulSimpetru/zotero-library-mcp (2026-03-04) and AlejandroArnaud/mcp-for-zotero (hosted, no repository). It passes the quality gate on recent commits and tests. It is a raw-GitHub/registry tier source, and the model that built it is unknown.
- Track: tooling
- Affects: research-pack export and source registry design (a Zotero/CSL-JSON export target)
- Magnitude: n/a (initial)
- Suggested response: point. historywright should export its source registry as CSL-JSON or BibTeX that Zotero imports, and name zotero-mcp for users who keep their library in Zotero. It should not depend on it.
- Sources: https://registry.modelcontextprotocol.io/v0/servers?search=zotero, https://api.github.com/repos/54yyyu/zotero-mcp, https://github.com/54yyyu/zotero-mcp

### F2 · 2026-10-16 · fuzheado/wikipedia-ai-skills: 61 Wikimedia skills with pytest and CI
- What: The repository has 23 stars and 10 forks, was pushed 2026-10-16, is MIT-licensed and has 430 commits. It holds 61 skills for Wikimedia work, including `wikidata` (SPARQL, Wikibase API, dumps), `wikidata-reconciliation` (label to QID with guardrails), `wikidata-vector-search`, `wikipedia-citations`, `wikipedia-reference-verifiability`, `wikisource`, `wikimedia-api-access` (User-Agent, rate limits) and `wikipedia-error-handling`. It ships `tests/` with pytest, CI that checks commands, URLs and snippets against registries, and an A/B study in `research/ab-testing/`. Install counts on skills.sh are tiny (2 to 6 per skill). The owner handle matches Andrew Lih's long-standing Wikimedia handle, but that is inferred, not read.
- Track: tooling
- Affects: the Wikidata/Wikipedia access sections of hw.py (User-Agent, retries, reconciliation guardrails)
- Magnitude: n/a (initial)
- Suggested response: point. Read `wikidata-reconciliation` and `wikimedia-api-access` before writing hw.py's QID resolution and HTTP layer.
- Sources: https://github.com/fuzheado/wikipedia-ai-skills, https://api.github.com/repos/fuzheado/wikipedia-ai-skills, https://skills.sh/api/search?q=wikidata

### F3 · 2026-10-15 · OpenAlex now runs on API keys and a daily dollar budget
- What: The help page ("Last updated October 15, 2026") says basic queries still work without a key. A free key raises the daily budget tenfold and is required for cursor paging past the first page. A free account gets "$1 a day". Rate limits are 10 requests per second without a key, 30 with a free key, 50 on an annual plan, and 1 per second for semantic search. The old "polite pool" `mailto` is not mentioned. developers.openalex.org and docs.openalex.org now 301 to help.openalex.org.
- Track: tooling (dependency)
- Affects: the hw.py OpenAlex command (key handling, paging)
- Magnitude: n/a (initial)
- Suggested response: adopt. Read an optional `OPENALEX_API_KEY` from the environment, never page past page 1 without one, and add an eval case that a keyless run returns page 1 and states that a key is needed for more.
- Sources: https://help.openalex.org/how-to-use-the-api/rate-limits-and-authentication

### F4 · 2026-10-15 · Most-installed OpenAlex skill is Google DeepMind's
- What: On skills.sh, google-deepmind/science-skills `literature-search-openalex` has 2,974 installs. The repository has 3,278 stars, was created 2026-05-13, pushed 2026-10-15, and is Apache-2.0. Its README says OpenAlex needs an API key and that dependencies come through `uv` (not stdlib). The same search shows k-dense-ai/scientific-agent-skills `paper-lookup` (2,135) and `citation-management` (2,115), and lingzhi227 `literature-search` (2,563). All of them aim at science literature, not historiography. I could not read the GDM SKILL.md (raw path 404).
- Track: tooling
- Affects: the OpenAlex part of hw.py
- Magnitude: n/a (initial)
- Suggested response: point. Name it as the option for heavy scholarly search; keep hw.py's own OpenAlex call minimal and stdlib.
- Sources: https://skills.sh/api/search?q=openalex, https://api.github.com/repos/google-deepmind/science-skills, https://github.com/google-deepmind/science-skills

### F5 · 2026-10-13 · cyanheads publishes current TypeScript MCP servers for Wikidata, Wikipedia and OpenAlex
- What:
  - wikidata-mcp-server v0.2.0 (2026-10-13; 3 stars) has 7 tools, including `wikidata_get_statements` with qualifiers and references, and `wikidata_resolve_external_id`, which normalizes DOI, ORCID and OpenAlex IDs and returns `match=null` with a warning that null is not proof of absence. SPARQL is SELECT-only, capped at 64 KB, 60 s, and 60 requests per minute.
  - wikipedia-mcp-server v0.2.6 (2026-10-08; 4 stars) does search, summaries, sections, nearby pages and language editions.
  - openalex-mcp-server v0.6.21 (16 stars, pushed 2026-09-30).
  - All three have tests and need Bun or Node 24. None documents how Wikidata time precision, calendar model or BCE dates are handled.
- Track: tooling
- Affects: none in the core; an optional-MCP note
- Magnitude: n/a (initial)
- Suggested response: note. Their stars are low and Node is required. The "null is not proof of absence" rule for external IDs is worth copying.
- Sources: https://registry.modelcontextprotocol.io/v0/servers?search=wikidata, https://github.com/cyanheads/wikidata-mcp-server, https://registry.modelcontextprotocol.io/v0/servers?search=wikipedia, https://api.github.com/repos/cyanheads/openalex-mcp-server

### F6 · 2026-09-27 · kltng/humanities-skills is the closest prior art: 21 historian skills, stdlib scripts and evals.json
- What: Kwok-leong Tang's repository has 7 stars and its last commits are dated 2026-09-27.
  - It ships 21 skills: cbdb-api/cbdb-local (China Biographical Database), jbdb-api, chgis-tgaz/tgaz-sqlite (CHGIS Temporal Gazetteer), `cjk-calendar`, `historical-timeline` (TimelineJS3 with BCE), `historical-map` (Leaflet), loc-catalog, hathitrust-catalog, europeana-collections, harvard/columbia/NLB catalogs, `wikidata-search`, zotero-local, archival-entity-linking (TEI to Wikidata), tei-validator, argue-against-me and human-eval-review.
  - `cjk-calendar` is stdlib Python 3.10+ over a one-time 14 MB SQLite download from the DILA Authority Database. It covers Chinese, Japanese, Korean and Vietnamese lunisolar calendars from about 220 BCE to 1945, with 1,637 eras and 131,808 months. It parses regnal years such as 崇禎三年四月初三, 元年 and 廿/卅, and handles sexagenary cycles. It uses JDN as the pivot and astronomical year numbering, and returns every match for an ambiguous era name. The DILA data licence is not stated.
  - `wikidata-search` is a stdlib script that uses the Action API, the vector DB at wd-vectordb.wmcloud.org (403 without a User-Agent), EntityData and WDQS. It honours maxlag and Retry-After, and notes that a maxlag error comes back as HTTP 200.
  - Ten skills ship `evals/evals.json` in the same shape evergreen uses. The wikidata-search file has 4 cases and 17 expectations, including a cross-database Su Shi lookup across CBDB, TGAZ and Wikidata.
- Track: tooling
- Affects: the calendar conversion (Chinese era names) and gazetteer scope of hw.py, and the evals design
- Magnitude: n/a (initial)
- Suggested response: adopt the cjk-calendar approach: either delegate to it, or reuse the DILA table pattern in hw.py once the data licence is checked. Point to the CBDB/CHGIS/TEI skills for East Asian depth. Use its eval cases as models for historywright's suite.
- Sources: https://github.com/kltng/humanities-skills, https://api.github.com/repos/kltng/humanities-skills/commits?per_page=5, https://raw.githubusercontent.com/kltng/humanities-skills/main/cjk-calendar/SKILL.md, https://raw.githubusercontent.com/kltng/humanities-skills/main/wikidata-search/SKILL.md, https://raw.githubusercontent.com/kltng/humanities-skills/main/wikidata-search/evals/evals.json

### F7 · 2026-09-21 · The official Wikidata MCP from Wikimedia Deutschland (Wikidata Embedding Project)
- What:
  - The endpoint is `https://wd-mcp.wmcloud.org/mcp/`, from the wmde/WikidataMCP repository (BSD-3, 35 stars, created 2025-06-24, pushed 2026-09-21, 1 open issue, no visible tests or evals).
  - It has six tools: `search_items` (hybrid vector plus keyword), `search_properties`, `get_statements` (no qualifiers or references), `get_statement_values` (qualifiers, references, all ranks), `get_instance_and_subclass_hierarchy` and `execute_sparql`.
  - Changelog: released 2025-10. Hybrid search 2026-01. Wikibase MCP 2026-05. External-ID exclusion 2026-07. Language fallback 2026-08.
  - The companion OpenCode plugin (dpriskorn) runs an 8-step grounded workflow: discover IDs, inspect, generate SPARQL, then validate items, statements and classes, looping up to 3 times. Its rule is "never invents QIDs or PIDs".
  - Neither documents date precision, calendar model or BCE handling. That is historywright's niche.
- Track: tooling
- Affects: the Wikidata SPARQL section (whether to call the MCP or WDQS directly)
- Magnitude: n/a (initial)
- Suggested response: point to the MCP as an optional accelerator. hw.py keeps direct WDQS plus `wikibase:timePrecision` and `wikibase:timeCalendarModel` handling. Adopt the "discover IDs before writing SPARQL, validate after" rule as a step, with an eval case: a query that uses a guessed QID fails the case.
- Sources: https://www.wikidata.org/wiki/Wikidata:MCP, https://github.com/wmde/WikidataMCP, https://api.github.com/repos/wmde/WikidataMCP, https://github.com/dpriskorn/opencode-wikidata-sparql-workflow

### F8 · 2026-09-09 (page edit) · The WDQS graph split leaves scholarly articles off query.wikidata.org
- What: Since 9 May 2025, query.wikidata.org holds the main graph only. Scholarly articles (P31 Q13442814 or P13046) are at query-scholarly.wikidata.org. The legacy full-graph endpoint was announced "until December 2025". A Blazegraph migration is underway, and the graphs will not be re-merged. Queries that span both need federation.
- Track: tooling (dependency)
- Affects: the hw.py SPARQL command and the source registry
- Magnitude: n/a (initial)
- Suggested response: adopt. Put both endpoints in the source registry, and add an eval case that a query for a scholarly article routes to the scholarly endpoint or federates.
- Sources: https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/WDQS_graph_split

### F9 · 2026 · Wikimedia's new rate limits make the User-Agent mandatory in practice
- What: The new 2026 limits are 10 requests per minute for unidentified clients, 200 per minute for bots with a compliant User-Agent (contact URL or email), and 2,000 for established authenticated editors. Clients should keep concurrency at 3 or less, honour Retry-After, and wait at least 5 s when it is absent. The limits apply to both the REST and Action APIs, and the page says they are "subject to experimentation and change". kltng's skill independently notes that the Wikidata vector DB and WDQS return 403 without a User-Agent.
- Track: tooling (dependency)
- Affects: the hw.py HTTP layer and the answer cache's reason to exist
- Magnitude: n/a (initial)
- Suggested response: adopt. Give hw.py one shared fetch function with a configurable contact User-Agent, at most 3 concurrent requests, and Retry-After handling. Add a smoke-test case that checks the User-Agent header is present.
- Sources: https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits

### F10 · 2026-09-29 and earlier · State of VLM handwriting recognition (HTR): general VLMs now compete, open models beat them on cost
- What:
  - arXiv 2609.37195 (2026-09-29) finds that in-context VLM HTR, without fine-tuning, competes with traditional HTR under domain shift.
  - CHURRO (Stanford OVAL, arXiv 2509.19768; repository 82 stars, last push 2026-04-18) is a 3B open VLM. It scored 70.1% normalized Levenshtein on handwriting, versus Gemini 2.5 Pro 6.5 points lower, at 15.5x the cost-effectiveness.
  - Earlier benchmarks show Claude 3.5 Sonnet and GPT-4o beating Tesseract, EasyOCR and TrOCR, but with no consistent edge over Transkribus (2503.15195). Another paper reports 5.7 to 7% character error rate for multimodal LLMs, which LLM correction brought to 1.8% (2411.03340).
  - Kraken is active: 1,084 stars, pushed 2026-10-12, Apache-2.0.
  - Not verified this pass: eScriptorium, PERO OCR and Calamari releases.
- Track: tooling
- Affects: scope (HTR is not in hw.py's plan)
- Magnitude: n/a (initial)
- Suggested response: note. Keep HTR out of v1. The research pack can mark a source "image only: transcribe with Claude vision or Transkribus", with a check that keeps the image next to its transcription.
- Sources: https://export.arxiv.org/api/query?search_query=abs:handwritten+AND+abs:historical+AND+(abs:LLM+OR+abs:VLM+OR+abs:multimodal)&sortBy=submittedDate&sortOrder=descending&max_results=15, https://api.github.com/repos/stanford-oval/Churro, https://api.github.com/repos/mittagessen/kraken

### F11 · 2026 · Transkribus pricing
- What:
  - Free: €0, 50 credits a month (about 50 pages).
  - Scholar: €99 a year for 900 credits.
  - Team: €449 a year for 1,500 credits and 5 seats.
  - Organisation: quote only.
  - The API comes only with the paid plans, and API jobs cost half the credits of the same job in the app. Handwriting recognition is 1 credit a page; line detection 0.25.
  - The page contradicts itself: its FAQ gives Team at €399 a year and Scholar at €19.99 a month. The only date on the page is "© 2026".
- Track: tooling
- Affects: none (HTR is out of scope)
- Magnitude: n/a (initial)
- Suggested response: point (as the paid HTR route, with the price caveat)
- Sources: https://www.transkribus.org/plans

### F12 · 2026-09 · Python date libraries, and which ones stdlib can replace
- What:
  - convertdate 2.5.1 (2026-09-13) depends on pymeeus. It covers Julian, Gregorian, Hebrew, Islamic, Persian, Coptic, French Republican, Mayan and JDN, but not Chinese. Its arithmetic calendars (Julian, Gregorian, JDN, tabular Islamic, Hebrew, Coptic) are easy to rewrite in stdlib. Its astronomical Persian calendar is the hard part.
  - edtf (python-edtf) 5.0.2 (2026-09-17) depends on pyparsing and dateutil, and implements EDTF levels 0 to 2. A regex subset for levels 0 and 1 (uncertain `?`, approximate `~`, unspecified `X`, intervals) is stdlib-feasible. Level 2 is not worth hand-rolling.
  - hijridate 2.6.0 (2026-01-06) has zero dependencies, but its Umm al-Qura tables cover only 1924 to 2077. Earlier dates need the tabular Islamic calendar.
  - sxtwl 2.0.7 is a C++/SWIG extension, so it is out for stdlib. The DILA SQLite table route (F6) covers Chinese, Japanese, Korean and Vietnamese with stdlib `sqlite3`.
  - SPARQLWrapper 2.0.0 was last released 2022-03-13 and needs rdflib. It is not needed: urllib with `format=json` replaces it.
  - pywikibot, wikipedia-api, jdcal and astropy Time are all replaceable by urllib plus about 20 lines of JDN code (jdcal and astropy were not re-fetched; this is from known behaviour).
- Track: tooling
- Affects: the calendar conversion and EDTF design of hw.py
- Magnitude: n/a (initial)
- Suggested response: adopt the stdlib plan. Make JDN the pivot, implement Julian, Gregorian and tabular Islamic in pure Python, use DILA tables for CJK eras, and parse EDTF levels 0 and 1 only. Name convertdate and edtf as optional cross-checks in evals (e.g. a golden-value case: 1582-10-04 Julian is followed by 1582-10-15 Gregorian, and 1 BCE is astronomical year 0).
- Sources: https://pypi.org/pypi/convertdate/json, https://pypi.org/pypi/edtf/json, https://pypi.org/pypi/hijridate/json, https://pypi.org/pypi/sxtwl/json, https://pypi.org/pypi/SPARQLWrapper/json

### F13 · 2026-08-07 · Programming Historian has a new Wikidata lesson that skips precision and calendar model
- What: "Wikidata for Historical Research" by Will Hanley (FSU), DOI 10.46430/phen0133, warns that references are uneven (one presidency date was sourced only from English Wikipedia), that P31 versus P279 taxonomies are inconsistent, that elite history is over-represented, and that chatbot SPARQL is unoptimized. It does not cover `wikibase:timePrecision`, `timeCalendarModel` or BCE. Other 2025-2026 lessons cover TEI part 1 (2025-12-10), nodegoat (2026-01-28) and IIIF manifests (2026-09-24). The gazetteer lessons are older: WHG (2022) and a gazetteer-building lesson (2024).
- Track: tooling (reference)
- Affects: Wikidata guidance; confirms the date-precision gap is real
- Magnitude: n/a (initial)
- Suggested response: point (cite as background reading), and put the lesson's pitfalls into the SKILL.md as guards: report reference counts per statement, and check both P31 and P279.
- Sources: https://programminghistorian.org/en/lessons/wikidata-for-historical-research, https://programminghistorian.org/en/lessons/

### F14 · 2026-08-03 · chinese-history-mcp: cited answers labelled with review status
- What: lizhuojunx86/chinese-history-mcp (registry v0.3.0; 3 stars; code MIT, data CC BY 4.0) has 4 tools over 9 classical texts (史记 through 资治通鉴). Every result carries a book, chapter and paragraph citation plus a `review_status` label (machine bulk-approved, draft, or consensus). Each `evidence_quote` is a real substring of the source, and tests enforce read-only access and the labelling.
- Track: tooling
- Affects: answer cache and source registry design
- Magnitude: n/a (initial)
- Suggested response: note. Copy the pattern that every claim carries a verbatim quote plus a provenance status, and add an eval that checks each quote is a substring of the fetched source.
- Sources: https://registry.modelcontextprotocol.io/v0/servers?search=history, https://github.com/lizhuojunx86/chinese-history-mcp

### F15 · 2026 · Gazetteer and archive APIs: what is live
- What:
  - Pleiades publishes a daily full JSON dump (`atlantides.org/downloads/pleiades/json/pleiades-places-latest.json.gz`) and per-place JSON at `pleiades.stoa.org/places/{ID}/json`. It is CC BY 3.0, and its latest numbered release is 4.1 (2025-05-28). Legacy CSV is deprecated.
  - World Historical Gazetteer is in a "Version 3 beta" (WorldHistoricalGazetteer/website pushed 2026-10-14). Every API documentation URL I tried returned 404.
  - The Chronicling America legacy API (2007 to 2025) is retired; the collection is now "accessible exclusively via the loc.gov API".
  - The ctext API is subscription-only.
- Track: tooling (dependency)
- Affects: the place lookup and source registry in hw.py
- Magnitude: n/a (initial)
- Suggested response: adopt the Pleiades per-place JSON and the loc.gov route in the source registry. Treat WHG as unverified until its v3 API documentation is found. Mark ctext as needing a subscription.
- Sources: https://pleiades.stoa.org/downloads, https://api.github.com/orgs/WorldHistoricalGazetteer/repos?sort=pushed&per_page=10, https://www.loc.gov/apis/additional-apis/chronicling-america-api/, https://ctext.org/tools/api

### F16 · 2026-10 · Skill catalogs have no historian skill with real installs
- What:
  - The Anthropic official plugin catalog (about 315 entries in marketplace.json) has no history, humanities, Zotero, Wikidata, library or OCR plugin. The research-adjacent ones are exa, tavily and youdotcom.
  - On skills.sh the scholarship-relevant hits are small: nomadamas/k-skill `joseon-sillok-search` (6,707, probably inflated by its bundle); garethmanning education `historical-*` skills (about 112 each, for teaching); bitwize-music `researchers-historical` (227); useosint `wayback-archives` (599); emaynard family-history-planning (54 installs, 118 stars, built on the Genealogical Proof Standard and Evidence Explained, no evals).
  - Generic fact-check skills lead on installs: shubhamsaboo `fact-checker` 3,297; jamditis `fact-check-workflow` 560.
  - The MCP registry has no server for Pleiades, WHG, Internet Archive, LoC or Chronicling America. Europeana has only pipeworx-io/mcp-europeana, a generic wrapper.
- Track: tooling
- Affects: positioning (no well-used tool already does historywright's job)
- Magnitude: n/a (initial)
- Suggested response: note. emaynard's GPS method is worth pointing to for any genealogy questions.
- Sources: https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/.claude-plugin/marketplace.json, https://skills.sh/api/search?q=historical, https://skills.sh/api/search?q=history, https://skills.sh/api/search?q=genealogy, https://skills.sh/api/search?q=fact-check, https://github.com/emaynard/claude-family-history-research-skill, https://registry.modelcontextprotocol.io/v0/servers?search=europeana

### F17 · 2026-10 · Research-agent frameworks: two active, STORM stale
- What: GPT Researcher has 30,140 stars and was pushed 2026-10-10. PaperQA2 (Future-House/paper-qa) has 9,399 stars, 156 open issues and was pushed 2026-10-13; it is built for science PDFs. STORM (stanford-oval) has 31,655 stars and 111 open issues, but its last push was 2025-09-30, so it fails the 90-day gate. Not checked this pass: OpenScholar, and the vendor assistants (JSTOR, Gale, ProQuest, Transkribus Sites).
- Track: tooling
- Affects: none (historywright is a skill plus CLI, not a framework)
- Magnitude: n/a (initial)
- Suggested response: note. STORM's outline-then-cite approach is still a useful design reference for long answers.
- Sources: https://api.github.com/repos/assafelovic/gpt-researcher, https://api.github.com/repos/Future-House/paper-qa, https://api.github.com/repos/stanford-oval/storm

### F18 · 2026-03-27 · zzaebok/mcp-wikidata has gone quiet
- What: 49 stars, MIT, last pushed 2026-03-27, 4 open issues. That is more than 90 days, so it fails the gate.
- Track: tooling
- Affects: none
- Magnitude: n/a (initial)
- Suggested response: note (superseded by wmde's official server, F7)
- Sources: https://api.github.com/repos/zzaebok/mcp-wikidata

## Overall magnitude: n/a (initial)

## Open questions:
- New: what is the World Historical Gazetteer v3 public API? Every documentation URL tried returned 404.
- New: what licence covers the DILA calendar data that kltng's cjk-calendar downloads? This decides whether hw.py can bundle or fetch it.
- New: does query-legacy-full.wikidata.org still answer after December 2025?
- New: what is Transkribus's real Team price (€449 on the plan card vs €399 in the FAQ)?
- Still open (not reached): Semantic Scholar and Internet Archive MCP servers, eScriptorium and PERO OCR releases, OpenScholar, JSTOR/Gale/ProQuest AI assistants, Europeana API key rules, and current versions of lunardate, cnlunar and jdcal.

## Search plan notes:
- The WebSearch budget ran out after 4 successful queries (3 more were refused: shared limit of 200 per turn). Everything else came from direct fetches of primary sources and registry or catalog APIs.
- Fetches that worked well:
  - `registry.modelcontextprotocol.io/v0/servers?search=` with wikidata, zotero, openalex, history, wikipedia, europeana and archive
  - `skills.sh/api/search?q=` (returns install counts; worked for wikidata, history, historical, openalex, genealogy and fact-check)
  - `api.github.com/repos/X` for stars and pushed_at
  - `git/trees/main?recursive=1` to find evals.json files
  - the arXiv export API for HTR papers
- Noise: the registry search for "history" and "library" is mostly chat history and code libraries. The skills.sh search for "history" is mostly git and chat history.
- Better sources found: kltng/humanities-skills, fuzheado/wikipedia-ai-skills, the wikidata.org/wiki/Wikidata:MCP changelog, the Wikimedia rate-limits page and the WDQS graph-split page.
- Forums to add next time: Wikidata Project chat or the wikidata mailing list for MCP and WDQS backend news, WHG's GitHub (WorldHistoricalGazetteer/website) and the OpenAlex help-center changelog.

## Tracks covered: subject: 0 queries (not assigned) · tooling: 4 web searches that returned results + 3 refused, and 30+ registry, catalog and repository API lookups · practice: 0 (not assigned; the GPS genealogy method in F16 is incidental) · testing: 0 dedicated (eval cases are folded into F3, F6, F7, F8, F9, F12 and F14)

## Upcoming events: none with a firm date. The Wikidata Query Service Blazegraph migration is underway with no date; the Wikimedia 2026 rate limits are "subject to change".

## Nothing changed: no (creation pass)

## Cost: searches 7 (4 answered, 3 refused by budget) · fetches 73 · tool calls 82
