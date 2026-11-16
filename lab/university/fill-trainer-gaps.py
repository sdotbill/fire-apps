#!/usr/bin/env python3
"""Fill the trainer clips the parallel build could not land.

Six languages (Swedish, Norwegian, Danish, Russian, Ukrainian,
Swahili) hit a flaky TTS path: the backend returns a 26-byte empty
response for their texts most of the time, but not every time — the
parallel run landed roughly half of them. This filler works SERIALLY,
with pauses, up to N attempts per clip. Idempotent; safe to re-run.
"""
import json, subprocess, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
ATTEMPTS = int(sys.argv[1]) if len(sys.argv) > 1 else 10

cat = json.load(open('catalogue.json'))
data = json.load(open('trainer-data.json'))['classes']
voice_of = {}
for s in cat['sections']:
    for c in s['classes']:
        voice_of[c['id']] = (c.get('professor') or s['professor'])['voiceId']

def speakable(text):
    return (text.replace('ø', 'o').replace('Ø', 'O')
                .replace('ʿ', '').replace('ʾ', ''))

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

missing = [j for j in jobs
           if not (os.path.exists(j[2]) and os.path.getsize(j[2]) > 3000)]
print(f'{len(missing)} clips missing', flush=True)

landed = still = 0
for voice, text, out in missing:
    ok = False
    for attempt in range(ATTEMPTS):
        r = subprocess.run(['/opt/hatch/bin/tts', 'speak', '--voice', voice,
                            '--text-stdin', '--output', out],
                           input=text.encode(), capture_output=True, timeout=240)
        if os.path.exists(out) and os.path.getsize(out) > 3000:
            ok = True
            break
        time.sleep(4)
    print(('OK  ' if ok else 'FAIL'), out, f'({attempt + 1} tries)', flush=True)
    if ok:
        landed += 1
    else:
        still += 1
    time.sleep(2)
print(f'gap fill done: {landed} landed, {still} still missing', flush=True)
