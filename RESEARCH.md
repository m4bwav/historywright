# Research: historywright

Findings that back the three historywright skills (`skills/historywright`, `-sources`, `-pack`) and `hw.py`. Changes they cause are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons in [LEARNINGS.md](LEARNINGS.md); test runs in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: the installed evergreen plugin's `protocol/PROTOCOL.md`.

Topic: answering history questions from sources, not model memory; a source registry of where historical answers live; research packs for 3D and video. Proposed tier `moderate`. Creation pass 2026-10-17; synthesis in [ai-docs/research/2026-10-17-creation-pass.md](ai-docs/research/2026-10-17-creation-pass.md), raw reports in [ai-docs/research/2026-10-17-creation-pass/](ai-docs/research/2026-10-17-creation-pass/).

## Current understanding

- **Where answers live.** Wikidata is the best structured route for who, when and with whom. Read its full statements (precision, calendar model, rank, qualifiers P1480, P1319, P1326) and cite the references on them. Never cite the truthy `wdt:` value alone: it hides disputed alternatives.
- **Wikipedia** is a finder and a QID lookup (REST summary gives `wikibase_item`). Cite the sources beneath it, never the article. None of the routing articles (outlines, timelines, lists) is featured or good. (R-20261017-2, -3)
- **Places**: Pleiades (daily dump, per-place JSON, CC BY), CHGIS TGAZ for China, PeriodO for period definitions (CC0) and Cliopatria for dated polity borders (CC BY 4.0, with QIDs) are open and current. World Historical Gazetteer needs a free token and has a daily quota. (R-20261017-4)
- **Access is moving fast.** Wikimedia now rate-limits clients without a contact User-Agent to 10 requests a minute. The Wikidata Query Service is split into main and scholarly graphs. OpenAlex runs on keys and a daily budget. Since 2024 the Met, Rijksmuseum, Getty, Chronicling America, HathiTrust, JSTOR (Constellate), Trove and NARA all retired or moved APIs, and ctext went subscription-only. Bot walls block many heritage sites; documented JSON APIs mostly answer. A scripted endpoint probe is worth more than prose about endpoints. (R-20261017-5, -6, -7)
- **Images for packs**: the CC0 open-access APIs (Met v1.1, Cleveland, Art Institute of Chicago, Getty, Smithsonian, Rijksmuseum) are reliable. They are thin on late-Republican Roman military gear, so a Roman legionary pack leans on Wikimedia Commons and Europeana with per-file licences. British Museum and Science Museum images are non-commercial. (R-20261017-8)
- **Regional coverage is uneven.** China is well served. India, Africa and Latin America have browse-only national archives, so answers there rest on scholarship and Wikidata references and should say so. (R-20261017-6)
- **Dates must be computed, not recalled.**
  - JDN is the pivot; astronomical years (1 BC = 0).
  - Wikidata JSON uses historical numbering, while RDF/SPARQL uses XSD year 0 converted to Gregorian.
  - Gregorian adoption differs by country.
  - Roman dates before 45 BC are republican-calendar dates.
  - CJK era names convert through the DILA tables.
  - Islamic dates before 1924 are tabular.
  - EDTF levels 0 and 1 are the machine form; a disputed date is a set or a range. (R-20261017-9, -10)
- **Method**: tertiary to route, follow footnotes, cite secondary or primary; source, contextualise, corroborate; a short reference interview pins down which reading of the question is answered; attribute disputes to named scholars and name the consensus; no false balance on settled findings. (R-20261017-11)
- **Gold answers**: Caesar is 12 or 13 July 100 BC, with the 102 BC argument (Mommsen) noted. Kangxi has the longest formal reign, 61 years; Qianlong holds the longest de facto power, about 63 years to 1799. Microsoft was founded 4 April 1975 by Gates and Allen in Albuquerque, but no official page prints the day. (R-20261017-12)
- **Tooling**: nothing well-used does this job. The closest prior art is kltng/humanities-skills (stdlib CJK calendar over DILA, CBDB, CHGIS, evals). The official Wikidata MCP exists but ignores precision and calendar. Zotero-mcp is the bibliography route. (R-20261017-13, -14)
- **Practice** (confident; many independent sources agree):
  - references from memory are mostly wrong;
  - real-but-unsupporting citations are now the main failure;
  - Wikipedia agreement is not independence;
  - models recall dates by memorisation;
  - memory is weakest for Africa, Oceania and recent periods;
  - AI period imagery is anachronistic;
  - agents stop early silently.
  
  Each is a guard in the skill text. (R-20261017-15 to -21)
- **Testing**: `claude plugin eval` with fixture mocks; quote-span, URL-health, DOI and QID checks in `hw.py verify`; RFC 7946 and EDTF checks in `validate-pack`; SimpleQA-style grading for undisputed facts and a NATCONFQA-style rubric for disputed ones. No benchmark exists for calendar or disputed-date handling. (R-20261017-22 to -24)

## Open questions

