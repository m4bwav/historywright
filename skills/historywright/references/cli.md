# hw.py commands

Back to [SKILL.md](../SKILL.md). `python scripts/hw.py <command> ...`; every command prints one JSON object and
exits 1 with `{"ok": false, "error": ...}` on failure. `HW_HOME` moves the home folder (default
`~/.historywright`: config, cache, fetch log, page store, DILA table). `HW_FIXTURES=<dir>` answers HTTP from
`<dir>/index.json` (tests, evals); `HW_RECORD=<dir>` saves live responses in that shape.

| Command | Does |
|---|---|
| `doctor [--net]` | Python, home, contact, keys, registry, era outline, DILA table, cache size |
| `wd search "<name>"` | Wikidata items for a name (QID, label, description) |
| `wd claims <QID> [--prop P569,P570]` | every statement with rank, decoded date (calendar, precision, EDTF, JDN range, flags), qualifiers, references; notes on disputes and unreferenced values |
| `wd entity <QID>` | label, description, aliases, Wikipedia titles; proves a QID exists |
| `wd sparql "<query or file>" [--scholarly]` | WDQS main or scholarly graph; warns on `wdt:` with time properties |
| `wp summary "<Title>"` | extract and the article's QID (finder only) |
| `wp refs "<Title>" [--near "<phrase>"]` | the footnotes (text, links, DOIs, ISBNs), or only those cited in the sentence holding the phrase |
| `wp search "<query>"`, `wp assess "<Title>"` | article search; quality class and redirects |
| `place search "<name>" [--source pleiades\|chgis\|whg\|wikidata] [--year N]` | gazetteer hits with `[lon, lat]`, names, periods, licence |
| `place pleiades <id>` | one Pleiades place |
| `oa search "<topic>" [--page N] [--filter ...]` | OpenAlex works (page 2+ needs the free key) |
| `doi <DOI> [--title --author --year]` | Crossref, then OpenAlex; `all_match` false means a blended or wrong reference |
| `src <id> "<query>" [--detail N]` | any registry source with a JSON search; `--detail` fetches records (museum objects) |
| `cal date "<date>" [--cal julian\|gregorian] [--country GB] [--cjk]` | read a date (BC/AD, ISO astronomical, AUC, AH, O.S./N.S.) to JDN, Julian, Gregorian, AUC, tabular Islamic, EDTF |
| `cal jdn <n> [--cjk]` | every calendar's reading of one day |
| `cal span "<start>" "<end>"` | exact days, years, months and days between two dates |
| `cal era <name>`, `cal cjk <date>` | East Asian eras (every match) and era dates to Western dates; `cal setup` builds the table |
| `cache get "<question>"`, `cache put <entry.json>`, `cache list` | researched answers with sources and retrieval dates |
| `verify url <url>...` | live, dead (with archived copy), likely_hallucinated, unknown |
| `verify quote --url U --quote "..."` | is the quote a span of the page (exact or normalised; `...` splits) |
| `verify doi <DOI> --title --author --year`, `verify qid <QID> [--label]` | does the reference exist and match |
| `verify sources <sources.json> [--offline] [--any-url]` | every source fetched this run, every quote in its page, independence and corroboration |
| `pack init <dir> --question "..." [--period] [--commercial]` | scaffold a research pack (historywright-pack) |
| `pack add-ref <dir> --image --page --title --licence --object-date --place --accession --institution` | download a reference image and record it |
| `pack csl <dir>` | sources.json as CSL-JSON for Zotero |
| `validate-pack <dir> [--network]` | the pack contract (files, EDTF, QIDs, RFC 7946, licences, completeness) |
| `probe [--only id,id]` | call every registry endpoint; ok, moved, gone, blocked, unreachable |
| `keys status`, `keys contact --set ADDR`, `keys openalex --email ADDR [--yes]`, `keys whg [--token T]` | optional free keys |
| `lint [--ids]` | registry and era outline checks |
