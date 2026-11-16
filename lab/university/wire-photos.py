#!/usr/bin/env python3
"""Wire landed portraits into the university data.

Scans portraits/*.jpg; for every file named <classId>.jpg, sets
"photo": "portraits/<classId>.jpg" on:
  - catalogue.json  (the class's professor object, and the section
    professor object when it is the same person — department heads
    teach their flagship class)
  - roster.json     (the professor entry for that classId)
  - professors.json (the section head, matched through their flagship
    class in the catalogue)
Idempotent; run after every generation batch, then commit + push.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PDIR = os.path.join(HERE, 'portraits')

def load(name):
    with open(os.path.join(HERE, name), encoding='utf-8') as f:
        return json.load(f)

def save(name, data):
    with open(os.path.join(HERE, name), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

def main():
    landed = {}
    if os.path.isdir(PDIR):
        for fn in os.listdir(PDIR):
            if fn.endswith('.jpg'):
                landed[fn[:-4]] = 'portraits/' + fn
    print('portrait files on disk:', len(landed))

    cat = load('catalogue.json')
    head_class = {}   # head name -> classId of flagship class
    wired = 0
    for sec in cat['sections']:
        for cls in sec['classes']:
            if cls['id'] in landed:
                cls['professor']['photo'] = landed[cls['id']]
                wired += 1
                if cls['professor']['name'] == sec['professor']['name']:
                    head_class[sec['professor']['name']] = cls['id']
        hn = sec['professor']['name']
        if hn in head_class:
            sec['professor']['photo'] = landed[head_class[hn]]
    save('catalogue.json', cat)
    print('catalogue class professors wired:', wired)

    roster = load('roster.json')
    n = 0
    for p in roster['professors']:
        if p['classId'] in landed:
            p['photo'] = landed[p['classId']]
            n += 1
    save('roster.json', roster)
    print('roster entries wired:', n)

    profs = load('professors.json')
    n = 0
    for sec in profs['sections']:
        hn = sec['professor']['name']
        if hn in head_class:
            sec['professor']['photo'] = landed[head_class[hn]]
            n += 1
    if 'stylised figures drawn in the page' in profs.get('note', ''):
        profs['note'] = profs['note'].replace(
            'Portraits are stylised figures drawn in the page from the '
            'portrait parameters — no photographs, no real people.',
            'Portraits are photorealistic AI-generated headshots, one per '
            'professor, filed under portraits/<classId>.jpg and wired in '
            'through the "photo" field — no real people are depicted.')
    save('professors.json', profs)
    print('department heads wired:', n)

if __name__ == '__main__':
    main()
