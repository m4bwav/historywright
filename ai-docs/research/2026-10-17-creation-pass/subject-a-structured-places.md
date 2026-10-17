# Creation pass 2026-10-17: subject-a-structured-places (raw researcher report)

Verbatim report of the evergreen-researcher pass for this track. Synthesis: [../2026-10-17-creation-pass.md](../2026-10-17-creation-pass.md).

## Findings (newest first)

### F1 · 2026-10-17 · Pleiades: the daily JSON dump is current, but the numbered releases stopped at 4.1
- What: The full place dump `https://atlantides.org/downloads/pleiades/json/pleiades-places-latest.json.gz` (129 MB) was regenerated today, 2026-10-17 07:09, and a week of daily files is kept. Each place also has its own JSON at `https://pleiades.stoa.org/places/{id}/json` (Athens: `/places/579885/json`), plus `/turtle` and `/kml`. The weekly RDF tarball is at `https://atlantides.org/downloads/pleiades/rdf/`. The legacy CSV dump is marked "DEPRECATED - DO NOT USE". The quarterly numbered releases at `github.com/isawnyu/pleiades.datasets` (Zenodo 10.5281/zenodo.1193921) have not moved since 4.1 on 2025-05-28, so cite the daily dump with its date. Licence is CC BY 3.0. The site documents no API, rate limit or User-Agent rule. Changes are published at `pleiades.stoa.org/news/changes/RSS`.
- Good for: the Greek and Roman world and the ancient Near East (roughly 3000 BC to AD 640). Tier 1.
- Track: subject
- Affects: hw.py Pleiades lookup (use the daily dump or per-place JSON; skip the CSV)
- Magnitude: n/a (initial)
- Suggested response: n/a (subject)
- Sources: https://pleiades.stoa.org/downloads, https://atlantides.org/downloads/pleiades/json/, https://github.com/isawnyu/pleiades.datasets/releases

### F2 · 2026-10-09 (latest change note in the docs) · World Historical Gazetteer: token, User-Agent and daily quota required
- What: The API is maintained and documented, with Swagger at `https://whgazetteer.org/api/schema/swagger-ui/`.
  - Entity endpoint: `https://whgazetteer.org/entity/place:{id}/api?token=…` returns Linked Places Format v1.1. Valid types are place, dataset, collection, area and period, where period means PeriodO.
  - Reconciliation and search: `https://whgazetteer.org/reconcile` (OpenRefine protocol, at most 50 queries per POST) and `/suggest/entity?prefix=Edin&limit=5&namespaces=whg&token=…`.
  - Tokens: most endpoints need one. Generate it on your profile page and send it as `?token=` or `Authorization: Bearer`.
  - User-Agent: required, and it must identify the client. Generic values such as `bot` are refused.
  - Limits: 600 queries per minute and 5,000 requests per day by default, with 429 plus Retry-After when exceeded.
  - Licence: set per source, with an `attribution` object in each response. The `redistributable` flag is false for `chgis`, `nl` and `kain_par`, and those records return HTTP 451.
- Good for: places worldwide and in every era, and for reconciling names to Wikidata, GeoNames, TGN and Pleiades. Tier 2 (aggregator).
- Track: subject
- Affects: hw.py WHG lookup (needs a stored token and a quota guard; never bulk-pull CHGIS through WHG)
- Magnitude: n/a (initial)
- Suggested response: n/a (subject)
- Sources: https://docs.whgazetteer.org/content/technical/apis.html

### F3 · 2026-03 to 2026-10 · Wikimedia APIs: new rate limits, API Portal retired, page summary still works
- What: Rate-limit enforcement began on 2026-03-12, and identified clients have been limited too since the week of 2026-04-28. Limits per minute:
  - 10 for a client identified by IP only.
  - 200 for an unauthenticated bot with a compliant User-Agent (name, version, contact email or URL).
  - 2000 for an established authenticated editor.
  - Keep concurrency at 3 or fewer. On 429, honour Retry-After, or wait at least 5 s with backoff.
  - The limits cover the Action API and the REST APIs.

  The API Portal at api.wikimedia.org was sunset in June 2026 (T415293). Build on `https://en.wikipedia.org/w/rest.php/...`, `/api/rest_v1/` or `w/api.php`, never on api.wikimedia.org. The page summary endpoint still works today: `https://en.wikipedia.org/api/rest_v1/page/summary/Julius_Caesar` returns title, description, extract, a thumbnail and `wikibase_item: "Q1048"`, so a Wikipedia title maps straight to its QID. An Attribution API (beta) was launched on 2026-04-20; I did not test it. OAuth 2 client-credential apps registered on or after 2026-10-19 stop counting as anonymous.
