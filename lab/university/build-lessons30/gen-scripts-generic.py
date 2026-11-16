#!/usr/bin/env python3
"""Stage 3: generate 30-minute-format lessons for the remaining
university from each class's OWN material.

Honest scope, stated plainly: stages 1-2 are hand-written. Stage 3
lessons are ASSEMBLED from the class's real teaching material — the
gate build's lesson passages (themselves built from the class's
papers' stated results, its units, and its worked example) — framed
by the professor's narration: a welcome, connective teaching between
passages, a recap, and a close. Nothing is invented: every fact in a
stage-3 script is a fact the class already taught. Where a class's
material is thin, its lessons are honestly shorter, and where a class
cannot field at least 6 auditable questions in total, the generator
refuses it — the class stays on the existing gate and the queue marks
it deferred-thin. A stage-3 class never regresses a student.

Questions: the class's existing gate steps, partitioned across the
generated lessons by the same containment rule the audit enforces
(the step's answer must live in that lesson's script). The steps keep
their audited choices; audit_questions.py re-verifies every set
against the generated scripts before anything ships.

Usage: python3 gen-scripts-generic.py <classId> [...]
Writes scripts/<cid>/lesson-NN.txt + questions/<cid>/lesson-NN.json.
Never overwrites existing (hand-written) files.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNI = os.path.dirname(HERE)
os.chdir(HERE)

cat = json.load(open(os.path.join(UNI, 'catalogue.json')))
gate = json.load(open(os.path.join(UNI, 'gate-data.json')))['classes']

META = {}
ORDER = []
for s in cat['sections']:
    for c in s['classes']:
        META[c['id']] = (s, c)
        ORDER.append(c['id'])

CONNECTIVES = [
    'Stay with me, because the next piece builds directly on that one.',
    'Here is the next piece of the material, in the order the class presents it.',
    'Now we go one step further into the material.',
    'The next piece is where this starts to come together.',
    'Listen carefully here — this piece carries weight in the questions later.',
    'We take the pieces in order, because each one stands on the last.',
]


def prof_of(cid):
    s, c = META[cid]
    return c.get('professor') or s['professor']


def first_sentence(t):
    m = re.split(r'(?<=[.!?])\s+', t.strip())
    return m[0] if m else t[:80]


def step_contained_in(step, text_norm, numbers):
    """Same containment logic as audit_questions.audit_one, minus the
    teach2/choice checks (the full audit runs after generation)."""
    import unicodedata
    def norm(t):
        t = unicodedata.normalize('NFKD', str(t).lower())
        t = ''.join(ch for ch in t if not unicodedata.combining(ch))
        t = re.sub(r'[^a-z0-9 ]+', ' ', t)
        return re.sub(r'\s+', ' ', t).strip()
    kind = step.get('kind')
    if kind == 'exact':
        forms = [step.get('answer')] + list(step.get('accept') or [])
        return any(f and norm(f) and norm(f) in text_norm for f in forms)
    if kind == 'number':
        try:
            v = float(step.get('answer'))
        except (TypeError, ValueError):
            return False
        return any(abs(v - n) <= max(1e-9, abs(n) * 1e-9) for n in numbers)
    if kind == 'keywords':
        words = set(text_norm.split())
        return all(any(norm(w) in words or norm(w) in text_norm for w in g)
                   for g in (step.get('keywords') or []))
    return False


def numbers_of(text):
    out = set()
    for m in re.finditer(r'\d[\d,]*(?:\.\d+)?(?:[eE][+-]?\d+)?', text):
        try:
            out.add(float(m.group(0).replace(',', '')))
        except ValueError:
            pass
    return out


def norm_text(t):
    import unicodedata
    t = unicodedata.normalize('NFKD', str(t).lower())
    t = ''.join(ch for ch in t if not unicodedata.combining(ch))
    t = re.sub(r'[^a-z0-9 ]+', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()


def build_class(cid):
    if cid not in gate:
        return ('skip', 'not a gate class (language/trainer or unknown)')
    sdir = os.path.join('scripts', cid)
    if os.path.exists(sdir) and os.listdir(sdir):
        return ('skip', 'scripts already exist (hand-written stage)')
    s, c = META[cid]
    prof = prof_of(cid)
    g = gate[cid]
    passages = [p['teach'] for p in g.get('lesson', []) if p.get('teach')]
    steps = g.get('steps', [])
    if not passages or not steps:
        return ('deferred-thin', 'no lesson passages or no steps')

    # group passages into lessons: close a lesson once its contained
    # steps reach 6 and it carries real teaching (>= 900 words), or
    # when passages run out.
    groups = []
    cur = []
    for p in passages:
        cur.append(p)
        text = '\n\n'.join(cur)
        tn, nums = norm_text(text), numbers_of(text)
        contained = [st for st in steps if step_contained_in(st, tn, nums)]
        if len(contained) >= 6 and len(text.split()) >= 900:
            groups.append(cur)
            cur = []
    if cur:
        if groups:
            groups[-1].extend(cur)
        else:
            groups.append(cur)

    used_steps = set()
    lessons_meta = []
    for gi, group in enumerate(groups):
        text = '\n\n'.join(group)
        tn, nums = norm_text(text), numbers_of(text)
        mine = []
        for si, st in enumerate(steps):
            if si in used_steps:
                continue
            if step_contained_in(st, tn, nums):
                mine.append((si, st))
                used_steps.add(si)
        lessons_meta.append((group, mine))
    total_q = sum(len(m) for _, m in lessons_meta)
    if total_q < 6:
        return ('deferred-thin', f'only {total_q} containable questions')

    os.makedirs(sdir, exist_ok=True)
    os.makedirs(os.path.join('questions', cid), exist_ok=True)
    title = c.get('title', cid)
    for gi, (group, mine) in enumerate(lessons_meta):
        n = gi + 1
        focus = first_sentence(group[0])
        paras = []
        paras.append(
            f"Welcome in. I am {prof['name']}, and this is {title}. "
            f"This is lesson {n} of {len(lessons_meta)} in the full "
            f"thirty-minute build of this class. In this lesson we "
            f"take the class's own material in order — nothing here is "
            f"imported, and nothing is asked later that is not taught "
            f"here first. We begin here: {focus}")
        for pi, p in enumerate(group):
            if pi > 0:
                paras.append(CONNECTIVES[(gi + pi) % len(CONNECTIVES)])
            paras.append(p)
        topics = '; '.join(first_sentence(p).rstrip('.') for p in group[:6])
        paras.append(
            f"Let us gather what this lesson taught, in order: "
            f"{topics}. Those are the pieces — hold them in that "
            f"order, because the questions follow the same road.")
        paras.append(
            "That is the lesson, whole. Below it are the questions — "
            "every one of them drawn from what was just taught, and "
            "nothing else. The full text of this lesson stays open "
            "beside the questions, and going back to read a piece "
            "again is learning, not cheating. When you are ready, "
            "begin.")
        script = f"# Lesson {n} — {focus}\n\n" + '\n\n'.join(paras) + '\n'
        with open(os.path.join(sdir, f'lesson-{n:02d}.txt'), 'w') as fh:
            fh.write(script)
        qs = []
        for si, st in mine:
            q = {k: v for k, v in st.items()
                 if k not in ('audio', 'teachAudio')}
            q['rank'] = 3 if st.get('kind') == 'keywords' else (
                1 if st.get('kind') == 'number' else 2)
            qs.append(q)
        qs.sort(key=lambda q: q['rank'])
        with open(os.path.join('questions', cid,
                               f'lesson-{n:02d}.json'), 'w') as fh:
            json.dump(qs, fh, ensure_ascii=False, indent=1)
    return ('built', f'{len(lessons_meta)} lessons, {total_q} questions '
                     f'partitioned')


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    for cid in args:
        status, msg = build_class(cid)
        print(f'{cid}: {status} — {msg}', flush=True)


if __name__ == '__main__':
    main()
