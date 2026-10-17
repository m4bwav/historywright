"""Checks for hw.py: citation verification, the research pack contract, and the answer cache.

The guards come from the creation pass: cite only what the run fetched and read (R-20261017-15), a quote must be a
real span of the fetched page (R-20261017-16), Wikipedia agreement is not independence (R-20261017-17), URL health
labels (R-20261017-23), and the pack rules in R-20261017-24 (RFC 7946, EDTF, QIDs, licences).
"""

import hashlib
import json
import re
import time
import urllib.parse
from pathlib import Path

import hw_dates as D
from hw_net import (write_text, decode_body, VERSION,fetch, fetched_urls, get_json, home, html_to_text, is_mirror, normalise,
                    stored_page, today)

PACK_FILES = ["manifest.json", "answer.md", "sources.json", "entities.json", "places.geojson", "timeline.json",
              "refs/index.json", "anachronism.md"]
OPEN_LICENCES = re.compile(r"(?i)^(cc0|public domain|pd|pdm|cc[- ]by(?![- ]?nc)[- \w.]*|ogl[\w .-]*|no known copyright)")
NC_LICENCES = re.compile(r"(?i)(nc|non-?commercial)")
KINDS = {"primary", "secondary", "tertiary", "structured"}


# ---------------------------------------------------------------- URL health

def url_health(url):
    """live, dead, likely_hallucinated or unknown: HEAD, then GET, then the Wayback Machine (arXiv 2604.03173)."""
    r = fetch(url, method="HEAD", accept="*/*", retries=0, log=False)
    if r.status in (405, 403, 400, 501) or r.status is None or (r.status and r.status >= 500):
        r = fetch(url, accept="text/html,*/*", retries=0)
    if r.ok or (r.status and 300 <= r.status < 400):
        return {"url": url, "label": "live", "status": r.status}
    if r.status in (401, 403, 429):
        return {"url": url, "label": "unknown", "status": r.status, "why": "blocked or rate-limited, not proof of absence"}
    wb, wr = get_json("https://archive.org/wayback/available?" + urllib.parse.urlencode({"url": url}))
    snap = (wb or {}).get("archived_snapshots", {}).get("closest") if wb else None
    if wb is None:
        return {"url": url, "label": "unknown", "status": r.status, "why": "Wayback check failed (%s)" % (wr.error or wr.status)}
    if snap:
        return {"url": url, "label": "dead", "status": r.status, "archived": snap.get("url"), "archived_at": snap.get("timestamp")}
    if r.status == 404 or r.status is None:
        return {"url": url, "label": "likely_hallucinated", "status": r.status,
                "why": "no live page and no archived copy"}
    return {"url": url, "label": "unknown", "status": r.status}


# ---------------------------------------------------------------- quotes

def page_text(url, refetch=False):
    body = None if refetch else stored_page(url)
    fetched, ctype = False, ""
    if body is None:
        r = fetch(url, accept="text/html,application/xhtml+xml,application/json,text/plain,*/*")
        if not r.ok:
            return None, "fetch failed: %s" % (r.error or r.status)
        body, fetched, ctype = r.body, True, r.headers.get("content-type", "")
    text = decode_body(body, ctype)
    if "<" in text[:2000] and re.search(r"(?i)<(html|body|div|p)\b", text[:5000]):
        text = html_to_text(text)
    return text, ("fetched now" if fetched else "from this run's page store")


def quote_in(quote, text):
    """Exact, then normalised (case, quotes, dashes, spaces); '...' splits a quote into parts found in order."""
    if quote in text:
        return {"found": True, "match": "exact"}
    nt = normalise(text)
    parts = [normalise(p) for p in re.split(r"\s*(?:\.\.\.|…|\[\.\.\.\])\s*", quote) if p.strip()]
    pos = 0
    for p in parts:
        i = nt.find(p, pos)
        if i < 0:
            near = _closest(p, nt)
            return {"found": False, "missing_part": p[:120], "closest": near}
        pos = i + len(p)
    return {"found": True, "match": "normalised" if len(parts) == 1 else "normalised, in parts"}


def _closest(part, text):
    words = part.split()
    if len(words) < 3:
        return None
    probe = " ".join(words[:3])
    i = text.find(probe)
    return text[max(0, i - 40): i + len(part) + 40] if i >= 0 else None