- Good for: Wikipedia as a tertiary source and a router. Tier 3.
- Track: subject
- Affects: hw.py HTTP layer (a mandatory User-Agent with contact, a throttle of 200/min or less, a 429 handler); never use api.wikimedia.org URLs
- Magnitude: n/a (initial)
- Suggested response: n/a (subject)
- Sources: https://www.mediawiki.org/wiki/Wikimedia_APIs/Changelog, https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits, https://www.mediawiki.org/wiki/Wikimedia_APIs/Access_policy

### F4 · 2026-10-17 (fetched live) · Routing articles on Wikipedia: none is a featured or good article, all are actively edited
- What: The pageassessments and info queries return the following.

| Article | Class | Size | Last touched |
|---|---|---|---|
| Outline of history | List (Outlines: Top) | 23.5 KB | 2026-10-11 |
| Outline of ancient history | List | 17 KB | 2026-10-07 |
| Periodization | C | 16.7 KB | 2026-10-15 |
| List of time periods | C/List | 30.9 KB | 2026-10-15 |
| Timeline of prehistory | List, High in five projects | 114 KB | n/a |
| Human evolution | B, Top | 285 KB | 2026-10-16 |
| Timeline of human evolution | C | 92 KB | n/a |
| List of archaeological periods | List | 10.6 KB, thin | 2026-09-30 |
| Timeline of Chinese history | List, Top | 190 KB | 2026-10-15 |
| List of Chinese monarchs (Q185373) | List, Top | 389 KB | 2026-10-11 |
| History of China | B, Top | 147 KB | n/a |
| Outline of China | List | 25 KB | n/a |
| Prehistory | B | 60 KB | n/a |
| Three-age system | C | 90 KB | n/a |

  - "Timeline of human prehistory" is now a redirect to "Timeline of prehistory", which is 114 KB.
  - "Human timeline" redirects to "Timeline of human evolution".
  - "Outline of the history of China" does not exist; use "Outline of China" and "History of China".
  - Human evolution still carries a "WikiProject Unreferenced articles" tag.
  - List of Chinese monarchs has 1,984 revisions, 651 editors and about 10k views a month (xtools).

  Use these pages for routing only and cite the sources underneath them.
- Track: subject
- Affects: the knowledge base routing map (fix the seed titles; record the class next to each entry)
- Magnitude: n/a (initial)
- Suggested response: n/a (subject)
- Sources: https://en.wikipedia.org/w/api.php?action=query&prop=pageassessments|info&redirects=1&titles=Outline_of_history|Timeline_of_human_prehistory|List_of_Chinese_monarchs, https://xtools.wmcloud.org/api/page/articleinfo/en.wikipedia.org/List_of_Chinese_monarchs

### F5 · 2026-09-22 · OpenHistoricalMap: dated boundaries and features, public domain (seed missed it)
- What: OpenHistoricalMap is an OSM-style map of every era. Features carry `start_date` and `end_date` tags.
  - Licence: data is "in general… public domain under a CC0 dedication", with per-feature exceptions. The Landmasses tileset is ODbL.
  - Planet files: `https://planet.openhistoricalmap.org/`, current contents daily and full history weekly.
  - Vector tiles: `https://vtiles.openhistoricalmap.org/maps/ohm/{z}/{x}/{y}.pbf`.
  - Overpass: `https://ohm.overpass-ultra.us/`.
  - SPARQL: QLever at `qlever.dev/ohm-planet`, which can federate with Wikidata.
  - Activity: QLever statistics since 2026-09-22 and new site features in July 2026.

  It fits places.geojson for 3D and video work, with crowd quality. Tier 3.
- Track: subject
- Affects: research pack export (places.geojson, boundaries at a given date)
- Magnitude: n/a (initial)
- Suggested response: n/a (subject)
- Sources: https://wiki.openstreetmap.org/wiki/OpenHistoricalMap, https://wiki.openstreetmap.org/wiki/OpenHistoricalMap/Reuse

