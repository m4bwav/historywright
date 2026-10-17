# Creation pass 2026-10-17: subject-c-archaeology-scholarship-museums (raw researcher report)

Verbatim report of the evergreen-researcher pass for this track. Synthesis: [../2026-10-17-creation-pass.md](../2026-10-17-creation-pass.md).

## Findings (newest first)

### F1 · 2026-10-01 · The Met's v1 search endpoint is retired; v1.1 is the only search route
- What: The Met's API docs listed `/public/collection/v1/search` as "deprecated and retiring October 1, 2026". The replacement is `/public/collection/v1.1/search`. It takes the same filters (`q`, `hasImages`, `departmentId`, `dateBegin`/`dateEnd` with negative years for BCE, `geoLocation`, `medium`), adds `offset`/`limit` (default 100, max 500), and caps `offset+limit` at 10,000. No key is needed, and the docs ask for under 80 requests per second. Records carry `isPublicDomain`, `primaryImage` and `additionalImages`; open-access images are CC0. Live test on 2026-10-17: `v1.1/search?q=helmet&hasImages=true&departmentId=13` returned 896 IDs. Object 255926 came back `isPublicDomain:true`, but it is a Greek Cretan helmet of 630–600 BCE. There is no culture filter, so date and culture have to be filtered after fetching.
- Track: subject
- Affects: the museum query module (the `/objects` endpoint or the Open Access CSV for bulk; never v1 search); the Roman legionary example pack
- Magnitude: n/a (initial)
- Sources: https://metmuseum.github.io/, https://collectionapi.metmuseum.org/public/collection/v1/objects/255926

### F2 · 2026-04-24 (page edit) · Wikimedia APIs need a User-Agent with contact details; Commons throttles clients it cannot identify
- What: Every request must send a User-Agent of the form client/version (contact) library/version. Requests without one "may be blocked without notice", and authenticated (OAuth 2.0) clients get higher limits. MediaWiki's InstantCommons notes say Commons began throttling unidentified server requests in late 2025. Licences differ per file and come from `prop=imageinfo&iiprop=extmetadata`. I did not confirm the exact field name `LicenseShortName`.
- Track: subject
- Affects: the CLI's HTTP layer (one shared User-Agent for every source); the image manifest's licence field
- Magnitude: n/a (initial)
- Sources: https://www.mediawiki.org/wiki/Wikimedia_APIs/Access_policy, https://www.mediawiki.org/wiki/Extension:CommonsMetadata/en, https://www.mediawiki.org/wiki/Instant_Commons

### F3 · 2026-03 · A successor to IntCal20 is in preparation; IntCal20 is still current
- What: A Cambridge talk listing (March 2026, titled "IntCal26 and Radiocarbon Dating") says the next IntCal update is underway, with publication hoped for in 2026 or 2027. intcal.org still lists only IntCal20, SHCal20 and Marine20 (August 2020). The Python route is IOSACal (GPL, a library plus CLI, built-in `intcal20`, commits into 2026). OxCal is a standalone program, not a Python library. IntChron exports dates in an OxCal format.
- Track: subject
- Affects: any "calibrated date" claim in answer.md; dates in timeline.json should record which curve was used
- Magnitude: n/a (initial)
- Sources: https://www.talks.cam.ac.uk/talk/index/243610/, https://www.intcal.org/publications.html, https://iosacal.readthedocs.io

### F4 · 2026-02-13 · OpenAlex now runs on API keys and a daily dollar budget; the polite pool is gone
- What: The official help pages give the rules. A free key gives $1.00 of usage per day, ten times the keyless budget (about $0.10). The rate cap is 10 requests per second without a key, 30 with a free key or prepaid usage, and 50 on an annual plan. Semantic search is limited to 1 request per second. Heavier use is pay-as-you-go, and each response reports its cost in `meta.cost_usd`. Budget is checked at `GET https://api.openalex.org/rate-limit?api_key=`. Keys come from openalex.org/signup, or an agent can `POST https://api.openalex.org/api-keys` with the user's email, after which the user must click an activation link. The `mailto` polite pool is no longer described; a client's docs say it is ignored. Many community OpenAlex skills and MCP servers still pass `mailto` and assume 100k calls a day.
- Track: subject
- Affects: the scholarship module (key flagged as "free sign-in"); budget handling
- Magnitude: n/a (initial)
- Sources: https://help.openalex.org/how-to-use-the-api/rate-limits-and-authentication, https://help.openalex.org/api-reference/authentication.md, https://casrai.org/news/openalex-api-keys-mandatory-usage-based-pricing-2026