def verify_quote(url, quote, refetch=False):
    text, how = page_text(url, refetch)
    if text is None:
        return {"ok": False, "url": url, "found": None, "error": how}
    res = quote_in(quote, text)
    res.update(ok=res["found"], url=url, source_text=how)
    return res


# ---------------------------------------------------------------- QIDs

def verify_qid(qid, label=None):
    from hw_sources import wd_entity
    if not re.fullmatch(r"Q\d+", qid or ""):
        return {"ok": False, "qid": qid, "error": "not a QID"}
    e = wd_entity(qid)
    if not e.get("ok"):
        return {"ok": False, "qid": qid, "exists": e.get("exists", None), "error": e.get("error")}
    out = {"ok": True, "qid": qid, "exists": True, "label": e.get("label")}
    if label:
        names = [e.get("label") or ""] + e.get("aliases", [])
        out["label_match"] = any(normalise(label) == normalise(n) or normalise(label) in normalise(n) for n in names)
        out["ok"] = out["label_match"]
    return out


# ---------------------------------------------------------------- sources.json

def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def check_sources(doc, network=True, require_fetched=True):
    """Every claim's quote is in its fetched page; corroboration counts independent, non-mirror sources."""
    problems, warnings, checked = [], [], []
    srcs = doc.get("sources") if isinstance(doc, dict) else None
    if not isinstance(srcs, list) or not srcs:
        return {"ok": False, "problems": ["sources.json needs a non-empty 'sources' list"]}
    ids = set()
    seen = fetched_urls() if require_fetched else set()
    for s in srcs:
        sid = s.get("id")
        if not sid:
            problems.append("a source has no id")
            continue
        if sid in ids:
            problems.append("duplicate source id %s" % sid)
        ids.add(sid)
        for k in ("title", "url", "retrieved", "kind", "tier"):
            if not s.get(k):
                problems.append("%s: missing %s" % (sid, k))
        if s.get("kind") and s["kind"] not in KINDS:
            problems.append("%s: kind must be one of %s" % (sid, ", ".join(sorted(KINDS))))
        url = s.get("url") or ""
        s_mirror = is_mirror(url)
        if s_mirror and s.get("kind") != "tertiary":
            problems.append("%s: %s is Wikipedia or a mirror; mark it tertiary and cite the source beneath it" % (sid, url))
        if require_fetched and url and url not in seen and not s.get("offline"):
            problems.append("%s: %s was not fetched in this run (fetch-log); cite only what was read" % (sid, url))
        for c in s.get("claims", []):
            if not c.get("claim"):
                problems.append("%s: a claim without text" % sid)
            q = c.get("quote")
            if not q:
                problems.append("%s: claim %r has no supporting quote" % (sid, (c.get("claim") or "")[:60]))
                continue
            if network and url:
                res = verify_quote(url, q)
                checked.append({"source": sid, "claim": c.get("claim", "")[:80], "found": res.get("found"),
                                "match": res.get("match"), "error": res.get("error")})
                if res.get("found") is False:
                    problems.append("%s: quote not found in %s: %r" % (sid, url, q[:80]))
                elif res.get("found") is None:
                    warnings.append("%s: could not re-read %s (%s)" % (sid, url, res.get("error")))
        if s.get("doi") and network:
            from hw_sources import doi_lookup
            first = re.split(r"[;,]", s.get("author") or "")[0].split()
            d = doi_lookup(s["doi"], s.get("title"), first[-1] if first else None, s.get("year"))
            if not d.get("exists"):
                problems.append("%s: DOI %s does not resolve" % (sid, s["doi"]))
            elif d.get("all_match") is False:
                problems.append("%s: DOI %s exists but title/author/year do not all match" % (sid, s["doi"]))
    for s in srcs:
        for d in s.get("derived_from") or []:
            if d not in ids and not re.match(r"https?://", str(d)):
                warnings.append("%s: derived_from %s is not a source id or URL" % (s.get("id"), d))
    indep = independent_set(srcs)
    strong = [s for s in indep if s.get("tier") == 1 or s.get("kind") in ("primary", "secondary")]
    corroborated = len(indep) >= 2 and len(strong) >= 1
    if not corroborated:
        warnings.append("not corroborated: %d independent non-mirror source(s), %d primary or scholarly; "
                        "the answer must say unverified" % (len(indep), len(strong)))
    return {"ok": not problems, "problems": problems, "warnings": warnings, "quote_checks": checked,
            "independent_sources": [s.get("id") for s in indep], "corroborated": corroborated}


