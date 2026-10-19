"""Shared layer for hw.py: paths, config and keys, the source registry, and one polite HTTP client.

Standard library only. Every request carries a User-Agent that names the tool and a contact, waits out the
per-host pace from the registry, honours Retry-After, and is written to the fetch log so a pack can prove which
pages the run actually read. HW_FIXTURES serves answers from files (tests and evals); HW_RECORD saves them.
"""

import hashlib
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

VERSION = "0.1.0"
REPO = "https://github.com/m4bwav/historywright"
HERE = Path(__file__).resolve().parent
SKILLS = HERE.parent.parent
REGISTRY_PATH = SKILLS / "historywright-sources" / "references" / "registry.json"

# Documented limits, used when the registry has no entry for a host (seconds between requests).
DEFAULT_PACE = {
    "www.wikidata.org": 0.35, "query.wikidata.org": 1.0, "query-scholarly.wikidata.org": 1.0,
    "en.wikipedia.org": 0.35, "commons.wikimedia.org": 0.35,
    "api.openalex.org": 0.2, "api.crossref.org": 0.2, "www.loc.gov": 3.0,
    "whgazetteer.org": 0.2, "pleiades.stoa.org": 1.0, "chgis.hudci.org": 1.0,
    "archive.org": 4.0, "web.archive.org": 4.0, "authority.dila.edu.tw": 1.0,
}
FALLBACK_PACE = 0.5
MAX_RETRY_AFTER = 60


def utf8_stdout():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def write_text(path, text):
    """Write UTF-8 with LF line endings on every OS (Path.write_text writes CRLF on Windows)."""
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def emit(obj, code=0):
    """Print one JSON object and return the exit code (commands return emit(...))."""
    sys.stdout.write(json.dumps(obj, ensure_ascii=False, indent=1) + "\n")
    return code


def fail(msg, **extra):
    d = {"ok": False, "error": msg}
    d.update(extra)
    return emit(d, 1)


def today():
    return time.strftime("%Y-%m-%d")


# ---------------------------------------------------------------- home, config, keys

def home_source():
    """Where answers and fetches live: HW_HOME, else a .historywright folder in the working directory when one
    exists (a project or an eval run keeps its own cache), else ~/.historywright."""
    if os.environ.get("HW_HOME"):
        return "HW_HOME", Path(os.environ["HW_HOME"])
    p = Path.cwd() / ".historywright"
    if p.is_dir():
        return "project", p
    return "user", Path.home() / ".historywright"


def home():
    h = home_source()[1]
    h.mkdir(parents=True, exist_ok=True)
    return h


def user_home():
    """Keys, the DILA table and the pace file: shared by every project, so pacing stays per host (HW_HOME wins)."""
    h = Path(os.environ.get("HW_HOME") or (Path.home() / ".historywright"))
    h.mkdir(parents=True, exist_ok=True)
    return h


def config_path():
    p = home() / "config.json"
    return p if p.exists() else user_home() / "config.json"