- Resolved 2026-10-17 (R-20261017-26): WHG's `suggest/entity?prefix=` and `api/index/?name=` answer with a Bearer token; `api/places/` is 404. v3 documentation pages still unchecked.
- Resolved 2026-10-17: the DILA Time Authority data is CC BY-SA 3.0 Unported (COPYING.rst in github.com/DILA-edu/Authority-Databases; the site footer says CC BY-SA 2.5 Taiwan). hw.py may download it on demand and build the table locally, with attribution. kltng/calendar_converter's repository has no licence, so do not fetch its prebuilt db.
- Resolved 2026-10-17 (R-20261017-25): `action=parse` HTML gives every footnote as `<li id="cite&#95;note-...">` with a `reference-text` span; `hw.py wp refs --near` maps a sentence to its footnotes. Parsoid untested.
- Seshat Polaris-2026 licence page not read (site states CC BY-NC-SA).
- Do Gallica, DPLA, QDL and HathiTrust 403s clear with an honest User-Agent? Test with hw.py's own agent.
- Islamic AH conversion beyond tabular, Japanese nengō before 1873, the Wanli reign figure, current CMOS edition, Smithsonian Human Origins terms, Paris Musées and National Palace Museum image terms: unsearched (budget ran out).
- Is the IntCal20 successor out (hoped 2026–2027)?
- The exact r/AskHistorians AI rule text (reddit is blocked to the fetcher; use RSS).

## Search plan

Four tracks; every refresh runs at least one query on each (scope each to the period since the last refresh; add the year). Run `hw.py probe` first: a dead or moved endpoint is the most likely change.

Subject (where answers live, how to query them, the method):

- `site:mediawiki.org Wikimedia APIs changelog <month year>`; `Wikidata Query Service graph split OR Blazegraph OR QLever <year>`
- Each registry source's own API page or changelog: help.openalex.org, crossref.org/blog, metmuseum.github.io, data.rijksmuseum.nl/docs, loc.gov/apis, docs.whgazetteer.org, pleiades.stoa.org/news/changes/RSS, getty.edu/research/tools/vocabularies/obtain
- `"<source>" API deprecated OR retired OR "rate limit" <year>` for the top fifteen registry sources
- `Gregorian adoption OR calendar conversion historians <year>`; `EDTF ISO 8601-2 revision <year>`
- Official forums and change feeds: Wikidata Project chat and the wikidata mailing list, mediawiki-api-announce, Phabricator (WDQS, Wikibase), blog.whgazetteer.org and github.com/WorldHistoricalGazetteer, community.crossref.org, the Europeana API Google Group, the IHR blog (BBIH), GLAM Workbench (Trove), current.ndl.go.jp (NDL), the LoC Signal blog, infoDOCKET. Search announcements first, then known issues, since the last check.

Tooling (skills, plugins, MCP servers, scripts built for this subject):

- `https://registry.modelcontextprotocol.io/v0/servers?search=` with wikidata, wikipedia, openalex, zotero, europeana, history, archive (worked well; "history" and "library" are mostly noise)
- `https://skills.sh/api/search?q=` with wikidata, historical, history, openalex, genealogy, fact-check (returns install counts)
- `api.github.com/repos/<owner>/<repo>` for stars and pushed_at of kltng/humanities-skills, wmde/WikidataMCP, fuzheado/wikipedia-ai-skills, 54yyyu/zotero-mcp, cyanheads wikidata/wikipedia/openalex servers, lizhuojunx86/chinese-history-mcp
- `raw.githubusercontent.com/anthropics/claude-plugins-official/main/.claude-plugin/marketplace.json` searched for history, humanities, wikidata, zotero
- `path:SKILL.md historian OR "historical research" OR wikidata` on GitHub, sorted by recently updated; the Programming Historian lessons index for new lessons
- Supersession sweep: `history skill OR "mcp server" deprecated OR archived <year>`; archive flag on every tool named here

Most discussed and the converged thinking:

- `generativehistory.substack.com` (Mark Humphries) archive; techpolicy.press and r/AskHistorians (via RSS) on AI answers; hn.algolia.com `historian AI` sorted by date
- OpenAlex `works?search=LLM historical knowledge OR history benchmark&sort=cited_by_count:desc&filter=from_publication_date:<last check>`

Practice:

- `historians test "deep research" OR agent <year>`; `site:arxiv.org LLM historical OR history benchmark OR hallucination <year>`
- `site:en.wikipedia.org WikiProject AI Cleanup`; Wikipedia List of citogenesis incidents (new entries)
- `AI generated history video OR images anachronism <year>`; incidentdatabase.ai and oecd.ai incidents searched for history, quotes, citations
- AHA (historians.org) AI statements; Royal Historical Society; anthology.ach.org proceedings

Testing:

