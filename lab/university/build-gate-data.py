#!/usr/bin/env python3
"""Build gate-data.json — the gated step sequence for every
non-language Exolex University class (Bill's order, Nov 16 2026:
every class lets the student talk/type an answer back, checks it
against the class's own material, and does not advance on a miss).

Steps are generated ONLY from material the catalogue itself carries:
  · paper classes — the headline values each paper's own result line
    reports (NAME = VALUE pairs), graded as numbers with tolerance;
  · units classes — the syllabus's own unit order (which unit comes
    next), graded by content words;
  · every class — its own set homework problem as the capstone,
    graded by keyword groups drawn from the worked answer the
    catalogue already carries.
A step whose answer cannot be grounded in that material is NOT
generated. Classes left with too little grounded material are listed
in GATE-COVERAGE.md with the reason — never padded with invented keys.

Hand-checked classes (the College flagships and the authored classes)
can be corrected or extended through gate-overrides.json:
  {"<classId>": {"steps": [ ...full replacement... ]},
   "<classId>": {"add": [ ...extra steps appended before capstone... ]}}

Audio: classes that already carry a recorded lesson (cls.audio) get
per-step clip paths (audio/gate/<id>/step-<n>.mp3, praise-<n>.mp3),
filled in by build-gate-audio.py in the professor's own voice. Every
other class presents on the board; its professor's praise and
re-teaching are on-screen text in the same flow. The audio pass is
idempotent and can be extended catalogue-wide later — the paths are
only written where the recorded-lesson set makes the voice real.
"""
import json, os, re, math
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

cat = json.load(open('catalogue.json'))
try:
    trainer = json.load(open('trainer-data.json'))['classes']
except Exception:
    trainer = {}
try:
    overrides = json.load(open('gate-overrides.json'))
except Exception:
    overrides = {}

# ---------------------------------------------------------------- papers
PAIR = re.compile(
    r'([A-Za-z][A-Za-z0-9_]{0,40}(?: [A-Za-z0-9_]{1,24}){0,3}?)\s*=\s*'
    r'(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)')
BAD_NAME = {'result', 'state', 'checks', 'title', 'doi', 'author',
            'licence', 'license', 'record', 'values', 'value', 'squared',
            'cubed', 'epsilon', 'equals', 'equal'}

def clean_text(t, limit=430):
    t = re.sub(r'\s+', ' ', (t or '')).strip()
    if len(t) <= limit:
        return t
    cut = t[:limit]
    end = max(cut.rfind('. '), cut.rfind('; '))
    return (cut[:end + 1] if end > 120 else cut).strip()

def is_record_dump(r):
    return ('- Record:' in r) or ('Checks:' in r) or r.lstrip().startswith('- Title:')

def paper_pairs(r):
    """(name, value, disp) pairs from a paper's own result line."""
    if not r or is_record_dump(r):
        return []
    m = re.search(r'[Hh]eadline', r)
    seg = r[m.start():m.start() + 700] if m else r[:700]
    out, seen = [], set()
    for name, val in PAIR.findall(seg):
        name = name.strip()
        low = name.lower()
        if low in BAD_NAME or len(name) < 2 or 'http' in low or 'verbatim' in low:
            continue
        # prose fragments that are not quantity names ("... in Mpc at
        # epsilon = 0.1" names nothing a student could be asked for)
        if re.search(r'\b(at|of|in|by|to) (epsilon|the|a|an)$', low):
            continue
        if re.match(r'^(at|of|in|by|to|from|with) ', low):
            continue
        if low in seen:
            continue
        seen.add(low)
        try:
            out.append((name, float(val), val))
        except ValueError:
            pass
    # prefer machine-named quantities (electron_T_MeV) over prose
    # fragments when a paper reports both
    out.sort(key=lambda p: 0 if '_' in p[0] else 1)
    return out

# ---------------------------------------------------------------- keywords
STOP = set("""a an the and or of to in on for with without is are was were be been
being it its this that these those from by at as into than then so such no not
one two can could would should may might must will shall do does did have has had
answer strong paper papers claim stated states result results word words wording
first second would check test name names say says said make makes made use used
using way ways thing things something anything really just also more most other
another own your you yours we our they their he she his her them him what when
where which who whom how why all any each per via about above after before
between under over again further once here there both few many much own same
only very too""".split())

