# Step 1 rulings (2026-10-17)

Small design rulings made during the creation pass, per the kickoff's "decide small rulings yourself". Each can be reversed in Step 2 if the build shows otherwise. The forks that are Mark's call are at the end of [../research/2026-10-17-creation-pass.md](../research/2026-10-17-creation-pass.md).

1. **Read Wikidata's full statements, never truthy values alone.** `wdt:` hides disputed alternatives (Caesar's 102 BC statement) and SPARQL's `timeValue` shifts BCE years and converts calendars. hw.py uses `wbgetclaims` or `p:/ps:/psv:` with precision, calendar, rank and qualifiers. Source: R-20261017-2.
2. **Drop DBpedia as a route.** It is derived from Wikipedia and adds nothing over Wikidata. Source: R-20261017-4.
3. **No paid sources; gated ones are link-out only.** ctext, JSTOR, eHRAF, the Oxford Classical Dictionary, New Pauly, BBIH and the rest are named in the registry with their access status, never queried. Source: R-20261017-6, -7.
4. **Handwriting recognition is out of v1.** A pack can mark a source "image only" with a pointer to Claude vision or Transkribus. Source: R-20261017-14.
5. **hw.py stays stdlib-only.** convertdate, edtf and hijridate serve only as test oracles; JDN is the pivot; EDTF levels 0 and 1 only. Source: R-20261017-9, -14.
6. **Licence gate for pack images.** CC0 and CC BY go in by default. Non-commercial images (British Museum, Science Museum, D-PLACE, CBDB data; Seshat until 2026-10-18, when its current terms proved CC BY-SA 4.0, R-20261018-4) are flagged `nc` and kept out of a pack marked for commercial use. Source: R-20261017-8.
7. **Tier `moderate`, with a scripted probe.** Most of this year's changes were endpoints moving, which `hw.py probe` catches between refreshes more cheaply than web research. Source: R-20261017-5 to -8.
8. **Size budget.** Plugin install: green under 400 KB, yellow to 1 MB, red above. Era outline: green under 12 KB, yellow to 25 KB, red above. Large tables (DILA, the Pleiades dump) download on demand into `~/.historywright/` and never ship in the repo.
9. **One shared HTTP layer.** A contact User-Agent (from `~/.historywright/config.json`), per-host throttles from the registry, concurrency 3, Retry-After honoured. Wikimedia, WHG, Open Context and EDGAR all refuse or throttle clients without one. Source: R-20261017-5, -6.
