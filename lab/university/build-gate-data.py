#!/usr/bin/env python3
"""Build gate-data.json — for every non-language Exolex University
class: a LESSON taught first, then end-of-class QUESTIONS.

Bill's model (Nov 16 2026, sharpened 03:50 EST): teach a real class
first, then ask questions at the end of the class to pass it —
every question strictly on what was taught; nobody can be expected
to just know answers. The old step types that quizzed untaught
material (syllabus-order recall, DOI recall) are deleted.

  · The lesson is the class's own material, presented in order:
    its recorded script where one exists, its units one by one,
    its papers with their stated results, and its set problem
    presented as the professor's worked example.
  · The questions are drawn only from that lesson: headline values
    the lesson's papers report (numbers, graded with tolerance),
    the one-line unpackings the lesson's units carry (keyword
    groups), and the class's set problem as the capstone (keyword
    groups from the worked answer the lesson presented).
  · THE CONTAINMENT AUDIT enforces the law mechanically: a question
    ships only if its answer is extractable from the lesson text.
    Failures are dropped and counted — never shipped, never padded.

Hand-checked classes can be corrected through gate-overrides.json:
  {"<classId>": {"lesson": [...], "steps": [...full replacements...]},
   "<classId>": {"capstone": {...}},
   "<classId>": {"add": [ ...extra questions; their passages join
   the lesson, so they are taught before they are asked... ]}}

Audio: classes that already carry a recorded lesson (cls.audio) get
per-passage and per-question clip paths (audio/gate/<id>/lesson-<n>.mp3,
step-<n>.mp3, praise-<n>.mp3, retry-<n>.mp3), filled in by
build-gate-audio.py in the professor's own voice. Every other class
presents on the board. The audio pass is idempotent.
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
# The retry line never promises "another side" it does not deliver:
# the re-teach (teach2) and, after a second miss, the walkthrough
# (walk) ARE the other side, on the board, every time. (Bill, Nov 16:
# stuck on AI Fundamentals Q1 — the old line claimed a different side
# and gave none.)
RETRY = [
    "Not yet — that is not what the material says.",
    "Not yet. Stay with the piece.",
]

def board_of(units):
    """The course's units as one numbered board string."""
    return ' · '.join("%d. %s" % (j + 1, u) for j, u in enumerate(units))

def heads_of(groups):
    """The display heads of keyword groups — the ideas an answer
    stands on. Bare one/two-digit numbers (fragments of 'N + 1')
    read as noise in prose; they stay in the CHECK, just not in
    the sentence that names the ideas."""
    heads = [g[0] for g in groups
             if not (re.fullmatch(r'\d+(\.\d+)?', g[0]) and len(g[0]) <= 2)]
    return ' · '.join(heads or [g[0] for g in groups])

def sentences(text, cap=4, limit=640):
    """A text's own sentences, in order, trimmed to a sane length."""
    parts = [s.strip() for s in
             re.split(r'(?<=[.!?])\s+', (text or '').strip()) if s.strip()]
    out = []
    total = 0
    for s in parts[:cap]:
        if total + len(s) > limit and out:
            break
        out.append(s)
        total += len(s)
    return out

def fmt_val(v, disp):
    return disp

def paper_chunk(p):
    """A paper presented as a lesson passage: its title and its own
    stated result. This is taught material — the questions at the end
    of the class may draw on it, and on nothing else."""
    return "'%s'. Its stated result: %s" % (p['t'], clean_text(p['r'], 700))

def value_questions(cls):
    """End-of-class questions on the lesson's papers. The question's
    own teach is a POINTER back to the lesson — it does not carry
    the answer; the answer lives in the lesson passage, and the
    containment audit (below) proves it is there before the
    question may ship. On a miss, the re-teach shows the exact
    taught passage plus a different-angle presentation (the
    quantities in a clean row)."""
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
        plain = "; ".join("%s = %s" % (n, d) for n, v, d in pairs[:3])
        teach = ("From the lesson: the paper '%s' and the result it "
                 "stated. One of the quantities it names is %s."
                 % (p['t'], name))
        teach2 = ("Back to the exact passage, from the lesson: %s "
                  "And the same result with the prose stripped away — "
                  "just the quantities standing in a row: %s. Find %s "
                  "in that row; the value beside it is the one this "
                  "question asks for. Say it in figures, any honest "
                  "form: as printed, rounded, or written out in full."
                  % (paper_chunk(p), plain, name))
        walk = ("Walk it through with me, step by step. (1) In the "
                "lesson, the paper '%s' stated its result. (2) That "
                "result pairs names with values: %s. (3) This question "
                "asks for the value paired with %s. (4) In that row, "
                "%s stands beside %s — so the answer the lesson gives "
                "is %s. Now it is yours: say that value, in any honest "
                "form." % (p['t'], plain, name, name, disp, disp))
        steps.append({
            "teach": teach, "teach2": teach2, "walk": walk,
            "q": ("From the lesson — the paper '%s': what value does "
                  "its stated result report for %s?" % (p['t'], name)),
            "kind": "number", "answer": val, "disp": disp, "tol": 0.03,
            "why": WHY_VALUE, "substantive": True,
        })
        if len(steps) >= 5:
            break
    return steps

