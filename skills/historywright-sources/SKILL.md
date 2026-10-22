---
name: historywright-sources
description: "Use to find or curate where historical answers live: which archive, database, library or museum covers an era, region or kind of question (ancient places, Chinese officials, US newspapers, UK records, museum objects), its route, licence, access and pace; add, rank or retire a source; probe every endpoint for moves (hw.py probe); edit the era outline or query recipes. Use on 'where can I find records of', 'what sources cover medieval Japan', 'is this archive reliable', 'add this source', 'probe the sources', 'which museums have open images'. Answering a history question is historywright; packs for 3D or video are historywright-pack."
---

# historywright-sources

The knowledge base of historywright: where answers live and how to reach them. It holds the source registry,
the era outline and the query recipes, and keeps them current. Answers are the hub's job (historywright).

Files (in `references/`):

- [registry.json](references/registry.json): 95 sources, each with `use`, `regions`, `eras`, `tier`
  (1 primary or expert-curated, 2 curated reference or aggregator, 3 crowd-sourced tertiary), `licence`,
  `access`, `key`, `host`, `pace_s`, `route`, a JSON `search` template where one works, a `probe`, `notes`,
  `checked` and the `R-` finding behind it; plus `mirrors` (Wikipedia copies that never count as corroboration)
  and `retired` sources with reasons.
- [eras.md](references/eras.md): the era outline that routes a question to sources (routing only, never cited;
  size budget green under 12 KB).
- [recipes.md](references/recipes.md): query patterns that worked, each dated.

Script: the hub's `hw.py` (`../historywright/scripts/hw.py`).

## Answer "where can I find ..."

1. Read the era outline section for the period and region.
2. `hw.py lint --ids` lists the registry; read the matching entries for route, access and licence.
3. Try it: `hw.py src <id> "<query>"` for sources with a JSON search, or the hub commands for the rest
   (`wd`, `wp`, `place`, `oa`, `doi`). Report what it returned, not what the source is said to hold.
4. Link-out sources (paid, gated, browse-only, bot-walled) are named with their access status and URL, never
   queried. Paid sources are never signed up for or bought.
5. Say where coverage is thin (India, much of Africa, Latin America, Oceania are browse-only or sparse;
   R-20261017-6, -19).

## Add or change a source

1. Check the source's own documentation for the endpoint, limits and licence; test the exact search URL once with
   `hw.py src` after adding it (or with a fetch), sending the tool's User-Agent.
2. Write the entry with every field; `route: "link-out"` and no `search` block when it is paid, gated,
   browse-only or bot-walled. Never write a key into a URL; use `{key}` and a `key` name.
3. Log the finding in RESEARCH.md (`R-` entry with the source URL and date) and the change in CHANGELOG.md.
4. `hw.py lint` must pass; `python tests/check_skills.py` from the repository root.

Tier rules: tier 1 needs primary material or expert curation with named editors (Pleiades, DPRR, CBDB, national
archives, museum collection records); tier 2 is curated reference or an aggregator (OpenAlex, Europeana, WHG);
tier 3 is crowd-sourced (Wikipedia; Wikidata unless the statement carries a real reference). Retire, don't
delete: move the entry to `retired` with the reason and date.

## Probe (every refresh, and when a run hits errors)

`hw.py probe` calls each entry's `probe` URL at its pace and writes `~/.historywright/probe-latest.json`.
Results: `ok`, `moved`, `gone`, `blocked` (a bot wall or a new key requirement), `unreachable`, `changed`. For each
problem: read the source's own announcements (the search plan in RESEARCH.md lists them), fix the entry or move
it to link-out, and log it. This year's changes were mostly endpoints moving (R-20261017-5 to -8), which the probe
catches more cheaply than web research.

## Era outline and recipes

Edit eras.md when a route changes or a region proves thinly served; keep it under 12 KB (`hw.py lint` reports
the band). Add a recipe to recipes.md when a query pattern saved a step, with its check date.

## Maintenance

Shares the plugin's evergreen unit (tier `moderate`): `evergreen.json` at the plugin root,
[RESEARCH.md](../../RESEARCH.md) (its search plan lists every source's change feed), [CHANGELOG.md](../../CHANGELOG.md),
[LEARNINGS.md](../../LEARNINGS.md), [TESTS.md](../../TESTS.md), [MAINTENANCE.md](../../MAINTENANCE.md). A refresh
runs `hw.py probe` first.
