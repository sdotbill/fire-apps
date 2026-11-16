#!/usr/bin/env python3
"""Final builder for the trainer clips the TTS backend keeps refusing.

Some strings in Swedish, Norwegian, Danish, Russian, Ukrainian and
Swahili are effectively poisoned at the backend right now: whole
sentences return 26-byte empties on every voice, and certain single
words ('morgon', 'från', 'Спасибо', 'Jambo') do too — while the SAME
word embedded in a short English carrier ('Repeat after me: morgon.')
synthesizes fine. So, per missing clip:

  1. whole text, a few tries;
  2. word by word — each word direct, and if a word is poisoned, via
     carrier-trim: synthesize a carrier sentence and cut the word out
     at the silence boundary (it is always the last speech segment);
  3. pieces are silence-trimmed and concatenated with a short pause —
     a deliberate word-by-word model.

Idempotent (>3 KB = landed). Logs the route per clip.
"""
import json, subprocess, os, re, sys, time, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
MIN_OK = 3000
GAP = '0.14'
CARRIERS = ['Repeat after me: {w}.', 'The word is {w}.',
            'One more time: {w}.', 'Listen: {w}.', 'And again: {w}.']

cat = json.load(open('catalogue.json'))
data = json.load(open('trainer-data.json'))['classes']
voice_of = {}
for s in cat['sections']:
    for c in s['classes']:
        voice_of[c['id']] = (c.get('professor') or s['professor'])['voiceId']

def speakable(t):
    return (t.replace('ø', 'o').replace('Ø', 'O')
             .replace('ʿ', '').replace('ʾ', ''))

def ok_file(p):
    return os.path.exists(p) and os.path.getsize(p) > MIN_OK

def tts_once(voice, text, out):
    subprocess.run(['/opt/hatch/bin/tts', 'speak', '--voice', voice,
                    '--text-stdin', '--output', out],
                   input=text.encode(), capture_output=True, timeout=240)
    return ok_file(out)

def duration(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                        'format=duration', '-of', 'csv=p=0', p],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except Exception:
        return 0.0

def last_speech_segment(p):
    """(start, end) of the final speech segment, via silencedetect."""
    r = subprocess.run(['ffmpeg', '-v', 'info', '-i', p, '-af',
                        'silencedetect=noise=-42dB:d=0.12', '-f', 'null', '-'],
                       capture_output=True, text=True)
    sil = []
    cur = None
    for line in r.stderr.splitlines():
        m = re.search(r'silence_start: ([\d.]+)', line)
        if m:
            cur = float(m.group(1))
        m = re.search(r'silence_end: ([\d.]+)', line)
        if m and cur is not None:
            sil.append((cur, float(m.group(1))))
            cur = None
    dur = duration(p)
    if cur is not None:
        sil.append((cur, dur))
    if not sil:
        return (0.0, dur)
    start = sil[-1][1] if sil[-1][1] <= dur else dur
    # if the file ENDS in silence, the last speech ends at that silence's start
    if sil[-1][1] >= dur - 0.01 and len(sil) >= 1:
        start = sil[-2][1] if len(sil) >= 2 else 0.0
        end = sil[-1][0]
        return (start, end)
    return (start, dur)

def carrier_trim(voice, word, td, tag):
    for tmpl in CARRIERS:
        for _ in range(2):
            raw = os.path.join(td, tag + '-raw.mp3')
            if not tts_once(voice, tmpl.format(w=word), raw):
                continue
            a, b = last_speech_segment(raw)
            seg = b - a
            if seg < 0.2 or seg > 2.5:
                continue
            out = os.path.join(td, tag + '.mp3')
            r = subprocess.run(
                ['ffmpeg', '-y', '-v', 'error', '-ss', f'{max(0.0, a - 0.03):.3f}',
                 '-to', f'{b + 0.03:.3f}', '-i', raw,
                 '-codec:a', 'libmp3lame', '-q:a', '4', out],
                capture_output=True)
            if r.returncode == 0 and ok_file(out):
                return out
        time.sleep(1)
    return None

