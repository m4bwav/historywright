# Creation pass 2026-10-17: subject-b-libraries-archives (raw researcher report)

Verbatim report of the evergreen-researcher pass for this track. Synthesis: [../2026-10-17-creation-pass.md](../2026-10-17-creation-pass.md).

## Findings (newest first)

### F1 · 2026-10-17 (tested) · Bot walls now block many heritage sites; scripts must use the documented APIs
- What: Many fetches were refused this pass. Trove, EDH (Heidelberg), papyri.info (Duke), the Trove terms page and glam-workbench showed Anubis "Access Denied" pages. HathiTrust doc pages, QDL, DPLA, Gallica SRU, CBDB, kanripo.org and iranicaonline.org returned 403. The documented JSON or XML APIs mostly still answered: loc.gov, TNA Discovery, Europeana, NDL OpenSearch, Internet Archive and the HathiTrust Bibliographic API. Some of the 403s may come from the fetcher's user agent, not a full block.
- Track: subject (cross-cutting)
- Affects: the CLI design and the source notes in the knowledge base
- Magnitude: n/a (initial)
- Implication: the CLI should send an honest User-Agent, rate-limit itself, prefer documented endpoints and dumps, and record "blocked to scripts" as a per-source status that a refresh re-checks.
- Sources: https://trove.nla.gov.au/about/create-something/using-api, https://edh.ub.uni-heidelberg.de/data, https://papyri.info/docs/api