# ---------------------------------------------------------------- lesson
# Bill's model (Nov 16, sharpened 03:50 EST): TEACH A REAL CLASS
# FIRST, THEN ask questions at the end of the class to pass it —
# every question strictly on what was taught. So every class now
# ships a LESSON (presentation passages, in order) and a set of
# end-of-class QUESTIONS. The old step types that quizzed untaught
# material — syllabus-order recall, DOI recall — are gone entirely.

def script_chunks(text, size=430):
    """A lesson script, chunked at sentence boundaries."""
    out, cur = [], ''
    for s in sentences(text, cap=99, limit=10 ** 9):
        if cur and len(cur) + len(s) + 1 > size:
            out.append(cur)
            cur = s
        else:
            cur = (cur + ' ' + s).strip()
    if cur:
        out.append(cur)
    return out

def worked_chunk(cls):
    """The class's set problem, presented in the lesson as the
    professor's worked example — the capstone question at the end
    asks the student to work the same problem in their own words."""
    hw = cls.get('homework') or {}
    if hw.get('q') and hw.get('worked'):
        return ("Now my worked example — this class's set problem, "
                "worked in full. The problem: %s The worked answer: %s"
                % (hw['q'], hw['worked']))
    return None

def lesson_papers(cls, prof):
    chunks = ["Settle in. I am %s, and this is %s. This class is built "
              "on real papers — deposited, citable work. I will present "
              "each paper and what it reports; that presentation is "
              "the lesson. At the end I will ask you questions on what "
              "was taught here — nothing else."
              % (prof['name'], cls['title'])]
    # only papers that carry a stated result can be taught (2,534
    # catalogue papers are title-and-DOI only — nothing to present,
    # and nothing a question could honestly draw on)
    for p in [p for p in cls['papers'] if p.get('r')][:6]:
        chunks.append(paper_chunk(p))
    wc = worked_chunk(cls)
    if wc:
        chunks.append(wc)
    return chunks

def lesson_units(cls, section, prof):
    chunks = []
    if cls.get('lesson'):
        chunks += script_chunks(cls['lesson'])
    else:
        chunks.append("%s I am %s, and this is %s — a class in %s at "
                      "Exolex University. Here is the whole course, "
                      "taught unit by unit, in order."
                      % (prof.get('greeting', 'Welcome.'), prof['name'],
                         cls['title'], section['name']))
    n = len(cls['units'])
    for j, u in enumerate(cls['units']):
        chunks.append("Unit %d of %d: %s." % (j + 1, n, u))
    wc = worked_chunk(cls)
    if wc:
        chunks.append(wc)
    return chunks

# ---------------------------------------------------------------- gloss questions
GLOSS_STOP = set("""the and a an of to in on for with is are its it by at from
or as how why what when your you that this says say said""".split())

def gloss_words(gloss):
    words = []
    for w in re.findall(r"[a-z][a-z\-']{2,}", gloss.lower()):
        w = w.strip("-'")
        if w in GLOSS_STOP or w in words:
            continue
        words.append(w)
    return words

def word_variants(w):
    out = {w}
    if w.endswith('s'):
        out.add(w[:-1])
    if w.endswith('ing'):
        out.add(w[:-3])
    if 'ising' in w:
        out.add(w.replace('ising', 'izing'))
    if 'ised' in w:
        out.add(w.replace('ised', 'ized'))
    return sorted(out)

def split_gloss(title):
    """'Topic: the gloss' or 'Topic — the gloss' → (topic, gloss)."""
    for sep in (': ', ' — '):
        if sep in title:
            topic, gloss = title.split(sep, 1)
            return topic.strip(), gloss.strip()
    return title.strip(), None

