"""Source commands for hw.py: Wikidata full statements, Wikipedia as a finder, places, OpenAlex, Crossref, and the
generic registry search. Each returns plain dicts; hw.py prints them."""

import html
import re
import urllib.parse

import hw_dates as D
from hw_net import (as_list, contact, dig, fetch, get_json, get_key, html_to_text, is_mirror, qs, redact, registry,
                    source)

WD_API = "https://www.wikidata.org/w/api.php"
WDQS = {"main": "https://query.wikidata.org/sparql", "scholarly": "https://query-scholarly.wikidata.org/sparql"}
WP_REST = "https://{lang}.wikipedia.org/api/rest_v1"
WP_API = "https://{lang}.wikipedia.org/w/api.php"

# Properties a history question usually needs, used when `wd claims` gets no --prop.
HISTORY_PROPS = ["P31", "P569", "P570", "P19", "P20", "P571", "P576", "P580", "P582", "P585", "P112", "P159",
                 "P740", "P39", "P26", "P22", "P25", "P27", "P625", "P1082", "P17", "P131", "P1584", "P2044"]
TIME_PROPS = {"P569", "P570", "P571", "P576", "P580", "P582", "P585", "P577", "P1191", "P1249", "P1319", "P1326",
              "P813", "P2031", "P2032", "P1619", "P3999", "P7124", "P7125"}
DISPUTED = {"Q18912752": "disputed", "Q5727902": "circa", "Q56644435": "probably", "Q18122778": "presumably",
            "Q30230067": "possibly", "Q21818619": "near", "Q110290992": "or"}
IMPORT_PROPS = {"P143", "P4656", "P3452"}  # imported from Wikimedia project, Wikimedia import URL, inferred from


# ---------------------------------------------------------------- Wikidata

def wd_search(query, lang="en", limit=7):
    data, r = get_json(WD_API + "?" + qs({"action": "wbsearchentities", "search": query, "language": lang,
                                           "uselang": lang, "type": "item", "limit": limit, "format": "json"}))
    if data is None:
        return {"ok": False, "error": r.error or "search failed", "status": r.status}
    return {"ok": True, "api": "wbsearchentities", "query": query,
            "results": [{"qid": x["id"], "label": x.get("label"), "description": x.get("description")}
                        for x in data.get("search", [])]}


def wd_labels(ids, lang="en"):
    ids = sorted({i for i in ids if i and re.fullmatch(r"[QPL]\d+", i)})
    out = {}
    for k in range(0, len(ids), 50):
        data, _ = get_json(WD_API + "?" + qs({"action": "wbgetentities", "ids": "|".join(ids[k:k + 50]),
                                               "props": "labels", "languages": lang + "|mul", "format": "json"}))
        for qid, ent in (data or {}).get("entities", {}).items():
            labels = ent.get("labels", {})
            lab = labels.get(lang) or labels.get("mul")
            out[qid] = lab["value"] if lab else None
    return out


def _snak_value(snak):
    if snak.get("snaktype") != "value":
        return {"special": snak.get("snaktype")}
    dv = snak.get("datavalue", {})
    t, v = dv.get("type"), dv.get("value")
    if t == "time":
        return {"time": D.wikidata_time(v)}
    if t == "wikibase-entityid":
        return {"qid": v.get("id")}
    if t == "globecoordinate":
        return {"coord": [v.get("longitude"), v.get("latitude")], "note": "[lon, lat]"}
    if t == "quantity":
        return {"amount": v.get("amount"), "unit": (v.get("unit") or "").rsplit("/", 1)[-1]}
    if t == "monolingualtext":
        return {"text": v.get("text"), "lang": v.get("language")}
    return {"value": v}