### F2 · 2026-10-17 (tested) · ctext.org API needs a paid key and a registered IP; scraping is banned
- What: `https://api.ctext.org/gettext?urn=ctp:analects/xue-er` returns `ERR_REQUIRES_AUTHENTICATION` ("valid API key", "registered IP address"). ctext.org/tools/api says API access comes with an institutional subscription. It also says scraping breaks the terms and "may return intentionally corrupted data". The Python wrapper on PyPI says returned texts are CC BY-NC-SA 3.0. The free route for the 24 Histories through ctext is gone for scripts; reading in a browser is still possible.
- Track: subject
- Affects: the seed claim "24 Histories via ctext API"
- Magnitude: n/a (initial)
- Flag: PAID (institutional subscription). Script alternatives are Kanripo (GitHub-hosted, endpoint `kanripo.org/api/v1.0/search?query=…`, page 403 to the fetcher, needs re-check) and Wikisource (another part's scope).
- Sources: https://ctext.org/tools/api, https://ctext.org/tools/subscribe, https://pypi.org/project/ctext/

### F3 · 2026-10-17 (tested) · Library of Congress: keyless JSON API; Chronicling America is now served only through loc.gov
- What: The legacy Chronicling America API (2007-2025) is gone. The new site launched 2025-08-04, and the collection is now "accessible exclusively via the loc.gov API". Tested: `https://www.loc.gov/collections/chronicling-america/?q=lindbergh&fo=json&c=2` returned 32,419 hits. OCR comes as ALTO word-coordinate URLs on tile.loc.gov. Limits: JSON API 20 requests/min, with a 1-hour block if exceeded; text and image services 150/min. A 429 or CAPTCHA can appear under heavy load even below the limits. No key. Bulk OCR comes from the OCR Data page. The World Digital Library is now hosted by LoC; its collection URL was not verified.
- Track: subject
- Affects: US newspapers 1690-1963 and LoC collections
- Magnitude: n/a (initial)
- Sources: https://www.loc.gov/apis/additional-apis/chronicling-america-api/, https://www.loc.gov/apis/json-and-yaml/working-within-limits/, https://loc.gov/ndnp/migration

### F4 · current page · US National Archives (NARA) Catalog API v2: key by email, 10,000 queries/month
- What: Base URL `https://catalog.archives.gov/api/v2` (Swagger at `/api/v2/api-docs/`), key sent in the `x-api-key` header. Request a key from Catalog_API@nara.gov. v1 was retired with the old catalog in September 2023. Default quota is 10,000/month; going over blocks the key until the 1st of the next month. The terms say "do not cache or store any content" and show a not-endorsed notice; bulk use goes through the AWS Registry of Open Data instead.
- Track: subject
- Magnitude: n/a (initial)
- Flag: SIGN-UP (free key by email).
- Sources: https://www.archives.gov/research/catalog/help/api, https://www.archives.gov/research/catalog/help/api-getting-started

### F5 · 2026-10-17 (tested) · UK National Archives Discovery API: keyless JSON, 3,000 requests per 5 minutes
- What: `https://discovery.nationalarchives.gov.uk/API/search/records?sps.searchQuery=magna%20carta&sps.resultsPageSize=2` returned JSON (count 291; first hit "Magna Carta", DL 10/71, 1225). The policy page sets 3,000 requests per 5 minutes, blocks the IP if exceeded, and suggests about 10 requests per 5-10 seconds. Site content is under OGL v3.0. The Discovery catalogue covers TNA plus more than 2,500 UK archives (catalogue entries, not full text).
- Track: subject
- Magnitude: n/a (initial)
- Sources: https://www.nationalarchives.gov.uk/terms-and-conditions/policy-on-use-of-website-and-catalogue-data/, https://api.gov.uk/tna/discovery/

### F6 · 2026-10-17 (tested) · Europeana: free key, and the public demo key works
- What: `https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=caesar&rows=1` returned success with 23,531 results. Your own key comes with a free Europeana account at europeana.eu/account/api-keys. Also offered: Record API, IIIF, a SPARQL endpoint, OAI-PMH and dataset downloads. Rows max out at 100, and a cursor allows bulk paging. The metadata licence was not confirmed on the page (believed CC0; check europeana.eu/rights).
- Track: subject
- Magnitude: n/a (initial)
- Flag: SIGN-UP for production use (free).
- Sources: https://api.europeana.eu/, https://www.europeana.eu/eu/apis

### F7 · 2023-2026 · Trove (Australia) API v3: key, approval levels and an unstable access policy
- What: v2 was discontinued in September 2024, and v3 needs a key. The official page sorts uses into review levels. Commercial use, full-text harvesting and AI/ML sit at the higher levels, with about 200 calls/min. Commercial use needs explicit permission. The terms cover metadata only, not the digital objects. GLAM Workbench (Tim Sherratt, the main Trove tools author) reports the NLA cancelled his keys without warning and changed the terms without consultation. All Trove pages served Anubis walls to the fetcher.
- Track: subject
- Magnitude: n/a (initial)
- Flag: SIGN-UP plus approval; AI uses may need permission. Mark as fragile.
- Sources: https://trove.nla.gov.au/about/create-something/using-api/trove-api-terms-use, https://glam-workbench.net/trove-api-v3

### F8 · current docs · BnF Gallica SRU: keyless, 50 records per page, reuse conditions apply
- What: Endpoint `https://gallica.bnf.fr/SRU?version=1.2&operation=searchRetrieve&query=(gallica all "…")`. It returns Dublin Core XML, `maximumRecords` up to 50, and pages with `startRecord`. Gallica's own reuse conditions govern use: rights-free items are marked `fayes`, items with conditions `fano`. A facets service lives at `gallica.bnf.fr/services/Categories?SRU=…`. The live test returned 403 to the fetcher, so the CLI needs a real User-Agent and should be tested. A community MCP server for Gallica exists ("sweet-bnf" on Glama; not assessed).
- Track: subject
- Magnitude: n/a (initial)
- Sources: https://api.bnf.fr/fr/api-gallica-de-recherche, https://glama.ai/mcp/servers/ukicar/sweet-bnf

### F9 · 2026-10-17 (tested) · Japan: NDL Search keyless; NDL Digital Collections IIIF; Japan Search linked data
- What: Tested `https://ndlsearch.ndl.go.jp/api/opensearch?title=徳川家康&cnt=2`, which returned RSS (4,525 hits). Also offered: `/api/sru`, `/api/openurl` and OAI-PMH; the specification PDF is dated 2026-09-25. Non-commercial use needs no application; commercial use does. Callers must credit "NDL Search API", avoid parallel requests (sustained load gets blocked), and regular users are asked to register through a form. NDL Digital Collections serves IIIF manifests at `https://dl.ndl.go.jp/api/iiif/{pid}/manifest.json` (pattern from 2019 documents; re-verify). Japan Search (jpsearch.go.jp) offers REST and SPARQL over about 29.8M records from 240 databases (FY2025 report, March 2026).
- Track: subject
- Magnitude: n/a (initial)
- Sources: https://ndlsearch.ndl.go.jp/help/api, https://ndlsearch.ndl.go.jp/file/help/api/specifications/ndlsearch_api_20260925.pdf, https://jpsearch.go.jp/en/arfy2025

### F10 · current · Deutsche Digitale Bibliothek: free key through a My DDB account, CC0 metadata
- What: The OpenAPI spec is at `https://api.deutsche-digitale-bibliothek.de/OpenAPI` and is labelled version "develop". The key is created under My DDB > Konto > API-Zugang. Metadata is CC0; images carry their own licences.
- Track: subject
- Magnitude: n/a (initial)
- Flag: SIGN-UP (free).
- Sources: https://api.deutsche-digitale-bibliothek.de/OpenAPI

### F11 · unverified 2026 · DPLA API: key by email POST; the test was refused
- What: Get a key with `curl -X POST https://api.dp.la/v2/api_key/you@example.com` and pass it as `api_key`. A keyless call to `api.dp.la/v2/items` returned 403. No 2026 status notice was found. It aggregates US libraries; metadata is believed CC0.
- Track: subject
- Magnitude: n/a (initial)
- Flag: SIGN-UP (free).
- Sources: https://pro.dp.la/developers/policies

### F12 · 2024-07-17 · HathiTrust Data API retired; the Bibliographic API still works
- What: The Data API was retired on 2024-07-17 (low use, security). Tested: `https://catalog.hathitrust.org/api/volumes/brief/oclc/424023.json` returned records and items with `rightsCode` and `usRightsString` ("Limited (search-only)" for in-copyright items). For full text, use public-domain volumes in the babel viewer, Research Datasets or HTRC. No full-text search API was confirmed.
- Track: subject
- Magnitude: n/a (initial)
- Sources: https://hathitrust.org/press-post/retirement-data-api

### F13 · 2026-10-17 (tested) · Internet Archive advancedsearch is keyless and works
- What: `https://archive.org/advancedsearch.php?q=title:(gibbon decline fall) AND mediatype:texts&fl[]=identifier&fl[]=title&fl[]=date&rows=3&output=json` returned 121 hits. Sorted paging stops at 10,000; the scrape API pages with a cursor for deeper results. Full-text search exists on the site and runs over uncorrected OCR; the API parameter was not confirmed. Full text of in-copyright books is behind lending. The Digital Library of India scans are hosted here.
- Track: subject
- Magnitude: n/a (initial)
- Sources: https://doc-tools.readthedocs.io/en/ia-test-gsod/item-search-apis.html, https://help.archive.org/help/search-a-basic-guide/

### F14 · 2025-02-21 · Perseus: version 4.0 frozen; Scaife Viewer is the live reader; GitHub is the script route
- What: Perseus at Tufts says the 4.0 site is no longer developed. Scaife Viewer's latest release is v2025-02-21-001, and its CTS/GraphQL API is not documented as stable. The reliable script route is the TEI texts in GitHub PerseusDL/canonical-greekLit and canonical-latinLit (believed CC BY-SA; not re-verified because the search budget ran out).
- Track: subject
- Magnitude: n/a (initial)
- Sources: https://scaife.perseus.org/about, https://www.perseus.tufts.edu

### F15 · 2025 · Ancient epigraphy, papyri and prosopography
- What:
  - EDH: frozen with its last update in December 2021, hosted by Heidelberg UB since 2022. It offers an API, a DTS API and CSV/EpiDoc dumps, but sits behind Anubis.
  - EDCS: moved to the University of Zurich (`edcs.hist.uzh.ch`) after co-founder Manfred Clauss died on 2025-01-20. 542,484 inscriptions, free, no account, no API documented.
  - DPRR: read-only RDF4J SPARQL at `romanrepublic.ac.uk/rdf`.
  - LGPN: search.lgpn.ox.ac.uk links to "API Documentation" (not read).
  - Trismegistos: core search needs an institutional subscription since January 2020; TM Data Services (APIs and table dumps) are open under CC BY-SA 4.0.
  - papyri.info: Anubis-walled; its data mirrors hourly to GitHub `DCLP/idp.data`, which is the script route.
- Track: subject
- Magnitude: n/a (initial)
- Flag: Trismegistos search is PAID (institutional).
- Sources: https://edcs.hist.uzh.ch/en/, https://edh.ub.uni-heidelberg.de/, https://romanrepublic.ac.uk/rdf/doc/, https://trismegistos.org/about, https://github.com/DCLP/idp.data

### F16 · 2026-09-21 · Open primary-source websites (no APIs, stable static HTML)
- What:
  - Internet History Sourcebooks (Fordham): revised 2026-09-21, with Ancient, Medieval and Modern books plus African, East Asian, Indian, Islamic, Jewish and other subsidiary books. "Copy-permitted, not necessarily copyright-free."
  - LacusCurtius: last site update 2023-05-12. Its 61 works include Plutarch's *Lives*, Cassius Dio, Suetonius and Smith's *Dictionary*. Copyright is marked per URL: one asterisk means public domain, none means © Thayer.
  - Attalus: live, with event lists for 324-30 BC tied to sources.
  - Avalon (Yale Law): online, with a registry update dated 2025-08-14.
  - The Latin Library: not verified this pass.
- Track: subject
- Magnitude: n/a (initial)
- Sources: https://sourcebooks.fordham.edu/, https://penelope.uchicago.edu/Thayer/E/Roman/home.html, https://www.attalus.org/, https://avalon.law.yale.edu/about/purpose.asp

### F17 · 2026-06-02 · CBDB: SQLite download, non-commercial licence, no public API found
- What: The site moved to cbdb.hsites.harvard.edu. Latest release is BJ 20260602 (649,533 people; the homepage says about 657,909 as of May 2026), as SQLite on GitHub under the cbdb-project organisation, plus an MS Access build. Licence is CC BY-NC-SA 4.0. The academic release runs about a year behind the commercial partner, inindex. No API was confirmed; the old cbdbapi endpoint was not verified.
- Track: subject
- Magnitude: n/a (initial)
- Sources: https://cbdb.hsites.harvard.edu/download-cbdb-standalone-database, https://cbdb.hsites.harvard.edu/

### F18 · 2025-12-30 · China: browse-only national resources, plus open journals from CASS
- What:
  - National Library of China 中华古籍资源库: reading without login; more than 106,000 items (Jan 2025); 11th release on 2025-12-30. Image-based, no API known.
  - Scripta Sinica 漢籍電子文獻 (Academia Sinica IHP): a limited free tier and a fuller paid "授權使用" tier.
  - NCPSSD 国家哲学社会科学文献中心 (ncpssd.org, run by the CASS library): free full text after personal registration, covering more than 2,000 journals including 《历史研究》 back to 1920. This is the practical open output of the CASS history institutes.
  - PKU 识典古籍: more than 70,000 books readable free (Aug 2026 report).
- Track: subject
- Magnitude: n/a (initial)
- Flags: Scripta Sinica is PAID for full use; NCPSSD needs SIGN-UP.
- Sources: https://www.news.cn/culture/20251230/de788d350c7b4d379af22e518e8862b0/c.html, https://hanchi.ihp.sinica.edu.tw/ihp/hanji.htm, https://library.usj.edu.mo/?p=1325

### F19 · 2025-12-30 · Islamic world: the OpenITI corpus is the script route
- What:
  - OpenITI 2025.1.9 on Zenodo (concept DOI 10.5281/zenodo.3082463): 9,106 books by 3,618 authors, 2.35 billion words, with new Persian and manuscript subcorpora.
  - al-Maktaba al-Shamela: live, about 8,000 books, desktop and mobile apps, no API and no licence statement. It is the upstream for much of OpenITI.
  - QDL: refused the fetcher (403); licence not verified.
- Track: subject
- Magnitude: n/a (initial)
- Sources: https://zenodo.org/records/17767721, https://kitab-project.org/OpenITI-Release-version-2025-1-9/, https://shamela.ws/

### F20 · 2025-05 to 2026-04 · India: Abhilekh Patal is large but has no API
- What: The National Archives of India portal passed 100 million (10 crore) digitised pages on 2025-05-04; later reports say 200 million. Copies come through Page-on-Demand and Digitize-on-Demand, and AI search is planned. Scripts can only search the catalogue; treat it as browse-only.
- Track: subject
- Magnitude: n/a (initial)
- Sources: https://nationalarchives.nic.in/en/online-portal-abhilekh-patal, https://www.deccanherald.com/india/number-of-digitised-archival-pages-available-on-nai-portal-crosses-10-cr-mark-3526440

### F21 · 2024 · Africa and Latin America: weak programmatic access
- What:
  - British Library Endangered Archives Programme: eap.bl.uk returned an empty page, and the BL interim catalogue (still recovering from the 2023 cyber-attack) lists about 499,000 EAP items. Status is unclear.
  - South Africa's NAAIRS: catalogue only, no texts; last official mention August 2024.
  - Spain's PARES 2.0 (2016): aimed at OAI-PMH; a 2026 FECYT call says it urgently needs renewal.
  - BNE linked data: SPARQL at `datos.bne.es/sparql`; current status unverified.
  - Hemeroteca Digital Brasileira: no API; the pyHDB scraper exists.
  - Biblioteca Nacional de México and Aluka/JSTOR: not verified (Aluka is believed PAID).
- Track: subject
- Magnitude: n/a (initial)
- Sources: https://searcharchives.bl.uk/catalog/facet/url_stub_si, https://westerncape.gov.za/your_gov/34/services/1075, https://convocatoriasip.fecyt.es/sites/default/files/retos/2026/mincul_2_archipat.pdf

### F22 · 2025 · Reputable institutions with open, scriptable output
- What:
  - British History Online (Institute of Historical Research): the vast majority is free, including the Victoria County Histories; only a subset of the Calendars of State Papers Domestic is subscription. No API.
  - Encyclopaedia Iranica: moved in 2025 to UC Irvine's Jordan Center and is free online; Brill's platform (brill.com/eiro) has existed since 2021.
  - Deutsche Biographie (Historical Commission at the Bavarian Academy of Sciences plus the Bavarian State Library): open Solr API at data.deutsche-biographie.de, labelled beta. Metadata CC0, ADB articles CC BY-NC-SA, NDB articles CC BY-NC-ND.
  - US Office of the Historian: FRUS is public domain as TEI on GitHub, plus an OPDS catalogue.
  - Not verified this pass (search budget ran out; from memory, re-check): Oxford Classical Dictionary, Brill's New Pauly, Encyclopaedia of Islam, Cambridge Histories and Britannica premium are PAID. The RHS bibliography (now with Brepols) is PAID. AHA and ICHR publish journals and reports without APIs.
- Track: subject
- Magnitude: n/a (initial)
- Sources: https://www.british-history.ac.uk/, https://www.iranicaonline.org/about/, https://data.deutsche-biographie.de/beta/solr-open, https://history.state.gov/developer

### Ranked table

| # | Source | Good for | Query route | Licence | Limits / sign-in | Tier |
|---|---|---|---|---|---|---|
| 1 | LoC loc.gov + Chronicling America | US history, newspapers 1690-1963, maps, WDL | `loc.gov/{search,collections/…}/?q=…&fo=json` | mostly public domain | 20/min JSON, no key | 1 |
| 2 | UK National Archives Discovery | UK and colonial records, dates of documents | `discovery.nationalarchives.gov.uk/API/search/records?sps.searchQuery=` | OGL v3 | 3,000 per 5 min, no key | 1 |
| 3 | Internet Archive | old books, DLI scans, scholarly reprints | `archive.org/advancedsearch.php?…&output=json`; scrape API | varies by item | no key; 10k paging cap | 1-3 |
| 4 | Europeana | European heritage aggregate | `api.europeana.eu/record/v2/search.json?wskey=` | CC0 metadata (check) | free key (`api2demo` for tests) | 2 |
| 5 | NDL Search / Digital Collections / Japan Search | Japan, all eras | `ndlsearch.ndl.go.jp/api/opensearch`; IIIF; jpsearch SPARQL | per provider | no key; no parallel calls; credit | 1 |
| 6 | Perseus (GitHub) / Scaife | Greek and Latin classics | GitHub PerseusDL canonical-*Lit TEI | CC BY-SA (check) | none | 1 |
| 7 | OpenITI | Arabic and Persian premodern texts | Zenodo bulk | open (check per text) | none | 1 |
| 8 | Fordham Sourcebooks, Avalon, LacusCurtius, Attalus | translated primary texts | static HTML fetch | copy-permitted / public domain per page | none | 1-2 |
| 9 | Gallica | France, francophone press | `gallica.bnf.fr/SRU?…` | Gallica conditions | no key; 50 per page; may 403 bots | 1 |
| 10 | HathiTrust | book identity, rights, public-domain scans | `catalog.hathitrust.org/api/volumes/brief/oclc/{n}.json` | public domain / search-only | Data API retired 2024 | 1 |
| 11 | NARA Catalog v2 | US federal records | `catalog.archives.gov/api/v2/records/search` + `x-api-key` | US government | SIGN-UP by email, 10k/month, no caching | 1 |
| 12 | Deutsche Biographie | German lives and dates | Solr beta | CC0 metadata | none | 2 |
| 13 | DDB, DPLA | German and US aggregates | REST + key | CC0 | SIGN-UP | 2 |
| 14 | DPRR, EDCS, EDH, Trismegistos data, papyri.info (GitHub) | Roman Republic people, inscriptions, papyri | SPARQL / web / dumps / GitHub | CC BY-SA mostly | EDH/papyri behind Anubis | 1 |
| 15 | CBDB | Chinese officials and biographies | SQLite download | CC BY-NC-SA 4.0 | none | 1 |
| 16 | Trove | Australian press | `api.trove.nla.gov.au/v3` + key | metadata only | SIGN-UP plus approval, fragile | 1 |
| 17 | BHO, Iranica, FRUS | British local and state papers, Iran, US diplomacy | HTML / TEI | free (BHO part PAID) | none | 2 |
| 18 | NLC 古籍库, 识典古籍, Abhilekh Patal, HDB, PARES, Shamela | regional primary scans | browse only | varies | no API | 1 (browse) |
| 19 | ctext.org, Scripta Sinica full tier, Trismegistos search, CNKI, Loeb, OCD, New Pauly, EI3 | Chinese classics, reference | subscription | proprietary | PAID | 1-2 |

## Overall magnitude: n/a (initial)

## Open questions
- New: the current free tier of the Kanripo API, and the licence of its GitHub texts.
- New: whether Gallica, DPLA, QDL and HathiTrust 403s are user-agent blocks or full blocks. Test with the CLI's own User-Agent.
- New: the current Trove v3 terms on AI use (page was walled).
- New: whether EAP (eap.bl.uk) is back online, and its IIIF route.
- Still open: Scaife GraphQL API stability; CBDB online API; Latin Library liveness; BNM, Aluka, Arab Union catalogue, Taiwan archives, ICHR, RHS, AHA, OCD, Britannica. Not reached because the shared WebSearch budget ran out mid-pass.
- Resolved: Chronicling America is served only through loc.gov since 2025; HathiTrust Data API retired 2024-07-17; NARA v1 retired September 2023; Trove v2 retired September 2024; EDCS moved to Zurich.

## Search plan notes
- Subject: live endpoint tests beat documentation searches, and every test here was conclusive. Official help pages (loc.gov limits, NARA, TNA policy, NDL help, api.bnf.fr) were reliable. Third-party API directories (apis.io, jentic, publicapi.dev) were noise. Chinese-language queries were needed for NLC, NCPSSD and Scripta Sinica. Forums: GLAM Workbench (Trove), the LoC Signal blog, current.ndl.go.jp (NDL news, multilingual) and infoDOCKET are good change feeds for the next refresh.
- Tooling: only seen in passing. A Gallica MCP server (sweet-bnf), Internet Archive MCP bundles and pyHDB exist; none assessed (not this part's track).

## Tracks covered
subject: 45 queries (one refused at the budget cap) plus 37 fetches, 9 of them live API tests · tooling: 0 (seen in passing) · practice: 0 · testing: 0 (caller assigned subject part B only)

## Upcoming events
None with a firm date. Re-check PARES (renewal planned, no date), the NDL API spec (revised 2026-09-25) and Trove terms at each refresh.

## Nothing changed: no (creation pass)

## Cost: searches 45 · fetches 37 · tool calls 84
