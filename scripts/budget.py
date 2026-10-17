"""Size budget for historywright: what every session loads (skill descriptions) and what an install weighs.

Run from the repository root: python scripts/budget.py   (red fails; yellow is reported)
Bands (ai-docs/decisions/2026-10-17-step1-rulings.md, ruling 8): install green under 400 KB, yellow to 1 MB;
era outline green under 12 KB, yellow to 25 KB; descriptions green under 600 tokens in all, yellow to 900.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INSTALLED = ["skills", ".claude-plugin", "README.md", "LICENSE", "SECURITY.md"]


def band(v, green, yellow):
    return "green" if v < green else ("yellow" if v <= yellow else "red")


def size(p):
    if p.is_file():
        return p.stat().st_size
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file() and "__pycache__" not in f.parts)


def main():
    rows = []
    inst = sum(size(ROOT / p) for p in INSTALLED if (ROOT / p).exists())
    rows.append(("install size", "%d KB" % (inst // 1024), band(inst, 400 * 1024, 1024 * 1024)))
    eras = ROOT / "skills" / "historywright-sources" / "references" / "eras.md"
    e = eras.stat().st_size if eras.exists() else 0
    rows.append(("era outline", "%d bytes" % e, band(e, 12000, 25000)))
    chars = 0
    for f in (ROOT / "skills").glob("*/SKILL.md"):
        m = re.search(r'(?m)^description:\s*"?(.*?)"?\s*$', f.read_text(encoding="utf-8"))
        chars += len(m.group(1)) if m else 0
    tokens = chars // 4
    rows.append(("descriptions (every session)", "~%d tokens" % tokens, band(tokens, 600, 900)))
    for name, val, b in rows:
        print("%-30s %-14s %s" % (name, val, b))
    reds = [r for r in rows if r[2] == "red"]
    if reds:
        print("RED: %s" % ", ".join(r[0] for r in reds))
    return 1 if reds else 0


if __name__ == "__main__":
    sys.exit(main())
