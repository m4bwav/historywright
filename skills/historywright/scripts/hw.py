#!/usr/bin/env python3
"""hw.py - historywright's command line. Python 3.9+, standard library only.

Every command prints one JSON object and fails soft ({"ok": false, "error": ...}, exit 1). Commands:

  doctor                          what works here: Python, home folder and its source, contact, keys, DILA, registry
  wd search|claims|entity|sparql  Wikidata: full statements with precision, calendar, rank, qualifiers, references
  wp summary|refs|search|assess   Wikipedia as a finder: QID per title, the references under a sentence
  place search|pleiades           Pleiades, CHGIS, World Historical Gazetteer, Wikidata coordinates ([lon, lat])
  oa search                       OpenAlex scholarship (keyless page 1; a free key pages further)
  doi DOI [--title --author --year]   Crossref, then OpenAlex; says whether every detail matches
  src ID QUERY                    any registry source with a JSON search (museums, libraries, archives)
  cal date|jdn|span|era|cjk|setup dates in code: JDN, Julian/Gregorian, BCE, AUC, O.S./N.S., Islamic, CJK eras
  cache get|put|list              answers already researched, with sources and retrieval dates
  verify url|quote|doi|qid|sources   URL health, quote spans, DOIs, QIDs, a whole sources.json
  pack init|add-ref|csl           research packs (polywright asset folders); validate-pack DIR checks one
  probe [--only ids]              every registry endpoint, to catch moves between refreshes
  keys status|openalex|whg|contact   optional free keys, stored in ~/.historywright/config.json
  lint                            the source registry and the era outline

HW_HOME overrides ~/.historywright; a .historywright folder in the working directory holds that project's cache.
HW_FIXTURES serves HTTP from files; HW_RECORD saves responses as fixtures.
"""

import argparse
import json
import os
import re
import shutil
import sqlite3
import sys
import uuid
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import hw_check as C  # noqa: E402
import hw_dates as D  # noqa: E402
import hw_sources as S  # noqa: E402
from hw_net import (write_text, REGISTRY_PATH, SKILLS, VERSION, config_path, contact, emit, fail, fetch,  # noqa: E402
                    get_json, get_key, home, home_source, load_config, mask, qs, registry, save_config, today,
                    user_agent, user_home, utf8_stdout)

ERAS_PATH = SKILLS / "historywright-sources" / "references" / "eras.md"


def out(d):
    return emit(d, 0 if d.get("ok", True) else 1)


# ---------------------------------------------------------------- cal

def dila_db(auto=True):
    p = user_home() / "dila_time.sqlite"
    if p.exists():
        return sqlite3.connect(str(p)), None
    if not auto:
        return None, "the East Asian table is not built yet: run hw.py cal setup"
    res = dila_setup()
    if not res.get("ok"):
        return None, res.get("error")
    return sqlite3.connect(str(p)), res


def dila_setup(force=False):
    p = user_home() / "dila_time.sqlite"
    if p.exists() and not force:
        return {"ok": True, "db": str(p), "built": False, "attribution": D.DILA_ATTRIBUTION}
    last = None
    for url in D.DILA_URLS:
        r = fetch(url, accept="application/zip,application/octet-stream,text/plain,*/*", timeout=120)
        if r.ok and len(r.body) > 100000:
            try:
                counts = D.build_dila_db(D.sql_from_download(r.body), p)
            except Exception as e:  # a changed dump format must say so, not crash
                last = "built failed from %s: %s" % (url, e)
                continue
            return {"ok": True, "db": str(p), "built": True, "from": url, "rows": counts,
                    "licence": "CC BY-SA 3.0 Unported; the table stays on this machine",
                    "attribution": D.DILA_ATTRIBUTION}
        last = "%s: %s" % (url, r.error or r.status)
    return {"ok": False, "error": "could not download the DILA time data (%s)" % last}


