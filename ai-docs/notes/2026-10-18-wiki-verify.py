"""Wiki verification for historywright: every example on the wiki, run against a pinned commit of main.

    python ai-docs/notes/2026-10-18-wiki-verify.py [COMMIT] > ai-docs/notes/2026-10-18-wiki-verify.out.txt

historywright has no release yet (0.1.0 is unreleased; users install main), so this downloads the repository zip
at COMMIT from GitHub into a scratch folder (never the working tree) and runs each page's commands as the page
shows them, from a scratch run folder, with HW_HOME pointing at a fresh scratch home: no keys, no contact, no cache.

Network: the commands that read sources call the live public APIs that need no key (Wikidata, Wikipedia,
Pleiades, CHGIS, Crossref, OpenAlex without a key, the Wayback Machine, DILA's calendar download), once each,
at hw.py's own pace. Keyed services (WHG, OpenAlex with a key, Smithsonian, Europeana) are never called. Live
answers drift as the sources are edited; diffout against the saved output shows where.

Output sections are '## label' lines, as wikiwright's diffout and outputs expect. The scratch paths are masked as
<work> and <home>, today's date as <today>, the Python version as <python>. Commands on the pages read
`python hw.py ...`; here `hw.py` is the zip's skills/historywright/scripts/hw.py.
"""
import io
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile

COMMIT = sys.argv[1] if len(sys.argv) > 1 else "29bc39771fd0f7cc9c12d9c0d55766d25ec5fddd"
WORK = tempfile.mkdtemp(prefix="hwwiki_")
url = "https://codeload.github.com/m4bwav/historywright/zip/" + COMMIT
zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(url, timeout=120).read())).extractall(WORK)
REPO = os.path.join(WORK, "historywright-" + COMMIT)
HW = os.path.join(REPO, "skills", "historywright", "scripts", "hw.py")
RUN = os.path.join(WORK, "run")
HOME = os.path.join(WORK, "home")
os.makedirs(RUN)
os.makedirs(HOME)
ENV = dict(os.environ, HW_HOME=HOME, PYTHONIOENCODING="utf-8")
for k in ("OPENALEX_API_KEY", "WHG_TOKEN", "HW_CONTACT", "HW_RECORD", "HW_FIXTURES", "SMITHSONIAN_API_KEY",
          "EUROPEANA_API_KEY"):
    ENV.pop(k, None)
TODAY = time.strftime("%Y-%m-%d")
PY = "%d.%d.%d" % sys.version_info[:3]


def mask(text):
    for w, name in ((HOME, "<home>"), (RUN, ""), (REPO, "<repo>"), (WORK, "<work>")):
        for form in (w.replace("\\", "\\\\"), w, w.replace("\\", "/")):
            if name:
                text = text.replace(form, name)
            else:
                text = text.replace(form + "\\\\", "").replace(form + "\\", "").replace(form + "/", "").replace(form, ".")
    text = text.replace(TODAY, "<today>").replace('"python": "%s"' % PY, '"python": "<python>"')
    text = re.sub(r"<today>T\d\d:\d\d:\d\d", "<now>", text)
    return text.rstrip()


def show(label, value):
    print("## " + label)
    print(value)
    print()


def snippet(label, text):
    """Run a page's shell block line by line, as the page shows it, in the scratch run folder."""
    out = []
    for line in text.strip().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        args = shlex.split(line)
        if args[:2] == ["python", "hw.py"]:
            args = [sys.executable, HW] + args[2:]
        elif args[:1] == ["python"]:
            args = [sys.executable] + args[1:]
        p = subprocess.run(args, cwd=RUN, env=ENV, capture_output=True, text=True, encoding="utf-8", errors="replace")
        out.append(mask(p.stdout))
        if p.stderr.strip():
            out.append("[stderr] " + mask(p.stderr))
        out.append("[exit %d]" % p.returncode)
    show(label, "\n".join(out))


