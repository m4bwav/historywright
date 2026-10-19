# PDF quote checks: live trial

2026-10-18, Step 5 session. Code: `skills/historywright/scripts/hw_pdf.py`, CHANGELOG C-20261018-7.

## Why

`verify quote` decoded every body as a web page. A PDF came out as cp1252 noise, so a real quote was reported
`found: false`, a false negative that looks like evidence. OpenAlex often links only the PDF.

## What was tried (one fetch per PDF, within each host's pace)

| PDF | producer | built-in reader | pdftotext |
|---|---|---|---|
| arXiv 2604.03173 | pdfTeX | 85,357 chars, readable, 0.10 s | 88,105 chars |
| govinfo CDOC-110hdoc50 (the Constitution, 4 MB) | GPO typesetting | 311,971 chars, 0.18 s | 308,025 chars |
| PLOS ONE 10.1371/journal.pone.0000001 | journal PDF | 49,962 chars, 0.05 s | 50,071 chars |

- The built-in text matched pdftotext's word for word in the samples, except the Constitution's drop cap and small
  caps: "W E THE P EOPLE". The reader has no glyph widths, so every horizontal `Td` move becomes a space. Fixed in
  matching, not in extraction: for PDF text only, and only for quotes of 20 or more letters, a last step compares
  with all whitespace removed. The altered quote ("of the United Kingdom") still fails.
- Two PDFs could not be fetched: bioRxiv answered 403 (bot wall), archives.gov's transcript URL is gone (404).

## Limits left

- Scans without a text layer and fonts without a ToUnicode map give no text: `found: null` with the reason, so
  `verify sources` warns. pdftotext does better on unusual encodings; `doctor` reports whether it is on PATH.
- No LZW, ASCII85 or other filters in the built-in reader; such streams are skipped.
- Reading order is the content-stream order; two-column layouts may interleave columns. Quotes that cross a column
  break can miss, and the miss carries a note to check by hand.
