#!/usr/bin/env python3
"""The containment + multiple-choice audit for 30-minute lessons.

Bill's law: a question ships only if its answer was actually taught —
here, taught in the FULL lesson script (not a short intro passage).
Checks per question (mirrors build-gate-data.py's rules, applied to
the lesson script text):
  exact    — the answer, or one of its accept forms, appears in the
             lesson text (normalized).
  number   — the value appears among the numbers the lesson states.
  keywords — every keyword group has at least one word in the lesson.
  MC       — >=3 unique choices; mcAnswer is one of them; the correct
             choice is contained in the lesson; every distractor is
             also lesson material (a phrase/value/concept the lesson
             itself states) — nothing invented.
  teach2   — must quote the lesson: a verbatim run of >=60 normalized
             characters from the script.
  shape    — full-sentence question (>=15 chars), walk present
             (>=40 chars), rank 1..3.
Survivors are sorted easy -> hard (rank, then authored order) and
written to questions/<cid>/lesson-NN.audited.json. A lesson needs
>=6 survivors to ship questions at all; the report says exactly what
was dropped and why. 0 unexplained failures is the ship standard.

Usage: python3 audit_questions.py <classId> [NN ...] | --all
"""
import json, os, re, sys, glob, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)


def norm(t):
    t = unicodedata.normalize('NFKD', str(t).lower())
    t = ''.join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r'[^a-z0-9 ]+', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()


def extract_numbers(text):
    out = set()
    for m in re.finditer(r'\d[\d,]*(?:\.\d+)?(?:[eE][+-]?\d+)?', text):
        try:
            out.add(float(m.group(0).replace(',', '')))
        except ValueError:
            pass
    return out


def parse_script(path):
    raw = open(path, encoding='utf-8').read()
    lines = raw.split('\n')
    if lines and lines[0].startswith('#'):
        lines = lines[1:]
    body = '\n'.join(lines)
    if '=== PHRASES ===' in body:
        body, phr = body.split('=== PHRASES ===', 1)
        body = body + '\n' + phr.replace('|', ' ')
    return body


def num_in(value, numbers):
    try:
        v = float(value)
    except (TypeError, ValueError):
        return False
    return any(abs(v - n) <= max(1e-9, abs(n) * 1e-9) for n in numbers)


def audit_one(q, lesson_norm, lesson_numbers):
    """Return None if the question ships, else the drop reason."""
    kind = q.get('kind')
    if kind not in ('exact', 'number', 'keywords'):
        return f'bad kind {kind!r}'
    question = str(q.get('q', '')).strip()
    if len(question) < 15:
        return 'question too short / not a full sentence'
    if q.get('rank') not in (1, 2, 3):
        return 'rank missing or not 1..3'
    if len(str(q.get('walk', ''))) < 40:
        return 'walkthrough missing or too short'
    # containment of the answer itself
    if kind == 'exact':
        forms = [q.get('answer')] + list(q.get('accept') or [])
        if not any(f and norm(f) and norm(f) in lesson_norm for f in forms):
            return 'exact answer not in the lesson text'
    elif kind == 'number':
        if not num_in(q.get('answer'), lesson_numbers):
            return 'number answer not among the lesson\u2019s numbers'
    else:
        groups = q.get('keywords') or []
        if not groups or not q.get('need'):
            return 'keywords question without groups/need'
        words = set(lesson_norm.split())
        for g in groups:
            if not any(norm(w) in words or norm(w) in lesson_norm for w in g):
                return f'keyword group {g} not in the lesson text'
        # if the question carries an MC set, its correct choice must
        # itself satisfy the keyword groups — otherwise picking it can
        # never pass (caught live: Computing Foundations capstones,
        # Nov 16 — mcAnswer was a callback phrase hitting 0 groups)
        if q.get('choices') and q.get('mcAnswer'):
            mtext = norm(q['mcAnswer'])
            hits = sum(1 for g in groups
                       if any(norm(s) in mtext for s in g))
            if hits < q['need']:
                return (f'mcAnswer satisfies only {hits}/{q["need"]} '
                        f'of its own keyword groups — unanswerable by picking')
    # teach2 must quote the lesson
    t2 = norm(q.get('teach2', ''))
    quoted = False
    for start in range(0, max(0, len(t2) - 60), 10):
        if t2[start:start + 60] in lesson_norm:
            quoted = True
            break
    if not quoted:
        return 'teach2 does not quote a 60-char run of the lesson'
    # multiple choice
    choices = q.get('choices') or []
    if choices:
        if len(choices) < 3:
            return 'fewer than 3 choices'
        if len({norm(c) for c in choices}) != len(choices):
            return 'duplicate choices'
        mc = q.get('mcAnswer')
        if mc is None or str(mc) not in [str(c) for c in choices]:
            return 'mcAnswer is not one of the choices'
        for c in choices:
            cn = norm(c)
            if cn and cn in lesson_norm:
                continue
            if num_in(c, lesson_numbers):
                continue
            # a choice may be a value phrase like "1.000e+13" — try its number
            nums = extract_numbers(str(c))
            if nums and all(num_in(n, lesson_numbers) for n in nums):
                continue
            return f'choice {c!r} is not lesson material'
    return None