def gloss_questions(cls):
    """Questions on the units' own one-line unpackings — the part of
    a unit title that actually teaches ('Overfitting: memorising
    instead of learning'). The gloss is presented verbatim in the
    lesson, so the answer is contained in the teaching by
    construction (and the audit below proves it). At most two per
    class: the richest glosses."""
    cand = []
    for j, u in enumerate(cls['units']):
        topic, gloss = split_gloss(u)
        if not gloss:
            continue
        words = gloss_words(gloss)
        if len(words) < 3:
            continue
        cand.append((j, u, topic, gloss, words))
    cand.sort(key=lambda c: -len(c[4]))
    chosen = sorted(cand[:2], key=lambda c: c[0])  # back into unit order
    out = []
    for j, u, topic, gloss, words in chosen:
        groups = [word_variants(w) for w in words]
        heads = ' · '.join(words)
        out.append({
            "teach": ("From the lesson: unit %d, '%s' — and the one "
                      "line that unpacks it." % (j + 1, u)),
            "teach2": ("The exact line, from the lesson: 'Unit %d of "
                       "%d: %s.' Break the unpacking into its pieces: "
                       "%s. An answer standing on those pieces, in your "
                       "own words, lands it."
                       % (j + 1, len(cls['units']), u, heads)),
            "walk": ("Walk it through with me, step by step. (1) In "
                     "the lesson, unit %d was '%s'. (2) Its one-line "
                     "unpacking was: '%s'. (3) The ideas in that line "
                     "are: %s. (4) Say an answer that stands on those "
                     "ideas — in your own words."
                     % (j + 1, u, gloss, heads)),
            "q": ("From the lesson: what does this class mean by "
                  "'%s'? Say it the way the lesson taught it." % topic),
            "kind": "keywords", "keywords": groups,
            "need": min(3, max(2, math.ceil(len(groups) / 2))),
            "why": ("You are doing this because a definition you can "
                    "produce is one you actually hold — and this one "
                    "was taught, in the lesson, in so many words."),
            "substantive": True,
        })
    return out

def capstone_step(cls):
    hw = cls.get('homework') or {}
    q, worked = hw.get('q', ''), hw.get('worked', '')
    groups = capstone_keywords(worked)
    if len(groups) < 3 or not q:
        return None
    first = re.split(r'(?<=[.!?])\s+', worked.strip())[0]
    heads = heads_of(groups)
    # the re-teach shows the exact taught passage — the worked
    # example from the lesson — plus the answer's SHAPE: the ideas
    # it stands on. A different thing from the question, and from
    # the teach (which only points back at the lesson)
    teach2 = ("Back to the exact passage, from the lesson — my "
              "worked example: %s And here is the shape of that "
              "answer: it stands on %s. Build yours on the same "
              "bones, in your own words — it does not have to sound "
              "like the book; it has to stand on the same ideas."
              % (worked_chunk(cls) or worked, heads))
    # the walkthrough walks the worked answer's own road, sentence
    # by sentence, then hands the pen back to the student
    road = ' '.join("(%d) %s" % (j + 1, s)
                    for j, s in enumerate(sentences(worked)))
    walk = ("Walk it through with me, step by step, along the worked "
            "answer's own road. %s An answer of yours that touches %s "
            "walks the same road. Now put it in your own words and "
            "say it." % (road, heads))
    return {
        "teach": ("The class's set problem — you met it in the lesson "
                  "as my worked example, worked in full. Now it is "
                  "yours to work, in your own words. Take your time: "
                  "say it out loud or type it; either door is open."),
        "teach2": teach2, "walk": walk,
        "q": q, "kind": "keywords", "keywords": groups,
        "need": max(2, min(3, math.ceil(len(groups) / 2))),
        "why": WHY_CAP, "substantive": True,
    }

# (The old orientation step — DOI recall — is deleted, not revised:
#  a DOI was never taught content, it was a label on the syllabus
#  card. Under Bill's model it cannot be a passing question.)

