#!/usr/bin/env python3
"""Regenerate ALL of Carmen Vega's audio in her new voice, slowed.

Bill (Nov 16 2026): her voice was too fast and not sultry enough.
Fix: Stately Sailboat (catalogue description: 'High-pitched Spanish
voice... Piping') -> Determined Mast ('Low-pitched Spanish voice with
moderate pacing', F, Spanish accent — the catalogue's only low-pitched
Spanish female voice, same 2694 family), and every synthesis at
--speed 88 (trainer slow-models at 76, word-spaced). Covers the full
Lesson 1 recording and all 40 trainer clips, so she never changes
voice or pace mid-lesson. Idempotent-ish: always re-synthesizes.
"""
import json, subprocess, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
VOICE = 'avocado_v2:vd3_vd2_r82_rep5k_2694_v068_28k_g5k'
SPEED, SLOW_SPEED = '88', '76'
CID = 'espanol-i-speak-from-zero'

cat = json.load(open('catalogue.json'))
data = json.load(open('trainer-data.json'))['classes'][CID]
lesson_text = None
for s in cat['sections']:
    for c in s['classes']:
        if c['id'] == CID:
            lesson_text = c['lesson']

def speakable(t):
    return t.replace('ø', 'o').replace('Ø', 'O').replace('ʿ', '').replace('ʾ', '')

def slow_text(target):
    words = speakable(target).replace(',', ' ').split()
    return ' … '.join(words) + '.'

def synth(text, out, speed):
    r = subprocess.run(['/opt/hatch/bin/tts', 'speak', '--voice', VOICE,
                        '--speed', speed, '--text-stdin', '--output', out],
                       input=speakable(text).encode(), capture_output=True, timeout=300)
    ok = os.path.exists(out) and os.path.getsize(out) > 3000
    print(('OK  ' if ok else 'FAIL'), out, f'(speed {speed})', flush=True)
    return ok

fails = 0
# the full Lesson 1 recording
if not synth(lesson_text, 'audio/espanol-i-speak-from-zero.mp3', SPEED):
    fails += 1
# trainer clips
if not synth(data['welcome'], data['welcomeAudio'], SPEED):
    fails += 1
for st in data['steps']:
    if not synth(st['target'], st['audio'], SPEED):
        fails += 1
    if st.get('slowAudio'):
        if not synth(slow_text(st['target']), st['slowAudio'], SLOW_SPEED):
            fails += 1
for text, path in zip(data['praise'], data['praiseAudio']):
    if not synth(text, path, SPEED):
        fails += 1
for text, path in zip(data['retry'], data['retryAudio']):
    if not synth(text, path, SPEED):
        fails += 1
print('carmen regen done, fails =', fails, flush=True)
sys.exit(1 if fails else 0)
