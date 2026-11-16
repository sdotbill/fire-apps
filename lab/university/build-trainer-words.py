#!/usr/bin/env python3
"""Last-resort builder for trainer clips the TTS backend won't take
whole: Swedish, Norwegian, Danish, Russian, Ukrainian and Swahili
texts come back as 26-byte empties most of the time, at sentence level
and often at word level — but per-attempt success is probabilistic, so
a word retried patiently lands. This builder:

  1. tries the whole text a few times;
  2. else synthesizes WORD BY WORD (up to WORD_TRIES each), trims the
     leading silence of each word, and concatenates with a short pause
     between words — a deliberate, word-by-word model, which for a
     beginner's phrase model is honest teaching audio;
  3. single words just get retried (up to WORD_TRIES).

Writes only clips still missing (>3 KB rule, same as the other
builders). Idempotent. Logs every clip's route: whole / words / fail.
"""
import json, subprocess, os, sys, time, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
WHOLE_TRIES = 3
WORD_TRIES = 18
GAP = '0.14'          # seconds of air between words
MIN_OK = 3000

cat = json.load(open('catalogue.json'))
data = json.load(open('trainer-data.json'))['classes']
voice_of = {}
for s in cat['sections']:
    for c in s['classes']:
        voice_of[c['id']] = (c.get('professor') or s['professor'])['voiceId']

def speakable(text):
    return (text.replace('ø', 'o').replace('Ø', 'O')
                .replace('ʿ', '').replace('ʾ', ''))

def ok_file(path):
    return os.path.exists(path) and os.path.getsize(path) > MIN_OK

def tts_once(voice, text, out):
    subprocess.run(['/opt/hatch/bin/tts', 'speak', '--voice', voice,
                    '--text-stdin', '--output', out],
                   input=text.encode(), capture_output=True, timeout=240)
    return ok_file(out)

def synth_word(voice, word, tmpdir, tag):
    out = os.path.join(tmpdir, tag + '.mp3')
    feed = word if word.endswith(('.', '!', '?')) else word + '.'
    for _ in range(WORD_TRIES):
        if tts_once(voice, feed, out):
            return out
        time.sleep(2)
    return None

def build_by_words(voice, text, out):
    words = text.replace('—', ' ').replace(',', ' ').split()
    words = [w for w in words if w.strip()]
    if len(words) < 2:
        return False
    with tempfile.TemporaryDirectory() as td:
        parts = []
        for i, w in enumerate(words):
            p = synth_word(voice, w, td, f'w{i}')
            if not p:
                print('    word failed:', w, flush=True)
                return False
            trimmed = os.path.join(td, f't{i}.wav')
            r = subprocess.run(
                ['ffmpeg', '-y', '-v', 'error', '-i', p, '-af',
                 'silenceremove=start_periods=1:start_silence=0.05:'
                 'start_threshold=-45dB,areverse,'
                 'silenceremove=start_periods=1:start_silence=0.05:'
                 'start_threshold=-45dB,areverse',
                 '-ar', '44100', trimmed], capture_output=True)
            if r.returncode != 0 or not os.path.exists(trimmed):
                return False
            parts.append(trimmed)
        # concat with GAP seconds of silence between words
        inputs, filt = [], []
        for i, p in enumerate(parts):
            inputs += ['-i', p]
        n = len(parts)
        chain = []
        labels = ''
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
            return True
        if os.path.exists(tmp_out):
            os.remove(tmp_out)
        return False

jobs = []
for cid, d in data.items():
    voice = voice_of[cid]
    jobs.append((voice, speakable(d['welcome']), d['welcomeAudio']))
    for st in d['steps']:
        jobs.append((voice, speakable(st['target']), st['audio']))
    for text, path in zip(d['praise'], d['praiseAudio']):
        jobs.append((voice, speakable(text), path))
    for text, path in zip(d['retry'], d['retryAudio']):
        jobs.append((voice, speakable(text), path))

missing = [j for j in jobs if not ok_file(j[2])]
print(f'{len(missing)} clips to build by words/retries', flush=True)
landed = failed = 0
for voice, text, out in missing:
    route = None
    for _ in range(WHOLE_TRIES):
        if tts_once(voice, text, out):
            route = 'whole'
            break
        time.sleep(2)
    if not route and build_by_words(voice, text, out):
        route = 'words'
    if not route:
        # single-word (or stubborn) clip: brute retries on the whole text
        for _ in range(WORD_TRIES):
            if tts_once(voice, text, out):
                route = 'retried'
                break
            time.sleep(2)
    print(('OK  ' if route else 'FAIL'), route or '-', out, flush=True)
    if route:
        landed += 1
    else:
        failed += 1
print(f'word build done: {landed} landed, {failed} failed', flush=True)