- `code.claude.com/docs/en/plugin-evals` (graders, mocks, sandbox) and agentskills.io evaluating-skills
- `site:arxiv.org citation verification OR "fact check" deep research agent <year>`; `"conflicting sources" QA benchmark <year>`
- SimpleQA Verified and FACTS leaderboards on Kaggle; promptfoo factuality, Inspect `model_graded_fact`, DeepEval faithfulness docs
- `path:SKILL.md wikidata OR historian evals` on GitHub (kltng's evals.json is the model)

Best sources (primary first): the Wikimedia API changelog and rate-limit pages, Wikidata Help:Dates and the WDQS graph-split page, each source's own API docs, live API calls (cheap and decisive), the MCP registry and skills.sh APIs, GitHub's API, Humphries' substack, arXiv HTML. Sources that proved noisy: API directories (apis.io, jentic, publicapi.dev, freeapihub), arXiv mirrors (themoonlight, alphaxiv, catalyzex), quote sites, SEO listicles; searches naming Devereaux without `site:acoup.blog`. Fetch-refused (route through fetchwright if needed): Britannica, GatesNotes, developer.nytimes.com, open-platform.theguardian.com, si.edu, pro.europeana.eu, Trove, glam-workbench.net.

## Findings log

Newest first within the day. Track is subject, tooling, practice, or testing. Creation-pass magnitudes are `n/a (initial)`. Their `Applied:` lines name where the Step 2 build (2026-10-17) used them: SKILL.md guards cite the `R-` id in place.

### R-20261018-3 · 2026-10-18 · Build: OpenHistoricalMap's Overpass terms, limits and date convention
- Summary: OHM publishes no rate limit or usage policy for its Overpass API: the OpenHistoricalMap/Overpass wiki page gives only the endpoint and examples, and openhistoricalmap.org/copyright covers the data (CC0 except features with a `license` tag; attribution appreciated, not required). The endpoint's `/api/status` reported "Rate limit: 2" (slots per client) on 2026-10-18. With no OHM figure, hw.py follows the general Overpass guidance (about 10,000 requests and 1 GB a day per client; after a 429 wait at least 30 s, since repeat 429s get clients banned): one attempt per query, a 5 s pace, exact tag matches only, `[timeout:25]`. OHM dates: YYYY, YYYY-MM or YYYY-MM-DD in proleptic Gregorian with astronomical years (1 BC = 0000, 2 BC = -0001); qualifiers go in `start_date:edtf`. Live 2026-10-18: "Kingdom of Prussia" year 1800 returned the 1795-10-24 to 1802-10-08 boundary (Q27306); "Roman Republic" year -44 returned the -0058 to -0042 boundary and the -0509 to -0027 chronology (Q17167), each query under 3 s.
- Track: tooling
- Sources: https://wiki.openstreetmap.org/wiki/OpenHistoricalMap/Overpass, https://www.openhistoricalmap.org/copyright, https://overpass-api.openhistoricalmap.org/api/status, https://dev.overpass-api.de/overpass-doc/en/preface/commons.html, https://wiki.openstreetmap.org/wiki/Overpass_API, https://wiki.openstreetmap.org/wiki/OpenHistoricalMap/Tags/Key/start_date
- Magnitude: minor
- Applied: skills/historywright/scripts/hw_sources.py (`_ohm`, `_ohm_year`), skills/historywright-sources/references/registry.json (ohm: route, pace, notes)

### R-20261018-2 · 2026-10-18 · Build: Wayback CDX `collapse=digest` drops repeated captures
- Summary: The CDX server's README: "Only show unique captures by digest (note that only adjacent digest are collapsed, duplicates elsewhere in the cdx are not affected)", example `cdx?url=archive.org&collapse=digest`. Tested live 2026-10-18 with hw.py's User-Agent: `url=microsoft.com&output=json&limit=6` returned the 19961020014044 capture six times; with `&collapse=digest` it returned six different captures (20, 22, 25 (two), 26 October 1996, then 5 December 1998).
- Track: tooling
- Sources: https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md
- Magnitude: minor
- Applied: skills/historywright-sources/references/registry.json (wayback search url and notes)

### R-20261018-1 · 2026-10-18 · Build: keyless paces held under each source's documented public limit
- Summary: The owner ruled on 2026-10-18 that live keyless calls are fine as long as they break no terms and risk no ban. Checked against the limits already recorded: Wikimedia allows 200 requests a minute to a client whose User-Agent names the tool, version and a contact (email or URL; hw.py always sends the repository URL), so 0.3 s (exactly 200/min) became 0.35 s for Wikidata, Wikipedia and Commons. Crossref's public pool (no `mailto`) allows 5 single-record requests a second, so 0.1 s became 0.2 s. OpenAlex keyless is capped at 10 a second, so 0.1 s became 0.15 s. The Wayback availability API (`archive.org/wayback/available`) answered 429 on every wiki-verifier run at 0.5 s, so `archive.org` now gets the same 4 s as the CDX host (about 15 a minute, the rate clients report). hw.py already honours Retry-After.
- Track: tooling
- Sources: https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits, https://www.mediawiki.org/wiki/Wikimedia_APIs/Access_policy, https://crossref.org/blog/announcing-changes-to-rest-api-rate-limits/, https://help.openalex.org/how-to-use-the-api/rate-limits-and-authentication; the 429s: ai-docs/notes/2026-10-18-wiki-verify.out.txt
- Magnitude: minor
- Applied: skills/historywright-sources/references/registry.json (pace_s of wikidata, wikipedia, commons, openalex, crossref, internet-archive), skills/historywright/scripts/hw_net.py (DEFAULT_PACE)

### R-20261017-27 · 2026-10-17 · Build: DILA's TLS certificate fails Python's strict X.509 check
- Summary: `authority.dila.edu.tw` serves a certificate without a Subject Key Identifier. Python 3.13+ verifies in X.509 strict mode by default and refuses it ("Missing Subject Key Identifier"); curl accepts it. hw.py retries such a host once with only `VERIFY_X509_STRICT` cleared (chain and hostname still verified). The same SQL dump is on GitHub (DILA-edu/Authority-Databases, authority_time/SQL/authority_time.sql, CC BY-SA 3.0), which hw.py uses as the fallback. The built table: 123 dynasties, 692 emperors, 1,503 eras, 117,428 months (China, Japan, Korea; no Vietnamese data in DILA).
- Track: tooling
- Sources: https://authority.dila.edu.tw/downloads/authority_time.2012-02.zip, https://github.com/DILA-edu/Authority-Databases/tree/master/authority_time
- Magnitude: n/a (build)
- Applied: scripts/hw_net.py (fetch), scripts/hw_dates.py (DILA_URLS)

### R-20261017-26 · 2026-10-17 · Build: World Historical Gazetteer endpoints that answer
- Summary: With `Authorization: Bearer <token>` and a contact User-Agent, `https://whgazetteer.org/suggest/entity?prefix=Alesia` returns places with `repr_point` [lon, lat], alternative names, country codes and AAT place types; `api/index/?name=` returns a GeoJSON FeatureCollection; `reconcile` answers the OpenRefine manifest; `api/places/?name=` is 404.
- Track: subject
- Sources: https://whgazetteer.org/suggest/entity?prefix=Alesia, https://docs.whgazetteer.org/content/technical/apis.html#reconciliation-service-api
- Magnitude: n/a (build)
- Applied: scripts/hw_sources.py (`_whg`)

### R-20261017-25 · 2026-10-17 · Build: Wikipedia footnotes from action=parse, and the Wayback outage
- Summary: `w/api.php?action=parse&prop=text&formatversion=2` holds each footnote as `<li id="cite&#95;note-...">` (escaped underscore) with a `reference-text` span; the sentence's `<sup class="reference">` links name its notes. On Microsoft, "April 4, 1975" maps to notes 6 to 8 (BBC timeline, 1995 Fortune interview, Allen's memoir). The same session, `archive.org/wayback/available` answered "Temporarily Offline" (HTML): URL health must call that `unknown`, never `likely_hallucinated`.
- Track: subject
- Sources: https://en.wikipedia.org/w/api.php?action=parse&page=Microsoft&prop=text&format=json&formatversion=2, https://archive.org/wayback/available?url=example.com
- Magnitude: n/a (build)
- Applied: scripts/hw_sources.py (`wp_refs`), scripts/hw_check.py (`url_health`)

