"""Dates for hw.py: the Julian Day Number is the pivot, all arithmetic is integer, nothing uses datetime
(which stops at year 1). Astronomical years internally (1 BC = 0, 100 BC = -99); historical labels outside.

Sources: Fliegel and Van Flandern / Richards algorithms (USNO, R-20261017-9); Gregorian adoption by country
(R-20261017-9); EDTF levels 0 and 1 (Library of Congress, ISO 8601-2); tabular Islamic calendar (civil epoch);
East Asian eras from the DILA Time Authority Database (CC BY-SA 3.0), design after kltng/humanities-skills
cjk-calendar (R-20261017-10).
"""

import io
import re
import sqlite3
import zipfile

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
MONTH_ABBR = {m[:3].lower(): i + 1 for i, m in enumerate(MONTHS)}
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


# ---------------------------------------------------------------- JDN core

def gregorian_to_jdn(y, m, d):
    a = (14 - m) // 12
    yy, mm = y + 4800 - a, m + 12 * a - 3
    return d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - yy // 100 + yy // 400 - 32045


def julian_to_jdn(y, m, d):
    a = (14 - m) // 12
    yy, mm = y + 4800 - a, m + 12 * a - 3
    return d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - 32083


def jdn_to_gregorian(j):
    a = j + 32044
    b = (4 * a + 3) // 146097
    c = a - 146097 * b // 4
    d = (4 * c + 3) // 1461
    e = c - 1461 * d // 4
    m = (5 * e + 2) // 153
    return 100 * b + d - 4800 + m // 10, m + 3 - 12 * (m // 10), e - (153 * m + 2) // 5 + 1


def jdn_to_julian(j):
    c = j + 32082
    d = (4 * c + 3) // 1461
    e = c - 1461 * d // 4
    m = (5 * e + 2) // 153
    return d - 4800 + m // 10, m + 3 - 12 * (m // 10), e - (153 * m + 2) // 5 + 1


def to_jdn(y, m, d, cal):
    return julian_to_jdn(y, m, d) if cal == "julian" else gregorian_to_jdn(y, m, d)


def from_jdn(j, cal):
    return jdn_to_julian(j) if cal == "julian" else jdn_to_gregorian(j)


def days_in_month(y, m, cal):
    nxt = (y + 1, 1) if m == 12 else (y, m + 1)
    return to_jdn(nxt[0], nxt[1], 1, cal) - to_jdn(y, m, 1, cal)


def weekday(j):
    return WEEKDAYS[j % 7]


def hist_to_astro(year, bc):
    if year <= 0:
        raise ValueError("historical years start at 1 (there is no year 0 in BC/AD counting)")
    return 1 - year if bc else year


def year_label(y):
    if y <= 0:
        return "%d BC" % (1 - y)
    return "AD %d" % y if y < 1000 else str(y)


def date_label(y, m=None, d=None):
    parts = []
    if d:
        parts.append(str(d))
    if m:
        parts.append(MONTHS[m - 1])
    parts.append(year_label(y))
    return " ".join(parts)


def iso_astro(y, m=None, d=None):
    s = ("-%04d" % -y) if y < 0 else "%04d" % y
    if m:
        s += "-%02d" % m
        if d:
            s += "-%02d" % d
    return s


# Rome's switch; Julian in force from 1 January 45 BC (astronomical -44)
GREGORIAN_START = 2299161  # 15 October 1582
JULIAN_REFORM = julian_to_jdn(-44, 1, 1)

# Last Julian day and first Gregorian day per country (R-20261017-9). Some states kept other calendars before:
# "pre" names them, so the agent knows the Julian date is proleptic there.
ADOPTION = {
    "default": ("1582-10-04", "1582-10-15", None),
    "IT": ("1582-10-04", "1582-10-15", None), "ES": ("1582-10-04", "1582-10-15", None),
    "PT": ("1582-10-04", "1582-10-15", None), "PL": ("1582-10-04", "1582-10-15", None),
    "FR": ("1582-12-09", "1582-12-20", None),
    "DE-catholic": ("1583-10-05", "1583-10-16", "dates differ by state; Bavaria shown"),
    "DE-protestant": ("1700-02-18", "1700-03-01", None),
    "GB": ("1752-09-02", "1752-09-14", "legal year began 25 March before 1752"),
    "US": ("1752-09-02", "1752-09-14", "British colonies followed Britain; legal year began 25 March"),
    "SE": ("1753-02-17", "1753-03-01", "Swedish calendar 1700-1712"),
    "JP": (None, "1873-01-01", "lunisolar before 1873: use cal cjk"),
    "CN": (None, "1912-01-01", "lunisolar before 1912: use cal cjk"),
    "KR": (None, "1896-01-01", "lunisolar before 1896: use cal cjk"),
    "RU": ("1918-01-31", "1918-02-14", None),
    "GR": ("1923-02-15", "1923-03-01", None),
    "TR": (None, "1926-01-01", "Rumi and Hijri calendars before 1926"),
}


