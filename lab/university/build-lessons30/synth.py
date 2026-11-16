#!/usr/bin/env python3
"""Synthesize the 30-minute lesson audio, in each professor's own
roster voice (catalogue.json). Carmen Vega is locked: Determined Mast
at --speed 88 (regen-carmen.py is the standing proof of the pair).

Method (house practice, TOOLS.md): the script is chunked at paragraph
boundaries (<=1200 chars; long paragraphs split at sentences), each
chunk goes through `tts speak`, a chunk that keeps failing is bisected
and retried (the backend has deterministic text triggers), and the
parts are concatenated with ffmpeg. Every finished lesson is verified
with ffprobe and its measured minutes land in state.json, which is
also the resume checkpoint: a lesson whose script hash matches its
state entry is skipped, so re-running synth.py only does new work.

Phrase models (language lessons): each PHRASES target at class speed,
plus a slow word-spaced model at speed 76, exactly as the trainer does.

A failed lesson is logged (synth-failures.log) and the batch moves on —
one poisoned clip never stalls the build.

Usage: python3 synth.py <classId> [NN ...] | --all [--force]
"""
import json, os, re, sys, glob, hashlib, subprocess
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
UNI = os.path.dirname(HERE)
os.chdir(HERE)

TTS = '/opt/hatch/bin/tts'
SPEEDS = {'espanol-i-speak-from-zero': '88'}   # Bill's lock for Carmen
SLOW_SPEED = '76'

cat = json.load(open(os.path.join(UNI, 'catalogue.json')))
VOICE_OF = {}
for s in cat['sections']:
    for c in s['classes']:
        VOICE_OF[c['id']] = (c.get('professor') or s['professor'])['voiceId']

state = {}
if os.path.exists('state.json'):
    state = json.load(open('state.json'))


def save_state():
    with open('state.json', 'w') as fh:
        json.dump(state, fh, ensure_ascii=False, indent=1)


def speakable(t):
    return (t.replace('ø', 'o').replace('Ø', 'O')
             .replace('ʿ', '').replace('ʾ', ''))


def parse_script(path):
    raw = open(path, encoding='utf-8').read()
    lines = raw.split('\n')
    if lines and lines[0].startswith('#'):
        lines = lines[1:]
    body = '\n'.join(lines)
    phrases = []
    if '=== PHRASES ===' in body:
        body, phr = body.split('=== PHRASES ===', 1)
        for line in phr.strip().split('\n'):
            line = line.strip()
            if line and '|' in line:
                phrases.append(line.split('|', 1)[0].strip())
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', body) if p.strip()]
    return paragraphs, phrases


def chunk_text(paragraphs, limit=1200):
    chunks = []
    cur = ''
    def push(t):
        nonlocal cur
        if cur:
            chunks.append(cur)
            cur = ''
        if len(t) <= limit:
            cur = t
        else:
            # split a long paragraph at sentence boundaries
            parts = re.split(r'(?<=[.!?])\s+', t)
            for p in parts:
                if len(p) > limit:
                    if cur:
                        chunks.append(cur)
                        cur = ''
                    for i in range(0, len(p), limit):
                        chunks.append(p[i:i + limit])
                elif len(cur) + len(p) + 1 <= limit:
                    cur = (cur + ' ' + p) if cur else p
                else:
                    chunks.append(cur)
                    cur = p
    for para in paragraphs:
        if len(cur) + len(para) + 2 <= limit:
            cur = (cur + '\n\n' + para) if cur else para
        else:
            push(para)
    if cur:
        chunks.append(cur)
    return chunks


def synth_chunk(voice, speed, text, out, depth=0):
    if os.path.exists(out) and os.path.getsize(out) > 3000:
        return True
    cmd = [TTS, 'speak', '--voice', voice]
    if speed:
        cmd += ['--speed', str(speed)]
    cmd += ['--text-stdin', '--output', out]
    for _ in range(2):
        subprocess.run(cmd, input=speakable(text).encode(),
                       capture_output=True, timeout=300)
        if os.path.exists(out) and os.path.getsize(out) > 3000:
            return True
    if depth < 3 and len(text) > 200:
        mid = len(text) // 2
        cut = text.rfind(' ', 0, mid)
        if cut < 50:
            cut = mid
        a, b = out + '.a.mp3', out + '.b.mp3'
        ok = (synth_chunk(voice, speed, text[:cut], a, depth + 1) and
              synth_chunk(voice, speed, text[cut:], b, depth + 1))
        if ok:
            r = subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i',
                                f'concat:{a}|{b}', '-c:a', 'libmp3lame',
                                '-q:a', '4', out], capture_output=True)
            if r.returncode == 0 and os.path.getsize(out) > 3000:
                os.remove(a)
                os.remove(b)
                return True
    return False


