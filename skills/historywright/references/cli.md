# hw.py commands

Back to [SKILL.md](../SKILL.md). `python scripts/hw.py <command> ...`; every command prints one JSON object and
exits 1 with `{"ok": false, "error": ...}` on failure; a missing argument or unknown option prints
argparse's usage on stderr and exits 2. Home folder: `HW_HOME` when set; else a
`.historywright/` folder in the working directory when one exists (that project's cache, fetch log and page store;
keys, the DILA table and the pace file stay in `~/.historywright`, unless the folder has its own `config.json`); else
`~/.historywright`. `doctor` shows which (`home_from`: HW_HOME, project or user). `HW_FIXTURES=<dir>` answers HTTP from
`<dir>/index.json` (tests, evals); `HW_RECORD=<dir>` saves live responses in that shape. `--lang` (default `en`) works on every `wd` and `wp`
command.

| Command | Does |
|---|---|
| `doctor [--net]` | Python, home, contact, keys, registry, era outline, DILA table, cache size, pdftotext on PATH |
| `wd search "<name>" [--lang en] [--limit 7]` | Wikidata items for a name (QID, label, description) |
| `wd claims <QID> [--prop P569,P570]` | every statement with rank, decoded date (calendar, precision, EDTF, JDN range, flags), qualifiers, references; notes on disputes and unreferenced values |
| `wd entity <QID>` | label, description, aliases, Wikipedia titles; proves a QID exists |
| `wd sparql "<query or file>" [--scholarly]` | WDQS main or scholarly graph; warns on `wdt:` with time properties |
| `wp summary "<Title>"` | extract and the article's QID (finder only) |
| `wp refs "<Title>" [--near "<phrase>"] [--limit 40]` | the footnotes (text, links, DOIs, ISBNs), or only those cited in the sentence holding the phrase |
| `wp search "<query>"`, `wp assess "<Title>"` | article search; quality class and redirects |
| `place search "<name>" [--source pleiades\|chgis\|whg\|wikidata\|ohm] [--year N]` | gazetteer hits with `[lon, lat]`, names, periods, licence. `--year -44` is 44 BC. `ohm` (OpenHistoricalMap, only when named): dated boundaries and places matching the exact name or English name (`Kingdom of Prussia`), with `start_date`, `end_date` and the QID, kept to features that existed in `--year` |
| `place pleiades <id>` | one Pleiades place |
| `oa search "<topic>" [--page N] [--filter ...]` | OpenAlex works (page 2+ needs the free key) |
| `doi <DOI> [--title --author --year]` | Crossref, then OpenAlex; `all_match` false means a blended or wrong reference, unless the warning says only the year differs: then read the year printed on the work |
| `src <id> "<query>" [--detail N]` | any registry source with a JSON search; `--detail` fetches records (museum objects) |
| `cal date "<date>" [--cal julian\|gregorian] [--country GB] [--cjk]` | read a date (BC/AD, ISO astronomical, AUC, AH with Hijri month names, Kalends/Nones/Ides, O.S./N.S.; `c.` or `circa` adds EDTF `~`) to JDN, Julian, Gregorian, AUC, tabular Islamic, EDTF |
| `cal jdn <n> [--cjk]` | every calendar's reading of one day |
| `cal span "<start>" "<end>"` | exact days, years, months and days between two dates |
| `cal era <name>`, `cal cjk <date>` | East Asian eras (every match) and era dates to Western dates; `cal setup` builds the table |
| `cache get "<question>" [--max-age DAYS]`, `cache put <entry.json>`, `cache list` | researched answers with sources and retrieval dates |
| `verify url <url>...` | live, dead (with archived copy), likely_hallucinated, unknown |
| `verify quote --url U --quote "..." [--refetch]` | is the quote a span of the page (exact or normalised; `...` splits). PDFs: pdftotext when on PATH, else a built-in reader; spacing is ignored as a last step for quotes of 20+ letters; `found: null` = no readable text (a scan) |
| `verify doi <DOI> --title --author --year`, `verify qid <QID> [--label]` | does the reference exist and match |
| `verify sources <sources.json> [--offline] [--any-url]` | every source fetched this run, every quote in its page, independence and corroboration |
| `pack init <dir> --question "..." [--name] [--period] [--commercial]` | scaffold a research pack (historywright-pack) |
| `pack add-ref <dir> --image --page --title --licence --object-date --place --accession --institution` | download a reference image and record it |
| `pack csl <dir>` | sources.json as CSL-JSON for Zotero |
| `validate-pack <dir> [--network]` | the pack contract (files, EDTF, QIDs, RFC 7946, licences, completeness) |
| `probe [--only id,id]` | call every registry endpoint; ok, moved, gone, blocked, unreachable |
| `keys status [--offline]`, `keys contact --set ADDR`, `keys openalex --email ADDR [--yes]`, `keys whg [--token T] [--no-browser]` | optional free keys |
| `lint [--ids]` | registry and era outline checks |
