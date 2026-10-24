---
name: historywright-pack
description: "Use when history research must feed a 3D model, a film, a video or images: build and validate a research pack (cited answer, sources with exact quotes, entities with QIDs and EDTF dates, places as GeoJSON, a timeline, reference images from museum collection records with licence and accession number, a period anachronism checklist) that polywright, cinewright and comfyui-gen read. Use on 'research a Roman legionary for my model', 'period-accurate references for a film scene', 'what did a samurai wear in 1600, for a 3D print', 'make a history pack', 'validate this pack'. A plain history question is historywright; where sources live is historywright-sources."
---

# historywright-pack

Turns history research into a folder other plugins can build from: polywright (3D models and prints), cinewright
(film and AI video), comfyui-gen (images). The research itself follows the hub (historywright); this skill adds
the visual and spatial evidence and the checks. Contract: [references/contract.md](references/contract.md).

Script: the hub's `hw.py` (`../historywright/scripts/hw.py`).

## Step 1: scope the subject

Pin down who or what, where, and when as narrowly as the sources allow ("a legionary of Caesar's army in Gaul,
about 52 BC", not "a Roman soldier"), and whether the work is commercial (it decides which image licences may
enter). Then `hw.py pack init <dir> --question "<question>" --period "<period>" [--commercial] [--mechanism]`;
`--mechanism` is for a machine or a building with machinery (a mill, a forge, a press, a ship's rig).

## Step 2: research (the hub's Steps 1 to 6)

Answer the question behind the pack with the hub's method and write it to `answer.md`. Record every source read in
`sources.json` with the exact supporting quote, every person, polity or object in `entities.json` with its QID
and date object (`hw.py wd claims`, `hw.py cal date` print the fields), places in `places.geojson`
(`hw.py place search`, coordinates `[lon, lat]`) and dated events in `timeline.json`, each row with the sentence
it rests on. Read every page through hw.py from the start: `hw.py fetch <url> [--find "<word>"]` stores the page
and writes its text to a file to read, `hw.py verify quote --url <url> --quote "<quote>"` checks a quote. Pages read
with curl or WebFetch are not in the fetch log, so `verify sources` fails on them in Step 5 (`verify url` checks a
link but stores nothing). Pre-1800 printing uses the long s, which OCR reads as "f": search "fhot" for "shot",
"fufficient" for "sufficient"; `--find` tries those spellings itself (L-012).

## Step 3: reference images from collection records only

AI imagery of the past is anachronistic by default, and image searches return reconstructions, film stills and
other AI pictures (R-20261017-20). So:

1. Search open collections first, CC0 before anything else: `hw.py src met "<object>" --detail 5`, then
   `cleveland`, `artic`, `getty`, `smithsonian` (key), `rijksmuseum`; then `commons` and `europeana` with per-file
   licences; non-commercial collections (British Museum, Science Museum Group) only for non-commercial packs.
   US buildings, mills, bridges and machinery: `hw.py src loc-habs "<subject>"` (HABS/HAER/HALS measured
   drawings, photographs and data pages, public domain).
2. Keep an object only if its record gives the object's own date and place and an accession number (or a Commons
   file page with author and licence), and the date fits the period; say so when the nearest evidence is earlier,
   later or from another region.
3. `hw.py pack add-ref <dir> --image <url> --page <record url> --title "..." --licence CC0 --object-date "..."
   --place "..." --accession "..." --institution "..."`.

`add-ref` refuses a non-commercial licence in a commercial pack and never overwrites an existing file. Expect gaps: the US CC0 APIs return Greek and Etruscan helmets for "Roman helmet" and little late-Republican kit;
that period comes from Commons and Europeana (R-20261017-8). An empty search is a finding: record it in
`completeness` with the reason.

## Step 4: the anachronism checklist

Write `anachronism.md`: what did not exist yet, what is commonly shown wrong, and what the evidence says about
colour, material and shape, each item cited to sources.json. Generated pictures made later from the pack are
labelled reconstructions, never evidence.

For a machine or a building with machinery (`--mechanism`), add the section "Mechanism: what drives what, and
where it must sit": the drive chain from the power source to the tool, one link per numbered item (what the part
is, where it must sit, what it drives, with sizes), then what a picture must never show (a blade outside the
building, a wheel with no shaft into it, free-floating gears). Image models get mechanisms wrong more often than
dates (L-010). For a water-powered machine, fill its "Water path" subsection too: the source (dam or weir and
its spill), head race or flume, gate, where the water meets the wheel for its type (overshot onto the top,
breastshot at the side, undershot against the bottom), the turning direction, the tail race back to the river,
and the prohibitions (no water from the hub; no trough ending above an undershot wheel; the wheel sits in its
race). Replace every `<fill: ...>` with cited facts, or delete the subsection for a wind, horse or steam drive;
validate-pack fails while any is left (L-011). Example: [references/mechanism-example.md](references/mechanism-example.md).

## Step 5: validate and hand over

1. Fill `manifest.json` `historywright.completeness`: every part present, or empty with a reason.
2. `hw.py verify sources <dir>/sources.json` (quotes re-read, independence counted), then
   `hw.py validate-pack <dir>`; fix every problem. Optional: `hw.py pack csl <dir>` for Zotero.
3. Hand over: polywright reads `manifest.json` and `refs/` (its polywright-references skill starts from them;
   `pw.py manifest <dir> --validate` passes); cinewright and comfyui-gen read `answer.md`, `refs/` and
   `anachronism.md`; `places.geojson` feeds maps and `pw.py place`.

Hand-over message:

```
Pack: <dir> for <who/what, where, when>   validate-pack: ok   sources: <n> (<k> independent)
Refs: <n> images (<CC0 n>, <CC BY n>, <NC n>)   Gaps: <empty parts and why>
Next: <the plugin that takes it and what to ask it for>
```

## Rules

- Nothing enters a pack that this run did not fetch and read; every image has a record page and a licence.
- A disputed date is a set or range in `entities.json`, never a point.
- Never strip an author or licence; never put a non-commercial image in a commercial pack.

## Maintenance

Shares the plugin's evergreen unit (tier `moderate`): `evergreen.json` at the plugin root,
[RESEARCH.md](../../RESEARCH.md), [CHANGELOG.md](../../CHANGELOG.md), [LEARNINGS.md](../../LEARNINGS.md),
[TESTS.md](../../TESTS.md), [MAINTENANCE.md](../../MAINTENANCE.md).