def independent_set(srcs):
    """Sources that are not mirrors and share no derived_from with each other (R-20261017-17)."""
    pool = [s for s in srcs if not is_mirror(s.get("url") or "") and s.get("kind") != "tertiary"]
    chosen, roots = [], set()
    for s in sorted(pool, key=lambda s: (s.get("tier") or 9)):
        r = set(s.get("derived_from") or []) | {s.get("id")}
        if r & roots:
            continue
        if any(s.get("id") in (c.get("derived_from") or []) for c in chosen):
            continue
        chosen.append(s)
        roots |= r
    return chosen


# ---------------------------------------------------------------- the pack

def _geo_problems(gj):
    probs, warns = [], []
    if not isinstance(gj, dict) or gj.get("type") != "FeatureCollection":
        return ["places.geojson must be a FeatureCollection"], warns
    if "crs" in gj:
        probs.append("places.geojson has a 'crs' member (RFC 7946 removed it; coordinates are WGS 84 [lon, lat])")

    def pos_ok(p, where):
        if not (isinstance(p, list) and len(p) >= 2 and all(isinstance(x, (int, float)) for x in p[:2])):
            probs.append("%s: a position must be [lon, lat]" % where)
            return
        lon, lat = p[0], p[1]
        if not -90 <= lat <= 90:
            probs.append("%s: latitude %s out of range (lon and lat swapped?)" % (where, lat))
        if not -180 <= lon <= 180:
            probs.append("%s: longitude %s out of range" % (where, lon))

    for i, f in enumerate(gj.get("features", [])):
        where = "feature %d (%s)" % (i, (f.get("properties") or {}).get("name", "?"))
        g = f.get("geometry")
        if f.get("type") != "Feature":
            probs.append("%s: type must be Feature" % where)
        if not g:
            continue
        t, c = g.get("type"), g.get("coordinates")
        if t == "Point":
            pos_ok(c, where)
        elif t in ("LineString", "MultiPoint"):
            for p in c or []:
                pos_ok(p, where)
        elif t in ("Polygon", "MultiPolygon"):
            polys = [c] if t == "Polygon" else (c or [])
            for poly in polys:
                for ring in poly or []:
                    if len(ring) < 4:
                        probs.append("%s: a ring needs at least four positions" % where)
                    elif ring[0] != ring[-1]:
                        probs.append("%s: ring not closed (first and last positions differ)" % where)
                    for p in ring:
                        pos_ok(p, where)
        props = f.get("properties") or {}
        for k in ("name", "source"):
            if not props.get(k):
                warns.append("%s: properties.%s missing" % (where, k))
        exp = props.get("expected_coord")
        if exp and t == "Point" and c and abs(c[0] - exp[1]) < 1e-6 and abs(c[1] - exp[0]) < 1e-6:
            probs.append("%s: coordinates are swapped relative to expected_coord" % where)
    return probs, warns


def _date_obj_problems(d, where):
    p = []
    if not isinstance(d, dict):
        return ["%s: a date must be an object" % where]
    for k in ("as_written", "calendar", "edtf", "precision", "sources"):
        if k not in d:
            p.append("%s: date missing %s" % (where, k))
    if d.get("edtf") and not D.edtf_valid(d["edtf"]):
        p.append("%s: %r is not EDTF level 0/1 (or a level 2 set)" % (where, d["edtf"]))
    j = d.get("jdn")
    if j is not None and not (isinstance(j, list) and len(j) == 2 and all(isinstance(x, int) for x in j) and j[0] <= j[1]):
        p.append("%s: jdn must be [first, last] integers" % where)
    if d.get("qualifier") == "disputed" and d.get("edtf") and not re.search(r"[\[\]{}/]", d["edtf"]):
        p.append("%s: a disputed date is a set or a range, never a point" % where)
    return p