def _iso_jdn(s, cal):
    y, m, d = (int(x) for x in s.split("-"))
    return to_jdn(y, m, d, cal)


def civil_calendar(j, country="default"):
    last, first, note = ADOPTION.get(country, ADOPTION["default"])
    if j >= _iso_jdn(first, "gregorian"):
        return "gregorian", note
    if last is None:
        return "other", note
    return "julian", note


# ---------------------------------------------------------------- other calendars

ISLAMIC_EPOCH = 1948440  # 1 Muharram AH 1 = 16 July 622 Julian (civil epoch)


def islamic_to_jdn(y, m, d):
    return d + (59 * (m - 1) + 1) // 2 + (y - 1) * 354 + (3 + 11 * y) // 30 + ISLAMIC_EPOCH - 1


def jdn_to_islamic(j):
    y = (30 * (j - ISLAMIC_EPOCH) + 10646) // 10631
    x = j - (29 + islamic_to_jdn(y, 1, 1))
    m = min(12, -((-2 * x) // 59) + 1)
    m = max(1, m)
    return y, m, j - islamic_to_jdn(y, m, 1) + 1


def auc(y):
    """Varronian ab urbe condita year for an astronomical year (AUC 1 = 753 BC)."""
    return y + 753


# ---------------------------------------------------------------- parsing Western date expressions

_BC = r"(?:b\.?c\.?e?\.?|bce)"
_AD = r"(?:a\.?d\.?|c\.?e\.?)"


def parse_date(text, cal="auto"):
    """Parse a written date to (astro_year, month or None, day or None, calendar, notes).

    Accepts '12 July 100 BC', 'July 12, 100 BC', '100 BC', 'AD 79', '1582-10-15', '-0099-07-12' (astronomical
    ISO, as EDTF writes it), 'AUC 654', 'AH 1300' (tabular), '1917-10-25 O.S.'. cal: julian, gregorian or auto
    (Julian before 15 October 1582, Gregorian after; 'O.S.' forces Julian, 'N.S.' Gregorian).
    """
    t = text.strip()
    notes = []
    low = t.lower()
    if re.search(r"\bo\.?s\.?$|old style", low):
        cal = "julian"
        t = re.sub(r"(?i)\s*(o\.?s\.?|\(?old style\)?)$", "", t).strip()
    elif re.search(r"\bn\.?s\.?$|new style", low):
        cal = "gregorian"
        t = re.sub(r"(?i)\s*(n\.?s\.?|\(?new style\)?)$", "", t).strip()
    m = re.fullmatch(r"(?i)a\.?u\.?c\.?\s*(\d{1,4})", t)
    if m:
        y = int(m.group(1)) - 753
        notes.append("AUC read as Varronian (AUC 1 = 753 BC)")
        return y, None, None, "julian" if cal == "auto" else cal, notes
    m = re.fullmatch(r"(?i)(?:a\.?h\.?\s*(\d{1,4})(?:-(\d{1,2})-(\d{1,2}))?)", t)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2) or 1), int(m.group(3) or 1)
        j = islamic_to_jdn(y, mo, d)
        notes.append("tabular Islamic calendar (civil epoch); observed dates can differ by a day or two")
        yy, mm, dd = from_jdn(j, "julian" if j < GREGORIAN_START else "gregorian")
        return yy, (mm if m.group(2) else None), (dd if m.group(3) else None), \
            ("julian" if j < GREGORIAN_START else "gregorian"), notes
    m = re.fullmatch(r"(-?)(\d{4,})(?:-(\d{2})(?:-(\d{2}))?)?", t)
    if m:
        y = int(m.group(2)) * (-1 if m.group(1) else 1)
        mo = int(m.group(3)) if m.group(3) else None
        d = int(m.group(4)) if m.group(4) else None
        if y <= 0:
            notes.append("ISO/EDTF years are astronomical: %s is %s" % (t, year_label(y)))
        return y, mo, d, _auto_cal(y, mo, d, cal), notes
    era = None
    if re.search(_BC + r"\s*$", low):
        era, t = "bc", re.sub(r"(?i)\s*" + _BC + r"\s*$", "", t)
    elif re.search(_AD + r"\s*$", low):
        era, t = "ad", re.sub(r"(?i)\s*" + _AD + r"\s*$", "", t)
    elif re.match(r"(?i)" + _AD + r"\s+\d", t):
        era, t = "ad", re.sub(r"(?i)^" + _AD + r"\s+", "", t)
    t = t.replace(",", " ").strip()
    toks = t.split()
    day = mon = year = None
    for tok in toks:
        k = tok.lower().rstrip(".")
        if k[:3] in MONTH_ABBR and not k.isdigit():
            mon = MONTH_ABBR[k[:3]]
        elif re.fullmatch(r"\d{1,2}(st|nd|rd|th)?", k) and day is None and (year is not None or mon is not None or len(toks) == 3):
            day = int(re.sub(r"\D", "", k))
        elif k.isdigit():
            if year is None:
                year = int(k)
            elif day is None:
                day, year = year, int(k)
    if year is None:
        raise ValueError("cannot read a year in %r" % text)
    y = hist_to_astro(year, era == "bc")
    return y, mon, day, _auto_cal(y, mon, day, cal), notes