### F5 · 2025-12-01 · New Crossref REST API rate limits
- What: Announced 2025-11-05 and effective 2025-12-01. Public pool: single records at 5 requests per second, lists at 1 per second, concurrency 1. Polite pool (`mailto=` parameter or in the User-Agent): single DOIs at 10 per second, lists at 3 per second, concurrency 3. Metadata Plus is paid and unaffected.
- Track: subject
- Affects: the DOI verification step (one request at a time, mailto always sent)
- Magnitude: n/a (initial)
- Sources: https://crossref.org/blog/announcing-changes-to-rest-api-rate-limits/

### F6 · 2025-09 · Archaeology Data Service: a new single catalogue replaced ArchSearch; no public API yet
- What: The new catalogue searches about 5,000 ADS archives and more than 100,000 grey-literature reports, plus Historic England and RCAHMW records. ADS ran a survey on APIs in May 2025, but I found no launched API. ADS says its archives are open access, but licences are per archive. The route is web search plus OAI-PMH or metadata harvesting.
- Track: subject
- Affects: the archaeology source list (manual or link-out tier)
- Magnitude: n/a (initial)
- Sources: https://archaeologydataservice.ac.uk/news-events/coming-soon/, https://archaeologydataservice.ac.uk/blog/author/nicky-garland/

### F7 · 2025-08-04 · Chronicling America is reachable only through the loc.gov API
- What: The dedicated API (2007–2025) is gone, and the collection is served through the loc.gov JSON API. Adding `?fo=json` to any loc.gov page returns its data. No key is needed. The official limit for the JSON/YAML API is 20 requests per minute with a one-hour block if exceeded; text and image services allow 150 per minute. LoC warns of 429s or CAPTCHAs even below those rates, a paging cap of 100,000 items, page sizes of 1,000 or less, and data that is not fully synced since the migration.
- Track: subject
- Affects: the newspaper module (throttle to 1 request per 3 s, handle 429 and CAPTCHA pages)
- Magnitude: n/a (initial)
- Sources: https://www.loc.gov/apis/additional-apis/chronicling-america-api/, https://www.loc.gov/apis/json-and-yaml/working-within-limits/, https://loc.gov/ndnp/migration

### F8 · 2025-07-01 · JSTOR Constellate shut down; JSTOR has no open search API
- What: ITHAKA retired Constellate on 2025-07-01. The replacement, JSTOR Text Analysis Support (jstor.org/ta-support), is a request process for full-text datasets, not a query API. JSTOR is a link-out or sign-in source only.
- Track: subject
- Affects: the scholarship list (JSTOR flagged as sign-in, no API)
- Magnitude: n/a (initial)
- Sources: https://mdl.library.utoronto.ca/mdl-blog/jstor-text-analysis-support-replaces-constellate, https://digitalhumanitiesnow.org/2025/08/constellate-an-experiment-and-retrospective/

### F9 · 2025-01 · The Bibliography of British and Irish History is no longer the RHS's
- What: The RHS left in January 2025. BBIH continues under the IHR and Brepols on a new five-year agreement, edited at the IHR and sold by subscription (Brepols). It is paid, with no open API. Update notes appear on the IHR blog (latest seen October 2025).
- Track: subject
- Affects: the seed list (rename it "IHR/Brepols BBIH", flag as paid)
- Magnitude: n/a (initial)
- Sources: https://royalhistsoc.org/the-bibliography-of-british-and-irish-history/, https://blog.history.ac.uk/2025/07/bibliography-of-british-and-irish-history-june-2025-update/