### R-20261017-1 · 2026-10-17 · Creation pass
- Summary: Seven parallel evergreen-researcher passes in creation mode: subject in four parts (structured and place sources; libraries, archives and corpora; archaeology, scholarship, museums and modern history; method and the gold answers), then tooling, practice and testing. Result: no existing tool does this job, the access landscape moved a lot in 2025–2026, and the practice literature converges on verification guards (fetched-only citations, quote-span support, independence, dates in code). The shared WebSearch budget (about 200 a turn across agents) ran out; the tooling pass got 4 searches and used registry, skills.sh and GitHub APIs instead (73 fetches). Cost: searches 211 (11 refused) · fetches 245 · tool calls 477.
- Track: subject
- Sources: ai-docs/research/2026-10-17-creation-pass/ (seven reports)
- Magnitude: n/a (initial)
- Applied: the build as a whole (ai-docs/log.md, 2026-10-17)

### R-20261017-2 · 2026-10-17 · Wikidata dates: read full statements, not truthy values
- Summary: Caesar (Q1048, P569) has four statements: preferred July 100 BC at month precision with earliest 12 and latest 13 July and P1480 disputed; 13 July at day precision; 102 BC flagged disputed (JRS 1917, Rice Holmes); 100 BC under the Gregorian model. `wdt:P569` returns only the preferred one. SPARQL `timeValue` gives `-0099-07-11` (XSD year 0, converted to Gregorian); JSON gives `-0100` (historical). Precision codes 11 day to 0 billion years; calendars Q1985727 Gregorian, Q1985786 Julian; manual entry defaults to Julian through 1582; 1 January values are often year-precision artefacts. Wikibase REST v1 is stable.
- Track: subject
- Sources: https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=Q1048&property=P569&format=json, https://www.wikidata.org/wiki/Help:Dates, https://www.mediawiki.org/wiki/Wikibase/Indexing/RDF_Dump_Format, https://www.wikidata.org/wiki/Wikidata:REST_API
- Magnitude: n/a (initial)
- Applied: skill guards and hw.py (cited in place)

### R-20261017-3 · 2026-10-17 · Wikipedia routing articles and the REST API
- Summary: None of the seed routing articles is featured or good. "Timeline of human prehistory" redirects to "Timeline of prehistory". "Outline of the history of China" does not exist. Human evolution is B (Top) and still carries an unreferenced-section tag. List of Chinese monarchs is List (Top), 651 editors. The page summary endpoint returns `wikibase_item`. The API Portal (api.wikimedia.org) was sunset in June 2026.
- Track: subject
- Sources: https://en.wikipedia.org/w/api.php?action=query&prop=pageassessments|info&redirects=1&titles=Outline_of_history, https://www.mediawiki.org/wiki/Wikimedia_APIs/Changelog
- Magnitude: n/a (initial)
- Applied: skill guards and hw.py (cited in place)

