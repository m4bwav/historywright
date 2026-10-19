"""PDF text for hw.py's quote checks: pdftotext when it is on PATH, else a small reader for the common case.

OpenAlex and repositories often link only a PDF. Decoding one as a web page gives noise, so a real quote would be
reported missing. The built-in reader handles Flate streams, object streams (PDF 1.5) and ToUnicode maps; scanned
pages and fonts with no ToUnicode map give too little text, and the caller then says the PDF is unreadable rather
than that the quote is absent.
"""

import os
import re
import shutil
import subprocess
import tempfile
import zlib

MAX_STREAM = 20 * 1024 * 1024  # decompressed bytes per stream; a zip bomb stops here
MAX_TOTAL = 80 * 1024 * 1024


def is_pdf(body, ctype=""):
    return b"%PDF-" in body[:1024] or "pdf" in (ctype or "").lower()


def readable(text):
    """Enough letters to be prose, not a scan or an undecoded font."""
    if not text or len(text.strip()) < 200:
        return False
    good = sum(1 for c in text if c.isalnum() or c.isspace() or c in ".,;:'\"()-")
    return good / len(text) > 0.8


def pdf_text(body, external=True):
    """(text, reader) or (None, why). Line-end hyphens are joined in a copy appended to the text, so a quote
    matches whether the PDF broke a word or not."""
    tried = []
    if external and os.environ.get("HW_PDFTOTEXT", "1") != "0" and shutil.which("pdftotext"):
        text = _pdftotext(body)
        if readable(text):
            return _dehyphen(text), "pdftotext"
        tried.append("pdftotext gave no readable text")
    try:
        text = builtin_text(body)
    except Exception as e:  # a malformed PDF must not crash a verify run
        text, tried = "", tried + ["built-in reader failed: %s" % type(e).__name__]
    if readable(text):
        return _dehyphen(text), "built-in"
    tried.append("built-in reader found no readable text (scanned pages, or fonts without a ToUnicode map)")
    if not shutil.which("pdftotext"):
        tried.append("install pdftotext (poppler) for a better reader")
    return None, "; ".join(tried)


def _dehyphen(text):
    joined = re.sub(r"(\w)-[ \t]*\r?\n[ \t]*(\w)", r"\1\2", text)
    return text if joined == text else text + "\n" + joined


def _pdftotext(body):
    fd, path = tempfile.mkstemp(suffix=".pdf")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(body)
        r = subprocess.run(["pdftotext", "-enc", "UTF-8", "-q", path, "-"], capture_output=True, timeout=90)
        return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


# ---------------------------------------------------------------- objects

_OBJ = re.compile(rb"(\d+)\s+\d+\s+obj\b(.*?)\bendobj", re.S)
_REF = re.compile(rb"(\d+)\s+\d+\s+R\b")


class _Budget:
    def __init__(self):
        self.left = MAX_TOTAL


def _inflate(data, budget):
    d = zlib.decompressobj()
    try:
        out = d.decompress(data, min(MAX_STREAM, max(budget.left, 0)))
    except zlib.error:
        return None
    budget.left -= len(out)
    return out


def _split(raw, budget):
    """(dictionary bytes, decoded stream bytes or None) of one object's body."""
    m = re.search(rb"\bstream\r?\n", raw)
    if not m:
        return raw, None
    head, data = raw[:m.start()], raw[m.end():]
    end = data.rfind(b"endstream")
    data = data[:end] if end >= 0 else data
    if b"/Subtype/Image" in head.replace(b" ", b""):
        return head, None
    filters = re.findall(rb"/(\w+Decode)", head)
    if filters == [b"FlateDecode"]:
        return head, _inflate(data, budget)
    return head, (data if not filters else None)


def objects(body):
    budget, objs = _Budget(), {}
    for m in _OBJ.finditer(body):
        objs[int(m.group(1))] = _split(m.group(2), budget)
    for num, (head, data) in list(objs.items()):
        if data is None or not re.search(rb"/Type\s*/ObjStm", head):
            continue
        n = re.search(rb"/N\s+(\d+)", head)
        first = re.search(rb"/First\s+(\d+)", head)
        if not (n and first):
            continue
        first = int(first.group(1))
        nums = [int(x) for x in data[:first].split()]
        pairs = list(zip(nums[0::2], nums[1::2]))
        for i, (onum, off) in enumerate(pairs):
            stop = pairs[i + 1][1] if i + 1 < len(pairs) else len(data) - first
            objs.setdefault(onum, (data[first + off: first + stop], None))
    return objs


def _deref(objs, raw):
    m = re.match(rb"\s*(\d+)\s+\d+\s+R\b", raw)
    return objs.get(int(m.group(1)), (b"", None))[0] if m else raw