### F10 · 2025 (undated) · Rijksmuseum: the old key-based API is removed; the new Linked Art search needs no key
- What: `https://data.rijksmuseum.nl/search/collection` takes `title`, `creator`, `type`, `material`, `technique`, `description`, `creationDate` (wildcards), `imageAvailable` and `pageToken`, returns 100 Linked Art IDs per page, and needs no key. Records are then resolved through the PID resolver. The docs label it beta, SRU is marked deprecated, and the old Rijksstudio key API is gone (third-party clients report 410 Gone). The data page covers 800,000 object records and 600,000 images, with most objects public domain since 2013. CC0 was not stated on the pages read, so the licence should be taken from each record.
- Track: subject
- Affects: the museum module (two-step search then resolve; per-record licence)
- Magnitude: n/a (initial)
- Sources: https://data.rijksmuseum.nl/docs/search, https://data.rijksmuseum.nl/, https://metacpan.org/pod/Museum::Rijksmuseum::Object

### F11 · undated (2024–2025) · Trove: v3 needs a key, commercial use needs permission, and keys have been cancelled
- What: Trove API v2 was decommissioned in September 2024, and v3 requires a key that is free and instant for non-commercial use. The GLAM Workbench maintainer, the main independent Trove tooling author, reports that the NLA cancelled his keys and changed the terms without consultation. He has archived his Trove code. The banner is undated and I found no NLA statement.
- Track: subject
- Affects: the newspaper module (Trove flagged as key plus terms risk)
- Magnitude: n/a (initial)
- Sources: https://trove.nla.gov.au/about/create-something/using-api, https://glam-workbench.net/trove/

### F12 · current · CC0 museum APIs worth building on (verified)
- What: These are verified from official docs or live calls.
  - **Cleveland:** `openaccess-api.clevelandart.org/api/artworks/?q=&has_image=1&cc0=1`, no key. Live test: "roman helmet" returned 34 hits, all `share_license_status: CC0`, but the helmets are Greek (Corinthian, Chalcidian), not Roman.
  - **Art Institute of Chicago:** 60 requests per minute per IP, an optional `AIC-User-Agent` header, `query[term][is_public_domain]=true`, and images at `iiif/2/{image_id}/full/843,/0/default.jpg`. Data is CC0 except `description` and place fields (CC-BY 4.0). Nightly dumps are at GitHub `art-institute-of-chicago/api-data`.
  - **Getty:** Linked Art API plus SPARQL at data.getty.edu, CC0 with exceptions; images CC0 (88,000+ as of 2024).
  - **Smithsonian:** `api.si.edu/openaccess/api/v1.0/search`, key from api.data.gov at 1,000 requests per hour (DEMO_KEY allows 30 per hour). Metadata is CC0; media only for CC0 items, so filter on the usage access field.
- Track: subject
- Affects: the image-reference module (CC0-first ordering)
- Magnitude: n/a (initial)
- Sources: https://openaccess-api.clevelandart.org/api/artworks/?q=roman%20helmet&has_image=1&cc0=1&limit=10, http://api.artic.edu/docs/, https://data.getty.edu/museum/collection/docs/, https://api.data.gov/docs/developer-manual/, https://edan.si.edu/openaccess/apidocs/

### F13 · current · Museums with restricted licences or no API (flag them, do not ship their images in a CC0 pack)
- What:
  - **British Museum:** CC BY-NC-SA 4.0 for most images; 750 px saved directly, 2,500 px by email request; commercial use is licensed separately. No current API found; the 2011 SPARQL beta was not seen live.
  - **Science Museum Group:** images CC BY-NC-SA 4.0; title, maker and date fields CC0; text CC BY. The API is "heavily rate limited", so use its JSON/CSV dumps.
  - **V&A:** API v2 is free but under the museum's own terms (section 9), not Creative Commons.
  - **Harvard Art Museums:** free key required; image terms not verified.
  - **Europeana:** `api.europeana.eu/record/v2/search.json` with a free `wskey`; rights differ per item, so filter on rights. The docs page refused the fetch.
  - **Prado:** no API. A 2020 claim of CC0 images is unverified, so treat them as restricted.
  - **Paris Musées and National Palace Museum Taipei:** unverified because the search budget ran out.