def duration(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                        'format=duration', '-of', 'csv=p=0', path],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def synth_lesson(cid, n, force=False):
    spath = os.path.join('scripts', cid, f'lesson-{n:02d}.txt')
    paragraphs, phrases = parse_script(spath)
    text = '\n\n'.join(paragraphs)
    h = hashlib.sha1(text.encode()).hexdigest()
    rel = f'audio/lessons30/{cid}/lesson-{n:02d}.mp3'
    out = os.path.join(UNI, rel)
    key = f'lesson-{n:02d}'
    st = state.setdefault(cid, {}).get(key, {})
    voice = VOICE_OF[cid]
    speed = SPEEDS.get(cid)
    if not force and st.get('hash') == h and os.path.exists(out):
        print(f'skip {cid} L{n:02d} (unchanged, {st.get("minutes")} min)',
              flush=True)
    else:
        chunks = chunk_text(paragraphs)
        pdir = os.path.join('parts', cid, f'l{n:02d}')
        os.makedirs(pdir, exist_ok=True)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        print(f'{cid} L{n:02d}: {len(text.split())} words, '
              f'{len(chunks)} chunks, voice {voice}'
              f'{" speed " + speed if speed else ""}', flush=True)
        jobs = [(voice, speed, ch, os.path.join(pdir, f'part-{i:03d}.mp3'))
                for i, ch in enumerate(chunks)]
        with ThreadPoolExecutor(max_workers=3) as ex:
            results = list(ex.map(lambda j: synth_chunk(*j), jobs))
        bad = [jobs[i][3] for i, ok in enumerate(results) if not ok]
        if bad:
            msg = f'{cid} L{n:02d}: {len(bad)} chunks failed: {bad}'
            print('FAIL', msg, flush=True)
            with open('synth-failures.log', 'a') as fh:
                fh.write(msg + '\n')
            return False
        lst = os.path.join(pdir, 'list.txt')
        with open(lst, 'w') as fh:
            for _, _, _, p in jobs:
                fh.write(f"file '{os.path.abspath(p)}'\n")
        r = subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat',
                            '-safe', '0', '-i', lst, '-c:a', 'libmp3lame',
                            '-q:a', '4', out], capture_output=True)
        if r.returncode != 0 or not os.path.exists(out):
            print(f'FAIL {cid} L{n:02d}: concat failed', flush=True)
            return False
        mins = duration(out) / 60.0
        state[cid][key] = {'hash': h, 'audio': rel,
                           'minutes': round(mins, 2)}
        save_state()
        print(f'OK   {cid} L{n:02d}: {mins:.1f} min -> {rel}', flush=True)
    # phrase models
    for i, target in enumerate(phrases):
        base = os.path.join(UNI, f'audio/lessons30/{cid}/l{n:02d}-phrase-{i:02d}')
        if force or not (os.path.exists(base + '.mp3') and
                         os.path.getsize(base + '.mp3') > 3000):
            synth_chunk(voice, speed, target, base + '.mp3')
        slow = ' … '.join(speakable(target).replace(',', ' ').split()) + '.'
        if force or not (os.path.exists(base + '-slow.mp3') and
                         os.path.getsize(base + '-slow.mp3') > 3000):
            synth_chunk(voice, SLOW_SPEED, slow, base + '-slow.mp3')
    return True


def main():
    args = sys.argv[1:]
    force = '--force' in args
    args = [a for a in args if a != '--force']
    if not args:
        print(__doc__)
        return
    jobs = []
    if args == ['--all']:
        for d in sorted(glob.glob('scripts/*')):
            if os.path.isdir(d):
                cid = os.path.basename(d)
                ns = sorted(int(re.search(r'lesson-(\d+)\.txt$', f).group(1))
                            for f in glob.glob(d + '/lesson-*.txt'))
                jobs += [(cid, n) for n in ns]
    else:
        cid = args[0]
        ns = [int(a) for a in args[1:]]
        if not ns:
            ns = sorted(int(re.search(r'lesson-(\d+)\.txt$', f).group(1))
                        for f in glob.glob(f'scripts/{cid}/lesson-*.txt'))
        jobs = [(cid, n) for n in ns]
    ok = bad = 0
    for cid, n in jobs:
        if synth_lesson(cid, n, force):
            ok += 1
        else:
            bad += 1
    print(f'SYNTH DONE: {ok} ok, {bad} failed', flush=True)


if __name__ == '__main__':
    main()