def _auto_cal(y, m, d, cal):
    if cal != "auto":
        return cal
    return "gregorian" if gregorian_to_jdn(y, m or 1, d or 1) >= GREGORIAN_START else "julian"


def span_range(y, m, d, cal):
    """First and last JDN covered by a date of year, month or day precision."""
    if m and d:
        j = to_jdn(y, m, d, cal)
        return j, j
    if m:
        a = to_jdn(y, m, 1, cal)
        return a, a + days_in_month(y, m, cal) - 1
    return to_jdn(y, 1, 1, cal), to_jdn(y + 1, 1, 1, cal) - 1


def describe_jdn(j, country=None):
    """Every calendar's reading of one day."""
    jy, jm, jd = jdn_to_julian(j)
    gy, gm, gd = jdn_to_gregorian(j)
    out = {
        "jdn": j,
        "weekday": weekday(j),
        "julian": {"iso": iso_astro(jy, jm, jd), "label": date_label(jy, jm, jd), "auc": auc(jy)},
        "gregorian": {"iso": iso_astro(gy, gm, gd), "label": date_label(gy, gm, gd)},
    }
    if j >= ISLAMIC_EPOCH:
        iy, im, idd = jdn_to_islamic(j)
        out["islamic_tabular"] = {"ah": "%d-%02d-%02d" % (iy, im, idd),
                                  "note": "tabular; observed dates can differ by a day or two"}
    notes = []
    if j < JULIAN_REFORM:
        notes.append("before 1 January 45 BC: Rome used the republican calendar, so a Roman date as written does "
                     "not map to this solar day; the Julian reading is proleptic")
    if j < GREGORIAN_START:
        notes.append("Gregorian reading before 15 October 1582 is proleptic")
    if country:
        civ, cnote = civil_calendar(j, country)
        out["civil_calendar"] = {"country": country, "calendar": civ}
        if cnote:
            notes.append(cnote)
        if country in ("GB", "US") and civ == "julian" and (jm < 3 or (jm == 3 and jd < 25)):
            out["civil_calendar"]["dual_year"] = "%d/%s" % (jy - 1, str(jy)[-2:])
    if GREGORIAN_START <= j and (jy, jm, jd) != (gy, gm, gd) and j < gregorian_to_jdn(1927, 1, 1):
        out["os_ns"] = {"old_style": date_label(jy, jm, jd), "new_style": date_label(gy, gm, gd),
                        "difference_days": j - gregorian_to_jdn(jy, jm, jd)}
    if notes:
        out["notes"] = notes
    return out


