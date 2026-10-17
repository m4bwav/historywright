---
kind: note
status: active
date: 2026-10-17
title: End-to-end example, a legionary at Alesia (52 BC)
tags: [pack, polywright, museums, example]
---

# End-to-end example: a legionary at Alesia, 52 BC

## Summary

A real pack built with hw.py alone passes verify sources (8 of 8 quotes), validate-pack and polywright's manifest check; open museum evidence for 52 BC is thin, and the pack says where.

The kickoff asked for a Roman legionary pack exported and read by polywright. The pack is in
[../../examples/legionary-alesia-52bc/](../../examples/legionary-alesia-52bc/answer.md); it was built with hw.py
commands only (script steps: `pack init`, `verify quote` on every cited page, two `pack add-ref`, the JSON files,
`verify sources`, `validate-pack`).

## Result

- `hw.py verify sources`: 8 of 8 quotes found exactly on their fetched pages; 5 independent sources; corroborated.
- `hw.py validate-pack`: ok, no problems, no warnings.
- `pw.py manifest <pack> --validate` (polywright 0.1.2): ok, status `references`, 2 sources with licences. The pack
  is a valid polywright asset folder, so polywright-references can start from its refs folder.

## What the search found (and did not)

- Primary texts on LacusCurtius answered well: Polybius 6.22-23 (Paton) for the kit of c. 150 BC, Caesar's
  Gallic War 2.21 (Edwards) for helmets, shield covers and badges in 57 BC. Thayer's pages declare their charset
  only in a `<meta>` tag, which led to `decode_body` in hw_net.py.
- CC0 museum APIs, as the creation pass predicted (R-20261017-8): "Roman helmet" at the Met returns 16th-century
  Italian helmets; "Montefortino" returns one Etruscan helmet of the late 4th to early 3rd century BC
  (2015.758.1, CC0), two centuries early. Cleveland and the Art Institute returned nothing in period.
- Commons gave a gladius hispaniensis of the 3rd to 1st century BC (Calahorra museum photo, CC BY-SA 4.0), whose
  hilt and point are painted restorations on the display board. Its file page gives no accession number; the pack
  says so in the field.
- "Alesia, vorgefundene Waffen" on Commons is a hand sketch, not a record: excluded by the pack rule.
- The helmet-typology footnotes on Wikipedia lead to an academia.edu paper behind a sign-in and a Google Books
  page; the Met's web page answers 429 to scripts (its API is fine). The answer's confidence line names these
  gaps; Montefortino against Coolus for 52 BC stays open.
- The Battle of Alesia's Wikidata start and end statements (July and September 52 BC) have no references; the
  timeline row says so.

## Follow-ups

- A modern open-access source on late-Republican equipment (OpenAlex returned PDFs only; hw.py's quote check
  reads HTML and plain text, not PDF).
- polywright-references has no command that ingests the pack's reference index notes yet; the notes are for the modeller.
