#!/usr/bin/env python3
"""Assemble lessons30/<classId>.json from the source files.

Sources (per class, per lesson NN):
  scripts/<cid>/lesson-NN.txt        the lesson script (FORMAT.md)
  questions/<cid>/lesson-NN.audited.json   ONLY audited questions ship;
                                     a raw questions file that has not
                                     passed audit_questions.py yields a
                                     lesson with no questions + a loud
                                     warning — unaudited never ships.
  state.json                         synth.py's record: per-lesson
                                     audio path + measured minutes.

Output: ../lessons30/<cid>.json and ../lessons30/index.json (manifest).
Idempotent: re-running rebuilds the data files from the sources.
Usage: python3 assemble.py <classId> [...] | --all
"""
import json, os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
UNI = os.path.dirname(HERE)
os.chdir(HERE)

cat = json.load(open(os.path.join(UNI, 'catalogue.json')))
CLASS_META = {}
for s in cat['sections']:
    for c in s['classes']:
        CLASS_META[c['id']] = c

state = {}
if os.path.exists('state.json'):
    state = json.load(open('state.json'))


def parse_script(path):
    raw = open(path, encoding='utf-8').read()
    lines = raw.split('\n')
    title = ''
    if lines and lines[0].startswith('#'):
        title = lines[0].lstrip('#').strip()
        lines = lines[1:]
    body = '\n'.join(lines)
    phrases = []
    if '=== PHRASES ===' in body:
        body, phr = body.split('=== PHRASES ===', 1)
        for line in phr.strip().split('\n'):
            line = line.strip()
            if not line or '|' not in line:
                continue
            target, meaning = line.split('|', 1)
            phrases.append({'target': target.strip(),
                            'display': target.strip(),
                            'meaning': meaning.strip()})
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', body) if p.strip()]
    text = '\n\n'.join(paragraphs)
    return title, paragraphs, text, phrases


def build_class(cid):
    meta = CLASS_META.get(cid, {})
    prof = meta.get('professor') or {}
    lessons = []
    sdir = os.path.join('scripts', cid)
    files = sorted(glob.glob(os.path.join(sdir, 'lesson-*.txt')))
    for f in files:
        m = re.search(r'lesson-(\d+)\.txt$', f)
        n = int(m.group(1))
        title, paragraphs, text, phrases = parse_script(f)
        st = state.get(cid, {}).get(f'lesson-{n:02d}', {})
        # phrases: attach audio paths where synth produced them
        for i, ph in enumerate(phrases):
            base = f'audio/lessons30/{cid}/l{n:02d}-phrase-{i:02d}'
            if os.path.exists(os.path.join(UNI, base + '.mp3')):
                ph['audio'] = base + '.mp3'
            if os.path.exists(os.path.join(UNI, base + '-slow.mp3')):
                ph['slowAudio'] = base + '-slow.mp3'
            ph['variants'] = []
        audited = os.path.join('questions', cid, f'lesson-{n:02d}.audited.json')
        raw_q = os.path.join('questions', cid, f'lesson-{n:02d}.json')
        questions = []
        if os.path.exists(audited):
            questions = json.load(open(audited))
        elif os.path.exists(raw_q):
            print(f'  !! {cid} lesson {n:02d}: questions exist but are '
                  f'UNAUDITED — shipping the lesson with none', flush=True)
        lessons.append({
            'n': n,
            'title': title,
            'paragraphs': paragraphs,
            'words': len(text.split()),
            'audio': st.get('audio'),
            'minutes': st.get('minutes', 0),
            'phrases': phrases,
            'questions': questions,
        })
    out = {
        'id': cid,
        'title': meta.get('title', cid),
        'professor': prof.get('name', ''),
        'lang': meta.get('lang') or ('es-ES' if cid.startswith('espanol') else None),
        'lessons': lessons,
    }
    if out['lang'] is None:
        del out['lang']
    os.makedirs(os.path.join(UNI, 'lessons30'), exist_ok=True)
    with open(os.path.join(UNI, 'lessons30', cid + '.json'), 'w') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    tot_min = sum(l['minutes'] for l in lessons)
    tot_q = sum(len(l['questions']) for l in lessons)
    print(f'{cid}: {len(lessons)} lessons, {tot_min:.1f} audio min, '
          f'{tot_q} audited questions', flush=True)
    return {'lessons': len(lessons), 'minutes': round(tot_min, 1),
            'questions': tot_q}


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    if args == ['--all']:
        args = sorted(os.path.basename(p) for p in glob.glob('scripts/*')
                      if os.path.isdir(p))
    manifest = {}
    mpath = os.path.join(UNI, 'lessons30', 'index.json')
    if os.path.exists(mpath):
        manifest = json.load(open(mpath)).get('classes', {})
    for cid in args:
        manifest[cid] = build_class(cid)
    with open(mpath, 'w') as fh:
        json.dump({'classes': manifest}, fh, ensure_ascii=False, indent=1)
    print('manifest updated:', len(manifest), 'classes', flush=True)


if __name__ == '__main__':
    main()