def validate_pack(path, network=False):
    root = Path(path)
    probs, warns = [], []
    if not root.is_dir():
        return {"ok": False, "problems": ["%s is not a folder" % path]}
    for f in PACK_FILES:
        if not (root / f).exists():
            probs.append("missing %s" % f)
    def jl(name):
        try:
            return load_json(root / name)
        except FileNotFoundError:
            return None
        except ValueError as e:
            probs.append("%s is not valid JSON: %s" % (name, e))
            return None
    man = jl("manifest.json") or {}
    hw = man.get("historywright") or {}
    for k in ("name", "kind", "route", "targets", "sources", "outputs"):
        if k not in man:
            probs.append("manifest.json missing %s (polywright asset contract)" % k)
    if not hw.get("question"):
        probs.append("manifest.json historywright.question missing")
    comp = hw.get("completeness") or []
    if not comp:
        probs.append("manifest.json historywright.completeness missing: list each part present or empty with a reason")
    for c in comp:
        if c.get("status") == "empty" and not c.get("reason"):
            probs.append("completeness: %s is empty without a reason" % c.get("item"))
    ans = (root / "answer.md").read_text(encoding="utf-8") if (root / "answer.md").exists() else ""
    if ans:
        if not re.search(r"(?im)^\**confidence\**\s*:", ans):
            probs.append("answer.md has no 'Confidence:' line")
        if not re.search(r"(?i)sources (disagree|agree)", ans):
            probs.append("answer.md has no 'Sources disagree' / 'Sources agree' note")
        if not re.search(r"(?i)AI[- ]researched", ans):
            probs.append("answer.md does not say it was AI-researched")
    src = jl("sources.json")
    if src is not None:
        res = check_sources(src, network=network, require_fetched=False)
        probs += res["problems"]
        warns += res["warnings"]
        src_ids = {s.get("id") for s in src.get("sources", [])}
    else:
        src_ids = set()
    ents = jl("entities.json")
    if ents is not None:
        for e in ents.get("entities", []):
            w = "entity %s" % (e.get("label") or e.get("qid"))
            if e.get("qid") and not re.fullmatch(r"Q\d+", e["qid"]):
                probs.append("%s: %r is not a QID" % (w, e["qid"]))
            for dk, dv in (e.get("dates") or {}).items():
                probs += _date_obj_problems(dv, "%s %s" % (w, dk))
                for sref in (dv.get("sources") or []) if isinstance(dv, dict) else []:
                    if sref not in src_ids:
                        probs.append("%s %s: source %s not in sources.json" % (w, dk, sref))
            c = e.get("coord")
            if c is not None and not (isinstance(c, list) and len(c) == 2 and -90 <= c[1] <= 90 and -180 <= c[0] <= 180):
                probs.append("%s: coord must be [lon, lat]" % w)
    gj = jl("places.geojson")
    if gj is not None:
        gp, gw = _geo_problems(gj)
        probs += gp
        warns += gw
    tl = jl("timeline.json")
    if tl is not None:
        for i, row in enumerate(tl.get("rows", [])):
            w = "timeline row %d" % i
            for k in ("when", "event", "source", "sentence", "jdn"):
                if not row.get(k):
                    probs.append("%s: missing %s" % (w, k))
            if row.get("when") and not D.edtf_valid(row["when"]):
                probs.append("%s: %r is not EDTF" % (w, row["when"]))
            if row.get("source") and row["source"] not in src_ids:
                probs.append("%s: source %s not in sources.json" % (w, row["source"]))
            j = row.get("jdn")
            if j is not None and not (isinstance(j, list) and len(j) == 2 and j[0] <= j[1]):
                probs.append("%s: jdn must be a [first, last] range" % w)
    refs = jl("refs/index.json")
    if refs is not None:
        commercial = bool(hw.get("commercial"))
        for r in refs.get("refs", []):
            w = "ref %s" % (r.get("file") or r.get("title"))
            for k in ("title", "licence", "url", "object_date", "place", "accession", "institution", "retrieved"):
                if not r.get(k):
                    probs.append("%s: missing %s" % (w, k))
            lic = r.get("licence") or ""
            if lic and not OPEN_LICENCES.search(lic) and not NC_LICENCES.search(lic):
                warns.append("%s: licence %r is neither open nor flagged non-commercial; check it" % (w, lic))
            if NC_LICENCES.search(lic):
                if not r.get("nc"):
                    probs.append("%s: non-commercial licence without nc: true" % w)
                if commercial:
                    probs.append("%s: non-commercial image in a pack marked commercial" % w)
            if r.get("file") and not (root / r["file"]).exists():
                probs.append("%s: file missing" % w)
            elif r.get("file") and r.get("sha256") and _sha(root / r["file"]) != r["sha256"]:
                probs.append("%s: file changed since it was recorded" % w)
            if r.get("generated"):
                probs.append("%s: generated images are not references (label them reconstructions elsewhere)" % w)
    if (root / "anachronism.md").exists():
        a = (root / "anachronism.md").read_text(encoding="utf-8")
        if len(re.findall(r"(?m)^\s*[-*] ", a)) < 3:
            probs.append("anachronism.md needs a checklist of at least three items")
    return {"ok": not probs, "pack": str(root), "problems": probs, "warnings": warns}


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