def _collect_ids(obj, acc):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "qid" and isinstance(v, str):
                acc.add(v)
            else:
                _collect_ids(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            _collect_ids(v, acc)


def _reference(ref):
    snaks = ref.get("snaks", {})
    out = {}
    for p, vals in snaks.items():
        vs = [_snak_value(s) for s in vals]
        if p == "P248":
            out["stated_in"] = [v.get("qid") for v in vs]
        elif p == "P854":
            out["url"] = [v.get("value") for v in vs]
        elif p == "P813":
            out["retrieved"] = [v.get("time", {}).get("as_written") for v in vs]
        elif p in ("P304", "P958", "P1545", "P792"):
            out.setdefault("locator", []).extend(str(v.get("value")) for v in vs)
        elif p in IMPORT_PROPS:
            out["imported_from"] = [v.get("qid") or v.get("value") for v in vs]
        elif p == "P1683":
            out["quote"] = [v.get("text") for v in vs]
        else:
            out.setdefault("other", {})[p] = vs
    out["wikimedia_import_only"] = bool(out.get("imported_from")) and not (out.get("stated_in") or out.get("url"))
    return out


def wd_claims(qid, props=None, lang="en"):
    """Full statements with rank, qualifiers and references; never the truthy value alone (R-20261017-2)."""
    if not re.fullmatch(r"Q\d+", qid or ""):
        return {"ok": False, "error": "not a QID: %r (discover it with wd search first; never invent one)" % qid}
    params = {"action": "wbgetclaims", "entity": qid, "format": "json"}
    if props and len(props) == 1:
        params["property"] = props[0]
    data, r = get_json(WD_API + "?" + qs(params))
    if data is None:
        return {"ok": False, "error": r.error or "wbgetclaims failed", "status": r.status}
    if "error" in data:
        return {"ok": False, "error": data["error"].get("info")}
    claims = data.get("claims", {})
    wanted = props or [p for p in HISTORY_PROPS if p in claims]
    out_claims = {}
    for p in wanted:
        stmts = []
        for s in claims.get(p, []):
            st = {"rank": s.get("rank"), "value": _snak_value(s.get("mainsnak", {}))}
            quals = {}
            for qp, qv in (s.get("qualifiers") or {}).items():
                quals[qp] = [_snak_value(x) for x in qv]
            if quals:
                st["qualifiers"] = quals
            circ = [DISPUTED.get(v.get("qid"), v.get("qid")) for v in quals.get("P1480", [])]
            if circ:
                st["sourcing_circumstances"] = circ
            if "P1319" in quals or "P1326" in quals:
                st["earliest"] = (quals.get("P1319") or [{}])[0].get("time", {}).get("as_written")
                st["latest"] = (quals.get("P1326") or [{}])[0].get("time", {}).get("as_written")
            refs = [_reference(x) for x in s.get("references", [])]
            st["references"] = refs
            st["referenced"] = any(not x["wikimedia_import_only"] for x in refs)
            stmts.append(st)
        if stmts:
            out_claims[p] = stmts
    ids = set(wanted)
    _collect_ids(out_claims, ids)
    for stl in out_claims.values():
        for st in stl:
            for ref in st["references"]:
                ids.update(x for x in ref.get("stated_in", []) if x)
                ids.update(q for q in (ref.get("other") or {}) if q.startswith("P"))
            ids.update(st.get("qualifiers", {}).keys())
    labels = wd_labels(ids | {qid}, lang)
    notes = []
    for p, stl in out_claims.items():
        if p in TIME_PROPS and len(stl) > 1:
            notes.append("%s has %d statements: a truthy (wdt:) read would show only the best-ranked one" % (p, len(stl)))
        if any("disputed" in (st.get("sourcing_circumstances") or []) for st in stl):
            notes.append("%s carries a disputed flag: report the alternatives and who holds each" % p)
        if stl and not any(st["referenced"] for st in stl):
            notes.append("%s has no reference beyond a Wikimedia import: find a source before citing it" % p)
    return {"ok": True, "api": "wbgetclaims", "qid": qid, "label": labels.get(qid), "claims": out_claims,
            "labels": {k: v for k, v in labels.items() if v}, "notes": notes,
            "url": "https://www.wikidata.org/wiki/%s" % qid}


def wd_entity(qid, lang="en"):
    data, r = get_json(WD_API + "?" + qs({"action": "wbgetentities", "ids": qid, "props": "labels|descriptions|"
                                           "sitelinks|aliases", "languages": lang + "|mul", "format": "json"}))
    if data is None:
        return {"ok": False, "error": r.error, "status": r.status}
    ent = data.get("entities", {}).get(qid, {})
    if "missing" in ent:
        return {"ok": False, "error": "%s does not exist" % qid, "exists": False}
    lab = ent.get("labels", {})
    sl = ent.get("sitelinks", {})
    return {"ok": True, "exists": True, "qid": qid,
            "label": (lab.get(lang) or lab.get("mul") or {}).get("value"),
            "description": (ent.get("descriptions", {}).get(lang) or {}).get("value"),
            "aliases": [a["value"] for a in ent.get("aliases", {}).get(lang, [])][:8],
            "wikipedia": {k: v.get("title") for k, v in sl.items() if k in (lang + "wiki", "enwiki", "zhwiki",
                                                                            "jawiki", "frwiki", "dewiki", "arwiki")}}


_WDT_TIME = re.compile(r"wdt:(P\d+)")


def sparql_warnings(query):
    w = []
    for p in _WDT_TIME.findall(query):
        if p in TIME_PROPS:
            w.append("wdt:%s returns only the best-ranked value and SPARQL shifts BCE years (XSD year 0) and converts "
                     "to Gregorian: use p:%s/psv:%s with wikibase:timePrecision and wikibase:timeCalendarModel, "
                     "or `hw.py wd claims`" % (p, p, p))
    return w


def wd_sparql(query, graph="main"):
    url = WDQS[graph] + "?" + qs({"query": query, "format": "json"})
    data, r = get_json(url, accept="application/sparql-results+json", timeout=70)
    out = {"api": "sparql", "graph": graph, "warnings": sparql_warnings(query)}
    if data is None:
        out.update(ok=False, error=r.error or "query failed", status=r.status, body=r.text()[:300])
        return out
    rows = []
    for b in data.get("results", {}).get("bindings", [])[:200]:
        rows.append({k: v.get("value") for k, v in b.items()})
    out.update(ok=True, vars=data.get("head", {}).get("vars"), rows=rows, count=len(rows))
    return out


# ---------------------------------------------------------------- Wikipedia (finder, never the authority)

def wp_summary(title, lang="en"):
    t = urllib.parse.quote(title.replace(" ", "_"), safe="")
    data, r = get_json(WP_REST.format(lang=lang) + "/page/summary/" + t)
    if data is None:
        return {"ok": False, "error": r.error, "status": r.status}
    return {"ok": True, "title": data.get("title"), "qid": data.get("wikibase_item"),
            "description": data.get("description"), "extract": data.get("extract"),
            "url": dig(data, "content_urls.desktop.page"), "revision": data.get("revision"),
            "timestamp": data.get("timestamp"),
            "role": "finder: follow its references and cite those, never the article (R-20261017-3)"}


def wp_search(query, lang="en", limit=8):
    data, r = get_json(WP_API.format(lang=lang) + "?" + qs({"action": "query", "list": "search", "srsearch": query,
                                                            "srlimit": limit, "format": "json"}))
    if data is None:
        return {"ok": False, "error": r.error, "status": r.status}
    return {"ok": True, "results": [{"title": x["title"], "snippet": html_to_text(x.get("snippet", ""))}
                                    for x in dig(data, "query.search") or []]}


def wp_assess(title, lang="en"):
    data, r = get_json(WP_API.format(lang=lang) + "?" + qs({"action": "query", "prop": "pageassessments|info",
                                                            "redirects": 1, "titles": title, "format": "json"}))
    if data is None:
        return {"ok": False, "error": r.error}
    pages = as_list(dig(data, "query.pages"))
    if not pages:
        return {"ok": False, "error": "no page"}
    p = pages[0]
    return {"ok": True, "title": p.get("title"), "redirected": dig(data, "query.redirects"),
            "assessments": {k: v.get("class") for k, v in (p.get("pageassessments") or {}).items()},
            "touched": p.get("touched")}


def _ref_item(raw):
    body = raw
    m = re.search(r'<span class="reference-text">(.*)', raw, re.S)
    if m:
        body = m.group(1)
    links = [html.unescape(u) for u in re.findall(r'class="external[^"]*"\s+href="([^"]+)"', body)]
    links += [html.unescape(u) for u in re.findall(r'href="([^"]+)"\s+class="external', body)]
    dois = sorted(set(re.findall(r"10\.\d{4,9}/[^\s\"<>&]+", html.unescape(body))))
    isbns = sorted(set(re.findall(r"ISBN[^0-9X]{0,3}([0-9X-]{10,17})", html_to_text(body))))
    return {"text": html_to_text(body)[:600], "links": list(dict.fromkeys(links))[:5], "dois": dois[:3],
            "isbns": isbns[:3]}


def wp_refs(title, lang="en", near=None, limit=40):
    """The references under an article; with near="phrase", only those cited in the sentence holding it."""
    data, r = get_json(WP_API.format(lang=lang) + "?" + qs({"action": "parse", "page": title, "prop": "text",
                                                            "format": "json", "formatversion": 2, "redirects": 1}))
    if data is None or "parse" not in data:
        return {"ok": False, "error": (data or {}).get("error", {}).get("info") or r.error, "status": r.status}
    page = data["parse"]["text"]
    notes = {}
    for m in re.finditer(r'<li id="(cite(?:&#95;|_)note-[^"]+)"[^>]*>(.*?)</li>\s*(?=<li id="cite|</ol>)', page, re.S):
        notes[html.unescape(m.group(1))] = m.group(2)
    out = {"ok": True, "title": data["parse"].get("title"), "references_total": len(notes),
           "url": "https://%s.wikipedia.org/wiki/%s" % (lang, urllib.parse.quote(data["parse"].get("title", title).replace(" ", "_"))),
           "role": "finder: read each reference and cite it, not the article"}
    if near:
        text_pos = None
        plain = page
        idx = plain.find(near)
        if idx < 0:
            # tolerate tags inside the phrase: search in a tag-stripped copy that keeps a position map
            stripped, pos_map, i = [], [], 0
            for m in re.finditer(r"<[^>]+>|[^<]+", plain):
                if not m.group(0).startswith("<"):
                    seg = html.unescape(m.group(0))
                    stripped.append(seg)
                    pos_map.extend([m.start()] * len(seg))
            flat = "".join(stripped)
            k = flat.find(near)
            if k >= 0:
                text_pos = pos_map[k]
        else:
            text_pos = idx
        if text_pos is None:
            out.update(ok=False, error="phrase not found in the article: %r" % near)
            return out
        # sentence start: the last full stop (or paragraph start) before the phrase
        back = plain[max(0, text_pos - 3000):text_pos]
        starts = [m.end() for m in re.finditer(r"<p>|\.(?:</a>)?(?:<sup.*?</sup>)*\s", back, re.S)]
        start = text_pos - len(back) + (starts[-1] if starts else 0)
        # sentence end: the first full stop after the phrase, plus the footnote markers right after it
        para_end = plain.find("</p>", text_pos)
        para_end = para_end if para_end > 0 else len(plain)
        stop = re.search(r"\.(?=\s|<sup|&#91;|</p>|$)", plain[text_pos:para_end])
        end = text_pos + stop.end() if stop else para_end
        tail = re.match(r"(?:\s*<sup[^>]*class=\"reference\"[^>]*>.*?</sup>)*", plain[end:], re.S)
        end += tail.end() if tail else 0
        window = plain[start:end]
        cites = re.findall(r'href="#(cite_note-[^"]+)"', window)
        out["sentence"] = re.sub(r"\s*\[\s*\d+\s*\]", "", html_to_text(window)).strip()
        picked = [c for c in dict.fromkeys(cites)]
        out["references"] = [{"id": c, **_ref_item(notes[c])} for c in picked if c in notes][:limit]
        if not out["references"]:
            out["note"] = "no footnote in that sentence: the claim is unreferenced here; find a source elsewhere"
    else:
        out["references"] = [{"id": k, **_ref_item(v)} for k, v in list(notes.items())[:limit]]
    return out


# ---------------------------------------------------------------- places

def place_search(name, src="auto", year=None, limit=5):
    results, errors = [], []
    srcs = ["pleiades", "chgis", "whg", "wikidata"] if src == "auto" else [src]
    if src == "auto" and not re.search(r"[㐀-鿿]", name):
        srcs.remove("chgis")
    if src == "auto" and not get_key("whg"):
        srcs.remove("whg")
    for s in srcs:
        try:
            got = PLACE_SOURCES[s](name, year, limit)
            results.extend(got)
        except Exception as e:  # one gazetteer failing must not hide the others
            errors.append("%s: %s" % (s, e))
    return {"ok": bool(results), "query": name, "year": year, "sources": srcs, "results": results,
            "errors": errors, "note": "coordinates are [lon, lat]"}


def _pleiades(name, year, limit):
    r = fetch("https://pleiades.stoa.org/search_rss?" + qs({"SearchableText": name, "portal_type": "Place"}),
              accept="application/rss+xml")
    if not r.ok:
        raise RuntimeError(r.error or "HTTP %s" % r.status)
    ids = re.findall(r'rdf:resource="https://pleiades.stoa.org/places/(\d+)"', r.text())[:limit]
    out = []
    for pid in ids:
        out.append(pleiades_place(pid))
    return out


def pleiades_place(pid):
    data, r = get_json("https://pleiades.stoa.org/places/%s/json" % pid)
    if data is None:
        return {"source": "pleiades", "id": pid, "error": r.error}
    names = [n.get("romanized") or n.get("attested") for n in data.get("names", [])][:6]
    periods = sorted({p for loc in data.get("locations", []) for p in
                      [a.get("timePeriod") for a in loc.get("attestations", [])] if p})
    return {"source": "pleiades", "id": pid, "name": data.get("title"), "names": names,
            "coord": data.get("reprPoint"), "types": data.get("placeTypes"), "periods": periods[:8],
            "description": data.get("description"), "url": "https://pleiades.stoa.org/places/%s" % pid,
            "licence": "CC BY 3.0 (Pleiades)"}


def _chgis(name, year, limit):
    data, r = get_json("https://chgis.hudci.org/tgaz/placename?" + qs({"n": name, "yr": year, "fmt": "json"}))
    if data is None:
        raise RuntimeError(r.error or "HTTP %s" % r.status)
    out = []
    for p in data.get("placenames", [])[:limit]:
        xy = p.get("xy coordinates")
        coord = [float(x) for x in xy.split(",")] if xy and "," in xy else None
        out.append({"source": "chgis", "id": p.get("sys_id"), "name": p.get("name"),
                    "transcription": p.get("transcription"), "years": p.get("years"), "coord": coord,
                    "parent": p.get("parent name"), "type": p.get("feature type"), "url": p.get("uri"),
                    "licence": "CHGIS terms (not redistributable); cite and link"})
    return out


def _whg(name, year, limit):
    tok = get_key("whg")
    if not tok:
        raise RuntimeError("no WHG token (hw.py keys whg)")
    data, r = get_json("https://whgazetteer.org/suggest/entity?" + qs({"prefix": name}),
                       headers={"Authorization": "Bearer " + tok})
    if data is None:
        raise RuntimeError(r.error or "HTTP %s" % r.status)
    out = []
    for p in data.get("result", [])[:limit]:
        out.append({"source": "whg", "id": p.get("id"), "name": p.get("name"), "names": p.get("alt_names", [])[:6],
                    "coord": p.get("repr_point"), "countries": p.get("ccodes"),
                    "types": [t.get("label") for t in p.get("place_types", [])],
                    "url": "https://whgazetteer.org/", "licence": "per contributing dataset"})
    return out


def _wikidata_place(name, year, limit):
    found = wd_search(name, limit=limit)
    out = []
    for x in found.get("results", [])[:limit]:
        c = wd_claims(x["qid"], ["P625"])
        coords = [st["value"].get("coord") for st in c.get("claims", {}).get("P625", [])]
        if coords:
            out.append({"source": "wikidata", "id": x["qid"], "name": x["label"], "description": x["description"],
                        "coord": coords[0], "url": "https://www.wikidata.org/wiki/%s" % x["qid"], "licence": "CC0"})
    return out


def _ohm_year(value):
    """The astronomical year at the start of an OHM date (ISO 8601: 0000 = 1 BC, -0043 = 44 BC)."""
    m = re.match(r"^\s*(-?\d{1,4})", value or "")
    return int(m.group(1)) if m else None


def _ohm(name, year, limit):
    """OpenHistoricalMap through its Overpass API: exact name matches only (no regex scans), one attempt; OHM
    publishes no limit, so the registry pace and Overpass's own rule after a 429 (wait 30 s) apply (R-20261018-3)."""
    esc = name.replace("\\", "\\\\").replace('"', '\\"')
    q = '[out:json][timeout:25];(nwr["name"="%s"];nwr["name:en"="%s"];);out tags center 60;' % (esc, esc)
    r = fetch("https://overpass-api.openhistoricalmap.org/api/interpreter?" + qs({"data": q}), retries=0, timeout=40)
    if r.status == 429:
        raise RuntimeError("OHM Overpass is busy (429): wait at least 30 s before another query")
    if not r.ok:
        raise RuntimeError(r.error or "HTTP %s" % r.status)
    try:
        elements = r.json().get("elements", [])
    except ValueError:
        raise RuntimeError("OHM answered something other than JSON")
    astro = None if year is None else (year + 1 if year < 0 else year)
    out = []
    for el in elements:
        t = el.get("tags", {})
        start, end = _ohm_year(t.get("start_date")), _ohm_year(t.get("end_date"))
        if astro is not None and ((start is not None and start > astro) or (end is not None and end < astro)):
            continue
        c = el.get("center") or el
        kind = next(("%s=%s" % (k, t[k]) for k in ("boundary", "place", "admin_level", "historic", "building",
                                                   "amenity", "landuse", "type") if k in t), None)
        out.append({"source": "ohm", "id": "%s/%s" % (el.get("type"), el.get("id")), "name": t.get("name"),
                    "name_en": t.get("name:en"), "start_date": t.get("start_date"), "end_date": t.get("end_date"),
                    "kind": kind, "wikidata": t.get("wikidata"),
                    "coord": [c["lon"], c["lat"]] if "lon" in c and "lat" in c else None,
                    "url": "https://www.openhistoricalmap.org/%s/%s" % (el.get("type"), el.get("id")),
                    "licence": t.get("license") or "CC0 (OpenHistoricalMap; a license tag on a feature overrides)"})
        if len(out) >= limit:
            break
    return out


PLACE_SOURCES = {"pleiades": _pleiades, "chgis": _chgis, "whg": _whg, "wikidata": _wikidata_place, "ohm": _ohm}


# ---------------------------------------------------------------- scholarship

def oa_search(query, page=1, per_page=10, filters=None):
    key = get_key("openalex")
    if page > 1 and not key:
        return {"ok": False, "error": "OpenAlex needs a free key to page past page 1 (hw.py keys openalex)"}
    params = {"search": query, "per-page": per_page, "page": page, "filter": filters,
              "select": "id,doi,title,publication_year,authorships,primary_location,cited_by_count,open_access,type"}
    data, r = get_json("https://api.openalex.org/works?" + qs(params),
                       headers={"Authorization": "Bearer " + key} if key else None)
    if data is None:
        return {"ok": False, "error": r.error, "status": r.status, "body": r.text()[:200]}
    works = []
    for w in data.get("results", []):
        works.append({"id": w.get("id"), "title": w.get("title"), "year": w.get("publication_year"),
                      "doi": w.get("doi"), "type": w.get("type"), "cited_by": w.get("cited_by_count"),
                      "authors": [dig(a, "author.display_name") for a in w.get("authorships", [])][:6],
                      "venue": dig(w, "primary_location.source.display_name"),
                      "oa_url": dig(w, "open_access.oa_url")})
    return {"ok": True, "api": "openalex", "keyed": bool(key), "count": dig(data, "meta.count"), "page": page,
            "works": works}


def _sim(a, b):
    ta = set(re.findall(r"\w+", (a or "").casefold()))
    tb = set(re.findall(r"\w+", (b or "").casefold()))
    return round(len(ta & tb) / max(1, len(ta | tb)), 2)


def doi_lookup(doi, title=None, author=None, year=None):
    """Crossref first, OpenAlex second; with title/author/year, say whether all three match (R-20261017-15)."""
    doi = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", doi.strip(), flags=re.I)
    from hw_net import contact
    params = {"mailto": contact()} if contact() else {}
    data, r = get_json("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/") +
                       ("?" + qs(params) if params else ""))
    rec = None
    if data and data.get("message"):
        m = data["message"]
        rec = {"source": "crossref", "doi": doi, "title": (m.get("title") or [None])[0],
               "authors": ["%s %s" % (a.get("given", ""), a.get("family", "")) for a in m.get("author", [])][:8],
               "year": (dig(m, "issued.date-parts.0.0")), "container": (m.get("container-title") or [None])[0],
               "type": m.get("type"), "url": m.get("URL")}
    else:
        d2, r2 = get_json("https://api.openalex.org/works/doi:" + doi)
        if d2:
            rec = {"source": "openalex", "doi": doi, "title": d2.get("title"),
                   "authors": [dig(a, "author.display_name") for a in d2.get("authorships", [])][:8],
                   "year": d2.get("publication_year"), "container": dig(d2, "primary_location.source.display_name"),
                   "type": d2.get("type"), "url": d2.get("doi")}
    if not rec:
        return {"ok": False, "exists": False, "doi": doi, "error": "DOI not found in Crossref or OpenAlex",
                "status": r.status}
    out = {"ok": True, "exists": True, "record": rec}
    if title or author or year:
        out.update(match_record(rec, title, author, year))
    return out