### R-20261017-4 · 2026-10-17 · Places and periods
- Summary: Pleiades: the daily JSON dump is current (numbered releases stopped at 4.1, 2025-05-28), CC BY 3.0, and the CSV is deprecated. CHGIS TGAZ was live-tested (長安, yr 700); its licence is unstated and it is not redistributable via WHG. WHG needs a token and a real User-Agent, allows 600/min and 5,000/day, and the licence is per source. PeriodO dumps are CC0. Cliopatria offers polity borders 3400 BCE–2024 CE, CC BY 4.0, with QIDs. OpenHistoricalMap is mostly CC0, with dated features, Overpass and QLever. ToposText's terms are unclear. DBpedia is dropped.
- Track: subject
- Sources: https://pleiades.stoa.org/downloads, https://docs.whgazetteer.org/content/technical/apis.html, https://chgis.hudci.org/tgaz/, https://perio.do/en/, https://github.com/Seshat-Global-History-Databank/cliopatria, https://wiki.openstreetmap.org/wiki/OpenHistoricalMap/Reuse
- Magnitude: n/a (initial)
- Applied: skill guards and hw.py (cited in place)

### R-20261017-5 · 2026-10-17 · Wikimedia rate limits and the WDQS split
- Summary: Enforced since 2026-03-12: 10/min for an unidentified client, 200/min with a compliant contact User-Agent, 2,000 for established editors; concurrency at most 3; honour Retry-After. WDQS: the main graph is at query.wikidata.org and the scholarly graph at query-scholarly.wikidata.org (since 2025-05-09); the legacy endpoint is gone; timeout 60 s, 5 parallel per IP. A Blazegraph replacement is undecided (QLever leads). OAuth client-credential apps registered from 2026-10-19 count as identified.
- Track: subject
- Sources: https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits, https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/WDQS_graph_split
- Magnitude: n/a (initial)
- Applied: skill guards and hw.py (cited in place)

### R-20261017-6 · 2026-10-17 · Libraries, archives, corpora: what scripts can reach
- Summary: Keyless and live-tested: loc.gov JSON (Chronicling America only through loc.gov since 2025-08-04; 20/min, 1-hour block), TNA Discovery (3,000 per 5 min), Internet Archive advancedsearch, NDL OpenSearch, Europeana (demo key), the HathiTrust Bibliographic API (its Data API retired 2024-07-17). Keyed: NARA v2 (email, 10k a month, no caching), DDB, DPLA, Trove v3 (approval levels; keys cancelled without notice for a major tool author). PAID: the ctext API (institutional, registered IP), the Trismegistos search, the Scripta Sinica full tier. Open dumps: Perseus TEI on GitHub, OpenITI 2025.1.9, CBDB SQLite (CC BY-NC-SA), papyri.info on GitHub, FRUS TEI. EDCS moved to Zurich in 2025. India, Africa and Latin America archives are browse-only. Bot walls block Trove, EDH, papyri.info, Gallica pages, QDL, DPLA and CBDB to the fetcher.
- Track: subject
- Sources: https://loc.gov/ndnp/migration, https://www.nationalarchives.gov.uk/terms-and-conditions/policy-on-use-of-website-and-catalogue-data/, https://ctext.org/tools/api, https://hathitrust.org/press-post/retirement-data-api, https://zenodo.org/records/17767721, https://cbdb.hsites.harvard.edu/
- Magnitude: n/a (initial)
- Applied: skill guards and hw.py (cited in place)

### R-20261017-7 · 2026-10-17 · Scholarship indexes
- Summary: OpenAlex (2026-02-13): keys and a daily dollar budget (free key $1 a day, 30/s; keyless about a tenth of that; a key is needed to page past page 1); `mailto` is gone, and many community skills still assume it. Crossref (2025-12-01): polite pool 10/s single, concurrency 3. Semantic Scholar is keyed at 1/s. CORE allows 5 per 10 s. DOAJ v4 needs no key. Persée has OAI-PMH and SPARQL. JSTOR Constellate shut 2025-07-01. BBIH moved to IHR/Brepols (paid). Google Scholar's terms forbid scraping.
- Track: subject
- Sources: https://help.openalex.org/how-to-use-the-api/rate-limits-and-authentication, https://crossref.org/blog/announcing-changes-to-rest-api-rate-limits/, https://royalhistsoc.org/the-bibliography-of-british-and-irish-history/
- Magnitude: n/a (initial)
- Applied: skill guards and hw.py (cited in place)

### R-20261017-8 · 2026-10-17 · Museum open access for packs
- Summary: The Met v1 search retired 2026-10-01; v1.1 has no culture filter. Cleveland (CC0, no key), Art Institute of Chicago (CC0 data, 60/min, IIIF), Getty (CC0 mostly) and Smithsonian (CC0, api.data.gov key) are good. Rijksmuseum has a new keyless Linked Art search (beta). British Museum and Science Museum images are CC BY-NC-SA; V&A uses its own terms. Live tests: "Roman helmet" in the US CC0 APIs returns Greek and Etruscan helmets. Late-Republican kit images come via Commons, Europeana or Livius, each with its own licence. The Portable Antiquities Scheme skews later.
- Track: subject
- Sources: https://metmuseum.github.io/, https://openaccess-api.clevelandart.org/api/artworks/?q=roman%20helmet&has_image=1&cc0=1&limit=10, http://api.artic.edu/docs/, https://data.rijksmuseum.nl/docs/search, https://www.britishmuseum.org/terms-use/copyright-and-permissions/images-and-photography
- Magnitude: n/a (initial)
- Applied: skill guards and hw.py (cited in place)

