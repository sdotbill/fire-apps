#!/usr/bin/env python3
"""Build the portrait generation manifest for Exolex University.

One entry per professor (760), keyed by classId, with a photorealistic
headshot prompt derived from the roster record itself: gender, background
group (matched against the name pools in build-stageb.py), the catalogue
portrait parameters (skin tone, hair colour/style, glasses, beard), a
deterministic age, and department-appropriate attire.

Priority tiers (Bill's order, Nov 16 2026):
  0 - Carmen Vega (Spanish flagship)
  1 - the 50 department heads (flagship classes)
  2 - the College ten faces (all classes)
  3 - everything else, by section
"""
import ast, hashlib, json, re, sys

HERE = __file__.rsplit('/', 1)[0]

# ---- recover BACKGROUNDS from build-stageb.py (literal data only) ----
src = open(HERE + '/build-stageb.py', encoding='utf-8').read()
tree = ast.parse(src)
bg_lists = None
for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') == 'BACKGROUNDS':
        bg_lists = ast.literal_eval(node.value.elts[0].args[0]) if False else None
# BG() calls wrap plain lists; evaluate them with a stub.
def BG(f, m, surnames, accents, skins, hairs):
    return {'f': f, 'm': m, 'surnames': surnames, 'accents': accents,
            'skins': skins, 'hairs': hairs}
for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') == 'BACKGROUNDS':
        bg_lists = eval(compile(ast.Expression(node.value), '<bg>', 'eval'),
                        {'BG': BG})
        break
GROUP_KEYS = ['anglo', 'blackam', 'hispanic', 'southasian', 'chinese',
              'japanese', 'korean', 'middleeast', 'african', 'easteuro',
              'seasia', 'scandi', 'mediterranean']
GROUPS = dict(zip(GROUP_KEYS, bg_lists))
ETHNICITY = {
    'anglo': 'white', 'blackam': 'Black American', 'hispanic': 'Latina Latino',
    'southasian': 'South Asian', 'chinese': 'Chinese', 'japanese': 'Japanese',
    'korean': 'Korean', 'middleeast': 'Middle Eastern',
    'african': 'Black African', 'easteuro': 'Eastern European',
    'seasia': 'Southeast Asian', 'scandi': 'Scandinavian',
    'mediterranean': 'Mediterranean Southern European',
}

def match_group(name, gender):
    clean = re.sub(r'^(Professor|Profesora|Madame|Herr|Dr\.)\s+', '', name)
    parts = clean.split()
    if len(parts) < 2:
        return None
    first, last = parts[0], parts[-1]
    best = None
    for key, g in GROUPS.items():
        firsts = g['f'] if gender == 'F' else g['m']
        if last in g['surnames'] and first in firsts:
            return key
        if last in g['surnames']:
            best = best or key
    return best

SKIN = {'#f6d7b8': 'fair skin', '#f2cfae': 'light skin',
        '#eec39a': 'light warm tan skin', '#d9a066': 'warm tan skin',
        '#b97a4a': 'medium brown skin', '#8d5524': 'deep brown skin',
        '#6f4420': 'deep brown skin', '#5d3a1a': 'rich deep brown skin'}
HAIRCOL = {'#14100c': 'black', '#191410': 'black', '#1c1410': 'black',
           '#2c1a10': 'very dark brown', '#3a2415': 'dark brown',
           '#57493a': 'medium brown', '#8a5a2a': 'light brown',
           '#a34d1c': 'auburn', '#caa06a': 'dark blonde',
           '#d8d3c8': 'silver-grey', '#6e6259': 'salt-and-pepper grey-brown'}
HAIRSTYLE = {'bob': 'a neat bob haircut', 'waves': 'shoulder-length wavy hair',
             'straight': 'long straight hair', 'curls': 'voluminous curly hair',
             'bun': 'hair in an elegant bun', 'ponytail': 'hair in a ponytail',
             'short': 'short, neatly cut hair'}