def _dict_after(raw, key):
    """The << ... >> or reference that follows /key in raw."""
    m = re.search(rb"/" + key + rb"\s*", raw)
    if not m:
        return None
    rest = raw[m.end():]
    if rest.startswith(b"<<"):
        depth, i = 0, 0
        while i < len(rest) - 1:
            two = rest[i:i + 2]
            if two == b"<<":
                depth, i = depth + 1, i + 2
                continue
            if two == b">>":
                depth, i = depth - 1, i + 2
                if depth == 0:
                    return rest[:i]
                continue
            i += 1
        return rest
    r = _REF.match(rest)
    return rest[:r.end()] if r else None


# ---------------------------------------------------------------- fonts

def _hex(s):
    s = re.sub(rb"[^0-9A-Fa-f]", b"", s).decode("ascii")
    return bytes.fromhex(s if len(s) % 2 == 0 else s + "0")


def _utf16(b):
    return b.decode("utf-16-be", "replace")


def cmap(data):
    """{code bytes: text} and the code width in bytes from a ToUnicode CMap."""
    out, width = {}, None
    for block in re.findall(rb"begincodespacerange(.*?)endcodespacerange", data, re.S):
        h = re.findall(rb"<([0-9A-Fa-f]+)>", block)
        if h:
            width = len(h[0]) // 2
    for block in re.findall(rb"beginbfchar(.*?)endbfchar", data, re.S):
        for src, dst in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]*)>", block):
            out[_hex(src)] = _utf16(_hex(dst))
    for block in re.findall(rb"beginbfrange(.*?)endbfrange", data, re.S):
        for lo, hi, rest in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*(<[0-9A-Fa-f]*>|\[[^\]]*\])", block):
            w, a, b = len(lo) // 2, int(lo, 16), int(hi, 16)
            if b - a > 65535:
                continue
            if rest.startswith(b"["):
                for i, d in enumerate(re.findall(rb"<([0-9A-Fa-f]*)>", rest)):
                    out[(a + i).to_bytes(w, "big")] = _utf16(_hex(d))
            else:
                base = _hex(rest[1:-1])
                start = int.from_bytes(base, "big")
                for i in range(b - a + 1):
                    out[(a + i).to_bytes(w, "big")] = _utf16((start + i).to_bytes(len(base), "big"))
    return out, (width or (len(next(iter(out))) if out else 1))


class Font:
    def __init__(self, objs, raw):
        raw = _deref(objs, raw)
        self.map, self.width = {}, 2 if re.search(rb"/Subtype\s*/Type0", raw) else 1
        tu = re.search(rb"/ToUnicode\s+(\d+)\s+\d+\s+R", raw)
        data = objs.get(int(tu.group(1)), (b"", None))[1] if tu else None
        if data:
            self.map, self.width = cmap(data)

    def decode(self, s):
        if not self.map:
            return "" if self.width == 2 else s.decode("cp1252", "replace")
        w, out = self.width, []
        for i in range(0, len(s) - w + 1, w):
            code = s[i:i + w]
            out.append(self.map.get(code, "" if w == 2 else code.decode("cp1252", "replace")))
        return "".join(out)


def _fonts(objs, res_raw, cache):
    fonts = {}
    res = _deref(objs, res_raw or b"")
    fd = _dict_after(res, b"Font")
    if fd:
        fd = _deref(objs, fd)
        for name, num in re.findall(rb"/([^\s/<>\[\]()]+)\s+(\d+)\s+\d+\s+R", fd):
            key = int(num)
            if key not in cache:
                cache[key] = Font(objs, b"%d 0 R" % key)
            fonts[name] = cache[key]
    return fonts


# ---------------------------------------------------------------- pages and content streams

def _pages(objs):
    """[(page dict, inherited resources)] in reading order, from the catalog's page tree when there is one."""
    root = next((h for h, _ in objs.values() if re.search(rb"/Type\s*/Catalog", h)), None)
    out, seen = [], set()

    def walk(num, res):
        if num in seen or num not in objs:
            return
        seen.add(num)
        head = objs[num][0]
        res = _dict_after(head, b"Resources") or res
        if re.search(rb"/Type\s*/Pages", head):
            kids = re.search(rb"/Kids\s*\[(.*?)\]", head, re.S)
            for k in _REF.findall(kids.group(1) if kids else b""):
                walk(int(k), res)
        elif re.search(rb"/Type\s*/Page\b", head):
            out.append((head, res))

    pages = re.search(rb"/Pages\s+(\d+)\s+\d+\s+R", root or b"")
    if pages:
        walk(int(pages.group(1)), None)
    if not out:
        out = [(h, _dict_after(h, b"Resources")) for h, _ in objs.values() if re.search(rb"/Type\s*/Page\b", h)]
    return out