def cmd_cal(a):
    if a.sub == "setup":
        return out(dila_setup(force=a.force))
    if a.sub == "jdn":
        d = D.describe_jdn(int(a.value), a.country)
        _cjk_extra(d, int(a.value), a)
        return out(dict(ok=True, **d))
    if a.sub == "date":
        if re.search(r"[㐀-鿿]", a.value):
            return cmd_cjk(a)
        try:
            y, m, d, cal, notes = D.parse_date(a.value, a.cal)
        except ValueError as e:
            return fail(str(e))
        first, last = D.span_range(y, m, d, cal)
        qual = D.qualifier_of(a.value)
        edtf = D.edtf_for(y, m, d, qual)
        read_as = {"astronomical_year": y, "month": m, "day": d, "calendar": cal, "label": D.date_label(y, m, d)}
        precision = "day" if d else ("month" if m else "year")
        parts = D.ah_parts(re.sub(D._CIRCA, "", a.value))
        if parts:  # label it in AH; the Western reading is where it starts
            read_as = {"calendar": "islamic (tabular)", "ah_year": parts[0], "ah_month": parts[1],
                       "ah_day": parts[2], "label": D.ah_label(*parts),
                       "western_start": dict(read_as, label=D.date_label(y, m, d))}
            precision = "day" if parts[2] else ("month" if parts[1] else "year")
        ah = D.ah_range(re.sub(D._CIRCA, "", a.value))
        if ah:  # the AH year's or month's own days, which straddle Western years and months
            first, last = ah
            edtf = "%s/%s" % tuple(D.describe_jdn(j)["gregorian" if j >= D.GREGORIAN_START else "julian"]["iso"]
                                   for j in ah)
            if qual:
                edtf = "/".join(x + "~" for x in edtf.split("/"))
        res = {"ok": True, "input": a.value, "read_as": read_as, "precision": precision, "jdn": [first, last],
               "edtf": edtf, "day": D.describe_jdn(first, a.country)}
        if qual:
            res["qualifier"] = qual
        if notes:
            res["notes"] = notes
        _cjk_extra(res, first, a)
        return out(res)
    if a.sub == "span":
        try:
            p1 = D.parse_date(a.value, a.cal)
            p2 = D.parse_date(a.value2, a.cal)
        except ValueError as e:
            return fail(str(e))
        return out(dict(ok=True, start=D.date_label(*p1[:3]), end=D.date_label(*p2[:3]),
                        **D.span(p1[:4], p2[:4])))
    if a.sub in ("era", "cjk"):
        return cmd_cjk(a)
    return fail("unknown cal command")


def _cjk_extra(res, j, a):
    if getattr(a, "cjk", False):
        con, err = dila_db(auto=True)
        res["cjk"] = D.jdn_to_cjk(con, j) if con else {"error": err}
        res["attribution"] = D.DILA_ATTRIBUTION


def cmd_cjk(a):
    con, err = dila_db(auto=True)
    if con is None:
        return fail(err)
    if a.sub == "era":
        rows = D.cjk_eras(con, a.value)
        for r in rows:
            r["start"] = D.describe_jdn(r["start_jdn"])["julian" if r["start_jdn"] < D.GREGORIAN_START else "gregorian"]["label"]
            r["end"] = D.describe_jdn(r["end_jdn"])["julian" if r["end_jdn"] < D.GREGORIAN_START else "gregorian"]["label"]
        return out({"ok": bool(rows), "era": a.value, "matches": rows, "attribution": D.DILA_ATTRIBUTION,
                    "note": "every era with this name is listed; pick by dynasty and country"})
    try:
        parsed, matches = D.cjk_to_jdn(con, a.value)
    except ValueError as e:
        return fail(str(e), attribution=D.DILA_ATTRIBUTION)
    return out({"ok": bool(matches), "input": a.value, "parsed": parsed, "matches": matches,
                "attribution": D.DILA_ATTRIBUTION,
                "note": "an ambiguous era name returns every match; DILA covers China c. 220 BCE-1912, Japan 593-1872, "
                        "Korea 56 BCE-1885"})


# ---------------------------------------------------------------- source commands

def cmd_wd(a):
    if a.sub == "search":
        return out(S.wd_search(a.value, a.lang, a.limit))
    if a.sub == "claims":
        props = [p.strip() for p in (a.prop or "").split(",") if p.strip()] or None
        return out(S.wd_claims(a.value, props, a.lang))
    if a.sub == "entity":
        return out(S.wd_entity(a.value, a.lang))
    if a.sub == "sparql":
        q = Path(a.value).read_text(encoding="utf-8") if os.path.isfile(a.value) else a.value
        return out(S.wd_sparql(q, "scholarly" if a.scholarly else "main"))
    return fail("unknown wd command")


