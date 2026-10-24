# The research pack contract

Back to [SKILL.md](../SKILL.md). A pack is one folder that a 3D, video or image plugin reads. It is also a valid
polywright asset folder: `manifest.json` follows polywright's asset contract and reference images sit in `refs/`,
so `pw.py manifest <pack> --validate` passes and polywright-references can start from it. `hw.py validate-pack`
checks everything below; `tests/fixtures/pack-good` passes and `tests/fixtures/pack-bad` must fail.

## Folder

```
<pack>/
  manifest.json     polywright asset contract + a "historywright" block
  answer.md         the answer: inline citations, Confidence line, Sources agree/disagree, AI-researched line
  sources.json      every source read, with the exact supporting quotes
  entities.json     people, polities, objects: QIDs and date objects
  places.geojson    RFC 7946 FeatureCollection, [lon, lat]
  timeline.json     dated events, each with its source sentence and JDN range
  refs/index.json   reference images from collection records; the images beside it
  anachronism.md    the period checklist, each item cited
  sources.csl.json  optional: hw.py pack csl (Zotero)
```

## manifest.json

```json
{
  "polywright": "1", "name": "Roman legionary, 50 BC", "kind": "real", "route": "found",
  "brief": "<the question>", "targets": [], "units": "m",
  "sources": [{"what": "reference image: ...", "url": "...", "author": "...", "licence": "CC0", "retrieved": "2026-10-17", "file": "refs/..."}],
  "tools": [{"name": "historywright", "version": "0.1.0"}], "outputs": [], "reviews": [], "status": "references",
  "historywright": {"version": "1", "question": "...", "period": "50 BC", "commercial": false, "created": "2026-10-17",
    "completeness": [{"item": "places", "status": "present"}, {"item": "timeline", "status": "empty", "reason": "a single moment, no sequence"}]}
}
```

`mechanism` (optional, set by `pack init --mechanism`): true when the subject is a machine or a building with
machinery; anachronism.md must then have a Mechanism section with items (see anachronism.md below).

`completeness` lists every part (answer, sources, entities, places, timeline, refs, anachronism) as `present`, or
`empty` with a reason. An agent that stops early must say what it skipped (R-20261017-21).

## sources.json

```json
{"sources": [{"id": "s1", "title": "Saturnalia 1.12.34", "author": "Macrobius", "year": null,
  "url": "https://...", "doi": null, "kind": "primary", "tier": 1, "retrieved": "2026-10-17",
  "licence": "public domain", "derived_from": [], "via": "Wikidata reference on Q1048 P569",
  "claims": [{"claim": "Caesar's birthday was kept on 12 July", "quote": "<exact words from the page>", "locator": "1.12.34"}]}]}
```

- `kind`: primary, secondary, tertiary (Wikipedia and mirrors must be tertiary), structured (Wikidata, gazetteers).
- `tier`: 1, 2 or 3 as in the registry.
- Every claim has a `quote` that is a span of the fetched page; `hw.py verify sources` re-reads it.
- `derived_from` names the source ids or URLs it copies; independence is counted from it.

## entities.json

```json
{"entities": [{"qid": "Q1048", "label": "Julius Caesar", "type": "person", "coord": null,
  "dates": {"birth": {"as_written": "12 or 13 July 100 BC", "calendar": "roman-republican",
    "edtf": "[-0099-07-12,-0099-07-13]", "jdn": [1685091, 1685092], "precision": "day",
    "qualifier": "disputed", "era_name": null, "sources": ["s1", "s2"]}}}]}
```

The date object: `as_written` (as the sources write it), `calendar`, `edtf` (level 0 or 1, or a level 2 set),
`jdn` [first, last], `precision`, `qualifier` (disputed, circa, floruit, tpq, taq, or null), `era_name`
(for East Asian dates) and `sources` (ids in sources.json). A disputed date is a set or a range, never a point.
`hw.py wd claims` and `hw.py cal date` print every field.

## places.geojson

RFC 7946: a FeatureCollection; positions `[lon, lat]`; rings closed with at least four positions; no `crs`.
Each feature's `properties` carry `name`, `source` (a source id or gazetteer URI), and optionally `when` (EDTF),
`certainty` and `expected_coord` (the gazetteer's coordinate, which lets the validator catch swapped axes).

## timeline.json

```json
{"rows": [{"when": "-0057/-0049", "jdn": [1700000, 1703000], "event": "Caesar's Gallic campaigns",
  "source": "s3", "sentence": "<the source sentence the row rests on>", "place": "Gaul"}]}
```

## refs/index.json

```json
{"refs": [{"file": "refs/met-....jpg", "title": "...", "object_date": "1st century BC", "place": "Italy",
  "accession": "...", "institution": "The Metropolitan Museum of Art", "url": "<the record page>",
  "image_url": "...", "licence": "CC0", "author": null, "nc": false, "retrieved": "2026-10-17",
  "sha256": "...", "bytes": 0}]}
```

- Only collection records: a museum, archive or Commons file with an accession number or file page and the
  object's own date. Never an image search result, a video still or a generated picture (R-20261017-20).
- Licence on every image. CC0 and CC BY by default; non-commercial (British Museum, Science Museum Group) gets
  `nc: true` and never enters a pack with `commercial: true`: `pack add-ref` refuses it there. A licence counts
  as non-commercial when it has "NC" as a word of its own or says non-commercial ("CC BY 4.0 licence" does not).
- File names come from institution and accession; a long one keeps the accession's tail and a short hash, and a
  name already taken by another image gets `-2`, `-3`.
- `hw.py pack add-ref` downloads, hashes and records an image in both `refs/index.json` and the manifest.

## anachronism.md

A checklist for the period, each item cited to a source in sources.json: what did not exist yet (stirrups in
50 BC Rome, glazed windows in a 1300s cottage), what is often shown wrong (lorica segmentata in the late
Republic), what the colour, material and shape evidence says. At least three filled items; an empty item (the template's
`- ` line) fails validation, and so does the answer template's `<answer with inline citations [s1]>` left in
answer.md.

When `historywright.mechanism` is true, a section headed `## Mechanism: what drives what, and where it must sit`
lists the drive chain from the power source to the tool, one link per item: what the part is, where it must sit,
what it drives, with sizes and citations. It is followed by what a picture or model must never show. Example:
[mechanism-example.md](mechanism-example.md).