def attire(section_id, section_name):
    s = (section_id + ' ' + section_name).lower()
    if any(k in s for k in ['medicine', 'health & medicine']):
        return 'a white lab coat over smart professional clothing'
    if any(k in s for k in ['nursing']):
        return 'smart clinical dress with a cardigan'
    if any(k in s for k in ['public health', 'social work', 'kinesiology']):
        return 'a smart blazer over a blouse' 
    if any(k in s for k in ['trades']):
        return 'a neat dark work shirt, the dress of a master trades instructor'
    if any(k in s for k in ['law', 'business', 'economics', 'criminal']):
        return 'a formal suit jacket and shirt'
    if any(k in s for k in ['agriculture', 'earth', 'geophysics', 'biology']):
        return 'a smart field shirt under a casual blazer'
    if any(k in s for k in ['music', 'theatre', 'art & design']):
        return 'smart, slightly creative professional dress'
    if any(k in s for k in ['architecture', 'engineering', 'designs',
                            'computer', 'ai &']):
        return 'a tailored blazer over a shirt'
    return 'a classic academic blazer over a shirt'

STYLE = ('Photorealistic professional university faculty portrait photograph, '
         'head and shoulders, facing the camera with a warm, confident, '
         'approachable expression, soft natural window light, warm neutral '
         'beige studio background, shallow depth of field, natural skin '
         'texture, shot on an 85mm lens, vertical portrait orientation, '
         'photorealistic and highly detailed.')

def age_phrase(class_id, gender):
    h = int(hashlib.md5(class_id.encode()).hexdigest()[:6], 16)
    age = 35 + (h % 28)  # 35..62
    decade = (age // 10) * 10
    part = 'early' if age % 10 <= 3 else ('mid' if age % 10 <= 6 else 'late')
    return 'in %s %s %ds' % ('her' if gender == 'F' else 'his', part, decade)

def make_prompt(entry):
    gender = entry['gender']
    who = 'woman' if gender == 'F' else 'man'
    eth = ''
    if entry['group']:
        label = ETHNICITY[entry['group']]
        if entry['group'] == 'hispanic':
            label = 'Latina' if gender == 'F' else 'Latino'
        elif entry['group'] == 'mediterranean':
            label = 'Mediterranean Southern European'
        eth = label + ' '
    p = entry['portraitParams'] or {}
    skin = SKIN.get(p.get('skin', ''), '')
    haircol = HAIRCOL.get(p.get('hair', ''), 'dark')
    style = HAIRSTYLE.get(p.get('hairStyle', ''), 'neatly styled hair')
    hair = '%s %s' % (haircol, style)
    if p.get('hair') in ('#d8d3c8',) and gender == 'M':
        hair = 'silver-grey short hair'
    extras = ''
    if p.get('glasses'):
        extras += ', wearing tasteful glasses'
    if p.get('beard') and gender == 'M':
        extras += ', with a neatly trimmed beard'
    dress = attire(entry['sectionId'], entry['sectionName'])
    if gender == 'F':
        dress = dress.replace('a shirt', 'a blouse').replace('and shirt', 'and blouse')
    return ('%s A %s%s, a university professor %s, with %s and %s%s, dressed in %s.'
            % (STYLE, eth, who, age_phrase(entry['classId'], gender),
               skin or 'natural skin', hair, extras, dress))

def main():
    cat = json.load(open(HERE + '/catalogue.json', encoding='utf-8'))
    profs_meta = json.load(open(HERE + '/professors.json', encoding='utf-8'))
    head_names = {s['professor']['name'] for s in profs_meta['sections']}
    entries = []
    for sec in cat['sections']:
        for cls in sec['classes']:
            pr = cls['professor']
            grp = match_group(pr['name'], pr['gender'])
            if cls['id'] == 'espanol-i-speak-from-zero':
                grp = 'hispanic'  # Profesora Carmen Vega, the Spanish flagship
            tier = 3
            if cls['id'] == 'espanol-i-speak-from-zero':
                tier = 0
            elif pr['name'] in head_names:
                tier = 1
            elif sec['group'] == 'The College — the ten faces':
                tier = 2
            entries.append({
                'classId': cls['id'], 'sectionId': sec['id'],
                'sectionName': sec['name'], 'group': grp,
                'name': pr['name'], 'gender': pr['gender'],
                'portraitParams': pr.get('portrait'), 'tier': tier,
            })
    for e in entries:
        e['prompt'] = make_prompt(e)
        del e['portraitParams']
    entries.sort(key=lambda e: (e['tier'], e['sectionId'], e['classId']))
    json.dump({'total': len(entries), 'entries': entries},
              open(HERE + '/portraits-manifest.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    from collections import Counter
    print('entries:', len(entries), Counter(e['tier'] for e in entries))
    print('unmatched background:', sum(1 for e in entries if not e['group']))

if __name__ == '__main__':
    main()