TEMPLATES = {
    "answer.md": "# {question}\n\n<answer with inline citations [s1]>\n\nConfidence: <high|medium|low>: <what is "
                 "uncertain and why>\n\nSources agree.  <or: Sources disagree (outdated source | frame | scholarly "
                 "dispute): ...>\n\n## Sources\n\n- [s1] ...\n\nAI-researched with historywright {version}; every "
                 "source above was fetched and read on {date}.\n",
    "sources.json": {"sources": []},
    "entities.json": {"entities": []},
    "places.geojson": {"type": "FeatureCollection", "features": []},
    "timeline.json": {"rows": []},
    "refs/index.json": {"refs": []},
    "anachronism.md": "# Anachronism checklist: {period}\n\nEach item cites its source.\n\n- \n- \n- \n",
}


def pack_init(path, question, name=None, period=None, commercial=False):
    root = Path(path)
    (root / "refs").mkdir(parents=True, exist_ok=True)
    made = []
    for f, t in TEMPLATES.items():
        p = root / f
        if p.exists():
            continue
        if isinstance(t, str):
            write_text(p, t.format(question=question, version=VERSION, date=today(), period=period or "?"))
        else:
            write_text(p, json.dumps(t, indent=1) + "\n")
        made.append(f)
    mp = root / "manifest.json"
    if not mp.exists():
        man = {"polywright": "1", "name": name or root.name, "kind": "real", "route": "found", "brief": question,
               "targets": [], "units": "m", "sources": [], "tools": [{"name": "historywright", "version": VERSION}],
               "outputs": [], "reviews": [], "status": "references",
               "historywright": {"version": "1", "question": question, "period": period, "commercial": commercial,
                                 "created": today(), "completeness": []}}
        write_text(mp, json.dumps(man, indent=1, ensure_ascii=False) + "\n")
        made.append("manifest.json")
    return {"ok": True, "pack": str(root), "created": made}


def pack_add_ref(path, image_url, page_url, title, licence, object_date, place, accession, institution,
                 author=None, nc=None):
    root = Path(path)
    r = fetch(image_url, accept="image/*,*/*")
    if not r.ok:
        return {"ok": False, "error": "image fetch failed: %s" % (r.error or r.status)}
    ext = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp", "image/tiff": ".tif",
           "image/gif": ".gif"}.get(r.headers.get("content-type", "").split(";")[0], ".jpg")
    slug = re.sub(r"[^a-z0-9]+", "-", ("%s %s" % (institution, accession)).lower()).strip("-")[:60] or "ref"
    rel = "refs/%s%s" % (slug, ext)
    (root / rel).write_bytes(r.body)
    is_nc = bool(NC_LICENCES.search(licence or "")) if nc is None else nc
    entry = {"file": rel, "title": title, "object_date": object_date, "place": place, "accession": accession,
             "institution": institution, "url": page_url, "image_url": image_url, "licence": licence,
             "author": author, "nc": is_nc, "retrieved": today(), "sha256": _sha(root / rel), "bytes": len(r.body)}
    ip = root / "refs" / "index.json"
    idx = load_json(ip) if ip.exists() else {"refs": []}
    idx["refs"] = [x for x in idx["refs"] if x.get("file") != rel] + [entry]
    write_text(ip, json.dumps(idx, indent=1, ensure_ascii=False) + "\n")
    mp = root / "manifest.json"
    if mp.exists():
        man = load_json(mp)
        man.setdefault("sources", [])
        man["sources"] = [s for s in man["sources"] if s.get("url") != page_url] + [
            {"what": "reference image: %s (%s, %s)" % (title, institution, accession), "url": page_url,
             "author": author or institution, "licence": licence, "retrieved": today(), "file": rel}]
        write_text(mp, json.dumps(man, indent=1, ensure_ascii=False) + "\n")
    return {"ok": True, "ref": entry}