### F6 · 2026 · Seshat moved to the Polaris-2026 snapshot and an open API; Cliopatria borders are CC BY 4.0 with Wikidata IDs
- What: Seshat's data page names Polaris-2026 as the current release. It is an Excel file at `github.com/Seshat-Global-History-Databank/build_polaris_dataset/blob/main/Polaris2026.xlsx`, and the repo includes the build scripts.
  - API: a browsable Django REST API at `https://seshat-db.com/api/` with groups core, general, sc, wf, rt, ec and crisisdb. The root opens without login. Python clients `seshat_api` and `SeshatDatasetAnalysis` exist.
  - Login: the older Equinox-2020 download sits behind a login.
  - Licence: Seshat states CC BY-NC-SA, which is non-commercial.
  - Cliopatria: polity borders from 3400 BCE to 2024 CE, published in Scientific Data on 2025-02-12. It ships as one GeoJSON (`cliopatria.geojson.zip`) with fields Name, FromYear and ToYear (negative = BCE), Area, a Wikidata ID and a Wikipedia phrase. The licence is CC BY 4.0, confirmed from LICENSE.md. Zenodo record 13363121.

  Good for comparative questions ("largest empire in 200 CE", polity durations) and animated borders. Tier 1, curated by experts.
- Track: subject
- Affects: research pack export (Cliopatria is the best open source for timed polity polygons); comparative-question routing
- Magnitude: n/a (initial)
- Suggested response: n/a (subject)
- Sources: https://www.seshatdatabank.info/data, https://seshat-db.com/api/, https://github.com/Seshat-Global-History-Databank/cliopatria, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11822181/

### F7 · 2026-01-30 · Getty vocabularies: XML services retired, linked open data only
- What: Getty's XML and relational downloads and its XML web services for AAT, TGN and ULAN (also CONA and IA) are discontinued. The final XML sets, drawn on 2026-01-30, are archived and will not be refreshed. What remains:
  - The SPARQL endpoint at `http://vocab.getty.edu/sparql` (UI at getty.edu/research/tools/vocabularies/lod/sparql.html; that documentation page is dated 2014).
  - OpenRefine reconciliation.
  - Full N-Triples dumps, refreshed monthly (e.g. `http://vocab.getty.edu/dataset/tgn/full.zip`).

  Licence is ODC-By 1.0. TGN covers historical names, ULAN covers artists and AAT covers objects and styles; useful for museum images and style terms. Tier 2. I could not fetch the new data-services page (it truncates) and did not check Linked Art.
- Track: subject
- Affects: any hw.py Getty route (SPARQL or N-Triples only)
- Magnitude: n/a (initial)
- Suggested response: n/a (subject)
- Sources: https://www.getty.edu/research/tools/vocabularies/obtain/, https://www.getty.edu/research/tools/vocabularies/lod/sparql.html

### F8 · 2026-01-13 · D-PLACE v3.3.0 (CLDF), non-commercial licence
- What: D-PLACE (`github.com/D-PLACE/dplace-cldf`) released v3.3.0 on 2026-01-13, after v3.2.0 and v3.2.1 in November 2025. It covers 1,400+ societies, mostly from pre-1950 ethnography (Murdock, Binford, Jorgensen). Licence is CC BY-NC 4.0. Good for comparative ethnographic questions, not dated events. Tier 1.
- Track: subject
- Affects: comparative-dataset routing (a niche source; flag NC)
- Magnitude: n/a (initial)
- Suggested response: n/a (subject)
- Sources: https://github.com/D-PLACE/dplace-cldf/releases, https://d-place.org/about

### F9 · 2025-11-20 · ToposText: GeoJSON and Pleiades/DARE crosswalk, terms unclear
- What: ToposText covers 8,150 places in the Greek and Roman world, about 279k references from ancient texts, and 22k names. Downloads are listed at `https://topostext.org/TT-downloads`:
  - `ToposText_places_2025-11-20.geojson`
  - `pelagios.ttl`, which maps places to Pleiades and DARE
  - `ToposTextGazetteer.jsonld` in WHG format, dated 2023-11
  - KMZ files

  It has no API. The data files ask for "appropriate attribution to ToposText", but the site footer says "All Rights Reserved". Treat it as attribution-only and confirm before redistributing. Useful for "which ancient author mentions this place". Tier 2.
- Track: subject
- Affects: places routing for the Greek and Roman world (a point to primary texts)
- Magnitude: n/a (initial)
- Suggested response: n/a (subject)
- Sources: https://topostext.org/, https://topostext.org/TT-downloads