def match_record(rec, title=None, author=None, year=None):
    """Compare a registry record with the cited title, author and year. Only the year off is not a blend:
    registries hold wrong years (Crossref gives 1970 for Falk and Bennett, Acta Orientalia 70, 2009)."""
    checks = {}
    if title:
        checks["title"] = _sim(title, rec["title"]) >= 0.6
    if author:
        checks["author"] = any(author.casefold() in (a or "").casefold() for a in rec["authors"])
    if year:
        checks["year"] = str(year) == str(rec["year"])
    out = {"match": checks, "all_match": all(checks.values())}
    if out["all_match"]:
        return out
    if checks.get("year") is False and checks.get("title") and checks.get("author"):
        out["warning"] = ("only the year differs: registry records sometimes carry a wrong year; check the year "
                          "printed on the work itself (masthead, title page) before calling it a wrong reference")
    else:
        out["warning"] = "the DOI exists but does not match every detail given: a blended or wrong reference"
    return out


# ---------------------------------------------------------------- generic registry search

def src_search(sid, query, limit=10, detail=0):
    s = source(sid)
    if not s:
        return {"ok": False, "error": "no source %r in the registry (hw.py lint lists ids)" % sid}
    if s.get("route") == "link-out" or not s.get("search"):
        return {"ok": False, "error": "%s is link-out only (%s); open %s yourself or ask the user" %
                (s["name"], s.get("access"), s.get("url")), "url": s.get("url")}
    sp = s["search"]
    key = get_key(s["key"]) if s.get("key") else None
    if s.get("key") and not key and "{key}" in sp["url"] and not sp.get("demo_key"):
        return {"ok": False, "error": "%s needs a free key (%s); see hw.py keys status" % (s["name"], s["key"])}
    url = sp["url"].replace("{q}", urllib.parse.quote(query)).replace("{key}", key or sp.get("demo_key", ""))
    url = url.replace("{limit}", str(limit))
    headers = dict(sp.get("headers") or {})
    if s.get("ua") == "plain":  # SEC refuses library-style agents and wants "name email"
        headers["User-Agent"] = ("historywright " + contact()).strip()
    data, r = get_json(url, headers=headers or None)
    if data is None:
        return {"ok": False, "error": r.error or "HTTP %s" % r.status, "status": r.status, "url": redact(url)}
    items = as_list(dig(data, sp.get("items")))[int(sp.get("skip") or 0):][:limit]
    fields = sp.get("fields") or {}
    rows = [{k: dig(it, p) for k, p in fields.items()} if fields else it for it in items]
    det = s.get("detail")
    if det and detail:
        for row, it in list(zip(rows, items))[:detail]:
            ident = row.get(det.get("id_field", "id")) if isinstance(row, dict) else it
            d2, r2 = get_json(det["url"].replace("{id}", urllib.parse.quote(str(ident))).replace("{key}", key or ""),
                              headers=headers or None)
            if d2 is not None:
                rec = dig(d2, det.get("items"))
                row.update({k: dig(rec, p) for k, p in det.get("fields", {}).items()})
            else:
                row["detail_error"] = r2.error
    if sp.get("link"):
        for row in rows:
            if isinstance(row, dict):
                try:
                    link = sp["link"].format(**{k: ("" if v is None else v) for k, v in row.items()})
                except (KeyError, IndexError, ValueError):
                    continue
                row.setdefault("link", link)
                if not row.get("url"):
                    row["url"] = link
    return {"ok": True, "source": sid, "name": s["name"], "tier": s.get("tier"), "licence": s.get("licence"),
            "url": redact(url), "count": len(rows), "results": rows,
            "mirror_warning": [row.get("url") for row in rows if isinstance(row, dict) and isinstance(row.get("url"), str)
                               and is_mirror(row["url"])] or None}


def registry_sources():
    return registry().get("sources", [])