def backfill_walk(step):
    """A walkthrough for a hand-written override step that carries
    none — built only from the step's own fields, never invented."""
    if step.get('walk'):
        return step['walk']
    kind = step.get('kind')
    if kind == 'number':
        disp = step.get('disp') or step.get('answer')
        return ("Walk it through with me, step by step. (1) Read the "
                "re-teach on the board — it states the result in plain "
                "figures. (2) The figure it states for this step is "
                "%s. (3) That figure is the answer the material gives. "
                "Now say it yourself, in any honest form." % disp)
    if kind == 'keywords':
        heads = heads_of(step.get('keywords', []))
        return ("Walk it through with me, step by step. (1) The "
                "re-teach on the board gives the pattern this answer "
                "is built from. (2) A correct answer stands on these "
                "ideas: %s. (3) Build yours on them, in your own "
                "words, and say it." % heads)
    if kind == 'title':
        return ("Walk it through with me, step by step. (1) The "
                "re-teach on the board states the order plainly. (2) "
                "Find the unit named in the question. (3) The name "
                "standing immediately after it is '%s'. (4) That name "
                "is the answer — say it whole." % step.get('answer'))
    if kind == 'exact':
        return ("Walk it through with me, step by step. (1) The "
                "re-teach on the board states this step's answer as "
                "the class's own material prints it. (2) It is: %s. "
                "(3) Say it back, exactly as printed."
                % step.get('answer'))
    return None

# ---------------------------------------------------------------- audit
# THE CONTAINMENT AUDIT — the mechanical enforcement of Bill's law.
# A question ships only if its answer is contained in the class's
# LESSON (the material presented before the questions begin):
#   number   — a value within tolerance is extractable from the lesson
#   exact    — the answer string appears in the lesson
#   keywords — at least `need` keyword groups have a synonym in the lesson
#   title    — at least 60% of the answer's content words are in the lesson
# A question that fails is DROPPED and counted — never shipped.

SUPER = {'⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5',
         '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁻': '-'}

