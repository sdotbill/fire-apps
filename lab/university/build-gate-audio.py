#!/usr/bin/env python3
"""Generate the gate's per-step clips for the classes that already
carry a recorded lesson — in each professor's own roster voice, the
same Helio TTS pipeline as gen-audio.py / build-trainer-audio.py.

Clips per class: one presentation per lesson passage and per
question (the teach texts), the praise lines, the retry lines.
Paths come from gate-data.json
(audio/gate/<classId>/...). Idempotent — existing clips over 3 KB are
skipped, so a re-run only fills gaps, and the same script extends to
more classes whenever their audio paths are written into the data.
"""
import json, subprocess, os
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

cat = json.load(open('catalogue.json'))
data = json.load(open('gate-data.json'))['classes']

voice_of = {}
for s in cat['sections']:
    for c in s['classes']:
        voice_of[c['id']] = (c.get('professor') or s['professor'])['voiceId']

def speakable(text):
    return (text.replace('ø', 'o').replace('Ø', 'O')
                .replace('ʿ', '').replace('ʾ', ''))

jobs = []  # (voice, text, outpath)
for cid, d in data.items():
    if 'audioBase' not in d:
        continue
    voice = voice_of[cid]
    for ch in d.get('lesson', []):
        if ch.get('audio'):
            jobs.append((voice, speakable(ch['teach']), ch['audio']))
    for st in d['steps']:
        if st.get('audio'):
            jobs.append((voice, speakable(st['teach']), st['audio']))
    for text, path in zip(d['praise'], d.get('praiseAudio', [])):
        jobs.append((voice, speakable(text), path))
    for text, path in zip(d['retry'], d.get('retryAudio', [])):
        jobs.append((voice, speakable(text), path))

todo = [j for j in jobs
        if not (os.path.exists(j[2]) and os.path.getsize(j[2]) > 3000)]
print(f'{len(jobs)} clips total, {len(todo)} to generate', flush=True)

def run(job):
    voice, text, out = job
    os.makedirs(os.path.dirname(out), exist_ok=True)
    for attempt in range(2):
        subprocess.run(['/opt/hatch/bin/tts', 'speak', '--voice', voice,
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