- Track: subject
- Affects: the licence gate in the manifest (NC and "own terms" images get a non-commercial flag or are left out)
- Magnitude: n/a (initial)
- Sources: https://www.britishmuseum.org/terms-use/copyright-and-permissions/images-and-photography, https://coimages.sciencemuseumgroup.org.uk/datasets/index.html, https://developers.vam.ac.uk/

### F14 · current · The "Roman legionary of 50 BC" pack has a real image gap
- What: The big US CC0 APIs (Met, Cleveland, AIC) return mostly Greek or Etruscan helmets for "Roman helmet" queries. I did not check the Getty or Smithsonian; that is the next search. Late Republican legionary kit (Montefortino or Coolus helmet, pilum, scutum, gladius hispaniensis, mail) survives mostly in European museums. Its images reach agents through Wikimedia Commons (per-file licence), Europeana (per-item rights) and Livius.org (photos stated as CC0). This is inference from the searches, not a full survey. UK Roman finds come from the Portable Antiquities Scheme (`finds.org.uk/database/search/results/q/.../thumbnail/1/format/json`; open-licence images, exact CC licence unconfirmed), though PAS material skews later than 50 BC. Seshat's API has Roman Republic warfare variables.
- Track: subject
- Affects: the example pack and the "sources disagree / thin evidence" note
- Magnitude: n/a (initial)
- Sources: https://www.livius.org/pictures/a/etruscan-art/helmet-from-central-italy/, https://nbviewer.org/github/o-date/notebooks-archdata/tree/master/Retrieving%20Data%20from%20the%20Portable%20Antiquities%20Scheme%20Database.ipynb, https://seshat-db.com/api/

### F15 · current · Archaeology and prehistory data routes (verified state)
- What:
  - **Open Context:** `opencontext.org/query/.json?...` (examples `?proj=24-murlo`, `response=geo-record` for GeoJSON, `rows` up to 1000, chronology parameters `allevent-start`/`allevent-stop`). No key, but it blocks requests without a User-Agent. Licences are CC per project; there is OAI-PMH.
  - **Neotoma:** v2.0 at `api.neotomadb.org`, no key.
  - **Paleobiology Database:** `paleobiodb.org/data1.2/occs/list.csv?...`, no key.
  - **IntChron:** an index rather than a store; REST in JSON, CSV or OxCal format; ORAU and NERC data contain duplicates.
  - **p3k14c:** over 170,000 dates; Zenodo v1.0.0 (2021-10-25) plus an updated DOI (10.6078/M7G73BT5).
  - **tDAR:** OpenSearch and OAI-PMH; downloads need registration.
  - **ARIADNE:** a 4M-record portal; no public API found.
  - **DAACS:** web query tools only.
  - **Database of Religious History:** no official API found; `drhwrapper` on PyPI is a community package.
  - **eHRAF:** institutional membership, interface only (paid, sign-in).
  - **Smithsonian Human Origins:** unverified because the search budget ran out.
