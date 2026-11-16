#!/usr/bin/env python3
"""Stage 3 queue runner — the non-stop background build.

Walks the catalogue in order; for every gate class with no lessons30
scripts yet: generate (gen-scripts-generic.py) -> audit -> synthesize
-> assemble -> ledger line -> scoped git commit. Each class is a
checkpoint: queue-state.json records done / deferred-thin / failed,
and every step is idempotent, so the runner can be killed and
restarted at any point and loses at most the class in flight.

A class whose material cannot field >=6 auditable questions is
deferred-thin: it stays on the existing gate, untouched. A synthesis
failure marks the class failed (audio retried on the next run) but
never stops the queue.

Usage: python3 run-queue.py [--max N] [--no-commit]
Run from lab/university/build-lessons30/.
"""
import json, os, subprocess, sys, glob, re

HERE = os.path.dirname(os.path.abspath(__file__))
UNI = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(UNI))
os.chdir(HERE)

LEDGER = os.path.expanduser(
    '~/workspace/your_files/thirty-minute-lessons-2026-11-16/LEDGER.md')

cat = json.load(open(os.path.join(UNI, 'catalogue.json')))
gate = json.load(open(os.path.join(UNI, 'gate-data.json')))['classes']
ORDER = []
for s in cat['sections']:
    for c in s['classes']:
        ORDER.append(c['id'])

qstate = {'done': [], 'deferred': [], 'failed': []}
if os.path.exists('queue-state.json'):
    qstate = json.load(open('queue-state.json'))


def save_qstate():
    with open('queue-state.json', 'w') as fh:
        json.dump(qstate, fh, indent=1)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def ledger_line(cid, lessons, minutes, questions, notes):
    with open(LEDGER, 'a') as fh:
        fh.write(f'| {cid} | {lessons} | {minutes} | {questions} | '
                 f'{notes} |\n')


def commit(cid):
    paths = [
        f'lab/university/build-lessons30/scripts/{cid}',
        f'lab/university/build-lessons30/questions/{cid}',
        f'lab/university/build-lessons30/state.json',
        f'lab/university/lessons30/{cid}.json',
        'lab/university/lessons30/index.json',
        f'lab/university/audio/lessons30/{cid}',
    ]
    run(['git', 'add', '--'] + paths, cwd=REPO)
    r = run(['git', 'commit', '-m',
             f'University 30-min lessons: {cid} (stage 3 queue)'],
            cwd=REPO)
    return r.returncode == 0


def process(cid, do_commit=True):
    gen = run([sys.executable, 'gen-scripts-generic.py', cid])
    out = gen.stdout + gen.stderr
    if 'deferred-thin' in out:
        qstate['deferred'].append(cid)
        save_qstate()
        print(f'{cid}: deferred-thin', flush=True)
        return 'deferred'
    if 'built' not in out:
        print(f'{cid}: generator said: {out.strip()[-200:]}', flush=True)
        return 'skip'
    aud = run([sys.executable, 'audit_questions.py', cid])
    shipped = 0
    for f in glob.glob(f'questions/{cid}/lesson-*.audited.json'):
        shipped += len(json.load(open(f)))
    if shipped < 6:
        qstate['deferred'].append(cid)
        save_qstate()
        print(f'{cid}: deferred-thin after audit ({shipped} questions)',
              flush=True)
        return 'deferred'
    syn = run([sys.executable, 'synth.py', cid])
    if 'SYNTH DONE' not in syn.stdout or ', 0 failed' not in syn.stdout:
        qstate['failed'].append(cid)
        save_qstate()
        print(f'{cid}: SYNTH FAILED — {(syn.stdout + syn.stderr)[-200:]}',
              flush=True)
        return 'failed'
    run([sys.executable, 'assemble.py', cid])
    data = json.load(open(os.path.join(UNI, 'lessons30', cid + '.json')))
    lessons = len(data['lessons'])
    minutes = round(sum(l['minutes'] for l in data['lessons']), 1)
    questions = sum(len(l['questions']) for l in data['lessons'])
    ledger_line(cid, lessons, minutes, questions,
                'stage 3, generated from class material')
    if do_commit:
        commit(cid)
    qstate['done'].append(cid)
    save_qstate()
    print(f'{cid}: DONE — {lessons} lessons, {minutes} min, '
          f'{questions} questions', flush=True)
    return 'done'


def main():
    args = sys.argv[1:]
    max_n = None
    do_commit = '--no-commit' not in args
    if '--max' in args:
        max_n = int(args[args.index('--max') + 1])
    settled = set(qstate['done']) | set(qstate['deferred'])
    todo = [cid for cid in ORDER
            if cid in gate and cid not in settled
            and not (os.path.exists(f'scripts/{cid}') and
                     os.listdir(f'scripts/{cid}'))]
    print(f'queue: {len(todo)} classes to process '
          f'({len(qstate["done"])} done, {len(qstate["deferred"])} '
          f'deferred so far)', flush=True)
    n = 0
    for cid in todo:
        if max_n is not None and n >= max_n:
            break
        process(cid, do_commit)
        n += 1
    print(f'queue run ended: {n} classes attempted; totals — '
          f'{len(qstate["done"])} done, {len(qstate["deferred"])} '
          f'deferred, {len(qstate["failed"])} failed', flush=True)


if __name__ == '__main__':
    main()
