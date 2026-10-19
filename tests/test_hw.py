"""Tests for hw.py. Standard library only; no network (HTTP comes from tests/fixtures/http through HW_FIXTURES).

Run from the repository root: python tests/test_hw.py
"""

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "historywright" / "scripts"
FIX = ROOT / "tests" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

TMP_HOME = tempfile.mkdtemp(prefix="hw-test-")
os.environ["HW_HOME"] = TMP_HOME
os.environ["HW_FIXTURES"] = str(FIX / "http")
for k in ("OPENALEX_API_KEY", "WHG_TOKEN", "HW_CONTACT", "HW_RECORD"):
    os.environ.pop(k, None)

import hw  # noqa: E402
import hw_check as C  # noqa: E402
import hw_dates as D  # noqa: E402
import hw_sources as S  # noqa: E402


def run(*argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = hw.main(list(argv))
    return code, json.loads(buf.getvalue())


class Dates(unittest.TestCase):
    def test_jdn_vectors(self):
        # R-20261017-9: JDN 2299160 = 4 Oct 1582 Julian, 2299161 = 15 Oct 1582 Gregorian, Julian 12 July 100 BC = 1685091
        self.assertEqual(D.julian_to_jdn(1582, 10, 4), 2299160)
        self.assertEqual(D.gregorian_to_jdn(1582, 10, 15), 2299161)
        self.assertEqual(D.julian_to_jdn(-99, 7, 12), 1685091)
        for j in (0, 1685091, 2299160, 2299161, 2460000):
            self.assertEqual(D.julian_to_jdn(*D.jdn_to_julian(j)), j)
            self.assertEqual(D.gregorian_to_jdn(*D.jdn_to_gregorian(j)), j)

    def test_parse_forms(self):
        self.assertEqual(D.parse_date("12 July 100 BC")[:4], (-99, 7, 12, "julian"))
        self.assertEqual(D.parse_date("July 12, 100 BC")[:4], (-99, 7, 12, "julian"))
        self.assertEqual(D.parse_date("-0099-07-12")[:3], (-99, 7, 12))
        self.assertEqual(D.parse_date("AUC 654")[0], -99)
        self.assertEqual(D.parse_date("AD 79")[0], 79)
        self.assertEqual(D.parse_date("1917-10-25 O.S.")[3], "julian")
        self.assertEqual(D.parse_date("1975-04-04")[3], "gregorian")
        with self.assertRaises(ValueError):
            D.parse_date("0 BC")

    def test_suffix_forms_and_refusals(self):
        self.assertEqual(D.parse_date("709 AUC")[0], -44)  # 45 BC, not AD 709
        self.assertEqual(D.parse_date("1300 AH")[0], D.parse_date("AH 1300")[0])
        for text in ("AUC 709 Martius", "Kalends 44 BC", "45 Ramadan 1445"):
            with self.assertRaises(ValueError):
                D.parse_date(text)

    def test_roman_day_counts(self):
        for text, md in (("Ides of March 44 BC", (3, 15)), ("Idus Martias 44 BC", (3, 15)),
                         ("the day before the Ides of March 44 BC", (3, 14)), ("a.d. III Id. Mar. 44 BC", (3, 13)),
                         ("a.d. XIX Kal. Apr. 44 BC", (3, 14)), ("pridie Kalendas Apriles 44 BC", (3, 31)),
                         ("Nones of May AD 14", (5, 7)), ("Nones of June AD 14", (6, 5)), ("Ides of April AD 14", (4, 13)),
                         ("Kalends of January 45 BC", (1, 1))):
            y, m, d, cal, notes = D.parse_date(text)
            self.assertEqual((m, d, cal), md + ("julian",), text)
        self.assertEqual(D.parse_date("Ides of March 44 BC")[0], -43)
        self.assertEqual(D.parse_date("a.d. XVIII Kal. Ian. 50 BC")[:3], (-50, 12, 15))  # back into December 51 BC
        self.assertTrue(any("Republican" in n for n in D.parse_date("a.d. XVIII Kal. Ian. 50 BC")[4]))

    def test_hijri_month_names(self):
        self.assertEqual(D.parse_date("1 Muharram 1 AH")[:3], (622, 7, 16))
        self.assertEqual(D.ah_parts("Dhu'l-Hijjah 1445 AH"), (1445, 12, None))
        self.assertEqual(D.ah_parts("12 Rabi' I 11"), (11, 3, 12))
        code, d = run("cal", "date", "Ramadan 1445")
        self.assertEqual((d["edtf"], d["precision"]), ("2024-03-11/2024-04-09", "month"))
        self.assertEqual(d["read_as"]["label"], "Ramadan AH 1445")

    def test_ah_label_and_circa(self):
        code, d = run("cal", "date", "1300 AH")
        self.assertEqual(d["read_as"]["label"], "AH 1300")  # not the Western year it starts in
        self.assertEqual(d["read_as"]["western_start"]["astronomical_year"], 1882)
        code, d = run("cal", "date", "c. 100 BC")
        self.assertEqual((d["edtf"], d["qualifier"]), ("-0099~", "circa"))
        self.assertEqual(D.parse_date("circa 12 July 100 BC")[:3], (-99, 7, 12))
        self.assertTrue(D.edtf_valid(run("cal", "date", "c. AH 1300")[1]["edtf"]))

    def test_ah_year_is_its_own_range(self):
        code, d = run("cal", "date", "AH 1300")
        self.assertEqual(code, 0)
        self.assertEqual(d["edtf"], "1882-11-12/1883-11-01")
        self.assertEqual(d["jdn"][1] - d["jdn"][0] + 1, 355)

    def test_no_year_zero_span(self):
        s = D.span((-99, 1, 1, "julian"), (100, 1, 1, "julian"))
        self.assertEqual(s["years"], 199)
        self.assertTrue(s["crosses_bc_ad"])

    def test_os_ns_and_dual_year(self):
        d = D.describe_jdn(D.julian_to_jdn(1917, 10, 25), "RU")
        self.assertEqual(d["gregorian"]["iso"], "1917-11-07")
        self.assertEqual(d["os_ns"]["difference_days"], 13)
        w = D.describe_jdn(D.julian_to_jdn(1732, 2, 11), "GB")
        self.assertEqual(w["civil_calendar"]["dual_year"], "1731/32")
        self.assertEqual(w["gregorian"]["iso"], "1732-02-22")

    def test_republican_warning(self):
        d = D.describe_jdn(1685091)
        self.assertTrue(any("republican" in n for n in d["notes"]))

    def test_islamic_epoch(self):
        self.assertEqual(D.jdn_to_islamic(D.ISLAMIC_EPOCH), (1, 1, 1))
        self.assertEqual(D.jdn_to_julian(D.ISLAMIC_EPOCH), (622, 7, 16))
        for j in range(D.ISLAMIC_EPOCH, D.ISLAMIC_EPOCH + 20000, 97):
            self.assertEqual(D.islamic_to_jdn(*D.jdn_to_islamic(j)), j)

    def test_edtf(self):
        for ok in ("1975-04-04", "-0099-07", "-0099-07~", "-0099-07-12?", "19XX", "1661/1722", "../1722",
                   "[-0099-07-12,-0099-07-13]", "{1667,1668}", "1985-04-12T23:20:30Z"):
            self.assertTrue(D.edtf_valid(ok), ok)
        for bad in ("July 100 BC", "2026-13", "100 BC", "", "/", "[]", "1975-4-4"):
            self.assertFalse(D.edtf_valid(bad), bad)

    def test_wikidata_time(self):
        t = D.wikidata_time({"time": "-0100-07-12T00:00:00Z", "precision": 11,
                             "calendarmodel": "http://www.wikidata.org/entity/Q1985786"})
        self.assertEqual(t["as_written"], "12 July 100 BC")
        self.assertEqual(t["edtf"], "-0099-07-12")
        self.assertEqual(t["jdn"], [1685091, 1685091])
        g = D.wikidata_time({"time": "-0100-00-00T00:00:00Z", "precision": 9,
                             "calendarmodel": "http://www.wikidata.org/entity/Q1985727"})
        self.assertTrue(any("proleptic Gregorian" in f for f in g["flags"]))
        c = D.wikidata_time({"time": "+1850-00-00T00:00:00Z", "precision": 7,
                             "calendarmodel": "http://www.wikidata.org/entity/Q1985727"})
        self.assertEqual(c["edtf"], "1801/1900")

    def test_cjk_parse(self):
        self.assertEqual(D.cn_number("六十一"), 61)
        self.assertEqual(D.cn_number("廿八"), 28)
        self.assertEqual(D.cn_number("初三"), 3)
        p = D.parse_cjk("天保三年閏十一月十五日")
        self.assertEqual((p["era"], p["year"], p["leap"], p["month"], p["day"]), ("天保", 3, True, 11, 15))
        self.assertEqual(D.parse_cjk("嘉慶甲子年")["year"], "甲子")

    def test_dila_build_from_mini_dump(self):
        sql = ("INSERT INTO `t_dynasty` VALUES (1,'chinese');\n"
               "INSERT INTO `t_dynasty_names` VALUES (1,'清',0,1);\n"
               "INSERT INTO `t_emperor` VALUES (7,1);\n"
               "INSERT INTO `t_emperor_names` VALUES (7,'聖祖',0,1),(7,'O\\'Brien test',1,2);\n"
               "INSERT INTO `t_era` VALUES (660,7);\n"
               "INSERT INTO `t_era_names` VALUES (660,'康熙',0,1);\n"
               "INSERT INTO `t_month` VALUES (1,61,12,'十二',0,660,2350379,2350408,'壬寅',1,'S',0);\n"
               "INSERT INTO `c_languages` VALUES (1,'zho','x','x','y','y');\n")
        db = Path(TMP_HOME) / "mini.sqlite"
        counts = D.build_dila_db(sql, db)
        self.assertEqual(counts["month"], 1)
        import sqlite3
        con = sqlite3.connect(str(db))
        parsed, matches = D.cjk_to_jdn(con, "康熙六十一年十二月二十九日")
        self.assertEqual(matches[0]["jdn"], [2350407, 2350407])
        self.assertEqual(matches[0]["western"][0], "4 February 1723")
        self.assertEqual(D.jdn_to_cjk(con, 2350407)[0]["era"], "康熙")
        con.close()


class Wikidata(unittest.TestCase):
    def test_claims_show_every_statement(self):
        code, d = run("wd", "claims", "Q1048", "--prop", "P569")
        self.assertEqual(code, 0, d)
        self.assertEqual(d["api"], "wbgetclaims")
        st = d["claims"]["P569"]
        self.assertEqual(len(st), 4)
        self.assertEqual(st[0]["earliest"], "12 July 100 BC")
        self.assertEqual(st[0]["latest"], "13 July 100 BC")
        self.assertIn("disputed", st[0]["sourcing_circumstances"])
        written = [s["value"]["time"]["as_written"] for s in st]
        self.assertIn("102 BC", written)
        self.assertFalse(any("99 BC" in w or "11 July" in w for w in written))
        self.assertTrue(any("truthy" in n for n in d["notes"]))
        self.assertEqual(d["labels"]["Q18912752"], "disputed")

    def test_invented_qid_refused(self):
        code, d = run("wd", "claims", "Caesar")
        self.assertEqual(code, 1)
        self.assertIn("never invent", d["error"])

    def test_sparql_warns_on_truthy_dates(self):
        w = S.sparql_warnings("SELECT ?d WHERE { wd:Q1048 wdt:P569 ?d }")
        self.assertTrue(w and "psv:P569" in w[0])
        self.assertEqual(S.sparql_warnings("SELECT ?x WHERE { ?x wdt:P31 wd:Q5 }"), [])

    def test_search_and_qid_check(self):
        code, d = run("wd", "search", "Julius Caesar", "--limit", "3")
        self.assertEqual(d["results"][0]["qid"], "Q1048")
        code, v = run("verify", "qid", "Q1048", "--label", "Julius Caesar")
        self.assertTrue(v["ok"], v)


class Verify(unittest.TestCase):
    def test_quote_span(self):
        code, d = run("verify", "quote", "--url", "https://example.org/caesar-source", "--quote",
                      "born on the twelfth day of July")
        self.assertTrue(d["found"], d)
        code, d = run("verify", "quote", "--url", "https://example.org/caesar-source", "--quote",
                      "Caesar was BORN on the twelfth day ... kept as his festival")
        self.assertTrue(d["found"], d)
        code, d = run("verify", "quote", "--url", "https://example.org/caesar-source", "--quote",
                      "born on the thirteenth day of July")
        self.assertFalse(d["found"])
        self.assertEqual(code, 1)

    def test_url_health_labels_missing_page(self):
        r = C.url_health("https://example.org/missing")
        self.assertEqual(r["label"], "likely_hallucinated")

    def test_independence(self):
        srcs = [{"id": "a", "url": "https://en.wikipedia.org/wiki/X", "kind": "tertiary", "tier": 3},
                {"id": "b", "url": "https://www.wikiwand.com/en/X", "kind": "secondary", "tier": 2},
                {"id": "c", "url": "https://example.org/book", "kind": "secondary", "tier": 1},
                {"id": "d", "url": "https://example.org/news", "kind": "secondary", "tier": 2, "derived_from": ["c"]}]
        ids = [s["id"] for s in C.independent_set(srcs)]
        self.assertEqual(ids, ["c"])
        res = C.check_sources({"sources": [dict(s, title="t", retrieved="2026-10-17", claims=[]) for s in srcs]},
                              network=False, require_fetched=False)
        self.assertFalse(res["corroborated"])
        self.assertTrue(any("mirror" in p for p in res["problems"]))

    def test_only_fetched_urls_count(self):
        doc = {"sources": [{"id": "s1", "title": "t", "url": "https://example.org/never-fetched", "kind": "primary",
                            "tier": 1, "retrieved": "2026-10-17", "claims": [{"claim": "x", "quote": "y"}]}]}
        res = C.check_sources(doc, network=False, require_fetched=True)
        self.assertTrue(any("not fetched in this run" in p for p in res["problems"]))


class Pack(unittest.TestCase):
    def test_good_pack_passes(self):
        code, d = run("validate-pack", str(FIX / "pack-good"))
        self.assertTrue(d["ok"], d["problems"])

    def test_bad_pack_fails_on_each_rule(self):
        code, d = run("validate-pack", str(FIX / "pack-bad"))
        self.assertEqual(code, 1)
        text = "\n".join(d["problems"])
        for needle in ("missing anachronism.md", "Confidence", "AI-researched", "no supporting quote",
                       "Wikipedia or a mirror", "not a QID", "never a point", "crs", "swapped", "four positions",
                       "not EDTF", "nc: true", "marked commercial", "generated images", "without a reason"):
            self.assertIn(needle, text)

    def test_init_then_csl(self):
        d = Path(TMP_HOME) / "pack1"
        code, r = run("pack", "init", str(d), "--question", "When was Caesar born?", "--period", "100 BC")
        self.assertTrue(r["ok"])
        self.assertTrue((d / "manifest.json").exists() and (d / "refs" / "index.json").exists())
        man = json.loads((d / "manifest.json").read_text(encoding="utf-8"))
        for k in ("name", "kind", "route", "targets", "sources", "outputs"):
            self.assertIn(k, man)  # polywright's manifest --validate keys
        shutil.copy(FIX / "pack-good" / "sources.json", d / "sources.json")
        code, r = run("pack", "csl", str(d))
        self.assertEqual(r["items"], 2)


class CacheAndKeys(unittest.TestCase):
    def test_cache_roundtrip(self):
        entry = {"question": "When was Julius Caesar born?", "answer": "12 or 13 July 100 BC", "confidence": "high",
                 "sources": [{"url": "https://example.org/caesar-source", "retrieved": "2026-10-17", "quote": "q"}]}
        p = Path(TMP_HOME) / "entry.json"
        p.write_text(json.dumps(entry), encoding="utf-8")
        code, r = run("cache", "put", str(p))
        self.assertTrue(r["ok"], r)
        code, r = run("cache", "get", "when was caesar born")
        self.assertEqual(r["hits"][0]["answer"], "12 or 13 July 100 BC")
        bad = Path(TMP_HOME) / "bad.json"
        bad.write_text(json.dumps({"question": "q", "answer": "a", "sources": [{"url": "u"}]}), encoding="utf-8")
        code, r = run("cache", "put", str(bad))
        self.assertFalse(r["ok"])

    def test_keys_status_offline_and_masked(self):
        os.environ["WHG_TOKEN"] = "abcdefghijklmnopqrstuvwxyz0123456789XYZ"
        try:
            code, r = run("keys", "status", "--offline")
        finally:
            os.environ.pop("WHG_TOKEN")
        self.assertTrue(r["keys"]["whg"]["set"])
        self.assertNotIn("abcdef", json.dumps(r))

    def test_openalex_needs_consent(self):
        code, r = run("keys", "openalex", "--email", "someone@example.org")
        self.assertTrue(r.get("needs_confirmation"))


class Registry(unittest.TestCase):
    def test_lint_passes(self):
        code, r = run("lint")
        self.assertTrue(r["ok"], r["problems"])
        self.assertGreaterEqual(r["sources"], 50)
        self.assertEqual(r["era_outline_band"], "green")

    def test_lint_catches_bad_entries(self):
        probs, _ = hw.lint_registry({"sources": [
            {"id": "x", "name": "X", "use": "u", "kind": "k", "tier": 4, "licence": "l", "access": "paid",
             "route": "src", "url": "ftp://x", "checked": "2026-10-17",
             "search": {"url": "https://x/?q=a&api_key=ABCDEFGHIJKLMNOPQRSTUV"}}]})
        text = "\n".join(probs)
        for needle in ("tier", "link-out", "lacks {q}", "real key", "not http"):
            self.assertIn(needle, text)

    def test_mirror_detection(self):
        import hw_net
        self.assertTrue(hw_net.is_mirror("https://en.m.wikipedia.org/wiki/X"))
        self.assertTrue(hw_net.is_mirror("https://www.wikiwand.com/en/X"))
        self.assertFalse(hw_net.is_mirror("https://penelope.uchicago.edu/Thayer/"))


class FailSoft(unittest.TestCase):
    def test_bad_input_is_json(self):
        code, r = run("cal", "date", "not a date at all")
        self.assertEqual(code, 1)
        self.assertFalse(r["ok"])

    def test_redact_and_decode(self):
        import hw_net
        u = hw_net.redact("https://api.example.org/s?wskey=SECRET123&query=x&api_key=ABC")
        self.assertNotIn("SECRET123", u)
        self.assertNotIn("ABC", u)
        self.assertIn("query=x", u)
        body = '<html><head><meta charset="windows-1252"></head><body>caf\xe9 \x95 two</body></html>'.encode("latin-1")
        self.assertIn("café", hw_net.decode_body(body, "text/html"))
        self.assertEqual(hw_net.decode_body("Ünïcode".encode("utf-8"), ""), "Ünïcode")

    def test_record_pattern_hides_keys(self):
        import re
        import hw_net
        url = "https://api.si.edu/openaccess/api/v1.0/search?q=helmet&api_key=SECRET123"
        pat = hw_net.record_pattern(url)
        self.assertNotIn("SECRET123", pat)
        self.assertTrue(re.search(pat, url))
        self.assertFalse(re.search(pat, url.replace("helmet", "sword")))

    def test_src_skip_and_link(self):
        code, d = run("src", "wayback", "microsoft.com", "--limit", "3")
        self.assertTrue(d["ok"], d)
        self.assertEqual(d["count"], 1)  # the CDX header row is skipped
        self.assertEqual(d["results"][0]["url"], "https://web.archive.org/web/19961020014044/http://www.microsoft.com:80/")

    def test_project_home(self):
        import hw_net as N
        saved_env, saved_cwd = os.environ.pop("HW_HOME"), os.getcwd()
        proj = Path(tempfile.mkdtemp(prefix="hw-proj-"))
        fake_user = Path(tempfile.mkdtemp(prefix="hw-user-"))
        real_home = Path.home
        try:
            Path.home = staticmethod(lambda: fake_user)
            os.chdir(str(proj))
            self.assertEqual(N.home_source()[0], "user")
            (proj / ".historywright").mkdir()
            src, h = N.home_source()
            self.assertEqual((src, h.resolve()), ("project", (proj / ".historywright").resolve()))
            # keys, the DILA table and the pace file stay in the user home unless the project has its own config
            self.assertEqual(N.user_home().resolve(), (fake_user / ".historywright").resolve())
            self.assertEqual(N.config_path().resolve(), (fake_user / ".historywright" / "config.json").resolve())
            (proj / ".historywright" / "config.json").write_text("{}", encoding="utf-8")
            self.assertEqual(N.config_path().resolve(), (proj / ".historywright" / "config.json").resolve())
            os.environ["HW_HOME"] = saved_env
            self.assertEqual(N.home_source()[0], "HW_HOME")
            self.assertEqual(N.user_home().resolve(), Path(saved_env).resolve())
        finally:
            Path.home = real_home
            os.environ["HW_HOME"] = saved_env
            os.chdir(saved_cwd)
            shutil.rmtree(str(proj), ignore_errors=True)
            shutil.rmtree(str(fake_user), ignore_errors=True)

    def test_dig(self):
        import hw_net
        obj = {"a": {"b": [{"c": 1}, {"c": 2}]}, "pages": {"1": {"t": "x"}, "2": {"t": "y"}}}
        self.assertEqual(hw_net.dig(obj, "a.b.1.c"), 2)
        self.assertEqual([p["t"] for p in hw_net.as_list(hw_net.dig(obj, "pages"))], ["x", "y"])


def make_pdf(content, extra_fonts=True):
    """A small valid PDF: Flate page content, a simple font F1, and a Type0 font F2 with a ToUnicode map that sits
    in an object stream (PDF 1.5)."""
    import zlib
    cmap = (b"/CIDInit /ProcSet findresource begin 12 dict begin begincmap 1 begincodespacerange <0000> <FFFF> "
            b"endcodespacerange 1 beginbfrange <0001> <0003> <0048> endbfrange 1 beginbfchar <0004> <FB01> "
            b"endbfchar endcmap end end")
    zc = zlib.compress(content)
    f2 = b"<< /Type /Font /Subtype /Type0 /BaseFont /X /Encoding /Identity-H /ToUnicode 7 0 R >>"
    objstm_body = b"5 0 " + f2
    first = len(b"5 0 ")
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 6 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        None,  # 5 lives in the object stream (8)
        b"<< /Length %d /Filter /FlateDecode >>\nstream\n" % len(zc) + zc + b"\nendstream",
        b"<< /Length %d >>\nstream\n" % len(cmap) + cmap + b"\nendstream",
        b"<< /Type /ObjStm /N 1 /First %d /Length %d >>\nstream\n" % (first, len(objstm_body)) + objstm_body
        + b"\nendstream",
    ]
    out = bytearray(b"%PDF-1.5\n")
    for i, o in enumerate(objs, 1):
        if o is not None and (extra_fonts or i not in (5, 7, 8)):
            out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
    out += b"trailer\n<< /Root 1 0 R /Size 9 >>\n%%EOF\n"
    return bytes(out)