def audit_lesson(cid, n):
    spath = os.path.join('scripts', cid, f'lesson-{n:02d}.txt')
    qpath = os.path.join('questions', cid, f'lesson-{n:02d}.json')
    if not os.path.exists(qpath):
        print(f'{cid} lesson {n:02d}: no questions file', flush=True)
        return 0, 0
    lesson = parse_script(spath)
    lesson_norm = norm(lesson)
    lesson_numbers = extract_numbers(lesson)
    raw = json.load(open(qpath))
    kept, dropped = [], []
    for i, q in enumerate(raw):
        reason = audit_one(q, lesson_norm, lesson_numbers)
        if reason is None:
            kept.append((q.get('rank', 2), i, q))
        else:
            dropped.append((i, q.get('q', '?')[:60], reason))
    kept.sort(key=lambda t: (t[0], t[1]))
    kept = [q for _, _, q in kept]
    for i, qq, reason in dropped:
        print(f'  DROP {cid} L{n:02d} q{i}: {reason} :: {qq}', flush=True)
    if len(kept) >= 6:
        out = os.path.join('questions', cid, f'lesson-{n:02d}.audited.json')
        with open(out, 'w') as fh:
            json.dump(kept, fh, ensure_ascii=False, indent=1)
        print(f'{cid} lesson {n:02d}: {len(kept)} ship, '
              f'{len(dropped)} dropped', flush=True)
    else:
        print(f'{cid} lesson {n:02d}: ONLY {len(kept)} survive '
              f'(<6) — questions do NOT ship', flush=True)
    return len(kept), len(dropped)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    jobs = []
    if args == ['--all']:
        for qf in sorted(glob.glob('questions/*/lesson-*.json')):
            if qf.endswith('.audited.json'):
                continue
            cid = qf.split('/')[1]
            n = int(re.search(r'lesson-(\d+)\.json$', qf).group(1))
            jobs.append((cid, n))
    else:
        cid = args[0]
        ns = [int(a) for a in args[1:]]
        if not ns:
            ns = sorted(int(re.search(r'lesson-(\d+)\.json$', f).group(1))
                        for f in glob.glob(f'questions/{cid}/lesson-*.json')
                        if not f.endswith('.audited.json'))
        jobs = [(cid, n) for n in ns]
    tk = td = 0
    for cid, n in jobs:
        k, d = audit_lesson(cid, n)
        tk += k
        td += d
    print(f'AUDIT TOTAL: {tk} ship, {td} dropped', flush=True)


if __name__ == '__main__':
    main()
