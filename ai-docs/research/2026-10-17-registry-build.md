# Seed registry build, 2026-10-17

Built `skills/historywright-sources/references/registry.json` (registry "1", 97 KB, UTF-8, LF) from the creation pass ([2026-10-17-creation-pass.md](2026-10-17-creation-pass.md) §1 and the four subject reports) and RESEARCH.md R-20261017-2 to -8 (plus -10 for DILA and -14 for Transkribus).

## Contents

- 85 sources: tier 1 = 53, tier 2 = 27, tier 3 = 5.
- Routes: link-out 53, src 22, place 4 (pleiades, chgis, whg, ohm), wd 2 (wikidata, wikidata-scholarly), wp 1, oa 1, doi 1, cal 1 (dila).
- Access: open 30, browse-only 17, paid 12, bulk-only 11, key-required 7, ua-required 6, key-optional 2.
- 13 retired entries: DBpedia, Clio Infra and Maddison (dropped sources), plus ten retired services (Chronicling America legacy API, Met v1 search, HathiTrust Data API, Constellate, Trove v2, NARA v1, Getty XML, Rijksmuseum key API, api.wikimedia.org, WDQS legacy full graph).
- 31 mirror domains. Most were confirmed on Wikipedia's "Mirrors and forks" pages (ABC to VWXYZ, fetched through the Action API). justapedia.org (asked for by name) and grokipedia.com (an AI encyclopedia that adapts Wikipedia text) are not on those pages; I added them anyway.
- Every source the reports rank is in, except some minor archaeology and news routes: NYT, Guardian, Neotoma, PBDB, p3k14c, IntChron, ADS, tDAR, ARIADNE, BASE, LGPN, Shamela, Harvard Art Museums. Add them if a question needs them.

## Live tests (curl, hw.py User-Agent, at least 2.1 s between calls to one host, no private keys, 0 WebSearch)

Every probe and every search block was run once. The searches used a test query, and their `items` and `fields` paths were resolved against the first result.

- **All 22 search blocks returned 200 and their paths resolved**: getty-vocab, doaj, core, edh, loc, chronicling-america, tna, internet-archive, japan-search, europeana (public demo key `api2demo`), deutsche-biographie, met (plus v1 objects detail), cleveland, artic, smithsonian (public `DEMO_KEY`), rijksmuseum, commons, vam, open-context, edgar, wayback, federal-register.
- **All 42 probes returned 200**, but two need a caveat. semantic-scholar returned 429 twice and then 200. DOAJ returned 502 twice in the first round and 200 later.
- **Other checks**: landing pages for most link-out entries answered 200, and are noted per entry. Bot walls or errors: british-museum, gallica and kanripo (Cloudflare 403), trismegistos ("Security Check" 403), science-museum, hemeroteca-brasileira, dp.la and oxfordre.com (403), pares (429), eap and abhilekh-patal (empty 202), jstor ("Client Challenge"). papyri.info served an Anubis challenge with status 200.

## Paths corrected or set during the build

- met: the v1.1 search returns only `objectIDs`. Added a `detail` call to `/v1/objects/{id}` (fields title, objectURL, objectDate, primaryImage, isPublicDomain).
- smithsonian: `url` changed from `content.descriptiveNonRepeating.record_link`, which some records lack, to `...descriptiveNonRepeating.guid` (the ARK permalink). Added `licence` from `metadata_usage.access`.
- core: `/v3/search/works` answers 301 with an empty body. It needs the trailing slash, `/v3/search/works/`.
- deutsche-biographie: a bare `q` matches nothing. Changed to `q=r_nam:{q}`, with fields defnam and r_flr; r_flr needs trimming.
- europeana: `guid` and `link` echo the API key (utm_campaign, wskey), so the result URL is built from `id` with a `link` template.
- edh: items `items`; fields transcription, not_before and not_after (some records have the two swapped), country.
- open-context: the default response is facets. `response=uri-meta` returns a bare list, so the items path is empty.
- wayback: the availability API returned empty `archived_snapshots` for microsoft.com at 1996, so the search uses CDX: a list of rows with a header row (`skip: 1`) and a `link` template.
- edgar: SEC returned 403 to the standard UA (`historywright/0.1 (url; email)`) on efts.sec.gov and data.sec.gov, and 200 to `historywright <email>`. The entry carries `"ua": "plain"`.
- ohm: the report's `ohm.overpass-ultra.us` is a browser front end. The probe uses `overpass-api.openhistoricalmap.org/api/status`.
- tna, internet-archive, artic, vam, core, edh, deutsche-biographie: added `link` templates because the results carry an id but no URL.
- commons: Artist and DateTimeOriginal are absent on some files and are treated as optional. LicenseShortName was confirmed.
- loc: some `url` values are protocol-relative (`//hdl.loc.gov/...`).

## Routes set to link-out, and why

- Failed or unverifiable live:
  - semantic-scholar: keyless pool 429, paths unverified.
  - getty (museum): `/museum/collection/docs/` returned 404 and no search endpoint was found.
  - gallica, kanripo: Cloudflare.
  - science-museum: 403.
  - pas: its `/format/json` route returns HTML.
  - seshat: `?search=` is ignored and all 864 polities come back.
  - cbdb: the legacy API answers, but with data Version 20131220.
- Open APIs that the JSON-only generic search cannot drive (each keeps its probe):
  - ndl: XML/RSS.
  - dprr: SPARQL XML.
  - persee: SPARQL only.
  - hathitrust: identifier lookup only.
  - owid: lookup by slug.
- Gated: nara (key by email, no-cache terms), trove (approval), ddb and dpla (a key is needed to check the fields).
- All paid, browse-only and bulk-only sources (paid ones never carry a search block).

## Schema additions (documented in the registry's `notes`)

hw.py must implement these:

- `search.link`: a URL template filled from the extracted fields.
- `search.skip`: leading rows to drop.
- An empty `items` path means the response root.
- An empty field path means the item itself (the Met's objectIDs).
- `detail.items: null` means the response is the record.
- Entry-level `"ua": "plain"`.

`pace_s` follows the documented limits, never below 0.1. Probes for europeana and smithsonian use the public demo keys.

## Open questions

- **Probe by status alone is fooled.** Anubis (papyri.info) and JSTOR's challenge page answer 200. `hw.py probe` should also check the content type or JSON parse; consider an `expect_type` field.
- PeriodO is bulk-only link-out. Should `hw.py cal` (or a new period command) cache `p0dataset.json`?
- Paths to check once keys or a quiet pool allow: Semantic Scholar, DPLA and DDB search blocks.
- The Getty Museum's Linked Art search route.
- The paid landing URLs (OCD, New Pauly, EI on referenceworks.brill.com) were not re-verified beyond a 200 or 403 on the landing page.
- internet-archive is set to tier 2 although items range from 1 to 3. Should hw.py tier per item?
- The registry is 97 KB against the plugin's 400 KB green budget. Trim the notes if the skill files grow.