### R-20261017-9 · 2026-10-17 · Calendars and machine dates
- Summary: Python `datetime` stops at year 1, so use JDN integer algorithms (Fliegel–Van Flandern; USNO). Test vectors: JDN 2299160 = 4 Oct 1582 Julian, 2299161 = 15 Oct 1582 Gregorian; Julian 12 July 100 BC = JDN 1685091. Gregorian adoption by country needs a table: Britain 1752 (2 Sep followed by 14 Sep; the year began 25 March before), Sweden 1753, Japan 1873, Russia 1918, Greece 1923. Roman dates before 45 BC are republican; BC = 754 − AUC (unverified this pass). EDTF levels 0 and 1 (`?`, `~`, `%`, `X`, open intervals, negative years) can be done in stdlib; level 2 is not worth hand-rolling. A disputed date is a set or range.
- Track: subject
- Sources: https://www.loc.gov/standards/datetime/, https://aa.usno.navy.mil/faq/JD_formula, https://www.legislation.gov.uk/apgb/Geo2/24/23/contents, https://en.wikipedia.org/wiki/List_of_adoption_dates_of_the_Gregorian_calendar_by_country
- Magnitude: n/a (initial)
- Applied: skill guards and hw.py (cited in place)

### R-20261017-10 · 2026-10-17 · East Asian and Islamic conversion
- Summary: The DILA Authority Database tables (about 220 BCE to 1945; 1,637 eras; 131,808 months) are the basis of kltng's stdlib cjk-calendar (a 14 MB SQLite download, every match returned for an ambiguous era name) and of the calendar_converter MCP (v0.1.0, self-declared untested at dynastic transitions). Academia Sinica's 兩千年中西曆轉換 is the check. hijridate's Umm al-Qura tables cover 1924–2077 only; earlier dates are tabular. sxtwl is a C extension (out).
- Track: subject
- Sources: https://raw.githubusercontent.com/kltng/humanities-skills/main/cjk-calendar/SKILL.md, https://github.com/kltng/calendar_converter, https://pypi.org/pypi/hijridate/json
- Magnitude: n/a (initial)
- Applied: skill guards and hw.py (cited in place)

### R-20261017-11 · 2026-10-17 · Method: how historians and reference librarians answer
- Summary: The Historical Thinking Chart (sourcing, contextualisation, corroboration, close reading; Wineburg). University guides: tertiary sources for orientation only, and primary or secondary depends on the question. RUSA's 2013 behavioural guidelines (a revision has been pending since 2022) imply a reference interview. Contested topics: Wikipedia's due weight and no false balance; Council of Europe multiperspectivity (principles endorsed in June 2025); UNESCO's Pingel guidebook. AHA (2025-07-29): AI "introduces a false sense of certainty where uncertainty exists", and gated or undigitised archives are invisible to AI.
- Track: subject
- Sources: https://www.inquirygroup.org/history-lessons/historical-thinking-chart, https://en.wikipedia.org/wiki/Wikipedia:Neutral_point_of_view, https://historians.org/AI-history-education
- Magnitude: n/a (initial)
- Applied: skill guards and hw.py (cited in place)

### R-20261017-12 · 2026-10-17 · Gold answers re-verified
- Summary: Caesar corrected: 12 or 13 July 100 BC. 12 July comes from Macrobius Sat. 1.12.34, and 13 July is a disputed reading of Dio 47.18. All ancient sources imply 100 BC (Suetonius, Jul. 88). Mommsen argued for 102 BC from office ages, and Badian (1959) defends 100 BC, the consensus. These are republican-calendar dates. Chinese emperors corrected: Kangxi 1661–1722, 61 years (era 1662–1722, regency at first). Qianlong acceded 1735 (era 1736), abdicated 9 Feb 1796 so as not to outlast Kangxi, and ruled as Taishang Huang until 7 Feb 1799, the longest de facto power at about 63 years. Zhao Tuo of Nanyue ruled about 66 years outside the dynastic list. Microsoft confirmed: 4 April 1975, Gates and Allen, Albuquerque, a partnership. It moved to Bellevue in 1979 and was incorporated 25 June 1981. Official pages give the year, not the day.
- Track: subject
- Sources: https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Cassius_Dio/47*.html, https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Suetonius/12Caesars/Julius*.html, https://resolve.cambridge.org/core/journals/journal-of-roman-studies/article/was-caesar-born-in-100-or-in-102-bc/BDE639D70E0F8A3A819F268D2E827975, https://museum.sinica.edu.tw/en/collection/17/item/146/, https://www.sec.gov/Archives/edgar/data/0000789019/000103221002001351/d10k.htm, https://news.microsoft.com/facts-about-microsoft/
- Magnitude: n/a (initial)
- Applied: evals/evals.json gold text; skills/historywright/references/answer-format.md