### F10 · 2025-05-09 to 2026-01 · Wikidata Query Service: graph split done, legacy endpoint gone, Blazegraph still in use
- What: Since 2025-05-09 `https://query.wikidata.org/sparql` serves the main graph only. Scholarly articles moved to `https://query-scholarly.wikidata.org/`, and the two can be federated (Internal Federation Guide). The legacy full-graph endpoint (`query-legacy-full`) was announced "until December 2025". Scholia and the Signpost place its sunset and the final split in the week of 2026-01-20. Historical people, places and events stay in the main graph.

  Limits:
  - Query timeout: 60 s.
  - Processing time: 60 s per 60 s for each User-Agent plus IP pair.
  - Errors: 30 error queries per minute.
  - Parallel queries: 5 per IP.
  - Over the limits: 429 with Retry-After, and persistent violators are banned.
  - User-Agent: clients that ignore the policy can be blocked.

  The planned Blazegraph replacement has no official decision. QLever is the leading candidate and already runs a full-graph mirror (`qlever.dev/wikidata`) that is unofficial.
- Track: subject
- Affects: hw.py SPARQL (main endpoint; keep queries well under 60 s; send a User-Agent)
- Magnitude: n/a (initial)
- Suggested response: n/a (subject)
- Sources: https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/WDQS_graph_split, https://www.mediawiki.org/wiki/Wikidata_Query_Service/User_Manual, https://signpost.news/2026-02-17/Technology_report, https://en.wikipedia.org/wiki/QLever

### F11 · undated (current docs) · Wikidata date model: precision, calendar and BCE traps
- What: Time values carry a precision: 11 day, 10 month, 9 year, 8 decade, 7 century, 6 millennium, 4 hundred thousand years, 3 million years, 0 billion years. There are only two calendar models, proleptic Gregorian `Q1985727` and proleptic Julian `Q1985786`. Manual entry defaults to Julian for dates up to 1582.
  - Gregorian conversion: in RDF/SPARQL the simple value `wikibase:timeValue` is converted to Gregorian, while `timeCalendarModel` keeps the original calendar. Read `psv:` full values to get back the date the sources state.
  - BCE numbering: RDF follows XSD 1.1, where 1 BCE is year 0. The JSON (`Special:EntityData/Q1048.json`) writes 1 BCE as -0001, so the two differ by one year for BCE dates.
  - Uncertainty qualifiers: `P1480` sourcing circumstances (`Q5727902` circa, `Q18912752` disputed, `Q21818619` near, `Q18195782` unspecified calendar), `P1319` earliest date, `P1326` latest date, `P4241` refine date.
  - January 1 artefacts: many P569 values set to 1 January are really year-precision data.

  Recipe: `SELECT ?t ?prec ?cal WHERE { wd:Q1048 p:P569/psv:P569 [wikibase:timeValue ?t; wikibase:timePrecision ?prec; wikibase:timeCalendarModel ?cal] }`.

  Wikidata is the best source for "when / who / with whom" facts, with references on its statements. Tier 3, with tier-2 strength where statements are referenced.
- Track: subject
- Affects: hw.py date handling and calendar conversion (render at the stored precision; convert Julian back; fix BCE off-by-one; carry circa and disputed into the confidence line)
- Magnitude: n/a (initial)
- Suggested response: n/a (subject)
- Sources: https://www.wikidata.org/wiki/Help:Dates, https://www.mediawiki.org/wiki/Wikibase/Indexing/RDF_Dump_Format

### F12 · current · Wikibase REST API v1 is stable
- What: `https://www.wikidata.org/w/rest.php/wikibase/v1` is covered by Wikidata's Stable Interface Policy, with OpenAPI docs at `https://doc.wikimedia.org/Wikibase/master/js/rest-api/`. Its rate limits are the Action API ones plus the global Wikimedia limits, and the User-Agent policy applies. A route of the form `/entities/items/Q1048/statements?property=P569` is the cheapest way to read one item. The search endpoint was not confirmed. Fallback: `Special:EntityData/Q1048.json`.
- Track: subject
- Affects: hw.py entity fetch (REST v1 or EntityData for single items; SPARQL for lists and rankings)
- Magnitude: n/a (initial)
- Suggested response: n/a (subject)
- Sources: https://www.wikidata.org/wiki/Wikidata:REST_API