def load_config():
    p = config_path()
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_config(cfg):
    p = config_path()
    tmp = p.with_suffix(".tmp")
    write_text(tmp, json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    os.replace(tmp, p)
    try:
        os.chmod(p, 0o600)  # owner only on macOS and Linux; on Windows the profile folder's ACL applies
    except OSError:
        pass
    return p


ENV_KEYS = {"openalex": ("OPENALEX_API_KEY", "api_key"), "whg": ("WHG_TOKEN", "token"),
            "smithsonian": ("SMITHSONIAN_API_KEY", "api_key"), "europeana": ("EUROPEANA_API_KEY", "api_key")}


def get_key(name):
    env, field = ENV_KEYS.get(name, (name.upper() + "_API_KEY", "api_key"))
    if os.environ.get(env):
        return os.environ[env]
    k = load_config().get("keys", {}).get(name, {})
    return k.get(field) or k.get("token") or k.get("api_key")


def contact():
    return os.environ.get("HW_CONTACT") or load_config().get("contact") or ""


def mask(secret):
    if not secret:
        return None
    return "set, ends ..." + secret[-2:] if len(secret) > 8 else "set"


def user_agent():
    c = contact()
    return "historywright/%s (%s%s)" % (VERSION, REPO, "; " + c if c else "")


# ---------------------------------------------------------------- registry

_REGISTRY = None


def registry():
    global _REGISTRY
    if _REGISTRY is None:
        p = Path(os.environ.get("HW_REGISTRY") or REGISTRY_PATH)
        try:
            _REGISTRY = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            _REGISTRY = {"sources": [], "mirrors": []}
    return _REGISTRY


def source(sid):
    for s in registry().get("sources", []):
        if s.get("id") == sid:
            return s
    return None


def pace_for(host):
    for s in registry().get("sources", []):
        if s.get("host") == host and isinstance(s.get("pace_s"), (int, float)):
            return float(s["pace_s"])
    return DEFAULT_PACE.get(host, FALLBACK_PACE)


def mirror_domains():
    base = {"wikipedia.org", "wikiwand.com", "dbpedia.org", "wikizero.com", "infogalactic.com",
            "everybodywiki.com", "kiddle.co", "alchetron.com", "en-academic.com", "wiki2.org",
            "justapedia.org", "encyclopedia2.thefreedictionary.com", "wikimili.com", "dbpedia.org"}
    return sorted(base | set(registry().get("mirrors", [])))


def is_mirror(url):
    host = (urllib.parse.urlparse(url).hostname or "").lower()
    return any(host == d or host.endswith("." + d) for d in mirror_domains())


# ---------------------------------------------------------------- HTTP

def decode_body(body, ctype=""):
    """Charset from the header, else from a <meta> tag, else UTF-8 if it decodes cleanly, else Windows-1252
    (older scholarly sites such as LacusCurtius declare their charset only in the page)."""
    m = re.search(r"charset=[\"']?([\w-]+)", ctype or "")
    if not m:
        m = re.search(rb"<meta[^>]+charset=[\"']?([\w-]+)", body[:4096], re.I)
    enc = (m.group(1).decode("ascii", "ignore") if m and isinstance(m.group(1), bytes) else m.group(1)) if m else None
    if enc:
        try:
            return body.decode(enc, "replace")
        except LookupError:
            pass
    try:
        return body.decode("utf-8")
    except UnicodeDecodeError:
        return body.decode("cp1252", "replace")


class Response:
    def __init__(self, status, headers, body, url, error=None, from_fixture=False):
        self.status, self.headers, self.body, self.url = status, headers or {}, body or b"", url
        self.error, self.from_fixture = error, from_fixture

    @property
    def ok(self):
        return self.status is not None and 200 <= self.status < 300

    def text(self):
        return decode_body(self.body, self.headers.get("content-type", ""))

    def json(self):
        return json.loads(self.text())


def _pace_wait(host):
    """Keep the per-host pace across separate hw.py processes with a small state file."""
    if os.environ.get("HW_FIXTURES"):
        return
    gap = pace_for(host)
    p = user_home() / "pace.json"
    try:
        state = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        state = {}
    last = state.get(host, 0)
    wait = last + gap - time.time()
    if wait > 0:
        time.sleep(min(wait, 30))
    state[host] = time.time()
    try:
        write_text(p, json.dumps(state))
    except OSError:
        pass


def _fixture(url, method):
    d = Path(os.environ["HW_FIXTURES"])
    try:
        index = json.loads((d / "index.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        index = []
    for row in index:
        if row.get("method", "GET") == method and re.search(row["match"], url):
            body = (d / row["file"]).read_bytes() if row.get("file") else row.get("body", "").encode("utf-8")
            return Response(row.get("status", 200), {"content-type": row.get("content_type", "application/json")},
                            body, url, from_fixture=True)
    return Response(None, {}, b"", url, error="no fixture matches " + url, from_fixture=True)


def _record(url, method, resp):
    d = Path(os.environ["HW_RECORD"])
    d.mkdir(parents=True, exist_ok=True)
    name = hashlib.sha1((method + url).encode("utf-8")).hexdigest()[:12] + ".body"
    (d / name).write_bytes(resp.body)
    ip = d / "index.json"
    try:
        index = json.loads(ip.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        index = []
    index.append({"match": record_pattern(url), "method": method, "file": name, "status": resp.status,
                  "content_type": resp.headers.get("content-type", "")})
    write_text(ip, json.dumps(index, indent=1) + "\n")


_SECRET_PARAM = re.compile(r"(?i)([?&](?:api_key|apikey|wskey|key|token|access_token)=)[^&#]+")


def redact(url):
    """Hide key and token query values so logs and outputs never carry them."""
    return _SECRET_PARAM.sub(r"\1***", url)


def record_pattern(url):
    """The fixture pattern for a recorded URL: key and token values match anything, so no key is written down."""
    return "^" + re.escape(redact(url)).replace(re.escape("***"), "[^&#]+") + "$"


def _log(url, method, resp):
    row = {"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "method": method, "url": redact(url), "status": resp.status,
           "bytes": len(resp.body), "sha256": hashlib.sha256(resp.body).hexdigest()[:16] if resp.body else None}
    if resp.error:
        row["error"] = resp.error[:200]
    try:
        with open(home() / "fetch-log.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(row) + "\n")
    except OSError:
        pass
    if resp.ok and method == "GET" and resp.body:
        try:
            pd = home() / "pages"
            pd.mkdir(exist_ok=True)
            (pd / (hashlib.sha1(url.encode("utf-8")).hexdigest() + ".body")).write_bytes(resp.body)
        except OSError:
            pass


def stored_page(url):
    p = home() / "pages" / (hashlib.sha1(url.encode("utf-8")).hexdigest() + ".body")
    return p.read_bytes() if p.exists() else None


def fetched_urls():
    """Every URL this HW_HOME fetched successfully, from the fetch log."""
    out = set()
    try:
        with open(home() / "fetch-log.jsonl", encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                if r.get("status") and 200 <= r["status"] < 400:
                    out.add(r["url"])
    except OSError:
        pass
    return out


def fetch(url, method="GET", data=None, headers=None, accept="application/json", timeout=40, retries=2, log=True):
    """One polite request. Never raises for HTTP or network errors: check resp.ok, resp.status, resp.error."""
    if os.environ.get("HW_FIXTURES"):
        resp = _fixture(url, method)
        if log:
            _log(url, method, resp)
        return resp
    host = urllib.parse.urlparse(url).hostname or ""
    h = {"User-Agent": user_agent(), "Accept": accept, "Accept-Encoding": "identity"}
    h.update(headers or {})
    body = None
    if data is not None:
        body = data if isinstance(data, bytes) else json.dumps(data).encode("utf-8")
        h.setdefault("Content-Type", "application/json")
    attempt = 0
    ctx = None
    while True:
        _pace_wait(host)
        req = urllib.request.Request(url, data=body, headers=h, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                resp = Response(r.status, {k.lower(): v for k, v in r.headers.items()}, r.read(), r.geturl())
        except urllib.error.HTTPError as e:
            hdrs = {k.lower(): v for k, v in (e.headers or {}).items()}
            try:
                b = e.read()
            except OSError:
                b = b""
            resp = Response(e.code, hdrs, b, url, error="HTTP %d" % e.code)
            if e.code in (429, 503) and attempt < retries:
                ra = hdrs.get("retry-after", "5")
                wait = int(ra) if ra.isdigit() else 5
                if wait <= MAX_RETRY_AFTER:
                    time.sleep(wait)
                    attempt += 1
                    continue
        except (urllib.error.URLError, OSError, ValueError) as e:
            resp = Response(None, {}, b"", url, error=str(getattr(e, "reason", e))[:200])
            if ctx is None and "CERTIFICATE_VERIFY_FAILED" in resp.error and "Missing" in resp.error:
                # Python 3.13+ verifies in X.509 strict mode; some archive hosts serve certificates without a key
                # identifier. Retry once with only that flag cleared: chain and hostname are still verified.
                ctx = ssl.create_default_context()
                ctx.verify_flags &= ~getattr(ssl, "VERIFY_X509_STRICT", 0)
                continue
            if attempt < 1:
                time.sleep(2)
                attempt += 1
                continue
        break
    if os.environ.get("HW_RECORD"):
        _record(url, method, resp)
    if log:
        _log(url, method, resp)
    return resp


def get_json(url, **kw):
    """fetch + parse; returns (data or None, resp)."""
    resp = fetch(url, **kw)
    if not resp.ok:
        return None, resp
    try:
        return resp.json(), resp
    except ValueError:
        resp.error = "not JSON"
        return None, resp


def qs(params):
    return urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})


def dig(obj, path):
    """Follow a dotted path; numeric segments index lists; a dict where a list is expected yields its values."""
    if path in (None, "", "."):
        return obj
    cur = obj
    for seg in path.split("."):
        if cur is None:
            return None
        if isinstance(cur, list):
            if seg.isdigit():
                i = int(seg)
                cur = cur[i] if i < len(cur) else None
            else:
                return None
        elif isinstance(cur, dict):
            cur = cur.get(seg)
        else:
            return None
    return cur


def as_list(x):
    if x is None:
        return []
    if isinstance(x, dict):
        return list(x.values())
    return x if isinstance(x, list) else [x]


# ---------------------------------------------------------------- text helpers

_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")


def html_to_text(s):
    import html as _html
    s = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</h\d>|</div>|</tr>", "\n", s)
    s = _TAG.sub(" ", s)
    return _WS.sub(" ", _html.unescape(s)).strip()


def normalise(s):
    import unicodedata
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    s = re.sub("[‐-―−]", "-", s)
    s = s.replace(" ", " ")
    return _WS.sub(" ", s).strip().casefold()
