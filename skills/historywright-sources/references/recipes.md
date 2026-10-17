# Query recipes

Back to [SKILL.md](../SKILL.md). Recipes that worked, with the date they were checked. Add one when a query
pattern saves a step; retire it when `hw.py probe` or a run shows it broken.

## Wikidata (checked 2026-10-17)

- Full statements: `hw.py wd claims Q1048 --prop P569` (wbgetclaims). Same in SPARQL, keeping rank, precision
  and calendar:

  ```sparql
  SELECT ?time ?precision ?calendar ?rank WHERE {
    wd:Q1048 p:P569 ?st . ?st psv:P569 ?v ; wikibase:rank ?rank .
    ?v wikibase:timeValue ?time ; wikibase:timePrecision ?precision ; wikibase:timeCalendarModel ?calendar .
  }
  ```

  `timeValue` is XSD (year 0, converted to Gregorian): read the date from `hw.py wd claims`, use SPARQL to find
  items.
- Scholarly articles live in the split graph: `hw.py wd sparql "<query>" --scholarly`.
- Discover IDs before writing SPARQL; never invent a QID or a property (the official Wikidata MCP's rule).

## Wikipedia footnotes (checked 2026-10-17)

- `hw.py wp refs "Microsoft" --near "April 4, 1975"` returns the sentence and only its footnotes (here a BBC
  timeline, a 1995 Fortune interview and Paul Allen's memoir). Then read each one.
- `action=parse` HTML holds the references as `<li id="cite_note-...">` with `reference-text` spans; Parsoid's
  `mw:Extension/references` is the alternative, untested here.

## Places (checked 2026-10-17)

- Pleiades search: `search_rss?SearchableText=<name>&portal_type=Place` lists place URLs; `/places/<id>/json`
  gives `reprPoint` [lon, lat], names and periods. Ranking is not by fame: "Alesia" lists a Greek Alesiai first.
- CHGIS: `tgaz/placename?n=長安&yr=700&fmt=json` (prefix match, year filter).
- WHG: `suggest/entity?prefix=<name>` with `Authorization: Bearer <token>` gives `repr_point`; `api/index/?name=`
  answers too. The token comes from the WHG profile page after an ORCID sign-in.

## Scholarship (checked 2026-10-17)

- OpenAlex: `works?search=<words>&select=...`; page 2+ needs the free key. `filter=publication_year:>2000` and
  `filter=type:book` narrow it.
- Crossref by DOI, then compare title, first author's surname and year: a real DOI with a different title is the
  commonest fabricated reference.

## Company history (checked 2026-10-17)

- SEC EDGAR full-text search and filings (10-K "Item 1. Business" states incorporation); a contact User-Agent is
  required. The Wayback Machine CDX API shows what a company page said and when.

## Dates

- `hw.py cal date`, `cal span`, `cal cjk`, `cal era`: see the hub's [dates reference](../../historywright/references/dates.md).