### F13 · current · OWID Charts API: CC BY 4.0, some series not redistributable
- What:
  - Routes: `https://ourworldindata.org/grapher/{slug}.csv`, `.metadata.json` and `.zip`. The metadata JSON carries per-source citations.
  - Parameters: `csvType=full|filtered`, `country`, `time=2000..2020`, `useColumnShortNames`.
  - Other APIs: Tables, Indicators (semantic search) and Search, all wrapped by `owid-catalog`. The docs say they are "under active development".
  - Redistribution: some series return 403 "Data is non-redistributable".
  - Limits: none documented. OWID's own samples send a custom User-Agent.

  Good for long-run quantitative questions such as population or GDP since 1800. Tier 2.
- Track: subject
- Affects: comparative-question routing
- Magnitude: n/a (initial)
- Suggested response: n/a (subject)
- Sources: https://docs.owid.io/projects/etl/api/, https://docs.owid.io/projects/etl/api/chart-api/

### F14 · live check 2026-10-17 · CHGIS TGAZ API works
- What: `https://chgis.hudci.org/tgaz/placename?n=長安&yr=700&fmt=json` returned hvd_70625 长安县 (666–702, xian, parent 京兆府, 108.907/34.246). A malformed call returns a PHP error page. Coverage is 221 BCE to 1911 CE (Harvard Fairbank Center and Fudan). No licence is stated on the site, and WHG marks CHGIS as not redistributable. Tier 1. Calendar note: Chinese regnal dates need conversion outside Wikidata, which supports only Julian and Gregorian.
- Track: subject
- Affects: hw.py China place lookup; the "Chinese emperor" recipe
- Magnitude: n/a (initial)
- Suggested response: n/a (subject)
- Sources: https://chgis.fas.harvard.edu/search, https://chgis.hudci.org/tgaz/

### F15 · current · PeriodO dumps are public domain
- What: The full dataset downloads as `https://n2t.net/ark:/99152/p0dataset.json`, `.ttl` and `.csv`. Browsing and editing are at `client.perio.do`. Licence is public domain (CC0). The `periodo/periodo-data` repo now only tracks data-quality issues. WHG serves PeriodO periods as `entity/period:`. Good for era-name to date-range lookups, with each definition tied to its scholarly source. Tier 1. Not checked: the date of the last dataset change (the technical overview URL returned 404).
- Track: subject
- Affects: the "which period is X" knowledge base; timeline.json
- Magnitude: n/a (initial)
- Suggested response: n/a (subject)
- Sources: https://perio.do/en/, https://github.com/periodo/periodo-data

### F16 · stale or weak sources · DBpedia, Clio Infra, Maddison, DARE, Trismegistos
- What:
  - DBpedia: the project is alive (blog post 2026-09-24) and the SPARQL endpoint is `https://dbpedia.org/sparql`. The last release I found is 2025-06, announced on OpenLink's site only. It is derived from Wikipedia and adds nothing over Wikidata. Tier 3; drop it as a route.
  - Clio Infra: 86 indicators for 224 countries, series from 1500 to about 2018, Excel files. The site states no licence or update date, so treat it as frozen.
  - Maddison Project Database: latest is 2023, and its page was last modified 2024-09.
  - DARE (`imperium.ahlfeldt.se`): the page rendered empty, so it is unverified. ToposText's crosswalk covers its IDs.
  - Trismegistos Places: TLS certificate error, unverified.
  - Not checked: GeoNames historical, Euratlas (commercial) and Linked Art.
- Track: subject
- Affects: the ranking (put these below the core sources)
- Magnitude: n/a (initial)
- Suggested response: n/a (subject)
- Sources: https://www.dbpedia.org/blog/, https://clio-infra.eu/, https://www.rug.nl/ggdc/historicaldevelopment/maddison/

### Ranked table