NOISE = set("""itself accept natural worked example neither because model notice
people content through pulled asking answer answers version almost always
letter want wants highest hardest taller suspect draw every equal suppose
here there then than that this with from have has had been were was are
their they them what when which while would could should there""".split())

def capstone_keywords(worked):
    groups = []
    # numbers the worked answer itself leans on
    for num in re.findall(r'\d+(?:\.\d+)?(?:[eE][+-]?\d+)?', worked):
        groups.append([num])
    # capitalised terms (names, places, coined terms)
    for phrase in re.findall(r'\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)\b', worked):
        low = phrase.lower()
        if low not in STOP and low not in NOISE and len(phrase) >= 4:
            groups.append([phrase])
    # distinctive content words
    words = re.findall(r"[a-z][a-z\-']{5,}", worked.lower())
    seen = set()
    for w in words:
        w = w.strip("-'")
        if w in STOP or w in NOISE or w in seen:
            continue
        seen.add(w)
        variants = {w}
        if w.endswith('s'):
            variants.add(w[:-1])
        if w.endswith('ing'):
            variants.add(w[:-3])
        groups.append(sorted(variants))
        if len(groups) >= 8:
            break
    # dedupe, cap
    out, seen = [], set()
    for g in groups:
        key = g[0].lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(g)
    return out[:8]

# ---------------------------------------------------------------- why lines
WHY_VALUE = ("You are doing this because a number you can produce from "
             "memory — and defend — is worth ten you have only seen glide past.")
WHY_ORDER = ("You are doing this because the order is the argument: each "
             "unit in this class stands on the one before it.")
WHY_CAP = ("You are doing this because this is the class's real problem — "
           "the one your professor set. It is answered here, in session, "
           "not taken away as homework.")

PRAISE = [
    "Exactly right — that is the material, produced in your own voice. On we go.",
    "Correct. You did not just see that — you can produce it. That is the difference.",
    "Right. Hold onto that one; the rest of the class leans on it.",
]
RETRY = ["Not yet — let us come at that piece from another side."]

def fmt_val(v, disp):
    return disp

def value_steps(cls, prof):
    steps = []
    used_values = set()
    for p in cls['papers']:
        pairs = paper_pairs(p.get('r'))
        if not pairs:
            continue
        name, val, disp = pairs[0]
        if val in used_values:
            # the same value again (a paper restating epsilon = 0.1 four
            # ways) is one check, not four
            alt = [pr for pr in pairs if pr[1] not in used_values]
            if not alt:
                continue
            name, val, disp = alt[0]
        used_values.add(val)
        r = clean_text(p['r'])
        teach = "%s. Its stated result: %s" % (p['t'], r)
        plain = "; ".join("%s = %s" % (n, d) for n, v, d in pairs[:3])
        teach2 = ("Look at it another way — the same paper, its own numbers "
                  "stated plainly: %s. Now say the value back to me, in "
                  "figures, any honest form: as printed, rounded, or "
                  "written out in full." % plain)
        steps.append({
            "teach": teach, "teach2": teach2,
            "q": "From that paper: what headline value does it report for %s?" % name,
            "kind": "number", "answer": val, "disp": disp, "tol": 0.03,
            "why": WHY_VALUE, "substantive": True,
        })
        if len(steps) >= 5:
            break
    return steps

def order_steps(cls, section, prof):
    units = cls['units']
    n = len(units)
    if cls.get('lesson'):
        intro = clean_text(cls['lesson'], 380)
    else:
        intro = ("%s I am %s, and this is %s — a class in %s at Exolex "
                 "University. The syllabus, in order: %s." %
                 (prof.get('greeting', 'Welcome.'), prof['name'], cls['title'],
                  section['name'], ' · '.join(units)))
    steps = []
    idxs = list(range(min(3, n - 1)))
    if n >= 5 and (n - 2) not in idxs:
        idxs.append(n - 2)
    for k, i in enumerate(idxs):
        teach = intro if k == 0 else (
            "Unit %d of %d: %s. We take them in order, because each one "
            "stands on the last." % (i + 1, n, units[i]))
        teach2 = ("The whole order, on the board: %s. Now — after '%s', "
                  "what comes next?" %
                  (' · '.join("%d. %s" % (j + 1, u) for j, u in enumerate(units)),
                   units[i]))
        steps.append({
            "teach": teach, "teach2": teach2,
            "q": "The units run in order. After '%s', which unit comes next?" % units[i],
            "kind": "title", "answer": units[i + 1],
            "why": WHY_ORDER, "substantive": True,
        })
    return steps