def pack_csl(path):
    """sources.json as CSL-JSON, which Zotero and most reference managers import."""
    src = load_json(Path(path) / "sources.json")
    items = []
    for s in src.get("sources", []):
        it = {"id": s.get("id"), "type": {"primary": "manuscript", "secondary": "book", "tertiary": "entry-encyclopedia",
                                           "structured": "dataset"}.get(s.get("kind"), "webpage"),
              "title": s.get("title"), "URL": s.get("url"), "DOI": s.get("doi"),
              "accessed": {"date-parts": [[int(x) for x in (s.get("retrieved") or today()).split("-")]]}}
        if s.get("author"):
            it["author"] = [{"literal": a.strip()} for a in s["author"].split(";")]
        if s.get("year"):
            it["issued"] = {"date-parts": [[int(s["year"])]]}
        items.append({k: v for k, v in it.items() if v})
    out = Path(path) / "sources.csl.json"
    write_text(out, json.dumps(items, indent=1, ensure_ascii=False) + "\n")
    return {"ok": True, "file": str(out), "items": len(items)}


# ---------------------------------------------------------------- cache

def _key(q):
    stop = {"the", "a", "an", "of", "in", "was", "is", "who", "what", "when", "did", "and", "with", "whom", "for", "to"}
    return sorted({w for w in re.findall(r"\w+", q.casefold()) if w not in stop})


def cache_dir():
    d = home() / "cache"
    d.mkdir(exist_ok=True)
    return d


def cache_put(entry):
    for k in ("question", "answer", "sources"):
        if not entry.get(k):
            return {"ok": False, "error": "a cache entry needs %s" % k}
    for s in entry["sources"]:
        if not (s.get("url") and s.get("retrieved")):
            return {"ok": False, "error": "every cached source needs url and retrieved"}
    entry = dict(entry)
    entry.setdefault("cached", today())
    entry["hw_version"] = VERSION
    entry["key"] = _key(entry["question"])
    slug = re.sub(r"[^a-z0-9]+", "-", entry["question"].lower()).strip("-")[:70]
    p = cache_dir() / (slug + ".json")
    write_text(p, json.dumps(entry, indent=1, ensure_ascii=False) + "\n")
    return {"ok": True, "file": str(p)}


def cache_get(question, max_age_days=None):
    want = set(_key(question))
    hits = []
    for p in cache_dir().glob("*.json"):
        try:
            e = load_json(p)
        except ValueError:
            continue
        have = set(e.get("key", []))
        score = len(want & have) / max(1, len(want | have))
        if score >= 0.5:
            age = (time.time() - p.stat().st_mtime) / 86400
            if max_age_days is None or age <= max_age_days:
                hits.append({"score": round(score, 2), "file": str(p), "question": e.get("question"),
                             "cached": e.get("cached"), "age_days": round(age, 1), "answer": e.get("answer"),
                             "confidence": e.get("confidence"), "sources": e.get("sources")})
    hits.sort(key=lambda h: -h["score"])
    return {"ok": True, "hits": hits[:3],
            "note": "a hit is a lead, not an answer: re-read at least one source if it is older than 180 days"}


def cache_list():
    rows = []
    for p in sorted(cache_dir().glob("*.json")):
        try:
            e = load_json(p)
            rows.append({"question": e.get("question"), "cached": e.get("cached"), "file": p.name})
        except ValueError:
            pass
    return {"ok": True, "count": len(rows), "entries": rows}