FILLER = b" ".join(b"0 -14 Td (This line is filler text so the page reads as prose, line %d.) Tj" % i
                   for i in range(8))
PDF_CONTENT = (b"BT /F1 11 Tf 72 720 Td (Caesar was born on 12 July 100 BC \\(Julian\\), in the Subura.) Tj "
               b"0 -14 Td [(Gaius Ju) -40 (lius) -300 (Caesar) ] TJ 0 -14 Td (the dicta-) Tj 0 -14 Td "
               b"(torship for life came in 44 BC; caf\\351 is a test.) Tj 0 -14 Td /F2 11 Tf <000100020003> Tj "
               b"/F1 11 Tf ( and ) Tj /F2 11 Tf <0004> Tj /F1 11 Tf (nd the record.) Tj " + FILLER + b" ET")


class Pdf(unittest.TestCase):
    def setUp(self):
        import hw_pdf
        self.P = hw_pdf
        os.environ["HW_PDFTOTEXT"] = "0"

    def tearDown(self):
        os.environ.pop("HW_PDFTOTEXT", None)

    def test_builtin_reader(self):
        text = self.P.builtin_text(make_pdf(PDF_CONTENT))
        self.assertIn("Caesar was born on 12 July 100 BC (Julian), in the Subura.", text)
        self.assertIn("Gaius Julius Caesar", text)
        self.assertIn("café", text)
        self.assertIn("HIJ and ﬁnd the record.", text)
        self.assertTrue(self.P.readable(text))

    def test_quotes_in_a_pdf(self):
        import hashlib
        import hw_net
        url = "https://example.org/paper.pdf"
        pages = hw_net.home() / "pages"
        pages.mkdir(parents=True, exist_ok=True)
        (pages / (hashlib.sha1(url.encode("utf-8")).hexdigest() + ".body")).write_bytes(make_pdf(PDF_CONTENT))
        r = C.verify_quote(url, "born on 12 July 100 BC (Julian), in the Subura")
        self.assertTrue(r["found"])
        self.assertIn("PDF read by built-in", r["source_text"])
        self.assertTrue(C.verify_quote(url, "the dictatorship for life came in 44 BC")["found"])  # line-end hyphen
        self.assertTrue(C.verify_quote(url, "HIJ and find the record")["found"])  # ToUnicode, ligature
        miss = C.verify_quote(url, "born on 13 July 100 BC")
        self.assertFalse(miss["found"])
        self.assertIn("pdftotext", miss["note"])

    def test_spacing_ignored_only_for_pdf(self):
        text = "Constitution of the United States W E THE P EOPLE of the United States, in Order to form"
        q = "We the People of the United States, in Order"
        self.assertFalse(C.quote_in(q, text)["found"])
        self.assertEqual(C.quote_in(q, text, pdf=True)["match"], "normalised, spacing ignored (PDF)")
        self.assertFalse(C.quote_in("WE THE PEOPLE", text, pdf=True)["found"])  # too short for the loose match

    def test_unreadable_pdf_is_not_a_miss(self):
        import hashlib
        import hw_net
        url = "https://example.org/scan.pdf"
        body = make_pdf(b"q 612 0 0 792 0 0 cm /Im1 Do Q", extra_fonts=False)
        (hw_net.home() / "pages").mkdir(parents=True, exist_ok=True)
        (hw_net.home() / "pages" / (hashlib.sha1(url.encode("utf-8")).hexdigest() + ".body")).write_bytes(body)
        r = C.verify_quote(url, "anything at all in this scan")
        self.assertIsNone(r["found"])
        self.assertIn("no readable text", r["error"])
        self.assertEqual(self.P.pdf_text(b"%PDF-1.4 garbage", external=False)[0], None)


if __name__ == "__main__":
    try:
        unittest.main(verbosity=1)
    finally:
        shutil.rmtree(TMP_HOME, ignore_errors=True)