_ESC = {ord("n"): b"\n", ord("r"): b"\r", ord("t"): b"\t", ord("b"): b"\b", ord("f"): b"\f"}
_DELIM = b"()<>[]{}/%"


def _literal(data, i):
    """The bytes of the literal string starting after '(' at i, and the index past its ')'."""
    out, depth, n = bytearray(), 1, len(data)
    while i < n:
        c = data[i]
        if c == 0x5C and i + 1 < n:  # backslash
            d = data[i + 1]
            if d in _ESC:
                out += _ESC[d]
                i += 2
            elif 0x30 <= d <= 0x37:
                j = i + 1
                while j < n and j < i + 4 and 0x30 <= data[j] <= 0x37:
                    j += 1
                out.append(int(data[i + 1:j], 8) & 0xFF)
                i = j
            elif d in (0x0A, 0x0D):
                i += 3 if data[i + 1:i + 3] == b"\r\n" else 2
            else:
                out.append(d)
                i += 2
            continue
        if c == 0x28:
            depth += 1
        elif c == 0x29:
            depth -= 1
            if depth == 0:
                return bytes(out), i + 1
        out.append(c)
        i += 1
    return bytes(out), n


def tokens(data):
    i, n = 0, len(data)
    while i < n:
        c = data[i:i + 1]
        if c.isspace():
            i += 1
        elif c == b"%":
            j = data.find(b"\n", i)
            i = n if j < 0 else j
        elif c == b"(":
            s, i = _literal(data, i + 1)
            yield ("str", s)
        elif data[i:i + 2] == b"<<" or data[i:i + 2] == b">>":
            yield ("op", data[i:i + 2])
            i += 2
        elif c == b"<":
            j = data.find(b">", i)
            j = n if j < 0 else j
            yield ("str", _hex(re.sub(rb"\s", b"", data[i + 1:j])))
            i = j + 1
        elif c in (b"[", b"]"):
            yield (c.decode(), None)
            i += 1
        else:
            j = i + 1
            while j < n and not data[j:j + 1].isspace() and data[j] not in _DELIM:
                j += 1
            word = data[i:j] if j > i else data[i:i + 1]
            i = max(j, i + 1)
            if word == b"BI":  # inline image: skip its binary data
                k = re.search(rb"\sEI(?=\s|$)", data[i:])
                i = n if not k else i + k.end()
                continue
            if word.startswith(b"/"):
                yield ("name", word[1:])
            elif re.match(rb"^[+-]?(\d+\.?\d*|\.\d+)$", word):
                yield ("num", float(word))
            else:
                yield ("op", word)


def content_text(data, fonts):
    out, stack, arr, font = [], [], None, None
    blank = Font({}, b"")
    for kind, val in tokens(data):
        if kind == "[":
            arr = []
        elif kind == "]":
            stack.append(("arr", arr or []))
            arr = None
        elif arr is not None:
            arr.append((kind, val))
        elif kind != "op":
            stack.append((kind, val))
        else:
            f = font or blank
            if val == b"Tf" and len(stack) >= 2 and stack[-2][0] == "name":
                font = fonts.get(stack[-2][1])
            elif val == b"Tj" and stack and stack[-1][0] == "str":
                out.append(f.decode(stack[-1][1]))
            elif val in (b"'", b'"') and stack and stack[-1][0] == "str":
                out.append("\n" + f.decode(stack[-1][1]))
            elif val == b"TJ" and stack and stack[-1][0] == "arr":
                for k, v in stack[-1][1]:
                    if k == "str":
                        out.append(f.decode(v))
                    elif k == "num" and v < -180:
                        out.append(" ")
            elif val in (b"Td", b"TD") and len(stack) >= 2 and stack[-1][0] == "num":
                out.append("\n" if stack[-1][1] != 0 else " ")
            elif val in (b"T*", b"Tm", b"ET"):
                out.append("\n")
            stack = []
    return "".join(out)


def builtin_text(body):
    objs = objects(body)
    cache, parts = {}, []
    for head, res in _pages(objs):
        fonts = _fonts(objs, res, cache)
        c = re.search(rb"/Contents\s*(\[[^\]]*\]|\d+\s+\d+\s+R)", head)
        refs = [int(x) for x in _REF.findall(c.group(1))] if c else []
        data = b"\n".join(objs[r][1] or b"" for r in refs if r in objs)
        parts.append(content_text(data, fonts))
    return "\n\n".join(parts)
