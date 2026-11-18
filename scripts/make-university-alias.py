#!/usr/bin/env python3
"""University alias /exolex-university/ (SEO change list section 1.2).

- Copies lab/university/index.html to exolex-university/index.html.
- Rewrites the relative asset paths the change list names to root-absolute:
  the five script srcs (uni-core, trainer-core, gate-core, gate-ui,
  lessons30-ui), the two hrefs (../ -> /lab/, ../room/ -> /lab/room/),
  and the three data fetches (prior-balance.json, trainer-data.json,
  catalogue.json).
- ALSO adds <base href="/lab/university/"> to the alias. This is the part
  the change list did not foresee: the data files the page fetches
  (catalogue.json, trainer-data.json, gate-data.json, lessons30/*.json)
  carry ~1,500 relative asset paths of their own (audio/..., portraits/...),
  set as <audio> / <img> srcs by the page's JS. An HTML rewrite cannot
  reach those; <base> resolves every relative URL in the document against
  /lab/university/, so the lesson audio, the trainer/gate clips and the
  professor portraits all load at the alias. It is safe here: every
  href="#" on the page is a JS-handled button (all seven call
  e.preventDefault()), and there is no in-page anchor navigation, so
  <base> cannot pull a click away to another URL.
- Sets canonical https://daveexolex.com/exolex-university/ and a meta
  description on BOTH the alias and lab/university/index.html (the
  original carries neither today; the alias is the canonical URL).
Run from the repo root:  python3 scripts/make-university-alias.py
"""
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "lab", "university", "index.html")
DST_DIR = os.path.join(ROOT, "exolex-university")
DST = os.path.join(DST_DIR, "index.html")
CANON = "https://daveexolex.com/exolex-university/"
DESC = ("Exolex University is free and open to everyone \u2014 classes with audio "
        "lessons, full text, and questions you can be tested on. "
        "No admissions wall, no degree claim.")
assert 140 <= len(DESC) <= 160, len(DESC)

ORIG_ADD = ('<link rel="canonical" href="' + CANON + '">\n'
            '<meta name="description" content="' + DESC + '">')
TITLE = "<title>Exolex University \u2014 The Catalogue &amp; The Classrooms</title>"

REWRITES = [
    ('<script src="uni-core.js?v=', '<script src="/lab/university/uni-core.js?v='),
    ('<script src="trainer-core.js?v=', '<script src="/lab/university/trainer-core.js?v='),
    ('<script src="gate-core.js?v=', '<script src="/lab/university/gate-core.js?v='),
    ('<script src="gate-ui.js?v=', '<script src="/lab/university/gate-ui.js?v='),
    ('<script src="lessons30-ui.js?v=', '<script src="/lab/university/lessons30-ui.js?v='),
    ('href="../room/"', 'href="/lab/room/"'),
    ('href="../"', 'href="/lab/"'),
    ("var PRIOR_URL = 'prior-balance.json';",
     "var PRIOR_URL = '/lab/university/prior-balance.json';"),
    ("fetch('trainer-data.json' + VQ)", "fetch('/lab/university/trainer-data.json' + VQ)"),
    ("fetch('catalogue.json' + VQ)", "fetch('/lab/university/catalogue.json' + VQ)"),
]


def replace_once(text, old, new, label):
    n = text.count(old)
    if n == 0:
        if new in text:
            print("  already applied: %s" % label)
            return text
        raise SystemExit("FAILED: not found (%s): %r" % (label, old[:100]))
    if n > 1:
        raise SystemExit("FAILED: %s found %d times (want 1)" % (label, n))
    print("  replaced: %s" % label)
    return text.replace(old, new)


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    text = open(DST, encoding="utf-8").read()
    # Head: base + canonical + description (right after the title).
    # Only add what is missing (a re-run copies the original, which may
    # already carry the canonical/description from a prior run).
    head_bits = []
    if '<base href="/lab/university/">' not in text:
        head_bits.append('<base href="/lab/university/">')
    if 'rel="canonical"' not in text:
        head_bits.append('<link rel="canonical" href="' + CANON + '">')
    if 'name="description"' not in text:
        head_bits.append('<meta name="description" content="' + DESC + '">')
    if head_bits:
        text = replace_once(text, TITLE, TITLE + "\n" + "\n".join(head_bits),
                            "alias head (%s)" % ", ".join(head_bits)[:60])
    else:
        print("  alias head already complete")
    for old, new in REWRITES:
        text = replace_once(text, old, new, old[:60])
    # Verification: the named relative paths are gone from the alias.
    for bad in ('src="uni-core.js', 'src="trainer-core.js', 'src="gate-core.js',
                'src="gate-ui.js', 'src="lessons30-ui.js', 'href="../room/"',
                'href="../"', "'prior-balance.json'", "'trainer-data.json'",
                "'catalogue.json'"):
        assert bad not in text, "still present in alias: %s" % bad
    assert '<base href="/lab/university/">' in text
    assert 'rel="canonical" href="' + CANON + '"' in text
    assert 'name="description" content="' + DESC + '"' in text
    open(DST, "w", encoding="utf-8").write(text)
    print("OK: %s (%d bytes)" % (DST, len(text)))

    # Original: canonical + description (it has neither today).
    orig = open(SRC, encoding="utf-8").read()
    if 'rel="canonical"' in orig or 'name="description"' in orig:
        print("  original already has canonical/description — leaving it")
        return
    orig = replace_once(orig, TITLE, TITLE + "\n" + ORIG_ADD, "original head (canonical + description)")
    open(SRC, "w", encoding="utf-8").write(orig)
    print("OK: %s updated (canonical + description)" % SRC)


if __name__ == "__main__":
    main()
