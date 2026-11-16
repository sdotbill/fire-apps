import json, subprocess, os, sys
cat = json.load(open('catalogue.json'))
os.makedirs('audio', exist_ok=True)
todo = []
for s in cat['sections']:
    for e in s['classes']:
        if e.get('audio') and e.get('lesson'):
            # The TTS backend deterministically chokes on 'ø' (verified
            # Nov 16 on the storytelling lesson): feed it the spoken
            # spelling; the board keeps the correct one.
            text = e['lesson'].replace('ø', 'o').replace('Ø', 'O')
            todo.append(((e.get('professor') or s['professor'])['voiceId'], text, e['audio']))
print(f'{len(todo)} lessons', flush=True)
for voice, text, out in todo:
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        print('skip', out, flush=True); continue
    r = subprocess.run(['/opt/hatch/bin/tts', 'speak', '--voice', voice,
                        '--text-stdin', '--output', out],
                       input=text.encode(), capture_output=True, timeout=240)
    ok = os.path.exists(out) and os.path.getsize(out) > 10000
    print(('OK  ' if ok else 'FAIL'), out, r.stdout.decode()[:120], r.stderr.decode()[:200], flush=True)
print('done', flush=True)
