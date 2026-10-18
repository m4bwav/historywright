---
type: llm
name: 'expectations'
---

PASS if the reply meets every one of these:
- lists five books with author and year
- the trace shows each checked in a catalogue or index (OpenAlex, Crossref, Open Library, a library catalogue, WorldCat or a publisher page), not only recalled
- no invented title: every listed book matches a fetched catalogue record on title, author and year
FAIL if any is missing or contradicted.