def cmd_wp(a):
    if a.sub == "summary":
        return out(S.wp_summary(a.value, a.lang))
    if a.sub == "refs":
        return out(S.wp_refs(a.value, a.lang, a.near, a.limit))
    if a.sub == "search":
        return out(S.wp_search(a.value, a.lang, a.limit))
    if a.sub == "assess":
        return out(S.wp_assess(a.value, a.lang))
    return fail("unknown wp command")


def cmd_place(a):
    if a.sub == "pleiades":
        return out(dict(ok=True, **S.pleiades_place(a.value)))
    return out(S.place_search(a.value, a.source, a.year, a.limit))


def cmd_oa(a):
    return out(S.oa_search(a.value, a.page, a.limit, a.filter))


def cmd_doi(a):
    return out(S.doi_lookup(a.doi, a.title, a.author, a.year))


def cmd_src(a):
    return out(S.src_search(a.id, a.query, a.limit, a.detail))


# ---------------------------------------------------------------- cache, verify, pack

def cmd_cache(a):
    if a.sub == "get":
        return out(C.cache_get(a.value, a.max_age))
    if a.sub == "list":
        return out(C.cache_list())
    if a.sub == "put":
        try:
            entry = C.load_json(a.value)
        except (OSError, ValueError) as e:
            return fail("cannot read %s: %s" % (a.value, e))
        return out(C.cache_put(entry))
    return fail("unknown cache command")


def cmd_verify(a):
    if a.sub == "url":
        rows = [C.url_health(u) for u in a.values]
        bad = [r for r in rows if r["label"] in ("dead", "likely_hallucinated")]
        return out({"ok": not bad, "results": rows})
    if a.sub == "quote":
        return out(C.verify_quote(a.url, a.quote, a.refetch))
    if a.sub == "doi":
        return out(S.doi_lookup(a.values[0], a.title, a.author, a.year))
    if a.sub == "qid":
        return out(C.verify_qid(a.values[0], a.label))
    if a.sub == "sources":
        try:
            doc = C.load_json(a.values[0])
        except (OSError, ValueError) as e:
            return fail("cannot read %s: %s" % (a.values[0], e))
        return out(C.check_sources(doc, network=not a.offline, require_fetched=not a.any_url))
    return fail("unknown verify command")


def cmd_pack(a):
    if a.sub == "init":
        return out(C.pack_init(a.dir, a.question, a.name, a.period, a.commercial, a.mechanism))
    if a.sub == "add-ref":
        return out(C.pack_add_ref(a.dir, a.image, a.page, a.title, a.licence, a.object_date, a.place, a.accession,
                                  a.institution, a.author))
    if a.sub == "csl":
        return out(C.pack_csl(a.dir))
    return fail("unknown pack command")


def cmd_validate_pack(a):
    return out(C.validate_pack(a.dir, network=a.network))


# ---------------------------------------------------------------- probe, lint, keys, doctor

CHALLENGE = re.compile(r"(?i)anubis|just a moment\.\.\.|cf-chl|security check|captcha|are you a robot|"
                       r"enable javascript and cookies")


def _parses(r):
    try:
        r.json()
        return True
    except ValueError:
        return False