- Track: subject
- Affects: the archaeology source list and the places.geojson builder (Open Context's GeoJSON fits it directly)
- Magnitude: n/a (initial)
- Sources: https://opencontext.org/about/services, https://github.com/NeotomaDB/Neotoma-API, https://intchron.org/host, https://p3k14c.org, https://hraf.yale.edu/faq/, https://www.daacs.org/aboutdaacs/

### F16 · current · Sources missing from the seed list: Seshat and D-PLACE
- What: **Seshat Global History Databank** covers 864 polities with variables on social complexity, warfare (chainmail, horses), religion, economy and crisis. It has a Django REST API at `seshat-db.com/api/` (`?format=json`; for example `/api/core/polities/`) and downloads; the licence page was not read. **D-PLACE** has 14 ethnographic datasets (including the Ethnographic Atlas and the Standard Cross-Cultural Sample) as CLDF on GitHub under CC-BY-NC-4.0, with a Zenodo DOI per dataset. D-PLACE is the open counterpart to eHRAF for cross-cultural questions.
- Track: subject
- Affects: the anthropology and structured-history sources
- Magnitude: n/a (initial)
- Sources: https://seshat-db.com/, https://seshat-db.com/api/, https://github.com/D-PLACE/dplace-cldf

### F17 · current · Other scholarship indexes
- What:
  - **Semantic Scholar:** anonymous use shares a 1,000 requests-per-second pool and may be throttled further; keyed use starts at 1 request per second; keys arrive by email.
  - **CORE:** no registration; one batch or five single requests per 10 s; faster rates are typically paid.
  - **DOAJ:** v4 API (`doaj.org/api/search/articles/{q}`), no key, plus public data dumps.
  - **BASE:** IP-whitelisted, non-commercial, request access.
  - **Persée:** OAI-PMH `http://oai.persee.fr/oai` and SPARQL at data.persee.fr.
  - **OpenEdition and Regesta Imperii:** no API found.
  - **Cairn, Brepols:** paid.
  - **Google Scholar:** no API, and its terms forbid scraping.
- Track: subject
- Affects: the scholarship module ranking
- Magnitude: n/a (initial)
- Sources: https://semanticscholar.org/product/api, https://core.ac.uk/services/api, https://testdoaj.cottagelabs.com/api/docs, https://info.persee.fr/data-persee/?lang=en

### F18 · current · Modern and business history routes
- What:
  - **SEC EDGAR:** 10 requests per second; a declared User-Agent with company and email is required. `data.sec.gov/submissions/CIK##########.json` is documented. The full-text search endpoint `efts.sec.gov/LATEST/search-index?q=` is unofficial.
  - **Federal Register:** `federalregister.gov/api/v1/documents.json?conditions[term]=` works with no key (live test 2026-10-17), but its docs page redirected the fetcher to an "unblock" bot page.
  - **Wayback CDX:** `web.archive.org/cdx/search/cdx?url=&output=json&from=&to=&collapse=&filter=&limit=`, with a resumeKey for paging. No official rate limit; third-party clients report 429s near 15 per minute.
  - **Computer History Museum oral histories:** web search only (`?s=`), no API; transcripts are online.
  - **Historic Hansard 1803–2005:** static pages at `api.parliament.uk/historic-hansard/`, with an undated "temporarily moved" notice.
  - **NYT Article Search:** key required; about 10 per minute and 4,000 per day (secondary sources; the developer site refused the fetch).
  - **Guardian:** key required; about 5,000 per day free (secondary; the site refused the fetch).
- Track: subject
- Affects: the modern-history module
- Magnitude: n/a (initial)
- Sources: https://www.sec.gov/os/accessing-edgar-data, https://www.federalregister.gov/api/v1/documents.json?per_page=2&conditions[term]=Microsoft, https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md, https://www.computerhistory.org/collections/oralhistories/

### F19 · current · Museum and OpenAlex MCP servers exist; none covers this unit's pack
- What:
  - **archival-imagery-mcp:** covers the Met, LoC, Smithsonian, Europeana and Wellcome, and routes Rijksmuseum through Europeana.
  - **mikechao/metmuseum-mcp:** has an 80 requests-per-second limiter. It may still use the retired v1 search; not checked.
  - **r-huijts/rijksmuseum-mcp:** last updated 2025-02, so likely built on the removed key API.
  - **art-mcp:** runs nightly live-API checks and reports a Rijksmuseum endpoint now returning 410.
  - **oksure/openalex-research-mcp:** ships both an MCP server and a skill.
  - **Kortix and other OpenAlex skills:** still rely on the `mailto` polite pool.

  I did not see install counts. None does licence-gated packs with manifests.
- Track: tooling
- Affects: none directly; the CLI stays stdlib
- Magnitude: n/a (initial)
- Suggested response: point (archival-imagery-mcp, oksure/openalex-research-mcp); note the rest as stale
- Sources: https://glama.ai/mcp/servers/chandhoke/archival-imagery-mcp, https://glama.ai/mcp/servers/puf3zin/art-mcp, https://github.com/oksure/openalex-research-mcp

### F20 · 2025–2026 · History benchmarks and citation-hallucination evidence
- What:
  - **Hist-LLM (reported January 2025):** built on Seshat; GPT-4 Turbo scored about 46%, and models over-rely on prominent data.
  - **ProHist-Bench (ACL 2026):** 400 expert questions with 10,891 rubrics; argues recall benchmarks overstate competence.
  - **ResearchQA (2026):** citation-grounded QA that rewards grounded refusal.
  - **arXiv 2605.07723:** measures non-existent citations at scale.
  - **Practitioner report:** the deep-research tool fabricated an OED-style quotation and claimed database access it could not have had.

  Implied eval cases: every cited URL resolves; every DOI resolves through Crossref; every quotation is found in its fetched source; every image in the manifest has licence, source URL, date and place; and the CC0-only mode rejects NC images.
- Track: testing
- Affects: the cases in evals/evals.json
- Magnitude: n/a (initial)
- Suggested response: adopt (citation-resolves and licence-present assertions); note (benchmarks)
- Sources: https://techcrunch.com/2025/01/19/ai-isnt-very-good-at-history-new-paper-finds, https://arxiv.org/pdf/2604.24690, https://www.alphaxiv.org/abs/2607.11074, https://arxiv.org/pdf/2605.07723, https://www.wordorigins.org/harmless-drudge/i-asked-chatgpt

### Ranked table

| Source | Good for | Query route | Licence | Limits / sign-in | Tier |
|---|---|---|---|---|---|
| Met Collection API | object data plus CC0 images | `collectionapi.metmuseum.org/public/collection/v1.1/search` then `/v1/objects/{id}` | CC0 when `isPublicDomain` | none; under 80/s | 1 |
| Cleveland Museum of Art | CC0 images | `openaccess-api.clevelandart.org/api/artworks/?cc0=1&has_image=1` | CC0 per record | none | 1 |
| Art Institute of Chicago | CC0 images over IIIF | `api.artic.edu/api/v1/artworks/search` | CC0 data, CC-BY descriptions | 60/min | 1 |
| Getty | CC0 images, Linked Art | data.getty.edu API and SPARQL | CC0 (some exceptions) | none seen | 1 |
| Smithsonian Open Access | objects, CC0 media | `api.si.edu/openaccess/api/v1.0/search` | CC0 | free api.data.gov key, 1000/h | 1 |
| Rijksmuseum | Dutch and colonial material, public-domain images | `data.rijksmuseum.nl/search/collection` | PD per record | none; beta | 1 |
| Wikimedia Commons | gap-filler images | `commons.wikimedia.org/w/api.php?prop=imageinfo&iiprop=extmetadata` | per file | UA required | 2 |
| Europeana | European museums | `api.europeana.eu/record/v2/search.json` | per item | free wskey | 2 |
| British Museum | Roman and Near East objects | web only | CC BY-NC-SA 4.0 | 750 px direct | 1 (NC) |
| Science Museum Group | technology history | dumps preferred | images CC BY-NC-SA | heavily throttled | 1 (NC) |
| V&A / Harvard | design, art | API v2 / API with key | own terms / unverified | Harvard key | 1 |
| Open Context | excavation data, GeoJSON | `opencontext.org/query/.json` | CC per project | UA required | 1 |
| PBDB / Neotoma | deep time, paleoecology | data1.2 / api.neotomadb.org | open | none | 1 |
| p3k14c / IntChron | radiocarbon dates | Zenodo dump / REST JSON | open | none | 1 |
| IOSACal | IntCal20 calibration | Python library | GPL code | local | 1 |
| Seshat | polity-level variables | `seshat-db.com/api/` | not read | none seen | 2 |
| D-PLACE | cross-cultural ethnography | GitHub CLDF | CC-BY-NC | none | 2 |
| PAS (finds.org.uk) | UK small finds | `/format/json` | open (CC unconfirmed) | some fields need login | 1 |
| ADS, tDAR, ARIADNE, DAACS | archaeology archives | web, OAI | per archive | tDAR login for downloads | 1 |
| eHRAF | ethnography | interface only | paid | sign-in | 2 |
| OpenAlex | scholarly index | `api.openalex.org/works?search=` | CC0 | free key, $1/day, 30/s | 2 |
| Crossref | DOI verification | `api.crossref.org/works/{doi}?mailto=` | facts open | 10/s polite, concurrency 3 | 2 |
| Semantic Scholar | abstracts, citations | `api.semanticscholar.org/graph/v1` | own licence | shared pool or key | 2 |
| CORE / DOAJ | open-access full text | api.core.ac.uk / doaj.org/api | per article | CORE 5 per 10 s | 2 |
| Persée | French scholarship | OAI-PMH, SPARQL | open | none | 2 |
| BASE | open-access search | HTTP API | non-commercial | IP whitelist | 2 |
| JSTOR, BBIH, Cairn, Brepols | scholarship | link-out | paid | sign-in | 2 |
| Chronicling America | US newspapers 1756–1963 | `loc.gov/...?fo=json` | mostly PD | 20/min, 1 h block | 1 |
| Trove | Australian newspapers | API v3 | per item | key; commercial needs permission | 1 |
| NYT / Guardian | 20th-century news | keyed APIs | metadata only | key | 1 |
| SEC EDGAR | company filings | data.sec.gov, efts | public | UA required, 10/s | 1 |
| Federal Register | US regulation since 1994 | `/api/v1/documents.json` | public | none | 1 |
| Wayback CDX | old company pages | `web.archive.org/cdx/search/cdx` | per site | about 15/min, unofficial | 1 |
| CHM oral histories | computing firms | web search | per item | none | 1 |
| Historic Hansard | UK debates 1803–2005 | static pages | Open Parliament Licence (assumed) | none | 1 |

## Overall magnitude: n/a (initial). The most consequential items: Met v1 search retired on 2026-10-01, OpenAlex keys and budget (2026-02-13), the Chronicling America move, and the shortage of CC0 Roman Republican military images.
## Open questions:
- New: Rijksmuseum image licence per record (CC0 or PDM?) and its IIIF route.
- New: Paris Musées, National Palace Museum and Prado image terms.
- New: Smithsonian Human Origins reuse terms.
- New: Seshat data licence.
- New: whether mikechao/metmuseum-mcp uses the retired v1 search.
- New: official NYT and Guardian limits.
- New: the IntCal successor's release date.
- New: whether CC0 sources hold enough Late Republican military gear, or the pack must lean on Commons and Europeana with per-file licences.
## Search plan notes:
- Subject: official doc pages beat search summaries; help.openalex.org, loc.gov "working within limits", metmuseum.github.io and data.rijksmuseum.nl/docs were the best. Live API calls (Met, Cleveland, Federal Register) are cheap and decisive.
- Subject (noise): apis.io, archivarix, freeapihub and gravitee "corpus" pages.
- Subject (refused fetches): developer.nytimes.com, open-platform.theguardian.com, si.edu, pro.europeana.eu and glam-workbench.net (Anubis).
- Forums the plan lacked: community.crossref.org; the IHR blog for BBIH; the Europeana API Google Group.
- Tooling: Glama listings surfaced the MCP servers; no install counts were gathered.
- Testing: arXiv and ACL searches work.
- The shared WebSearch budget ran out at the end of the pass, so the Seshat licence, D-PLACE version, Human Origins, Paris Musées and NPM checks were not run.
## Tracks covered: subject: 46 queries · tooling: 4 · practice: 2 · testing: 2 (3 further searches were refused by the budget)
## Upcoming events: 2026–2027 · IntCal20 successor publication (date unconfirmed); none other dated
## Nothing changed: no (creation pass)
## Cost: searches 57 (3 refused) · fetches 32 · tool calls 90