def norm_text(t):
    t = (t or '').lower()
    t = re.sub(r'[^\w.\s]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

def extract_numbers(text):
    t = text or ''
    t = re.sub(r'10([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)', lambda m: '10^' + ''.join(
        SUPER.get(ch, ch) for ch in m.group(1)), t)
    t = ''.join(SUPER.get(ch, ch) for ch in t)
    out = []
    for m in re.finditer(r'(-?\d+(?:\.\d+)?)\s*(?:×|x|\*)\s*10\s*\^\s*(-?\d+)', t):
        out.append(float(m.group(1)) * 10 ** int(m.group(2)))
    t2 = re.sub(r'(-?\d+(?:\.\d+)?)\s*(?:×|x|\*)\s*10\s*\^\s*(-?\d+)', ' ', t)
    for m in re.finditer(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?', t2.replace(',', '')):
        try:
            out.append(float(m.group(0)))
        except ValueError:
            pass
    return out

def audit_step(step, lesson_norm, lesson_numbers):
    kind = step.get('kind')
    if kind == 'number':
        want = step.get('answer')
        if not isinstance(want, (int, float)):
            return False, 'number key is not a value'
        tol = step.get('tol') or 0.03
        if want == 0:
            return (0.0 in lesson_numbers), 'zero not in the lesson'
        ok = any(abs(v - want) / abs(want) <= tol for v in lesson_numbers)
        return ok, 'value %s not extractable from the lesson' % want
    if kind == 'exact':
        ok = norm_text(str(step.get('answer'))) in lesson_norm
        return ok, 'answer string not in the lesson'
    if kind == 'keywords':
        groups = step.get('keywords') or []
        if not groups:
            return False, 'no keyword key'
        present = 0
        for g in groups:
            if any((' ' + norm_text(syn) + ' ') in (' ' + lesson_norm + ' ')
                   or norm_text(syn) in lesson_norm for syn in g):
                present += 1
        need = step.get('need') or max(1, math.ceil(len(groups) / 2))
        return present >= need, ('only %d of %d keyword groups in the '
                                 'lesson (need %d)' % (present, len(groups), need))
    if kind == 'title':
        words = gloss_words(str(step.get('answer') or ''))
        if not words:
            return False, 'no content words in the key'
        present = sum(1 for w in words if w in lesson_norm)
        return present >= math.ceil(len(words) * 0.6), \
            'title key not in the lesson'
    return False, 'unknown kind %s' % kind

# ---------------------------------------------------------------- build
classes = {}
report = {}
dropped = Counter()
for s in cat['sections']:
    for cls in s['classes']:
        cid = cls['id']
        if cid in trainer or s['id'] == 'languages':
            report[cid] = ('language', 'taught by the listen-and-repeat trainer')
            continue
        prof = cls.get('professor') or s.get('professor')
        ov = overrides.get(cid) or {}
        # ---- the lesson, taught first
        if ov.get('lesson') is not None:
            lesson = list(ov['lesson'])
        elif cls.get('units'):
            lesson = lesson_units(cls, s, prof)
        else:
            lesson = lesson_papers(cls, prof)
        # ---- the end-of-class questions
        steps = []
        if ov.get('steps') is not None:
            steps = list(ov['steps'])
        else:
            if cls.get('units'):
                steps += gloss_questions(cls)
            else:
                steps += value_questions(cls)
            if ov.get('add'):
                # a hand-written extra question: its passage joins
                # the lesson (it becomes taught material), and the
                # question points back at it like any other
                for add in ov['add']:
                    lesson.append(add['teach'])
                    q = dict(add)
                    q['teach'] = ("From the lesson: one paper's stated "
                                  "result — the passage your professor "
                                  "presented on it.")
                    steps.append(q)
            cap = ov['capstone'] if 'capstone' in ov else capstone_step(cls)
            if cap:
                steps.append(cap)
        steps = steps[:8]
        for st in steps:
            w = backfill_walk(st)
            if w:
                st['walk'] = w
        # ---- the containment audit: no untaught question ships
        lesson_text = ' '.join(lesson)
        lesson_norm = norm_text(lesson_text)
        lesson_numbers = extract_numbers(lesson_text)
        kept = []
        for st in steps:
            ok, why = audit_step(st, lesson_norm, lesson_numbers)
            if ok:
                kept.append(st)
            else:
                dropped['%s: %s' % (st.get('kind'), why)] += 1
        steps = kept
        substantive = sum(1 for st in steps if st.get('substantive'))
        if not steps:
            report[cid] = ('lesson-only',
                           'a lesson of %d passages; no question could be '
                           'grounded in it' % len(lesson))
            classes[cid] = {"lesson": [{"teach": t} for t in lesson],
                            "steps": [], "praise": PRAISE, "retry": RETRY}
            continue
        entry = {"lesson": [{"teach": t} for t in lesson],
                 "steps": steps, "praise": PRAISE, "retry": RETRY}
        if cls.get('audio'):
            base = "audio/gate/%s/" % cid
            entry['audioBase'] = base
            for k, ch in enumerate(entry['lesson']):
                ch['audio'] = base + "lesson-%d.mp3" % k
            for i, st in enumerate(steps):
                st['audio'] = base + "step-%d.mp3" % i
            entry['praiseAudio'] = [base + "praise-%d.mp3" % i for i in range(len(PRAISE))]
            entry['retryAudio'] = [base + "retry-0.mp3" for _ in RETRY]
        classes[cid] = entry
        report[cid] = ('full' if substantive >= 3 else
                       'partial' if substantive >= 1 else 'orientation',
                       '%d questions on a lesson of %d passages'
                       % (len(steps), len(lesson)))

out = {"generated": "build-gate-data.py — gated steps for every non-language class",
       "classes": classes}
with open('gate-data.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

counts = Counter(v[0] for v in report.values())
print('gate-data.json:', len(classes), 'gated classes of',
      sum(1 for s in cat['sections'] for _ in s['classes']), 'total')
print('coverage:', dict(counts))
print('questions dropped by the containment audit:', sum(dropped.values()))
for k, v in dropped.most_common():
    print('  dropped', v, '×', k)

with open('GATE-COVERAGE.md', 'w', encoding='utf-8') as f:
    f.write("# Gate coverage — build-gate-data.py\n\n")
    f.write("Every non-language class gets a LESSON taught first — its "
            "own material, presented in order — and then end-of-class "
            "questions drawn only from that lesson. The containment "
            "audit in the generator drops any question whose answer "
            "is not in the lesson; the drops are counted in the build "
            "output and in the teaching-fix report.\n\n")
    for k in ('full', 'partial', 'lesson-only', 'language'):
        f.write("## %s (%d)\n\n" % (k, counts.get(k, 0)))
        for s in cat['sections']:
            for cls in s['classes']:
                if report[cls['id']][0] == k:
                    f.write("- `%s` (%s) — %s\n" % (cls['id'], s['id'], report[cls['id']][1]))
        f.write("\n")
print('GATE-COVERAGE.md written')