def cmd_probe(a):
    rows, only = [], set((a.only or "").split(",")) - {""}
    for s in registry().get("sources", []):
        if only and s["id"] not in only:
            continue
        pr = s.get("probe")
        if not pr or not pr.get("url"):
            continue
        url = pr["url"]
        if "{key}" in url:
            k = get_key(s.get("key") or "")
            if not k:
                rows.append({"id": s["id"], "result": "skipped", "why": "needs key %s" % s.get("key")})
                continue
            url = url.replace("{key}", k)
        hdr = dict((s.get("search") or {}).get("headers") or {})
        if s.get("ua") == "plain":
            hdr["User-Agent"] = ("historywright " + contact()).strip()
        r = fetch(url, accept=pr.get("accept", "application/json,*/*"), headers=hdr or None, retries=0)
        want = pr.get("expect", 200)
        if r.status == want:
            res = "ok"
            head = r.text()[:4000]
            if CHALLENGE.search(head):
                res = "blocked"  # bot walls (Anubis, Cloudflare) often answer 200 with a challenge page
            elif pr.get("contains") and pr["contains"] not in r.text():
                res = "changed"
            elif pr.get("json", s.get("route") == "src") and not _parses(r):
                res = "changed"
        elif r.status in (401, 403):
            res = "blocked"
        elif r.status in (301, 302, 308) or (r.url and r.url != url and r.ok):
            res = "moved"
        elif r.status == 404 or r.status == 410:
            res = "gone"
        elif r.status is None:
            res = "unreachable"
        else:
            res = "error"
        rows.append({"id": s["id"], "result": res, "status": r.status,
                     **({"error": r.error} if r.error and res != "ok" else {})})
    summary = {}
    for r in rows:
        summary[r["result"]] = summary.get(r["result"], 0) + 1
    res = {"ok": all(r["result"] in ("ok", "skipped") for r in rows), "date": today(), "summary": summary,
           "problems": [r for r in rows if r["result"] not in ("ok", "skipped")], "probed": len(rows)}
    write_text(home() / "probe-latest.json", json.dumps(dict(res, rows=rows), indent=1) + "\n")
    return out(res)


ACCESS = {"open", "ua-required", "key-optional", "key-required", "paid", "browse-only", "bulk-only", "link-out"}
ROUTES = {"wd", "wp", "place", "oa", "doi", "cal", "src", "link-out"}


def lint_registry(reg):
    probs, warns, ids = [], [], set()
    for s in reg.get("sources", []):
        sid = s.get("id", "?")
        if sid in ids:
            probs.append("duplicate id %s" % sid)
        ids.add(sid)
        for k in ("id", "name", "use", "kind", "tier", "licence", "access", "route", "url", "checked"):
            if s.get(k) in (None, ""):
                probs.append("%s: missing %s" % (sid, k))
        if s.get("tier") not in (1, 2, 3):
            probs.append("%s: tier must be 1, 2 or 3" % sid)
        if s.get("access") not in ACCESS:
            probs.append("%s: access %r not one of %s" % (sid, s.get("access"), sorted(ACCESS)))
        if s.get("route") not in ROUTES:
            probs.append("%s: route %r not one of %s" % (sid, s.get("route"), sorted(ROUTES)))
        if s.get("route") == "src" and not (s.get("search") or {}).get("url"):
            probs.append("%s: route src needs a search url" % sid)
        if s.get("search") and "{q}" not in s["search"].get("url", ""):
            probs.append("%s: search url lacks {q}" % sid)
        if s.get("access") == "paid" and s.get("route") != "link-out":
            probs.append("%s: paid sources are link-out only" % sid)
        if s.get("route") != "link-out" and not s.get("probe"):
            warns.append("%s: no probe, so endpoint moves go unnoticed" % sid)
        for u in [s.get("url"), (s.get("search") or {}).get("url"), (s.get("probe") or {}).get("url")]:
            if u and not u.startswith("https://") and not u.startswith("http://"):
                probs.append("%s: url %r is not http(s)" % (sid, u))
            if u and re.search(r"(api_key|token|key)=[A-Za-z0-9_-]{16,}", u):
                probs.append("%s: a real key is written into a URL; use {key}" % sid)
        if not isinstance(s.get("pace_s", 0.5), (int, float)):
            probs.append("%s: pace_s must be a number" % sid)
    return probs, warns


