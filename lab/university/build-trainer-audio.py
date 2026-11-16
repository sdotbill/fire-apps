#!/usr/bin/env python3
"""Generate the trainer's per-phrase clips with the Helio TTS pipeline,
in each professor's own roster voice (read from catalogue.json).

Clips: welcome, one model per step, a slow model per step for classes
with slow_all (Spanish), praise and retry lines. Idempotent — existing
clips over 3 KB are skipped, so a re-run only fills gaps.
"""
import json, subprocess, os, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

cat = json.load(open('catalogue.json'))
data = json.load(open('trainer-data.json'))['classes']

voice_of = {}
for s in cat['sections']:
    for c in s['classes']:
        voice_of[c['id']] = (c.get('professor') or s['professor'])['voiceId']

def speakable(text):
    # The TTS backend deterministically chokes on 'ø' (see gen-audio.py)
    # and on transliteration-only marks; the board keeps the true text.
    return (text.replace('ø', 'o').replace('Ø', 'O')
                .replace('ʿ', '').replace('ʾ', ''))

def slow_text(target):
    # Word-by-word, with air between the words — the slow model.
    words = speakable(target).replace(',', ' ').split()
    return ' … '.join(words) + '.'

jobs = []  # (voice, text, outpath)
for cid, d in data.items():
    voice = voice_of[cid]
    jobs.append((voice, speakable(d['welcome']), d['welcomeAudio']))
    for st in d['steps']:
        jobs.append((voice, speakable(st['target']), st['audio']))
        if st.get('slowAudio'):
            jobs.append((voice, slow_text(st['target']), st['slowAudio']))
    for text, path in zip(d['praise'], d['praiseAudio']):
        jobs.append((voice, speakable(text), path))
    for text, path in zip(d['retry'], d['retryAudio']):
        jobs.append((voice, speakable(text), path))

todo = [j for j in jobs
        if not (os.path.exists(j[2]) and os.path.getsize(j[2]) > 3000)]
print(f'{len(jobs)} clips total, {len(todo)} to generate', flush=True)

def run(job):
    voice, text, out = job
    os.makedirs(os.path.dirname(out), exist_ok=True)
    for attempt in range(2):
        r = subprocess.run(['/opt/hatch/bin/tts', 'speak', '--voice', voice,
                            '--text-stdin', '--output', out],
                           input=text.encode(), capture_output=True, timeout=240)
        if os.path.exists(out) and os.path.getsize(out) > 3000:
            return ('OK  ', out)
    return ('FAIL', out)

done = fail = 0
with ThreadPoolExecutor(max_workers=4) as ex:
    for status, out in ex.map(run, todo):
        if status == 'OK  ':
            done += 1
        else:
            fail += 1
            print('FAIL', out, flush=True)
        if (done + fail) % 25 == 0:
            print(f'…{done + fail}/{len(todo)}', flush=True)
print(f'done: {done} generated, {fail} failed', flush=True)