def span(a, b):
    """Exact distance between two (astro_year, month, day, cal) points: days and whole years, months, days."""
    ja, jb = to_jdn(a[0], a[1] or 1, a[2] or 1, a[3]), to_jdn(b[0], b[1] or 1, b[2] or 1, b[3])
    sign = 1
    if jb < ja:
        ja, jb, sign = jb, ja, -1
    cal ="julian" if a[3] == "julian" and b[3] == "julian" else "gregorian"
    y1, m1, d1 = from_jdn(ja, cal)
    y2, m2, d2 = from_jdn(jb, cal)
    years = y2 - y1
    months = m2 - m1
    days = d2 - d1
    if days < 0:
        months -= 1
        pm, py = (m2 - 1, y2) if m2 > 1 else (12, y2 - 1)
        days += days_in_month(py, pm, cal)
    if months < 0:
        years -= 1
        months += 12
    return {"days": sign * (jb - ja), "years": years, "months": months, "rest_days": days,
            "calendar_for_y_m_d": cal, "crosses_bc_ad": (y1 <= 0 < y2),
            "note": "no year 0 between 1 BC and AD 1; computed on astronomical years" if y1 <= 0 < y2 else None}


# ---------------------------------------------------------------- EDTF (levels 0 and 1, plus level 2 sets)

_Y = r"-?\d{4}"
_YU = r"-?(?:\d{4}|\d{3}X|\d{2}XX)"
_M = r"(?:0[1-9]|1[0-2]|2[1-4]|XX)"
_D = r"(?:0[1-9]|[12]\d|3[01]|XX)"
_DATE1 = r"(?:Y-?\d{5,}|" + _YU + r"(?:-" + _M + r"(?:-" + _D + r")?)?)[?~%]?"
_EDTF_DATE = re.compile(r"^" + _DATE1 + r"$")
_EDTF_TIME = re.compile(r"^" + _Y + r"-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}(:\d{2})?)?$")


def edtf_valid(s):
    """True for EDTF level 0 and 1 dates and intervals, and level 2 'one of' / 'all of' sets of them."""
    if not isinstance(s, str) or not s:
        return False
    if s[0] in "[{" and s[-1] in "]}" and (s[0] == "[") == (s[-1] == "]"):
        items = [x.strip() for x in s[1:-1].split(",") if x.strip()]
        if not items:
            return False
        for it in items:
            parts = it.split("..")
            if len(parts) > 2 or not all((not p) or _EDTF_DATE.match(p) for p in parts) or not any(parts):
                return False
        return True
    if _EDTF_TIME.match(s):
        return True
    if "/" in s:
        a, b = s.split("/", 1)
        ok = lambda x: x in ("", "..") or bool(_EDTF_DATE.match(x))  # noqa: E731
        return ok(a) and ok(b) and not (a in ("", "..") and b in ("", ".."))
    return bool(_EDTF_DATE.match(s))


def edtf_for(y, m=None, d=None, qualifier=None):
    s = iso_astro(y, m, d)
    if qualifier in ("circa", "approximate"):
        s += "~"
    elif qualifier in ("uncertain", "probably", "presumably", "possibly"):
        s += "?"
    return s


# ---------------------------------------------------------------- Wikidata time values

WD_CAL = {"Q1985727": "gregorian", "Q1985786": "julian"}
WD_PRECISION = {14: "second", 13: "minute", 12: "hour", 11: "day", 10: "month", 9: "year", 8: "decade",
                7: "century", 6: "millennium", 5: "ten millennia", 4: "hundred millennia", 3: "million years",
                2: "ten million years", 1: "hundred million years", 0: "billion years"}


