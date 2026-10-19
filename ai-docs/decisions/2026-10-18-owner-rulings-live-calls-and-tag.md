---
title: Owner rulings - live keyless calls in the wiki verifier, and the v0.1.0 tag
kind: decision
date: 2026-10-18
tags: [wiki, network, release, rulings]
summary: "the owner allowed live keyless API calls (wikiwright L-160) on condition that no terms are broken and no ban is risked; paces were tightened to the documented public limits to meet it; the owner approved the v0.1.0 tag"
---

# Owner rulings: live keyless calls and the v0.1.0 tag

Asked at the start of the Step 4 session (2026-10-18).

## 1. Live keyless calls in the wiki verifier (wikiwright L-160 `live-public-sources`)

Ruling, in the owner's words: "yes, ignore wikiwright's rule if this doesn't break terms or will result in them
banning us". The verifier keeps calling the keyless public sources live; wikiwright L-160 is adopted for this
kind of tool (a research CLI over public keyless APIs), departing from L-122.

Checked against the condition, source by source (limits from the 2026-10-17 research, cited in RESEARCH.md):

| Source | Public rule | hw.py before | hw.py now |
|---|---|---|---|
| Wikidata, Wikipedia, Commons | 200/min with a User-Agent naming tool, version and a contact (email or URL); concurrency 3; honour Retry-After | 0.3 s (exactly 200/min) | 0.35 s |
| Crossref (public pool, no mailto) | 5 single records a second, concurrency 1 | 0.1 s | 0.2 s |
| OpenAlex keyless | basic queries allowed; 10 a second, about $0.10 a day | 0.1 s | 0.15 s |
| Wayback availability API (archive.org) | no published limit; clients report 429 near 15/min; it answered 429 on every verifier run | 0.5 s | 4 s |
| Wayback CDX (web.archive.org) | as above | 4 s | 4 s |
| Pleiades, CHGIS, DILA download | no published limit; open data | 0.5 to 1 s | unchanged |

hw.py always sends `historywright/<version> (<repo URL>)`, honours Retry-After, keeps the pace across processes,
and calls no keyed service in the verifier. One verifier run is about 30 requests in three minutes; it runs only
when a packaged file changes. Keep the Windows and WSL runs one after the other, not at once (each has its own pace
file, so running both doubles the rate per host).

Applied in PR "Keyless paces under each source's public limit" (C-20261018-4, R-20261018-1).

## 2. The v0.1.0 tag

Ruling: "yes". Tagged after the pace PR merged, so the release zip carries the tightened paces. The release
workflow checks that plugin.json says 0.1.0, runs the structure checks and the budget, and publishes the zip.
Follow-ups that the wiki note lists for after the first release: a row in Versions-and-Upgrading, the release-zip
install route on Getting-Started, and the verifier's download switched to the release zip.