def write(name, text):
    path = os.path.join(RUN, name)
    os.makedirs(os.path.dirname(path) or RUN, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


show("installed", "historywright at %s from %s" % (COMMIT[:7], url))

# ---------------------------------------------------------------- Getting-Started
snippet("version", """
python hw.py --version
""")

snippet("doctor", """
python hw.py doctor
""")

snippet("keys-status", """
python hw.py keys status --offline
""")

# ---------------------------------------------------------------- Commands: Wikidata and Wikipedia
snippet("wd-search", """
python hw.py wd search "Julius Caesar" --limit 3
""")

snippet("wd-claims", """
python hw.py wd claims Q1048 --prop P569
""")

snippet("verify-qid", """
python hw.py verify qid Q1048 --label "Julius Caesar"
""")

snippet("wp-refs", """
python hw.py wp refs "Microsoft" --near "April 4, 1975"
""")

# ---------------------------------------------------------------- Commands: places
snippet("place-pleiades", """
python hw.py place search "Alesia" --source pleiades --limit 3
""")

snippet("place-chgis", """
python hw.py place search "長安" --source chgis --year 700
""")

# ---------------------------------------------------------------- Commands: scholarship and checks
snippet("oa-search", """
python hw.py oa search "Julius Caesar late Roman Republic" --limit 2
""")

snippet("doi-match", """
python hw.py doi 10.20381/ruor-23791 --title "Portfolios of Power: Julius Caesar in the Late Roman Republic" --author Ficocelli --year 2019
""")

snippet("doi-blended", """
python hw.py doi 10.20381/ruor-23791 --title "The Gallic War and the Roman Army" --author Ficocelli --year 2019
""")

snippet("verify-quote", """
python hw.py verify quote --url "https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Suetonius/12Caesars/Julius*.html" --quote "He died in the fifty-sixth year of his age"
""")

snippet("verify-url", """
python hw.py verify url "https://en.wikipedia.org/wiki/Julius_Caesar" "https://en.wikipedia.org/wiki/The_Fourth_Gallic_Diary_of_Caesar"
""")

snippet("src-wayback", """
python hw.py src wayback microsoft.com --limit 3
""")

# ---------------------------------------------------------------- How-Dates-Are-Computed
snippet("cal-caesar", """
python hw.py cal date "12 July 100 BC"
""")

snippet("cal-os-ru", """
python hw.py cal date "1917-10-25 O.S." --country RU
""")

snippet("cal-os-gb", """
python hw.py cal date "1732-02-11 O.S." --country GB
""")

snippet("cal-span-kangxi", """
python hw.py cal span "1661-02-05" "1722-12-20"
""")

snippet("cal-span-bc-ad", """
python hw.py cal span "44 BC" "AD 14"
""")

snippet("cal-auc", """
python hw.py cal date "709 AUC"
""")

snippet("cal-ah", """
python hw.py cal date "AH 1300"
""")

snippet("cal-jdn", """
python hw.py cal jdn 2299161
""")

snippet("cal-setup", """
python hw.py cal setup
""")

snippet("cal-era", """
python hw.py cal era 康熙
""")

snippet("cal-cjk", """
python hw.py cal cjk 崇禎三年四月初三
""")

# ---------------------------------------------------------------- Errors-and-Edge-Cases
snippet("err-year-zero", """
python hw.py cal date "0 AD"
""")

snippet("err-ides", """
python hw.py cal date "Ides of March 44 BC"
""")

snippet("err-ah-month", """
python hw.py cal date "1 Muharram 1 AH"
""")

snippet("err-ignored-words", """
python hw.py cal date "c. 100 BC"
""")

snippet("err-not-a-qid", """
python hw.py wd claims Caesar
""")

snippet("err-usage", """
python hw.py wd claims
""")

# ---------------------------------------------------------------- cache
write("entry.json", json.dumps({
    "question": "When was Julius Caesar born?",
    "reading": "birth date, Roman calendar as recorded",
    "answer": "12 or 13 July 100 BC",
    "confidence": "medium",
    "sources": [{"url": "https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Suetonius/12Caesars/Julius*.html",
                 "title": "Suetonius, Life of Julius Caesar 88 (LacusCurtius)", "retrieved": TODAY,
                 "quote": "He died in the fifty-sixth year of his age"}],
}, indent=1) + "\n")
snippet("cache", """
python hw.py cache put entry.json
python hw.py cache get "when was caesar born"
python hw.py cache list
""")

# ---------------------------------------------------------------- The-Research-Pack
shutil.copytree(os.path.join(REPO, "tests", "fixtures", "pack-good"), os.path.join(RUN, "pack-good"))
shutil.copytree(os.path.join(REPO, "tests", "fixtures", "pack-bad"), os.path.join(RUN, "pack-bad"))
snippet("pack-init", """
python hw.py pack init legionary --question "What did a legionary in Gaul wear about 52 BC?" --period "52 BC"
""")
show("pack-init-files", "\n".join(sorted(os.path.relpath(os.path.join(d, f), RUN).replace("\\", "/")
                                         for d, _, fs in os.walk(os.path.join(RUN, "legionary")) for f in fs)))

snippet("validate-good", """
python hw.py validate-pack pack-good
""")

snippet("validate-bad", """
python hw.py validate-pack pack-bad
""")

snippet("sources-offline", """
python hw.py verify sources pack-good/sources.json --offline
""")

snippet("sources-offline-any-url", """
python hw.py verify sources pack-good/sources.json --offline --any-url
""")

snippet("pack-csl", """
python hw.py pack csl pack-good
""")

# ---------------------------------------------------------------- historywright-sources
snippet("lint", """
python hw.py lint
""")

snippet("probe", """
python hw.py probe --only pleiades,chgis
""")

# ---------------------------------------------------------------- Recipes: hw.py from your own script
REIGN_PY = """
import json
import os
import subprocess
import sys

HW = os.environ.get("HW_PY", "hw.py")


def hw(*args):
    p = subprocess.run([sys.executable, HW, *args], capture_output=True, text=True, encoding="utf-8")
    return json.loads(p.stdout)


spans = {"formal reign": ("1661-02-05", "1722-12-20"), "era name 康熙": ("1662-02-18", "1722-12-20")}
for name, (start, end) in spans.items():
    s = hw("cal", "span", start, end)
    print(f"{name}: {s['years']} years, {s['months']} months, {s['rest_days']} days ({s['days']} days)")
""".lstrip("\n")
write("reign.py", REIGN_PY)
ENV["HW_PY"] = HW
snippet("recipe-script", """
python reign.py
""")

# ---------------------------------------------------------------- keys (last: it sets a contact in the scratch home)
snippet("keys-contact", """
python hw.py keys contact --set you@example.com
""")

shutil.rmtree(WORK, ignore_errors=True)