def cmd_lint(a):
    reg = registry()
    probs, warns = lint_registry(reg)
    if not reg.get("sources"):
        probs.append("registry empty or unreadable: %s" % REGISTRY_PATH)
    size = ERAS_PATH.stat().st_size if ERAS_PATH.exists() else 0
    band = "green" if size < 12000 else ("yellow" if size < 25000 else "red")
    if not size:
        probs.append("era outline missing: %s" % ERAS_PATH)
    elif band == "red":
        probs.append("era outline is %d bytes (red above 25 KB)" % size)
    tiers, routes = {}, {}
    for s in reg.get("sources", []):
        tiers[s.get("tier")] = tiers.get(s.get("tier"), 0) + 1
        routes[s.get("route")] = routes.get(s.get("route"), 0) + 1
    return out({"ok": not probs, "sources": len(reg.get("sources", [])), "by_tier": tiers, "by_route": routes,
                "era_outline_bytes": size, "era_outline_band": band, "problems": probs, "warnings": warns,
                "ids": sorted(s.get("id") for s in reg.get("sources", [])) if a.ids else None})


OPENALEX_KEYS = "https://api.openalex.org/api-keys"
WHG_LOGIN = "https://whgazetteer.org/accounts/login/?next=/profile/"


def cmd_keys(a):
    cfg = load_config()
    keys = cfg.setdefault("keys", {})
    if a.sub == "status":
        rows = {"contact": {"set": bool(contact()), "why": "goes into the User-Agent; Wikimedia allows 10 requests a "
                            "minute without one and 200 with one"}}
        k = get_key("openalex")
        row = {"set": bool(k), "key": mask(k)}
        if k and not a.offline:
            d, r = get_json("https://api.openalex.org/rate-limit", headers={"Authorization": "Bearer " + k})
            row["check"] = "ok" if d is not None else ("not activated: click the email" if r.status == 403 else r.error)
            if d:
                row["daily_budget"] = d.get("daily_budget_usd") or (d.get("rate_limit") or {}).get("daily_budget_usd")
        rows["openalex"] = row
        t = get_key("whg")
        row = {"set": bool(t), "token": mask(t)}
        if t and not a.offline:
            d, r = get_json("https://whgazetteer.org/suggest/entity?prefix=Roma", headers={"Authorization": "Bearer " + t})
            row["check"] = "ok" if d is not None else "failed (%s)" % (r.status or r.error)
        rows["whg"] = row
        for name in ("smithsonian", "europeana"):
            rows[name] = {"set": bool(get_key(name))}
        return out({"ok": True, "config": str(config_path()), "keys": rows,
                    "note": "every key is optional and free; historywright works without any"})
    if a.sub == "contact":
        if not a.set:
            return out({"ok": True, "contact": contact() or None})
        cfg["contact"] = a.set
        save_config(cfg)
        return out({"ok": True, "contact": a.set, "user_agent": user_agent()})
    if a.sub == "openalex":
        if not a.email:
            return fail("give the user's own email with --email (never invent one) and run again with --yes")
        if not a.yes:
            return out({"ok": False, "needs_confirmation": True,
                        "will": "POST %s with this email; OpenAlex emails an activation link (valid 7 days)" % OPENALEX_KEYS,
                        "email": a.email, "then": "run again with --yes once the user agrees"})
        r = fetch(OPENALEX_KEYS, method="POST", data={"email": a.email, "name": "historywright", "agent": "historywright"},
                  headers={"Idempotency-Key": str(uuid.uuid4())}, retries=0)
        try:
            body = r.json()
        except ValueError:
            body = {}
        key = body.get("api_key") or body.get("key")
        if not key:
            return fail("OpenAlex did not return a key (%s)" % (r.status or r.error), body=str(body)[:300])
        keys["openalex"] = {"api_key": key, "status": body.get("status", "pending_activation"), "requested": today()}
        cfg.setdefault("contact", a.email)
        save_config(cfg)
        return out({"ok": True, "saved": str(config_path()), "key": mask(key),
                    "next": "the user clicks 'Activate your OpenAlex API key' in their email, then: hw.py keys status"})
    if a.sub == "whg":
        if a.token:
            keys["whg"] = {"token": a.token, "saved": today()}
            save_config(cfg)
            return out({"ok": True, "saved": str(config_path()), "token": mask(a.token),
                        "next": "hw.py keys status"})
        opened = False
        if not a.no_browser:
            try:
                opened = webbrowser.open(WHG_LOGIN)  # picks the platform's opener on Windows, macOS and Linux
            except webbrowser.Error:
                opened = False
        return out({"ok": True, "opened": opened, "url": WHG_LOGIN,
                    "steps": ["choose 'Sign in with ORCiD' (ORCID is free; it offers to register an iD)",
                              "the first sign-in creates the WHG account",
                              "on the Profile page, generate an API token",
                              "run: hw.py keys whg --token <the token>"]})
    return fail("unknown keys command")