def synth_word(voice, word, td, tag):
    out = os.path.join(td, tag + '.mp3')
    feed = word if word.endswith(('.', '!', '?')) else word + '.'
    for _ in range(6):
        if tts_once(voice, feed, out):
            return out
        time.sleep(1)
    trimmed = carrier_trim(voice, word, td, tag + 'c')
    if trimmed:
        os.replace(trimmed, out)
        return out
    return None

def trim_edges(p, td, tag):
    out = os.path.join(td, tag + '.wav')
    r = subprocess.run(
        ['ffmpeg', '-y', '-v', 'error', '-i', p, '-af',
         'silenceremove=start_periods=1:start_silence=0.05:start_threshold=-45dB,'
         'areverse,silenceremove=start_periods=1:start_silence=0.05:'
         'start_threshold=-45dB,areverse', '-ar', '44100', out],
        capture_output=True)
    return out if r.returncode == 0 and os.path.exists(out) else None

def build_clip(voice, text, out):
    for _ in range(3):
        if tts_once(voice, text, out):
            return 'whole'
        time.sleep(1)
    words = [w for w in text.replace('—', ' ').replace(',', ' ').split() if w.strip()]
    if len(words) == 1:
        with tempfile.TemporaryDirectory() as td:
            p = synth_word(voice, words[0], td, 'one')
            if p:
                tmp = out + '.tmp.mp3'
                subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', p,
                                '-codec:a', 'libmp3lame', '-q:a', '4', tmp],
                               capture_output=True)
                if ok_file(tmp):
                    os.replace(tmp, out)
                    return 'carrier/word'
        return None
    with tempfile.TemporaryDirectory() as td:
        parts = []
        for i, w in enumerate(words):
            p = synth_word(voice, w, td, f'w{i}')
            if not p:
                print('    word failed:', w, flush=True)
                return None
            t = trim_edges(p, td, f't{i}')
            if not t:
                return None
            parts.append(t)
        inputs = []
        for p in parts:
            inputs += ['-i', p]
        n = len(parts)
        chain, labels = [], ''
        for i in range(n):
            labels += f'[{i}:a]'
            if i < n - 1:
                labels += f'[gap{i}]'
                chain.append(f'anullsrc=r=44100:cl=mono,atrim=0:{GAP}[gap{i}]')
        filt = ';'.join(chain + [labels + f'concat=n={2 * n - 1}:v=0:a=1[out]'])
        tmp_out = out + '.tmp.mp3'
        r = subprocess.run(['ffmpeg', '-y', '-v', 'error'] + inputs +
                           ['-filter_complex', filt, '-map', '[out]',
                            '-codec:a', 'libmp3lame', '-q:a', '4', tmp_out],
                           capture_output=True)
        if r.returncode == 0 and ok_file(tmp_out):
            os.replace(tmp_out, out)
            return 'words'
        if os.path.exists(tmp_out):
            os.remove(tmp_out)
    return None

jobs = []
for cid, d in data.items():
    voice = voice_of[cid]
    jobs.append((voice, speakable(d['welcome']), d['welcomeAudio']))
    for st in d['steps']:
        jobs.append((voice, speakable(st['target']), st['audio']))
        if st.get('slowAudio'):
            jobs.append((voice, None, st['slowAudio']))  # Spanish only; landed already
    for text, path in zip(d['praise'], d['praiseAudio']):
        jobs.append((voice, speakable(text), path))
    for text, path in zip(d['retry'], d['retryAudio']):
        jobs.append((voice, speakable(text), path))

missing = [(v, t, o) for (v, t, o) in jobs if t and not ok_file(o)]
print(f'{len(missing)} clips for the stubborn builder', flush=True)
landed = failed = 0
for voice, text, out in missing:
    route = build_clip(voice, text, out)
    print(('OK  ' if route else 'FAIL'), route or '-', out, flush=True)
    if route:
        landed += 1
    else:
        failed += 1
print(f'stubborn build done: {landed} landed, {failed} failed', flush=True)
