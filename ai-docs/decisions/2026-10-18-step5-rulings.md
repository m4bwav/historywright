# Step 5 small rulings (2026-10-18)

Decided in session under the "decide small rulings, flag them" rule. Mark can overturn any of them.

1. **PDF quotes: pdftotext first, stdlib reader second, never a false "absent".** pdftotext (poppler) is used when
   it is on PATH because it knows glyph widths and odd encodings; it is optional, so hw.py stays standard library.
   The built-in reader covers the common case. A PDF with no readable text answers `found: null`, which
   `verify sources` reports as a warning. `HW_PDFTOTEXT=0` forces the built-in reader (tests use it).
2. **Spacing-insensitive match for PDFs only, 20+ letters.** Drop caps and small caps split words in extracted
   text. Removing whitespace from a long quote barely raises the chance of a false match; short quotes and HTML
   pages keep the strict match. The match label says "spacing ignored (PDF)" so the reader of the result knows.
3. **The reader is a new module, `hw_pdf.py`,** not more lines in hw_check.py (now six modules).
4. **OHM only when named (`--source ohm`), not in `auto`.** It is tier 3 (crowd-sourced), OHM publishes no limit,
   and every client shares two Overpass slots; `auto` stays on the four gazetteers. Exact name or `name:en`
   matches only: a regex over every name is the kind of query that loads a public Overpass server.
5. **`--year` negative means BC in historical numbering** (`-44` = 44 BC, no year 0), the way people write it;
   hw.py converts to OHM's astronomical years. CHGIS gets the year as before.