def wikidata_time(v):
    """Decode a Wikidata JSON time value. Its JSON uses historical numbering (-0100 is 100 BC), unlike its RDF and
    SPARQL output, which use XSD year 0 and convert to Gregorian (R-20261017-2)."""
    m = re.match(r"([+-])(\d+)-(\d\d)-(\d\d)", v.get("time", ""))
    if not m:
        return {"error": "unreadable time %r" % v.get("time")}
    hy = int(m.group(2))
    bc = m.group(1) == "-"
    mo, d = int(m.group(3)), int(m.group(4))
    prec = v.get("precision", 11)
    cal = WD_CAL.get(v.get("calendarmodel", "").rsplit("/", 1)[-1], "unknown")
    if hy == 0:
        return {"error": "year 0 in a Wikidata JSON time value", "raw": v.get("time")}
    y = hist_to_astro(hy, bc)
    c = cal if cal in ("julian", "gregorian") else "gregorian"
    out = {"raw": v.get("time"), "calendar": cal, "precision": WD_PRECISION.get(prec, str(prec))}
    if prec >= 11:
        out.update(as_written=date_label(y, mo, d), edtf=edtf_for(y, mo, d))
        a, b = span_range(y, mo, d, c)
    elif prec == 10:
        out.update(as_written=date_label(y, mo), edtf=edtf_for(y, mo))
        a, b = span_range(y, mo, None, c)
    elif prec == 9:
        out.update(as_written=year_label(y), edtf=edtf_for(y))
        a, b = span_range(y, None, None, c)
    else:
        size = {8: 10, 7: 100, 6: 1000}.get(prec, 10 ** max(1, 9 - prec + 1))
        if prec == 8:
            lo = (y // 10) * 10
            hi = lo + 9
        else:  # Wikidata stores the 19th century as 1801-1900 written with any year inside it
            n = (hy - 1) // size + 1
            lo_h, hi_h = (n - 1) * size + 1, n * size
            lo, hi = (hist_to_astro(hi_h, True), hist_to_astro(lo_h, True)) if bc else (lo_h, hi_h)
        out.update(as_written="%s to %s (%s)" % (year_label(lo), year_label(hi), out["precision"]),
                   edtf="%s/%s" % (iso_astro(lo), iso_astro(hi)))
        a, b = to_jdn(lo, 1, 1, c), to_jdn(hi, 12, 31, c)
    out["jdn"] = [a, b]
    flags = []
    if cal == "gregorian" and a < GREGORIAN_START:
        flags.append("proleptic Gregorian value before 1582: check whether the source meant Julian")
        jy, jm, jd = jdn_to_julian(a)
        out["julian_reading"] = date_label(jy, jm if prec >= 10 else None, jd if prec >= 11 else None)
    if prec >= 11 and mo == 1 and d == 1:
        flags.append("1 January at day precision is often a year-precision artefact")
    if a < JULIAN_REFORM:
        flags.append("before 45 BC: Roman republican calendar date")
    if flags:
        out["flags"] = flags
    return out


# ---------------------------------------------------------------- East Asian eras (DILA)

DILA_URLS = ["https://authority.dila.edu.tw/downloads/authority_time.2012-02.zip",
             "https://raw.githubusercontent.com/DILA-edu/Authority-Databases/master/authority_time/SQL/authority_time.sql"]
DILA_ATTRIBUTION = ("East Asian calendar data: DILA Time Authority Database, Dharma Drum Institute of Liberal Arts "
                    "(authority.dila.edu.tw), CC BY-SA 3.0. Lookup design after kltng/humanities-skills cjk-calendar.")
KEEP_TABLES = {"t_dynasty", "t_dynasty_names", "t_emperor", "t_emperor_names", "t_era", "t_era_names", "t_month"}


def _sql_rows(values):
    """Parse a MySQL VALUES list: (1,'a\\'b',NULL),(...) -> list of tuples."""
    rows, row, i, n = [], [], 0, len(values)
    cur = None
    while i < n:
        c = values[i]
        if c == "(":
            row, cur = [], ""
        elif c == "'":
            i += 1
            buf = []
            while i < n:
                ch = values[i]
                if ch == "\\" and i + 1 < n:
                    nxt = values[i + 1]
                    buf.append({"n": "\n", "t": "\t", "r": "\r", "0": "\0"}.get(nxt, nxt))
                    i += 2
                    continue
                if ch == "'":
                    if i + 1 < n and values[i + 1] == "'":
                        buf.append("'")
                        i += 2
                        continue
                    break
                buf.append(ch)
                i += 1
            cur = ("S", "".join(buf))
        elif c in ",)":
            if cur is not None:
                if isinstance(cur, tuple):
                    row.append(cur[1])
                else:
                    tok = cur.strip()
                    row.append(None if tok in ("NULL", "") else (int(tok) if re.fullmatch(r"-?\d+", tok) else tok))
            cur = "" if c == "," else None
            if c == ")":
                rows.append(tuple(row))
        elif cur is not None and not isinstance(cur, tuple):
            cur += c
        i += 1
    return rows


def build_dila_db(sql_text, db_path):
    tmp = str(db_path) + ".tmp"
    import os
    if os.path.exists(tmp):
        os.remove(tmp)
    con = sqlite3.connect(tmp)
    con.executescript("""
    CREATE TABLE dynasty(id INTEGER PRIMARY KEY, type TEXT);
    CREATE TABLE dynasty_name(dynasty_id INTEGER, name TEXT, ranking INTEGER, language_id INTEGER);
    CREATE TABLE emperor(id INTEGER PRIMARY KEY, dynasty_id INTEGER);
    CREATE TABLE emperor_name(emperor_id INTEGER, name TEXT, ranking INTEGER, language_id INTEGER);
    CREATE TABLE era(id INTEGER PRIMARY KEY, emperor_id INTEGER);
    CREATE TABLE era_name(era_id INTEGER, name TEXT, ranking INTEGER, language_id INTEGER);
    CREATE TABLE month(id INTEGER PRIMARY KEY, year INTEGER, month INTEGER, month_name TEXT, leap_month INTEGER,
      era_id INTEGER, first_jdn INTEGER, last_jdn INTEGER, ganzhi TEXT, start_from INTEGER, status TEXT, eclipse INTEGER);
    CREATE TABLE meta(k TEXT PRIMARY KEY, v TEXT);
    """)
    target = {"t_dynasty": "dynasty", "t_dynasty_names": "dynasty_name", "t_emperor": "emperor",
              "t_emperor_names": "emperor_name", "t_era": "era", "t_era_names": "era_name", "t_month": "month"}
    counts = {}
    for m in re.finditer(r"INSERT INTO `(\w+)` VALUES (.*?);\n", sql_text, re.S):
        tb = m.group(1)
        if tb not in KEEP_TABLES:
            continue
        rows = _sql_rows(m.group(2))
        if not rows:
            continue
        ph = ",".join("?" * len(rows[0]))
        con.executemany("INSERT OR REPLACE INTO %s VALUES (%s)" % (target[tb], ph), rows)
        counts[target[tb]] = counts.get(target[tb], 0) + len(rows)
    con.executescript("""
    CREATE INDEX idx_month_jdn ON month(first_jdn, last_jdn);
    CREATE INDEX idx_month_era ON month(era_id, year, month, leap_month);
    CREATE INDEX idx_era_name ON era_name(name);
    CREATE VIEW era_summary AS
      SELECT e.id AS era_id,
        (SELECT name FROM era_name WHERE era_id=e.id ORDER BY ranking LIMIT 1) AS era_name,
        em.id AS emperor_id,
        (SELECT name FROM emperor_name WHERE emperor_id=em.id ORDER BY ranking LIMIT 1) AS emperor_name,
        d.id AS dynasty_id,
        (SELECT name FROM dynasty_name WHERE dynasty_id=d.id ORDER BY ranking LIMIT 1) AS dynasty_name,
        d.type AS country,
        (SELECT MIN(first_jdn) FROM month WHERE era_id=e.id) AS start_jdn,
        (SELECT MAX(last_jdn) FROM month WHERE era_id=e.id) AS end_jdn
      FROM era e JOIN emperor em ON em.id=e.emperor_id JOIN dynasty d ON d.id=em.dynasty_id;
    """)
    con.execute("INSERT INTO meta VALUES('attribution', ?)", (DILA_ATTRIBUTION,))
    con.execute("INSERT INTO meta VALUES('licence', 'CC BY-SA 3.0 Unported')")
    con.commit()
    con.close()
    os.replace(tmp, db_path)
    return counts


def sql_from_download(body):
    if body[:2] == b"PK":
        z = zipfile.ZipFile(io.BytesIO(body))
        name = next(n for n in z.namelist() if n.endswith("authority_time.sql"))
        return z.read(name).decode("utf-8")
    return body.decode("utf-8")


CN_DIGITS = {"〇": 0, "零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9,
             "兩": 2}


def cn_number(s):
    """Chinese numerals as used in dates: 元=1, 正=1, 十, 廿=20, 卅=30, 百; Arabic digits pass through."""
    s = s.strip()
    if s.isdigit():
        return int(s)
    if s in ("元", "正", "端"):
        return 1
    if s in ("冬",):
        return 11
    if s in ("臘", "腊"):
        return 12
    s = s.replace("廿", "二十").replace("卅", "三十").replace("初", "")
    total, cur = 0, 0
    for ch in s:
        if ch in CN_DIGITS:
            cur = CN_DIGITS[ch]
        elif ch == "十":
            total += (cur or 1) * 10
            cur = 0
        elif ch == "百":
            total += (cur or 1) * 100
            cur = 0
        else:
            raise ValueError("not a Chinese numeral: %r" % s)
    return total + cur


GANZHI_RE = r"[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]"
CJK_DATE = re.compile(r"^(?P<era>.+?)(?P<year>元|[〇零一二三四五六七八九十廿卅百兩\d]+|" + GANZHI_RE +
                      r")年(?:(?P<leap>閏|闰)?(?P<month>正|冬|臘|腊|[一二三四五六七八九十\d]+)月)?"
                      r"(?:(?P<day>初?[一二三四五六七八九十廿卅\d]+)日?)?$")


def parse_cjk(text):
    m = CJK_DATE.match(text.strip())
    if not m:
        raise ValueError("cannot read %r as era + year (年) + month (月) + day" % text)
    year = m.group("year")
    return {"era": m.group("era"), "year": year if re.fullmatch(GANZHI_RE, year) else cn_number(year),
            "leap": bool(m.group("leap")), "month": cn_number(m.group("month")) if m.group("month") else None,
            "day": cn_number(m.group("day")) if m.group("day") else None}


def cjk_eras(con, name):
    q = """SELECT DISTINCT s.* FROM era_summary s JOIN era_name n ON n.era_id=s.era_id WHERE n.name=?
           ORDER BY s.start_jdn"""
    cols = [c[0] for c in con.execute("SELECT * FROM era_summary LIMIT 0").description]
    return [dict(zip(cols, r)) for r in con.execute(q, (name,))]


def cjk_to_jdn(con, text):
    p = parse_cjk(text)
    eras = cjk_eras(con, p["era"])
    if not eras:
        return p, []
    out = []
    for e in eras:
        if isinstance(p["year"], str):
            yrs = [r[0] for r in con.execute("SELECT DISTINCT year FROM month WHERE era_id=? AND ganzhi=?",
                                             (e["era_id"], p["year"]))]
        else:
            yrs = [p["year"]]
        for y in yrs:
            if p["month"]:
                rows = con.execute("SELECT first_jdn,last_jdn,month_name,start_from,ganzhi FROM month WHERE era_id=? "
                                   "AND year=? AND month=? AND leap_month=?",
                                   (e["era_id"], y, p["month"], 1 if p["leap"] else 0)).fetchall()
            else:
                rows = con.execute("SELECT MIN(first_jdn),MAX(last_jdn),NULL,1,MIN(ganzhi) FROM month WHERE era_id=? "
                                   "AND year=?", (e["era_id"], y)).fetchall()
                rows = [r for r in rows if r[0] is not None]
            for first, last, mname, start, gz in rows:
                if p["day"]:
                    j = first + p["day"] - (start or 1)
                    if j > last:
                        continue
                    rng = [j, j]
                else:
                    rng = [first, last]
                out.append({"era": e["era_name"], "emperor": e["emperor_name"], "dynasty": e["dynasty_name"],
                            "country": e["country"], "era_year": y, "year_ganzhi": gz,
                            "month_name": (mname + "月") if mname else None, "jdn": rng,
                            "western": [describe_jdn(rng[0])["julian" if rng[0] < GREGORIAN_START else "gregorian"]["label"],
                                        describe_jdn(rng[1])["julian" if rng[1] < GREGORIAN_START else "gregorian"]["label"]]})
    return p, out


def jdn_to_cjk(con, j):
    rows = con.execute("""SELECT m.year, m.month_name, m.leap_month, m.first_jdn, m.start_from, m.ganzhi, s.era_name,
        s.emperor_name, s.dynasty_name, s.country FROM month m JOIN era_summary s ON s.era_id=m.era_id
        WHERE m.first_jdn<=? AND m.last_jdn>=? ORDER BY s.country, s.dynasty_id""", (j, j)).fetchall()
    out = []
    for y, mname, leap, first, start, gz, era, emp, dyn, country in rows:
        day = j - first + (start or 1)
        out.append({"country": country, "dynasty": dyn, "emperor": emp, "era": era, "era_year": y,
                    "year_ganzhi": gz, "month": (mname or "") + "月", "day": day,
                    "written": "%s%s年%s月%s日" % (era, "元" if y == 1 else y, mname or "", day)})
    return out