def cmd_doctor(a):
    cfg = load_config()
    reg = registry()
    db = user_home() / "dila_time.sqlite"
    src, _ = home_source()
    checks = {
        "python": sys.version.split()[0],
        "python_ok": sys.version_info >= (3, 9),
        "home": str(home()),
        "home_from": src,
        "config": str(config_path()),
        "contact": bool(contact()),
        "keys": {k: bool(get_key(k)) for k in ("openalex", "whg", "smithsonian", "europeana")},
        "registry": {"path": str(REGISTRY_PATH), "sources": len(reg.get("sources", []))},
        "era_outline": ERAS_PATH.exists(),
        "dila_table": db.exists(),
        "cache_entries": len(list((home() / "cache").glob("*.json"))) if (home() / "cache").exists() else 0,
        "user_agent": user_agent(),
        "pdftotext": bool(shutil.which("pdftotext")),
    }
    todo = []
    if not checks["contact"]:
        todo.append("set a contact address for the User-Agent: hw.py keys contact --set ADDRESS (the user's own)")
    checks["cwd_in_skill_folder"] = Path.cwd().resolve().is_relative_to(SKILLS.resolve())
    if checks["cwd_in_skill_folder"]:
        todo.append("the working directory is the skill folder: run hw.py by its full path from the project "
                    "folder, or a project's .historywright/ cache is not used")
    if not checks["dila_table"]:
        todo.append("East Asian eras build on first use (hw.py cal setup, 1.3 MB download)")
    if not checks["registry"]["sources"]:
        todo.append("registry missing: reinstall the plugin")
    if a.net:
        r = fetch("https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q1048&props=labels&languages=en&format=json")
        checks["wikidata_reachable"] = r.ok
    return out({"ok": checks["python_ok"] and bool(checks["registry"]["sources"]), "version": VERSION,
                "checks": checks, "todo": todo, "config_has": sorted(cfg.keys())})


# ---------------------------------------------------------------- argparse