| # | Source | Good for | Query route | Licence | Limits / auth | Tier |
|---|---|---|---|---|---|---|
| 1 | Wikidata | who, when, with whom; ranked lists; QIDs; every era | `query.wikidata.org/sparql`; REST `w/rest.php/wikibase/v1`; `Special:EntityData/Q.json` | CC0 | 60 s timeout; 60 s/60 s per UA+IP; 5 parallel; UA required | 3 (2 when referenced) |
| 2 | Pleiades | ancient Mediterranean and Near East places | daily `pleiades-places-latest.json.gz`; `/places/{id}/json` | CC BY 3.0 | none stated | 1 |
| 3 | PeriodO | period names to date ranges, with their sources | `n2t.net/ark:/99152/p0dataset.json` | CC0 | none | 1 |
| 4 | Cliopatria (Seshat) | polity borders 3400 BCE–2024 CE, with QIDs | GitHub `cliopatria.geojson.zip`; Zenodo | CC BY 4.0 | none | 1 |
| 5 | WHG | places worldwide, all eras; reconciliation | `whgazetteer.org/entity/place:{id}/api`; `/reconcile` | per source | token; 600/min; 5,000/day; UA | 2 |
| 6 | CHGIS TGAZ | Chinese places 221 BCE–1911 | `chgis.hudci.org/tgaz/placename?n=&yr=&fmt=json` | unstated, not redistributable | none stated | 1 |
| 7 | Wikipedia REST/Action | routing; summaries; QID per title | `/api/rest_v1/page/summary/{title}`; `w/api.php` | CC BY-SA 4.0 | 200/min with contact UA; 10/min without | 3 |
| 8 | Seshat Polaris-2026 | comparative polity variables | `seshat-db.com/api/`; Polaris2026.xlsx | CC BY-NC-SA | API root open | 1 |
| 9 | OWID | quantitative long-run series | `/grapher/{slug}.csv`/`.metadata.json` | CC BY 4.0 (some series 403) | none documented | 2 |
| 10 | Getty TGN/ULAN/AAT | historical place names, artists, object terms | `vocab.getty.edu/sparql`; monthly N-Triples | ODC-By 1.0 | none stated | 2 |
| 11 | OpenHistoricalMap | dated map features, boundaries | planet dumps, vector tiles, Overpass, QLever | CC0 (mostly) | none stated | 3 |
| 12 | ToposText | ancient places with text citations | GeoJSON or TTL downloads | attribution, unclear | no API | 2 |
| 13 | D-PLACE | comparative ethnography | dplace-cldf v3.3.0 | CC BY-NC 4.0 | none | 1 |
| 14 | Clio Infra / Maddison | historical economics | Excel downloads | unstated / see site | none | 2, frozen |
| 15 | DBpedia | nothing Wikidata lacks | `dbpedia.org/sparql` | CC BY-SA | n/a | 3, drop |

## Overall magnitude: n/a (initial)

## Open questions:
- Resolved: the WDQS endpoints after the split; the Wikidata date and calendar model; the 2026 Wikimedia rate limits; that api.wikimedia.org is sunset; the WHG auth and quotas; the Seshat access route in 2026; the Pleiades formats.
- New: how to fetch a page's references robustly. Candidates are the Parsoid `/w/rest.php/v1/page/{title}/html` (the `mw:Extension/references` list) or `action=parse&prop=text|externallinks`; neither was tested.
- New: is the Attribution API (beta, 2026-04-20) useful for citation lines?
- New: WDQS backend migration (QLever?) has no date.
- Still open: DARE and Imperium data routes; Trismegistos access (TLS error); GeoNames historical; Linked Art; the date of PeriodO's last dataset change; the Clio Infra licence.

## Search plan notes:
- Subject: the strongest primary sources were the Wikimedia APIs changelog, Help:Dates, the WDQS graph-split page, WHG's technical docs and the Pleiades downloads page, plus live endpoint probes (TGAZ, page summary, pageassessments, xtools).
- Search hits from listicles and mirrors were noise.
- Getty's new data-services page truncates in WebFetch; use getty.edu/research/tools/vocabularies/obtain/.
- Forums to watch: the Wikidata Project chat and WDQS pages, mediawiki-api-announce, WHG's blog.whgazetteer.org, and the Pleiades changes RSS.
- Lead for the tooling pass: community skills and MCP servers for CHGIS already exist (skills.cat `kltng/humanities-skills/chgis-tgaz`, Glama `huajibing/CHGIS_MCP_Server`).
- The shared WebSearch budget ran out after 16 searches (two more were refused: Clio Infra and D-PLACE). I covered those with direct fetches.

## Tracks covered: subject: 18 queries (2 refused by budget) · tooling: 0 (another part) · practice: 0 (another part) · testing: 0 (another part)

## Upcoming events:
- 2026-10-19 · OAuth 2 client-credential apps registered from this date are no longer treated as anonymous by Wikimedia rate limits.
- end of September 2026 (passed) · Wikimedia Math API sunset (irrelevant here).
- undated · WDQS Blazegraph replacement.

## Nothing changed: no (creation pass; state of the art established).

## Cost: searches 18 · fetches 42 · tool calls 62