### R-20261017-13 · 2026-10-17 · Tooling: prior art to build on
- Summary: kltng/humanities-skills (21 historian skills, stdlib scripts, evals.json in evergreen's shape, active 2026-09): adopt the cjk-calendar design; point to the CBDB, CHGIS and Wikidata skills. fuzheado/wikipedia-ai-skills (61 skills, pytest, CI): read `wikimedia-api-access` and `wikidata-reconciliation` before writing hw.py. lizhuojunx86/chinese-history-mcp: copy its rule that every claim carries a verbatim quote plus a review status. Programming Historian "Wikidata for Historical Research" (2026-08) skips precision and calendar. Nothing in the Anthropic official catalog, and no historian skill with real installs on skills.sh.
- Track: tooling
- Sources: https://github.com/kltng/humanities-skills, https://github.com/fuzheado/wikipedia-ai-skills, https://github.com/lizhuojunx86/chinese-history-mcp, https://programminghistorian.org/en/lessons/wikidata-for-historical-research
- Magnitude: n/a (initial)
- Suggested response: adopt (kltng calendar design, quote rule); point (the rest)
- Applied: skill guards and hw.py (cited in place)

### R-20261017-14 · 2026-10-17 · Tooling: MCP servers and libraries
- Summary: wmde/WikidataMCP is official (`wd-mcp.wmcloud.org/mcp/`, hybrid search, statements with qualifiers and references) but has no precision, calendar or BCE handling: point to it as optional, and adopt "discover IDs before SPARQL, never invent a QID". zzaebok/mcp-wikidata is quiet since 2026-03. cyanheads Wikidata, Wikipedia and OpenAlex servers need Node and have low use. 54yyyu/zotero-mcp (5,443 stars): point; export CSL-JSON. GDM `literature-search-openalex` (2,974 installs): point. HTR (Transkribus paid API; Kraken, CHURRO open) is out of v1. convertdate 2.5.1, edtf 5.0.2 and hijridate 2.6.0 are test oracles only; hw.py stays stdlib.
- Track: tooling
- Sources: https://github.com/wmde/WikidataMCP, https://github.com/54yyyu/zotero-mcp, https://skills.sh/api/search?q=openalex, https://www.transkribus.org/plans, https://pypi.org/pypi/convertdate/json
- Magnitude: n/a (initial)
- Suggested response: point; note
- Applied: skill guards and hw.py (cited in place)

### R-20261017-15 · 2026-10-17 · Practice: fabricated and blended references
- Summary: 26.5% of 400 chatbot references were fully correct, and 39.8% were wrong or invented (eight models, 2025). GPTZero found at least 100 hallucinated citations in NeurIPS 2025 accepted papers, many blending real authors with invented titles. The AHA rates an unchecked AI reference in a footnote "never acceptable". Guard: cite only what the run retrieved; match title, author and year together in a catalogue.
- Track: practice
- Sources: https://arxiv.org/abs/2505.18059, https://gptzero.me/news/neurips/, https://historians.org/AI-history-education
- Magnitude: n/a (initial)
- Suggested response: adopt
- Applied: skill guards and hw.py (cited in place)

### R-20261017-16 · 2026-10-17 · Practice: real sources that do not support the claim
- Summary: WikiProject AI Cleanup: models "usually cite real sources but often don't verify that they support the content"; fake foreign-language sources; WP:LLM bans LLM-written article content (March 2026). Fabricated quotes passed a publisher's fact-check (Rosenbaum, May 2026). Deep Research invented quotes and claimed analyses it never ran (Humphries, 2025). Guard: a quote-span check for every claim, and a direct quote only with its exact words in a fetched text naming the speaker.
- Track: practice
- Sources: https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup, https://oecd.ai/en/incidents/2026-05-19-f57e, https://generativehistory.substack.com/p/is-this-the-last-generation-of-historians
- Magnitude: n/a (initial)
- Suggested response: adopt
- Applied: skill guards and hw.py (cited in place)

### R-20261017-17 · 2026-10-17 · Practice: citogenesis and independence
- Summary: Documented cases where books, newspapers and a museum copied Wikipedia errors that were then cited back (Alan MacMasters 2012–2022, Bazalgette, Meighen). Guard: trace the earliest source; record `derived_from`; corroboration needs two sources that are not Wikipedia mirrors and do not derive from each other; prefer sources that predate the claim's first appearance on Wikipedia.
- Track: practice
- Sources: https://en.wikipedia.org/wiki/Wikipedia:List_of_citogenesis_incidents, https://en.wikipedia.org/wiki/Circular_reporting
- Magnitude: n/a (initial)
- Suggested response: adopt
- Applied: skill guards and hw.py (cited in place)

### R-20261017-18 · 2026-10-17 · Practice: dates and chronology in code
- Summary: ChronoSense and ChroKnowledge show memorised dates and missed spans. The "AI Historian" agent (arXiv 2608.29133) anchored claims to source sentences and scored 86.2% against 17.1% for direct prompting on Shiji chronology (six cases). Guard: date arithmetic in hw.py; timeline rows carry their source sentence and a range.
- Track: practice
- Sources: https://arxiv.org/abs/2501.03040, https://arxiv.org/abs/2410.09870, https://arxiv.org/abs/2608.29133
- Magnitude: n/a (initial)
- Suggested response: adopt
- Applied: skill guards and hw.py (cited in place)

### R-20261017-19 · 2026-10-17 · Practice: regional and language bias
- Summary: HiST-LLM (NeurIPS 2024, Seshat): best model 46.0% on Table 1 (chance 25%), worst for Sub-Saharan Africa and Oceania and for recent periods, built mostly on English sources. The prompt's language changes the framing of a contested event (Asia Minor 1922 case study, 2026). ProHist-Bench (ACL 2026) shows all 18 models short on evidence-based reasoning. Guard: lower default confidence there; seek regional or non-English scholarship; on contested topics, search in each party's language and attribute each account; interpretive claims cite a historian.
- Track: practice
- Sources: https://proceedings.neurips.cc/paper_files/paper/2024/file/38cc5cba8e513547b96bc326e25610dc-Paper-Datasets_and_Benchmarks_Track.pdf, https://link.springer.com/article/10.1007/s43681-026-01138-8, https://arxiv.org/abs/2604.24690
- Magnitude: n/a (initial)
- Suggested response: adopt
- Applied: skill guards and hw.py (cited in place)

### R-20261017-20 · 2026-10-17 · Practice: anachronism in AI imagery and period text
- Summary: HistVis (2025): diffusion models stereotype eras and add anachronisms. AI "Boring History" videos (404 Media, 2025-09) show glazed windows and train tracks in the 1300s. Gemini paused people images in February 2024 after historically wrong depictions. Prompting cannot remove anachronism from period text (Underwood et al., 2025). AHA calls AI images of the past "fabrications, not authentic reconstructions". Guard: museum-record references only, with accession number and date; a per-period anachronism checklist in each pack; generated images and period dialogue labelled as reconstructions or pastiche.
- Track: practice
- Sources: https://arxiv.org/abs/2505.17064, https://www.404media.co/ai-generated-boring-history-videos-are-flooding-youtube-and-drowning-out-real-history/, https://arxiv.org/abs/2505.00030
- Magnitude: n/a (initial)
- Suggested response: adopt
- Applied: skill guards and hw.py (cited in place)

### R-20261017-21 · 2026-10-17 · Practice: agents stop early, overclaim, and need outside checks
- Summary:
  - FutureSearch (2025, updated 2026-01): Deep Research gave wrong figures without hedging, cited Statista over the original, and silently returned 34 of 45 rows.
  - Humphries (2026-04): agents stop before the task is complete and loop; "can't self verify". Humphries (2026-05): a second model family caught 76% of transcription errors.
  - AskHistorians removes undisclosed AI answers.
  
  Guard: a completeness checklist with reasons for gaps; checks by script or a separate pass; second-model checks for scan-derived quotes and dates; answers say they are AI-researched.
- Track: practice
- Sources: https://futuresearch.ai/blog/oaidr-feb-2025/, https://generativehistory.substack.com/p/the-agents-are-waking-up, https://generativehistory.substack.com/p/when-models-disagree-transcription, https://techpolicy.press/millions-of-volunteers-are-keeping-the-internet-human-for-now
- Magnitude: n/a (initial)
- Suggested response: adopt
- Applied: skill guards and hw.py (cited in place)

### R-20261017-22 · 2026-10-17 · Testing: harness and action evidence
- Summary: `claude plugin eval` has graders `regex` (on the last message, the trace, files or mock calls), `tool_used` with `input_match`, `tool_order`, `file_exists`, `llm` and `baseline`. Mock MCP servers with fixtures; WebFetch scoped by domain. Bash needs an OS sandbox (WSL2 on Windows). Action case: the trace matches `wbgetclaims|p:P569|psv:P569` before the answer is written, not a lone `wdt:`. hw.py honours `HW_HOME` so the cache can be graded. DRIFT/TELBench (2026-06): audit claims against the trajectory; the cheap form is that every URL in sources.json appears in a fetch in the trace.
- Track: testing
- Sources: https://code.claude.com/docs/en/plugin-evals, https://papers.cool/arxiv/2606.02060
- Magnitude: n/a (initial)
- Suggested response: adopt
- Applied: skill guards and hw.py (cited in place)

### R-20261017-23 · 2026-10-17 · Testing: citation checks
- Summary: "Cited but Not Verified" (2026-05): link works 94%+, fact check 39–77%, falling with more tool calls. URL health (arXiv 2604.03173): 3–13% of agent URLs hallucinated; HEAD, then GET, then Wayback; labels live, dead, likely hallucinated, unknown; cut non-resolving below 1% (about 40 stdlib lines; the package is not found). ALCE defines citation recall and precision. Guard and checks: `hw.py verify` does quote span, URL health, DOI and QID; zero likely-hallucinated URLs per pack.
- Track: testing
- Sources: https://arxiv.org/html/2605.06635v1, https://arxiv.org/html/2604.03173v1, https://arxiv.org/pdf/2305.14627
- Magnitude: n/a (initial)
- Suggested response: adopt
- Applied: skill guards and hw.py (cited in place)

### R-20261017-24 · 2026-10-17 · Testing: grading undisputed and disputed facts; pack validation
- Summary:
  - SimpleQA Verified grades correct, incorrect or not attempted, and requires committing to one answer; it removed conflicted questions, so it shows how not to grade disputes.
  - NATCONFQA and CONFLICTS: name every valid answer, state the conflict, attribute each side, classify the conflict type.
  - FACTS (Parametric against Search) is the precedent for the baseline.
  - RFC 7946: [lon, lat], closed rings with at least four positions, no `crs`.
  - EDTF L0/L1 regex. No calendar or dispute benchmark exists, so build those cases (October Revolution O.S./N.S., a non-Western reign). Full fact-check pipelines (SAFE, VeriScore, FActScore, AVeriTeC) are too heavy; borrow the atomic-claim pattern.
- Track: testing
- Sources: https://arxiv.org/html/2509.07968v2, https://arxiv.org/abs/2508.12355v1, https://arxiv.org/abs/2506.08500, https://www.rfc-editor.org/rfc/rfc7946, https://arxiv.org/html/2512.10791v1
- Magnitude: n/a (initial)
- Suggested response: adopt
- Applied: skill guards and hw.py (cited in place)