def build():
    p = argparse.ArgumentParser(prog="hw.py", description="historywright: answers from sources, not memory")
    p.add_argument("--version", action="version", version=VERSION)
    sp = p.add_subparsers(dest="cmd", required=True)

    x = sp.add_parser("doctor")
    x.add_argument("--net", action="store_true")
    x.set_defaults(fn=cmd_doctor)

    x = sp.add_parser("wd")
    x.add_argument("sub", choices=["search", "claims", "entity", "sparql"])
    x.add_argument("value")
    x.add_argument("--prop", help="comma list, e.g. P569,P570")
    x.add_argument("--lang", default="en")
    x.add_argument("--limit", type=int, default=7)
    x.add_argument("--scholarly", action="store_true", help="query-scholarly.wikidata.org")
    x.set_defaults(fn=cmd_wd)

    x = sp.add_parser("wp")
    x.add_argument("sub", choices=["summary", "refs", "search", "assess"])
    x.add_argument("value")
    x.add_argument("--near", help="only references cited in the sentence holding this phrase")
    x.add_argument("--lang", default="en")
    x.add_argument("--limit", type=int, default=40)
    x.set_defaults(fn=cmd_wp)

    x = sp.add_parser("place")
    x.add_argument("sub", choices=["search", "pleiades"])
    x.add_argument("value")
    x.add_argument("--source", default="auto", choices=["auto", "pleiades", "chgis", "whg", "wikidata", "ohm"])
    x.add_argument("--year", type=int)
    x.add_argument("--limit", type=int, default=5)
    x.set_defaults(fn=cmd_place)

    x = sp.add_parser("oa")
    x.add_argument("sub", choices=["search"])
    x.add_argument("value")
    x.add_argument("--page", type=int, default=1)
    x.add_argument("--limit", type=int, default=10)
    x.add_argument("--filter")
    x.set_defaults(fn=cmd_oa)

    x = sp.add_parser("doi")
    x.add_argument("doi")
    x.add_argument("--title")
    x.add_argument("--author")
    x.add_argument("--year")
    x.set_defaults(fn=cmd_doi)

    x = sp.add_parser("src")
    x.add_argument("id")
    x.add_argument("query")
    x.add_argument("--limit", type=int, default=10)
    x.add_argument("--detail", type=int, default=0, help="fetch the detail record for the first N results")
    x.set_defaults(fn=cmd_src)

    x = sp.add_parser("cal")
    x.add_argument("sub", choices=["date", "jdn", "span", "era", "cjk", "setup"])
    x.add_argument("value", nargs="?", default="")
    x.add_argument("value2", nargs="?", default="")
    x.add_argument("--cal", default="auto", choices=["auto", "julian", "gregorian"])
    x.add_argument("--country", help="civil calendar in force: GB, US, RU, SE, FR, GR, JP, CN, KR, TR, ...")
    x.add_argument("--cjk", action="store_true", help="also give concurrent Chinese, Japanese and Korean dates")
    x.add_argument("--force", action="store_true")
    x.set_defaults(fn=cmd_cal)

    x = sp.add_parser("cache")
    x.add_argument("sub", choices=["get", "put", "list"])
    x.add_argument("value", nargs="?", default="")
    x.add_argument("--max-age", type=float)
    x.set_defaults(fn=cmd_cache)

    x = sp.add_parser("verify")
    x.add_argument("sub", choices=["url", "quote", "doi", "qid", "sources"])
    x.add_argument("values", nargs="*")
    x.add_argument("--url")
    x.add_argument("--quote")
    x.add_argument("--refetch", action="store_true")
    x.add_argument("--title")
    x.add_argument("--author")
    x.add_argument("--year")
    x.add_argument("--label")
    x.add_argument("--offline", action="store_true", help="sources: structure only, no network")
    x.add_argument("--any-url", action="store_true", help="sources: do not require each URL in the fetch log")
    x.set_defaults(fn=cmd_verify)

    x = sp.add_parser("pack")
    x.add_argument("sub", choices=["init", "add-ref", "csl"])
    x.add_argument("dir")
    x.add_argument("--question", default="")
    x.add_argument("--name")
    x.add_argument("--period")
    x.add_argument("--commercial", action="store_true")
    x.add_argument("--mechanism", action="store_true",
                   help="init: a machine or a building with machinery; anachronism.md gets the Mechanism section")
    for k in ("image", "page", "title", "licence", "object-date", "place", "accession", "institution", "author"):
        x.add_argument("--" + k)
    x.set_defaults(fn=cmd_pack)

    x = sp.add_parser("validate-pack")
    x.add_argument("dir")
    x.add_argument("--network", action="store_true", help="also re-read every quote and DOI")
    x.set_defaults(fn=cmd_validate_pack)

    x = sp.add_parser("probe")
    x.add_argument("--only")
    x.set_defaults(fn=cmd_probe)

    x = sp.add_parser("keys")
    x.add_argument("sub", choices=["status", "openalex", "whg", "contact"])
    x.add_argument("--email")
    x.add_argument("--yes", action="store_true")
    x.add_argument("--token")
    x.add_argument("--set")
    x.add_argument("--no-browser", action="store_true")
    x.add_argument("--offline", action="store_true")
    x.set_defaults(fn=cmd_keys)

    x = sp.add_parser("lint")
    x.add_argument("--ids", action="store_true")
    x.set_defaults(fn=cmd_lint)
    return p


def main(argv=None):
    utf8_stdout()
    args = build().parse_args(argv)
    if args.cmd == "verify" and args.sub == "quote" and not (args.url and args.quote):
        return fail("verify quote needs --url and --quote")
    if args.cmd == "pack" and args.sub == "init" and not args.question:
        return fail("pack init needs --question")
    try:
        return args.fn(args)
    except KeyboardInterrupt:
        return fail("interrupted")
    except Exception as e:  # fail soft: one JSON object, never a traceback the agent must parse
        return fail("%s: %s" % (type(e).__name__, e))


if __name__ == "__main__":
    sys.exit(main())