def capstone_step(cls):
    hw = cls.get('homework') or {}
    q, worked = hw.get('q', ''), hw.get('worked', '')
    groups = capstone_keywords(worked)
    if len(groups) < 3 or not q:
        return None
    first = re.split(r'(?<=[.!?])\s+', worked.strip())[0]
    return {
        "teach": ("Now the class's own problem — the one your professor "
                  "set for this room. Take your time. Say it out loud or "
                  "type it; either door is open."),
        "teach2": "Think about it this way: %s" % first,
        "q": q, "kind": "keywords", "keywords": groups,
        "need": max(2, min(3, math.ceil(len(groups) / 2))),
        "why": WHY_CAP, "substantive": True,
    }

def orientation_steps(cls):
    steps = []
    if cls['papers']:
        p0 = cls['papers'][0]
        steps.append({
            "teach": ("The syllabus is real papers, deposited and citable. "
                      "The first is '%s'." % p0['t']),
            "teach2": ("It is on the syllabus card, with its DOI: %s. "
                       "Say the DOI back to me." % p0['doi']),
            "q": "What is the DOI of '%s'?" % p0['t'],
            "kind": "exact", "answer": p0['doi'],
            "why": ("You are doing this because a citation you can produce "
                    "is a paper you can actually go and read."),
            "substantive": False,
        })
    return steps

# ---------------------------------------------------------------- build
classes = {}
report = {}
for s in cat['sections']:
    for cls in s['classes']:
        cid = cls['id']
        if cid in trainer or s['id'] == 'languages':
            report[cid] = ('language', 'taught by the listen-and-repeat trainer')
            continue
        prof = cls.get('professor') or s.get('professor')
        steps = []
        if cls.get('units'):
            steps += order_steps(cls, s, prof)
        else:
            steps += value_steps(cls, prof)
            if len(steps) < 2:
                steps = orientation_steps(cls) + steps
        cap = capstone_step(cls)
        ov = overrides.get(cid)
        if ov and 'capstone' in ov:
            cap = ov['capstone']
        if ov and ov.get('add'):
            steps += ov['add']
        if cap:
            steps.append(cap)
        if ov and ov.get('steps') is not None:
            steps = ov['steps']
        steps = steps[:8]
        substantive = sum(1 for st in steps if st.get('substantive'))
        if not steps:
            report[cid] = ('none', 'no grounded check could be built from its material')
            continue
        entry = {"steps": steps, "praise": PRAISE, "retry": RETRY}
        if cls.get('audio'):
            base = "audio/gate/%s/" % cid
            entry['audioBase'] = base
            for i, st in enumerate(steps):
                st['audio'] = base + "step-%d.mp3" % i
            entry['praiseAudio'] = [base + "praise-%d.mp3" % i for i in range(len(PRAISE))]
            entry['retryAudio'] = [base + "retry-0.mp3"]
        classes[cid] = entry
        report[cid] = ('full' if substantive >= 3 else
                       'partial' if substantive >= 1 else 'orientation',
                       '%d steps, %d substantive' % (len(steps), substantive))

out = {"generated": "build-gate-data.py — gated steps for every non-language class",
       "classes": classes}
with open('gate-data.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

counts = Counter(v[0] for v in report.values())
print('gate-data.json:', len(classes), 'gated classes of',
      sum(1 for s in cat['sections'] for _ in s['classes']), 'total')
print('coverage:', dict(counts))

with open('GATE-COVERAGE.md', 'w', encoding='utf-8') as f:
    f.write("# Gate coverage — build-gate-data.py\n\n")
    f.write("Every non-language class gets a gated lesson built only from "
            "its own material.\n\n")
    for k in ('full', 'partial', 'orientation', 'none', 'language'):
        f.write("## %s (%d)\n\n" % (k, counts.get(k, 0)))
        for s in cat['sections']:
            for cls in s['classes']:
                if report[cls['id']][0] == k:
                    f.write("- `%s` (%s) — %s\n" % (cls['id'], s['id'], report[cls['id']][1]))
        f.write("\n")
print('GATE-COVERAGE.md written')
