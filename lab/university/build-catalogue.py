#!/usr/bin/env python3
"""Exolex University — catalogue builder (stage A, 2026-11-16).

Reads the College's own index of the Aldred corpus —
  MASTER-INDEX.md (4,671 entries, organised by divisions, waves and
  'Territory' topic headings) and INDEX-SUPPLEMENT-2026-11-14.md
  (2,535 entries, each carrying its College face) —
and builds lab/university/catalogue.json: sections (the ten faces, the
designs/engineering line, and the founding Foundations & Arts sections),
classes, and each class's real syllabus (paper titles + DOIs + result
lines exactly as the index prints them).

Method (no invented titles, no invented counts):
  * Master-index classes ARE the index's own groupings: a 'Territory'
    heading where one exists, otherwise the section heading itself.
  * Supplement classes are clusters of a face's papers by deterministic
    keyword themes on titles (the same style of rule the supplement
    itself used to assign faces); unmatched papers fall into the face's
    'open programme' class.
  * A master-index class's face is assigned by deterministic keyword
    scoring over its title and its papers' titles (designs first);
    no signal -> mathematical physics, the supplement's own stated
    default. Supplement papers keep their printed face.
  * DOIs are de-duplicated across the two files (master copy wins —
    it carries the fuller result lines).
Foundations & Arts classes are authored in this file (founding
curriculum) and labelled as such in the output.
"""
import json, re, sys, unicodedata
from collections import OrderedDict, defaultdict

BASE = '/home/hatch/workspace/your_files/cross-reference-2026-11-10'
HERE = '/home/hatch/workspace/fire-apps-git/lab/university'

FACE_OF = {
    'cosmology': 'cosmology', 'galactic dynamics': 'galactic',
    'astrophysics': 'astrophysics', 'particle': 'particle',
    'nuclear': 'nuclear', 'atomic/molecular': 'atomic',
    'condensed matter': 'condensed', 'plasma': 'plasma',
    'geophysics': 'geophysics', 'mathematical physics': 'mathematical',
    'designs/engineering': 'designs',
}

DOI_RE = re.compile(r'\*\*DOI:\*\*\s*(10\.5281/zenodo\.\d+)')
CLS_RE = re.compile(r'\*\*Class:\*\*\s*([a-z ]+?)\s*(?:·|$)')
FACE_RE = re.compile(r'\*\*Face:\*\*\s*([a-z/ ]+?)\s*(?:·|$)')
RES_RE = re.compile(r'^-\s*\*\*Result:\*\*\s*(.*)$')

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s.lower()).strip('-')
    return s[:64] or 'class'

def clean_result(r):
    if not r:
        return ''
    r = r.strip()
    if r.lower().startswith('result not yet abstracted'):
        return ''
    # wave entries repeat their DOI at the head of the result line
    r = re.sub(r'^DOI:\s*10\.5281/zenodo\.\d+\s+', '', r)
    r = re.sub(r'^\*\*DOI:\*\*\s*10\.5281/zenodo\.\d+\s*\*+\s*', '', r)
    r = r.replace('**', '')
    r = re.sub(r'\s*The full calculation, its stated assumptions, and its '
               r'comparison with published observational values are given '
               r'in the deposited paper.*$', '', r)
    if len(r) > 420:
        cut = r[:420]
        dot = cut.rfind('. ')
        r = (cut[:dot + 1] if dot > 200 else cut).strip()
    return r.strip()

def parse_index(path, kind):
    """Yield entries {title, doi, cls, face, result, group} where group is
    the class grouping key supplied by the file's own structure."""
    entries = []
    section = None
    territory = None
    cur = None
    def flush():
        nonlocal cur
        if cur and cur.get('doi'):
            entries.append(cur)
        cur = None
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('## '):
                flush()
                section = line[3:].strip()
                territory = None
                continue
            if line.startswith('### '):
                flush()
                t = line[4:].strip()
                if t.lower().startswith('territory'):
                    territory = re.sub(r'^Territory\s*[—–-]\s*', '', t)
                    continue
                cur = {'title': t, 'section': section, 'territory': territory}
                continue
            if cur is not None:
                m = DOI_RE.search(line)
                if m:
                    cur['doi'] = m.group(1)
                    c = CLS_RE.search(line)
                    if c: cur['cls'] = c.group(1).strip()
                    fc = FACE_RE.search(line)
                    if fc: cur['face'] = fc.group(1).strip()
                m = RES_RE.match(line)
                if m:
                    cur['result'] = clean_result(m.group(1))
    flush()
    return entries

def clean_section_title(s):
    if not s:
        return 'Untitled section'
    s = re.sub(r'\s*[—–-]\s*\d+\s+works.*$', '', s)
    s = re.sub(r'\s*\((?:added|20\d\d)[^)]*\)\s*$', '', s)
    s = re.sub(r'\s*\(Physics Wave \d+\)\s*$', '', s)
    s = re.sub(r'\s*\(College Face \d+\)\s*$', '', s)
    s = re.sub(r'\s*[—–-]\s*20\d\d-\d\d-\d\d\s*$', '', s)
    return s.strip() or 'Untitled section'


def kw_hit(kw, text):
    if kw.endswith('*'):
        return re.search(r'(?<![a-z])' + re.escape(kw[:-1]), text) is not None
    if ' ' in kw or '-' in kw:
        return kw in text
    return re.search(r'(?<![a-z])' + re.escape(kw) + r'(?![a-z])', text) is not None

# ---------------- face assignment for master-index classes ----------------
FACE_KEYWORDS = OrderedDict([
    ('designs', ['blueprint', 'design blueprint']),
    ('cosmology', ['bounce', 'cosmolog*', 'big bang', 'cmb', 'cosmic microwave',
                   'inflation', 'dark energy', 'vacuum', 'aldred limit',
                   'flatness', 'horizon problem', 'reheating', 'primordial',
                   'friedmann', 'fifth coordinate', 'transit', 'expansion of the universe']),
    ('galactic', ['galax*', 'galactic', 'milky way', 'rotation curve', 'dark matter halo']),
    ('astrophysics', ['stars', 'stellar', 'supernova', 'neutron star', 'white dwarf',
                      'black hole', 'pulsar', 'quasar', 'accretion', 'exoplanet',
                      'solar', 'gravitational wave', 'gamma-ray', 'cosmic ray',
                      'magnetar', 'asteroid', 'comet', 'planet']),
    ('particle', ['neutrino', 'lepton', 'quark', 'higgs', 'collider', 'muon',
                  'electroweak', 'particle', 'antimatter', 'positron']),
    ('nuclear', ['nuclear', 'nucleus', 'nuclei', 'fission', 'isotope', 'radioactiv*',
                 'nucleosynthesis', 'r-process', 'alpha decay']),
    ('atomic', ['atomic', 'atom', 'molecule', 'molecular', 'spectr*', 'laser',
                'optical clock', 'rydberg', 'photon', 'ion trap']),
    ('condensed', ['superconduct', 'condensate', 'bose-einstein', 'superfluid',
                    'magnetocaloric', 'semiconductor', 'graphene', 'spintronic',
                    'crystal lattice', 'phonon']),
    ('plasma', ['plasma', 'tokamak', 'magnetohydrodynamic', 'ionosphere']),
    ('geophysics', ['earth', 'seismic', 'earthquake', 'climate', 'ocean',
                    'atmospher', 'geothermal', 'volcano', 'groundwater',
                    'hydrolog', 'river', 'flood', 'soil', 'weather']),
    ('mathematical', ['theorem', 'proof', 'topology', 'formalism', 'foundations',
                      'impossibility', 'census', 'audit', 'index', 'counting',
                      'programme', 'reconstruction', 'geometry']),
])
DESIGN_TITLE_HINTS = ['pump', 'kiln', 'stove', 'filter', 'loom', 'press', 'mill',
                      'sanitation', 'housing', 'greenhouse', 'desalination',
                      'refrigerator', 'oven', 'latrine', 'well', 'roof']

def assign_face(class_title, papers):
    t = class_title.lower()
    if ('blueprint' in t or 'habitat' in t or 'systems derive' in t or
            'devices derive' in t or t.startswith('builds & designs')):
        return 'designs'
    scores = defaultdict(int)
    for face, kws in FACE_KEYWORDS.items():
        for kw in kws:
            if kw_hit(kw, t):
                scores[face] += 3
    for p in papers:
        pt = p['t'].lower()
        if pt.startswith('design blueprint'):
            scores['designs'] += 2
            continue
        for face, kws in FACE_KEYWORDS.items():
            if face == 'designs':
                continue
            for kw in kws:
                if kw_hit(kw, pt):
                    scores[face] += 1
                    break
    if not scores:
        for hint in DESIGN_TITLE_HINTS:
            if hint in t:
                return 'designs'
        return 'mathematical'
    return max(scores.items(), key=lambda kv: kv[1])[0]

def score_title_face(title):
    """Keyword face score for a single paper title (designs checked by
    the caller via the 'Design Blueprint' prefix rule)."""
    tl = title.lower()
    scores = defaultdict(int)
    for face, kws in FACE_KEYWORDS.items():
        if face == 'designs':
            continue
        for kw in kws:
            if kw_hit(kw, tl):
                scores[face] += 1
    if not scores:
        return 'mathematical'
    return max(scores.items(), key=lambda kv: kv[1])[0]

# The corpus's world-problems divisions and the Wave 6/7/8 applied
# collections are the applied line: the supplement files this same
# material under designs/engineering, so the catalogue does the same.
WORLD_DIVISIONS = {'Water', 'Food', 'Energy access', 'Health',
                   'Shelter & infrastructure', 'Air, fire & disaster',
                   'House record', 'Life in the universe',
                   'DNA & carbon computing', 'Information & computation'}
BARE_WAVE = re.compile(r'^(Physics\s+)?Wave\s+\d+\b', re.I)

# ---------------- supplement theme clustering ----------------
THEMES = {
    'cosmology': [
        ('The Bounce & the Aldred Limit', ['bounce', 'aldred limit', 'einstein–cartan', 'einstein-cartan', 'torsion']),
        ('The Surviving Count & Vacuum', ['count', 'vacuum', 'denominator', 'integer']),
        ('Matching & Modes Across the Bounce', ['matching', 'mode', 'conjugate', 'perturbation']),
        ('CMB & the Early Sky', ['cmb', 'microwave', 'axis', 'cold spot', 'anisotrop']),
        ('Dark Energy & Expansion', ['dark energy', 'expansion', 'hubble', 'cosmological constant', 'lambda']),
        ('Charges, Boundaries & Channels', ['charge', 'boundary', 'channel', 'slab']),
        ('Founding Papers, Re-read', ['paper #', 'reconstruction', 're-read', 'assembled']),
    ],
    'galactic': [
        ('Rotation & Haloes', ['rotation', 'halo', 'curve']),
        ('Dwarfs & Satellites', ['dwarf', 'satellite', 'spheroidal']),
        ('The Milky Way', ['milky way', 'galactic centre', 'galactic center']),
    ],
    'astrophysics': [
        ('Black Holes & Remnants', ['black hole', 'remnant', 'evaporation', 'hawking']),
        ('Stars & Their Deaths', ['star', 'supernova', 'white dwarf', 'neutron']),
        ('Waves & Signals', ['gravitational wave', 'gamma', 'cosmic ray', 'signal']),
        ('Planets & Systems', ['planet', 'exoplanet', 'asteroid', 'comet']),
    ],
    'particle': [
        ('Neutrinos & Leptons', ['neutrino', 'lepton', 'muon']),
        ('Quarks, Higgs & the Standard Model', ['quark', 'higgs', 'standard model', 'electroweak']),
        ('Collisions & Detectors', ['collid', 'detector', 'scattering', 'cross-section']),
    ],
    'nuclear': [
        ('Nuclei & Decays', ['nucle', 'decay', 'isotope']),
        ('Fission, Fusion & Capture', ['fission', 'fusion', 'capture']),
    ],
    'atomic': [
        ('Spectra & Light', ['spectr', 'photon', 'laser', 'optical']),
        ('Atoms, Ions & Clocks', ['atom', 'ion', 'clock', 'rydberg']),
        ('Molecules & Bonds', ['molecule', 'molecular', 'bond']),
    ],
    'condensed': [
        ('Superconductors & Condensates', ['superconduct', 'condensate', 'superfluid', 'bose']),
        ('Magnets & Cold Matter', ['magnet', 'spin', 'cryogen', 'cold']),
        ('Crystals, Lattices & Devices', ['crystal', 'lattice', 'semiconductor', 'device']),
    ],
    'plasma': [
        ('Plasma States & Discharges', ['plasma', 'discharge', 'tokamak']),
    ],
    'geophysics': [
        ('Water & the Ground', ['water', 'groundwater', 'well', 'river', 'flood', 'hydrolog']),
        ('Earth, Rock & Quakes', ['earth', 'seismic', 'quake', 'rock', 'soil', 'volcano']),
        ('Air, Climate & Oceans', ['climate', 'atmospher', 'ocean', 'weather', 'carbon']),
    ],
    'mathematical': [
        ('The Count & Its Constructions', ['count', 'construction', 'integer', 'denominator']),
        ('Theorems, Proofs & Bounds', ['theorem', 'proof', 'bound', 'lemma', 'inequality']),
        ('Frames, Coordinates & Formalisms', ['frame', 'coordinate', 'formalism', 'geometry', 'topology']),
        ('The Corpus Examining Itself', ['census', 'audit', 'index', 'paper #', 'reconstruction', 'catalogue', 'ledger']),
        ('Charges, Currents & Conservation', ['charge', 'current', 'conservation', 'symmetry']),
        ('Fields, Actions & Variations', ['field', 'action', 'lagrangian', 'variation', 'hamiltonian']),
    ],
    'designs': [
        ('Water, Wells & Sanitation', ['water', 'well', 'pump', 'sanitation', 'latrine', 'filter']),
        ('Food, Farming & Storage', ['food', 'farm', 'grain', 'storage', 'mill', 'oven', 'cook']),
        ('Shelter, Building & Materials', ['shelter', 'building', 'brick', 'roof', 'housing', 'material']),
        ('Energy, Light & Power', ['energy', 'solar', 'power', 'battery', 'light', 'charging']),
        ('Health & the Body', ['health', 'medical', 'clinic', 'prosthetic', 'diagnos']),
        ('Machines, Tools & Making', ['machine', 'tool', 'kiln', 'loom', 'press', 'engine', 'device']),
        ('Signals, Computing & Data', ['signal', 'computing', 'data', 'sensor', 'radio', 'network']),
    ],
}

def theme_for(face, title):
    tl = title.lower()
    for label, kws in THEMES.get(face, []):
        for kw in kws:
            if kw in tl:
                return label
    return None

# ---------------- Foundations & Arts: the founding curriculum ----------------
# Authored for stage A and labelled 'founding curriculum' in the output.
# Each class: syllabus units, a spoken opening lesson (~150 words, in the
# professor's manner), and one piece of homework with a worked answer.
FOUNDATIONS = [
 {'section': 'mathematics', 'title': 'Numbers & Proof — Foundations of Mathematics',
  'units': ['Counting and the natural numbers', 'Integers, rationals, and why fractions behave',
            'Irrational numbers and the real line', 'What a proof is: direct proof and contradiction',
            'Proof by induction — the ladder argument', 'Sets, functions, and the language of mathematics'],
  'lesson': "Welcome in. I am Professor Eleanor Whitfield, and this is Numbers and Proof — the class where mathematics stops being arithmetic you were handed and becomes reasoning you can check. We begin with counting, because everything else is built on it and almost nobody examines it. By the fourth week you will prove things — really prove them — first directly, then by contradiction, then by induction, which is a ladder you climb once and trust forever. Bring a pencil and a suspicious mind. If a step in my argument does not convince you, your job is to say so, out loud, in this room. That is not rudeness here. That is the subject.",
  'homework': {'q': 'Prove, in your own words, that there is no largest natural number — then say exactly which step of your proof would break if you tried it on the integers between 0 and 1.',
               'worked': 'Suppose there were a largest natural number, N. Then N + 1 is also a natural number, and it is larger — contradiction, so no largest exists. Between 0 and 1 the same trick fails at the first step: N + 1 leaves the set entirely, so the contradiction never forms. A proof is only as good as the ground it stands on.'}},
 {'section': 'mathematics', 'title': 'Geometry — Euclid\u2019s Workshop',
  'units': ['Points, lines, and the five postulates', 'Triangles: congruence and similarity',
            'Circles and their theorems', 'Constructions with straightedge and compass',
            'Area, volume, and the Pythagorean theorem proved three ways', 'What happens when the fifth postulate falls: a first look at curved geometry'],
  'lesson': "I am Eleanor Whitfield. This is Geometry — Euclid's Workshop, and the word workshop is chosen carefully: in here, we build. Two thousand three hundred years ago Euclid took five postulates — five sentences he declined to prove — and raised all of classical geometry on them, theorem by theorem, like courses of brick. We will do the same, with straightedge and compass in hand, because a construction you have performed is a theorem you understand in your fingers. In the final week we knock out the fifth postulate and watch the whole building lean into curved space — which is where, much later, Einstein will be waiting for you.",
  'homework': {'q': 'With straightedge and compass only, construct the perpendicular bisector of a line segment, and write one sentence explaining why every point on it is exactly as far from one end of the segment as from the other.',
               'worked': 'Draw circles of equal radius from both endpoints; where they cross, above and below, join the crossings — that line is the bisector. Every point on it sits on both circles\u2019 symmetry: the two triangles it forms with the endpoints are congruent, so the distances to the ends are equal. Equal radii in, equal distances out.'}},
 {'section': 'mathematics', 'title': 'Algebra — The Language of Unknowns',
  'units': ['Letters that stand for numbers', 'Equations and the balance principle',
            'Linear equations and their graphs', 'Quadratics: factoring and the formula',
            'Systems of equations', 'Inequalities and absolute value'],
  'lesson': "Eleanor Whitfield, once more — welcome to Algebra, the language of unknowns. Algebra begins the moment you let a letter stand for a number you do not yet know, and refuse to be frightened by it. An equation is a balance: whatever you do to one side, you do to the other, and the truth stays level. We will solve, graph, factor, and finally meet the quadratic formula — not as a spell to memorise but as a machine you will watch being built from completing the square. By the end, an unknown will feel less like a wall and more like a door with the handle on your side.",
  'homework': {'q': 'Solve 3x + 7 = 25, showing the balance step you use at each line. Then solve x\u00b2 \u2212 5x + 6 = 0 by factoring.',
               'worked': '3x + 7 = 25 \u2192 subtract 7 from both sides: 3x = 18 \u2192 divide both sides by 3: x = 6. For the quadratic, find two numbers that multiply to 6 and add to \u22125: \u22122 and \u22123, so (x \u2212 2)(x \u2212 3) = 0, giving x = 2 or x = 3. Check both in the original — algebra trusts, and then verifies.'}},
 {'section': 'english', 'title': 'English Grammar & the Sentence',
  'units': ['The parts of speech, without tears', 'Subjects, verbs, and the complete thought',
            'Clauses: independent, dependent, and runaway', 'Punctuation as traffic signals',
            'Agreement, tense, and pronoun discipline', 'Editing a broken paragraph back to health'],
  'lesson': "Enter, and bring your voice — I am Professor Clara Beaumont, and this is English Grammar and the Sentence. Grammar is not a set of traps laid by examiners; it is the engineering of English, the load-bearing structure under every sentence you will ever write or speak. We will name the parts of speech, find the subject and verb hiding in long sentences like actors in a crowd, and learn punctuation as what it truly is: traffic signals for the reader's eye. You will read aloud in this room — everyone does — because a sentence you cannot say smoothly is a sentence that is not finished. Curtain up.",
  'homework': {'q': 'Take this broken sentence — "Running down the street, the bag fell open and the letters scattered everywhere" — name the fault, and rewrite it so the grammar carries the meaning.',
               'worked': 'The fault is a dangling modifier: "running down the street" grammatically attaches to "the bag", and bags do not run. Rewrite: "Running down the street, I dropped the bag; it fell open and the letters scattered everywhere." Now the runner is a person, and the sentence stands up straight.'}},
 {'section': 'english', 'title': 'Literature — Stories That Built the Language',
  'units': ['Why stories survive: the test of rereading', 'Shakespeare: one play, read slowly',
            'The novel arrives: Austen and the free indirect voice', 'Poetry: sound carrying sense',
            'The short story: Chekhov\u2019s gun and other honest machinery', 'Modern voices and where literature goes next'],
  'lesson': "Clara Beaumont. This is Literature — Stories That Built the Language. We will not skim a hundred books in this room; we will read a few great ones slowly, aloud, the way they were built to be heard. Shakespeare first — one play, taken at walking pace, until the four-hundred-year-old jokes land again. Then Austen, who taught the novel to think in two voices at once; then poetry, where sound itself carries the sense; then the short story, the most honest machine in literature. A story survives because every generation finds itself inside it. Your task this term is to find where you are standing in each one.",
  'homework': {'q': 'Choose any scene from the play we are reading. In five sentences: what does each character on stage want, and what is stopping them getting it?',
               'worked': 'A strong answer names wants, not events. Example shape: "She wants the letter delivered before dawn, because everything she has planned depends on it. He wants to delay her, politely, because her success is his ruin. Neither can say so — the room is full of witnesses — so the want goes underground and comes out as manners." Want plus obstacle is the engine of every scene ever written.'}},
 {'section': 'english', 'title': 'Composition — Saying It Plain',
  'units': ['The plain sentence as a discipline', 'Paragraphs: one idea, fully landed',
            'Structure: opening, argument, close', 'Cutting: the ten-percent rule',
            'Writing for a reader who is busy', 'The essay: a position defended in the open'],
  'lesson': "I am Clara Beaumont, and this is Composition — Saying It Plain. Orwell gave the whole course in one line: never use a long word where a short one will do. Plain writing is not simple-minded writing; it is the hardest kind, because nothing hides. We will build paragraphs that land one idea at a time, structure arguments a busy reader can follow at speed, and practise cutting — every draft you bring me leaves ten percent lighter. Bring me your worst paragraph on the first day. We will make it stand up straight, and then we will make it walk.",
  'homework': {'q': 'Write one paragraph — five sentences at most — arguing for something you genuinely believe. Then cut twenty percent of its words without losing any of its meaning, and hand in both versions.',
               'worked': 'The cut version almost always wins by removing throat-clearing ("I think that", "in my opinion"), dead adverbs, and any sentence that repeats its neighbour in grander words. If a word can leave without the meaning limping, it was luggage, not cargo.'}},
 {'section': 'french', 'title': 'Fran\u00e7ais I — First Words, Real Sentences',
  'units': ['Sounds of French: vowels first', 'Bonjour, je m\u2019appelle\u2026 — introductions that work',
            '\u00catre et avoir: the two pillars', 'Numbers, days, and the caf\u00e9',
            'Questions: asking your way around Paris', 'The present tense of regular verbs'],
  'lesson': "Bonjour, et bienvenue. Je suis Madame Colette Marchand, and in this room, French is not studied — it is spoken, from the very first minute, mistakes and all, because mistakes are how a language moves in. Today: the vowels, which in French are pure and do not slide; your first introductions; and the two pillar verbs, \u00eatre and avoir, to be and to have, on which everything else will stand. By the end of this lesson you will order coffee, give your name, and say where you live — en fran\u00e7ais. Repeat after me, and do not whisper. A language learned quietly stays quiet.",
  'homework': {'q': 'Write five true sentences about yourself in French using \u00eatre and avoir — for example "Je suis \u00e9tudiant" or "J\u2019ai un chien" — and read them aloud twice.',
               'worked': 'Model answers: "Je suis d\u00e9butant, mais je suis patient. J\u2019ai un cahier et un stylo. Je suis content aujourd\u2019hui." Notice: \u00eatre for what you are, avoir for what you have — and "j\u2019ai" contracts because avoir begins with a vowel sound. Say them aloud; the mouth learns faster than the eye.'}},
 {'section': 'french', 'title': 'Fran\u00e7ais II — Conversation & the Pass\u00e9 Compos\u00e9',
  'units': ['Talking about yesterday: the pass\u00e9 compos\u00e9 with avoir', 'Verbs that travel with \u00eatre',
            'The imperfect: how things used to be', 'Future plans: aller + infinitive and the futur simple',
            'Opinions, preferences, and polite disagreement', 'A full conversation, start to finish'],
  'lesson': "Re-bonjour. Madame Marchand, and welcome to Fran\u00e7ais Two — the class where your French learns to talk about yesterday. Until now everything you said happened in the present; today we build the pass\u00e9 compos\u00e9, the workhorse past tense: a helper verb, avoir or \u00eatre, carrying a past participle, like a friend carrying the heavy end of a table. J'ai mang\u00e9 — I ate. Je suis all\u00e9 — I went. With those two shapes you can tell the story of your whole day, and a person who can tell stories in a language is no longer a tourist in it. Allez — racontez-moi votre journ\u00e9e.",
  'homework': {'q': 'Write four sentences about what you did yesterday, in the pass\u00e9 compos\u00e9: two with avoir, two with \u00eatre (aller, venir, arriver, partir\u2026).',
               'worked': 'Model: "Hier, j\u2019ai travaill\u00e9 le matin et j\u2019ai lu un livre. Je suis all\u00e9 au march\u00e9, puis je suis rentr\u00e9 \u00e0 la maison." Avoir carries most verbs; \u00eatre carries the verbs of coming and going — and with \u00eatre, the participle agrees: "elle est all\u00e9e".'}},
 {'section': 'music', 'title': 'Singing I — Breath, Pitch, and Your Own Voice',
  'units': ['Breath: the engine under the note', 'Posture and the open throat',
            'Finding pitch: matching a tone', 'Intervals you can hear: seconds, thirds, fifths',
            'Vowels and diction while singing', 'Your first song, performed in this room'],
  'lesson': "In, in — stand up straight and breathe with me. I am Professor Rosa Delgado, and this is Singing One. Your voice is not something you either have or don't have; it is an instrument you already own and have simply never been taught to play. We start with breath, because breath is the engine under every note you will ever sing, then posture, then the great first skill: hearing a pitch and matching it, cleanly, without sliding. You will sing in this room from the first day — briefly, kindly, and together — because the ear learns by doing, never by being described to. Pronti? Breathe in. Now — sing me that note back.",
  'homework': {'q': 'Practise the five-note scale (do re mi fa sol) on one breath, three times a day. Then record yourself matching three single piano or app tones, and write down which was hardest to match and why you think so.',
               'worked': 'Most people find the highest tone hardest: the breath runs thin and the pitch sags flat. The fix is not pushing — it is a taller posture and a slower, fuller breath before the note. Pitch problems are usually breath problems wearing a disguise.'}},
 {'section': 'music', 'title': 'Music Theory — Notes, Scales, and Why Songs Work',
  'units': ['The staff and the twelve notes', 'Major scales: the pattern of whole and half steps',
            'Intervals and how they feel', 'Chords: triads built in thirds',
            'The I\u2013IV\u2013V engine of a thousand songs', 'Minor keys and borrowed sadness'],
  'lesson': "Rosa Delgado — welcome to Music Theory, the class that answers the question every listener has asked: why does that song work? Twelve notes are all we get, and everything — every anthem, every lullaby — is arrangement. We will learn the staff, build the major scale from its pattern of whole and half steps, stack notes into chords, and take apart the famous one-four-five progression that powers a thousand songs, so you can hear the machine running under the music. Theory is not the enemy of feeling. It is feeling, with the lights turned on. By the end of term, no chord change will sneak past you ever again.",
  'homework': {'q': 'Build the C major scale and name its notes. Then build the three primary chords — I, IV, and V — and write out which scale notes each chord contains.',
               'worked': 'C major: C D E F G A B C — no sharps, no flats, the pattern W-W-H-W-W-W-H. Chord I (C major): C-E-G. Chord IV (F major): F-A-C. Chord V (G major): G-B-D. Those three chords, in that family, carry most of the songs you have ever loved.'}},
 {'section': 'music', 'title': 'Rhythm & Ear Training',
  'units': ['Pulse: finding the beat in anything', 'Note values and simple time',
            'Syncopation: the note that arrives early on purpose', 'Clapping patterns in two and three',
            'Hearing intervals by their songs', 'Dictation: writing down what you hear'],
  'lesson': "Professor Rosa Delgado. Rhythm and Ear Training — the class your feet attend as much as your ears. Rhythm is the oldest part of music; there were drums long before there were melodies, and a song with perfect notes and a wandering beat is a speech with the words in the wrong order. We will find the pulse in everything, clap in two and in three, meet syncopation — the note that arrives early on purpose and makes you move — and train the ear to name intervals by the songs they hide in. Homework in this class can be done walking, and I will know if you skipped it. Your feet will tell me.",
  'homework': {'q': 'Clap a steady pulse and count it in 4/4 for one minute without speeding up. Then clap the same pulse in 3/4. Write two sentences on how the two counts feel different in your body.',
               'worked': 'In 4/4 the weight lands squarely, like marching: ONE two three four. In 3/4 it rolls: ONE two three, ONE two three — a waltz lean. If your 4/4 sped up, your pulse was chasing your excitement; anchor it by breathing out on beat one.'}},
 {'section': 'history', 'title': 'World History — From River Valleys to Railways',
  'units': ['River valleys: farming, cities, and the first states', 'Empires and the roads that held them',
            'Faiths, philosophies, and the examined life', 'Trade winds: goods, germs, and ideas',
            'Revolutions: political and industrial', 'The twentieth century in one hard look'],
  'lesson': "Sit down. I am Professor Margaret Hale, and this is World History — from river valleys to railways. We begin where civilisation begins: beside rivers, where farming first let people stay in one place long enough to build cities, argue about gods, and invent writing to keep track of the grain. Everything after is the same story at larger scale — empires and the roads that held them, faiths that crossed oceans, revolutions that crossed everything. I will give you dates, because dates are anchors, but hear me: the dates are not the cargo. The cargo is people, deciding — often badly, sometimes magnificently — what to do next. That is what we study here.",
  'homework': {'q': 'Pick one river-valley civilisation (Nile, Mesopotamia, Indus, Yellow River). In six sentences: what did the river give them, what did it demand of them, and what did they build because of both?',
               'worked': 'Strong answers pair gift with demand. Egypt: the Nile gave predictable floods and rich silt — and demanded a calendar, surveying, and a state organised enough to manage both; what rose from that pairing was bureaucracy, monumental building, and three thousand years of continuity. Gift, demand, response: that triangle explains more history than any list of kings.'}},
 {'section': 'history', 'title': 'American History — The Republic\u2019s Argument With Itself',
  'units': ['Colonies and the road to independence', 'A constitution: the argument written down',
            'Expansion, and its price', 'Civil war: the argument turns violent',
            'Industry, immigration, and the new century', 'Depression, world wars, and the American century'],
  'lesson': "Margaret Hale. American History — the Republic's Argument With Itself, and I chose that title because it is the literal truth: this country was founded in an argument, written down in a constitution, and it has been arguing ever since about what its own words mean. We will follow that argument from the colonies to the present — through expansion and its price, through a civil war when the argument turned violent, through industry, depression, and world wars. I am not here to hand you a verdict on America, favourable or otherwise. I am here to make you able to argue about it with the evidence open on the table. That is a citizen's skill, and it is learnable.",
  'homework': {'q': 'Read the preamble of the Constitution — all fifty-two words. Choose the three words you think carry the most weight, and defend each choice in two sentences.',
               'worked': 'A defensible set: "We" (who is included in the author of this document?), "Union" (the thing being made more perfect — the document admits imperfection at its start), and "posterity" (the audience is the unborn; the argument is addressed to the future). Any three words can win if the defence is honest — marks go to the reasoning, not the choice.'}},
 {'section': 'writing', 'title': 'Writing I — The Clear Sentence',
  'units': ['What a sentence is for', 'Verbs that carry weight',
            'Cutting the fat: adverbs and throat-clearing', 'Rhythm: long and short sentences together',
            'The paragraph as a room the reader walks through', 'Revision: writing is rewriting'],
  'lesson': "Bring me a sentence you love. I am Professor June Calloway, and this is Writing One — The Clear Sentence. Everything you will ever write — letters, arguments, stories, applications that decide your life — is built from sentences, and a sentence has one job: to carry an idea from your mind into a stranger's without spilling it. We will put strong verbs back in charge, cut the adverbs that lean on them like drunks on a lamppost, and learn rhythm — the long sentence and the short one, played against each other like music. Revision is not punishment here; revision is the writing. The first draft is just you telling yourself the story.",
  'homework': {'q': 'Write one sentence about something you did today, using the strongest verb you can find. Then write it again with the verb weakened by an adverb — and note, honestly, what was lost.',
               'worked': 'Strong: "I tore the letter open." Weakened: "I quickly opened the letter." The strong verb carries speed, appetite, and feeling inside itself; the weak pair needs an adverb as a crutch and still says less. Verbs are the engine; adverbs are usually an apology for the engine.'}},
 {'section': 'writing', 'title': 'Storytelling — Structure, Scene, and Voice',
  'units': ['The shape of stories: setup, turn, landing', 'Scene versus summary',
            'Characters who want something', 'Dialogue that does two jobs at once',
            'Voice: the sound of a mind on the page', 'Endings that earn their feeling'],
  'lesson': "June Calloway. Storytelling — Structure, Scene, and Voice. Every story you have ever loved has the same skeleton under it: someone wants something, the world declines to hand it over, and the wanting changes them. We will learn to see that skeleton — setup, turn, landing — then put meat on it: scenes that happen in front of the reader instead of being reported, dialogue that does two jobs at once, and voice, which is simply the sound of one particular mind on the page. Bring a story you cannot forget. By the end of term you will know exactly why you cannot forget it — and you will be dangerous with a pen.",
  'homework': {'q': 'Take a true event from your own life, small as you like. Write it twice: once as summary ("Then I went home and\u2026"), once as a scene with dialogue. Four sentences each. Which one makes a reader feel something, and why?',
               'worked': 'The scene wins, almost every time — because the reader is present for it. Summary tells the reader what happened; a scene lets it happen to them. Dialogue does the heaviest lifting: two lines of speech can carry character, conflict, and feeling that a paragraph of summary can only describe from outside.'}},
]

# ---------------- speech sanitising for generated lessons ----------------
def speechify(text):
    t = text
    t = re.sub(r'(\d+(?:\.\d+)?)e([+-]?\d+)', r'\1 times ten to the \2', t)
    t = t.replace('rho_A', 'the Aldred Limit density').replace('ρ_A', 'the Aldred Limit density')
    t = t.replace('σ₈', 'sigma eight').replace('ΛCDM', 'the standard cosmological model')
    t = t.replace('×', ' by ').replace('−', '-').replace('–', '-')
    t = t.replace('ten to the +', 'ten to the ')
    if t.count('=') >= 3:
        # raw key = value dumps from computation receipts do not speak;
        # keep the prose lead-in and point at the deposit for figures
        m = re.search(r'\b[A-Za-z_][A-Za-z0-9_]*\s*=', t)
        if m:
            t = t[:m.start()].rstrip(' :,-') + \
                ' — the figures themselves are in the deposit, and on ' \
                'your syllabus.'
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

def first_sentenceish(text, cap=230):
    t = re.sub(r'\s+', ' ', text or '').strip()
    if len(t) <= cap:
        return t
    cut = t[:cap]
    dot = cut.rfind('. ')
    return (cut[:dot + 1] if dot > 120 else cut).strip()

def flagship_script(section, cls, prof):
    name = prof['name']
    papers = cls['papers']
    with_res = [p for p in papers if p.get('r')]
    parts = []
    parts.append(prof['greeting'] + ' I am ' + name + ', and this is ' +
                 cls['title'] + ' — a class in ' + section['name'] +
                 ' at Exolex University.')
    parts.append('The syllabus is real: ' + str(len(papers)) +
                 ' papers from the Aldred corpus, every one deposited and '
                 'citable, and in this room we read them for what they '
                 'actually claim.')
    walk = with_res[:3] if with_res else papers[:3]
    lead = ['First, ', 'Next, ', 'And then, ']
    for i, p in enumerate(walk):
        if p.get('r'):
            parts.append(lead[i] + p['t'] + '. Its stated result: ' +
                         speechify(first_sentenceish(p['r'], 260)))
        else:
            parts.append(lead[i] + p['t'] + '. Its result is read from '
                         'the deposit itself — the index carries the title '
                         'and the DOI, and the paper carries the numbers.')
    parts.append('That is the shape of this class: real claims, real '
                 'numbers, and the arguments between them. Your homework '
                 'is waiting on your desk.')
    return ' '.join(parts)

def college_homework(cls):
    p = cls['papers'][0]
    if p.get('r'):
        q = ('Take the paper \u201c' + p['t'] + '\u201d. Its stated result is: ' +
             first_sentenceish(p['r'], 300) +
             ' (a) Restate the claim in your own words. (b) Name one observation '
             'or computation that could prove it wrong.')
        w = ('A strong answer restates the claim without borrowing the paper\u2019s '
             'wording, then names a test the paper itself would accept — here, '
             'the natural test is to recompute or re-measure the headline '
             'quantity in the stated result and check it against the paper\u2019s '
             'own number, under the paper\u2019s own stated assumptions.')
    else:
        q = ('Read the deposit of \u201c' + p['t'] + '\u201d (DOI ' + p['doi'] +
             '). Write its result in one sentence of your own, and name the '
             'assumption the paper leans on hardest.')
        w = ('The index has not yet abstracted this paper\u2019s result, so the '
             'worked answer lives in the deposit itself: your one sentence '
             'should state what was computed or built, the headline number or '
             'specification, and the conditions it holds under — nothing the '
             'paper does not say.')
    return {'q': q, 'worked': w}

# ---------------- assembly ----------------
def main():
    roster = json.load(open(HERE + '/professors.json', encoding='utf-8'))
    sections_meta = {s['id']: s for s in roster['sections']}

    master = parse_index(BASE + '/MASTER-INDEX.md', 'master')
    supp = parse_index(BASE + '/INDEX-SUPPLEMENT-2026-11-14.md', 'supp')

    seen_doi = {}
    classes = OrderedDict()   # key -> {title, face, papers, source}

    def add_class(key, title, face, source):
        if key not in classes:
            classes[key] = {'title': title, 'face': face, 'papers': [], 'source': source}
        return classes[key]

    # master: classes are the index's own groupings — except bare wave
    # headings ('Physics Wave 9 — 102 works'), which group nothing; their
    # papers are clustered by title themes like the supplement's.
    for e in master:
        paper = {'t': e['title'], 'doi': e['doi']}
        if e.get('result'): paper['r'] = e['result']
        if e['doi'] in seen_doi:
            continue
        group = e.get('territory') or clean_section_title(e.get('section'))
        if not e.get('territory') and BARE_WAVE.match(group):
            face = ('designs' if e['title'].lower().startswith('design blueprint')
                    else score_title_face(e['title']))
            label = theme_for(face, e['title']) or (sections_meta[face]['name'] + ' — the open programme')
            key = 's:' + face + ':' + slug(label)
            c = add_class(key, label, face, 'master wave papers, theme cluster')
        else:
            key = 'm:' + slug(group)
            c = add_class(key, group, None, 'master-index grouping')
            c.setdefault('rawSection', e.get('section') or '')
        seen_doi[e['doi']] = key
        c['papers'].append(paper)
    for c in classes.values():
        if c['face'] is None and c['papers']:
            raw = c.get('rawSection', '')
            if (re.search(r'\(Wave [678]\)', raw) or
                    clean_section_title(raw) in WORLD_DIVISIONS or
                    c['title'] in WORLD_DIVISIONS):
                c['face'] = 'designs'
            else:
                c['face'] = assign_face(c['title'], c['papers'])

    # supplement: faces printed; classes are title-theme clusters per face
    for e in supp:
        if e['doi'] in seen_doi:
            continue
        face = FACE_OF.get((e.get('face') or '').strip(), 'mathematical')
        label = theme_for(face, e['title']) or (sections_meta[face]['name'] + ' — the open programme')
        key = 's:' + face + ':' + slug(label)
        c = add_class(key, label, face, 'supplement theme cluster')
        paper = {'t': e['title'], 'doi': e['doi']}
        if e.get('result'): paper['r'] = e['result']
        seen_doi[e['doi']] = key
        c['papers'].append(paper)

    # foundations
    for f in FOUNDATIONS:
        key = 'f:' + slug(f['title'])
        classes[key] = {'title': f['title'], 'face': f['section'],
                        'papers': [], 'source': 'founding curriculum',
                        'units': f['units'], 'lesson': f['lesson'],
                        'homework': f['homework']}

    # drop empties, assign ids + homework, pick flagships for audio
    out_sections = []
    total_classes = 0
    total_papers = 0
    for s in roster['sections']:
        sid = s['id']
        scls = []
        for key, c in classes.items():
            if c['face'] != sid or not (c['papers'] or c.get('units')):
                continue
            cid = slug(c['title'])
            entry = {'id': cid, 'title': c['title'], 'source': c['source'],
                     'count': len(c['papers']), 'papers': c['papers']}
            if c.get('units'): entry['units'] = c['units']
            if c.get('lesson'):
                entry['lesson'] = c['lesson']
                entry['audio'] = 'audio/' + entry['id'] + '.mp3'
            if c.get('homework'): entry['homework'] = c['homework']
            else: entry['homework'] = college_homework(c)
            scls.append(entry)
            total_papers += len(c['papers'])
        scls.sort(key=lambda x: -x['count'])
        # flagship: richest in real result lines, then largest
        best, best_score = None, -1
        for entry in scls:
            if entry['source'] == 'founding curriculum':
                continue
            score = sum(1 for p in entry['papers'] if p.get('r')) * 1000 + entry['count']
            if score > best_score:
                best, best_score = entry, score
        if best is not None:
            best['lesson'] = flagship_script(s, best, s['professor'])
            best['audio'] = 'audio/' + best['id'] + '.mp3'
        total_classes += len(scls)
        out_sections.append({'id': sid, 'name': s['name'], 'group': s['group'],
                             'professor': s['professor'], 'classes': scls,
                             'classCount': len(scls),
                             'paperCount': sum(e['count'] for e in scls)})

    catalogue = {
        'generated': '2026-11-16',
        'sources': ['MASTER-INDEX.md', 'INDEX-SUPPLEMENT-2026-11-14.md',
                    'founding curriculum (authored, stage A)'],
        'totals': {'papers': total_papers, 'classes': total_classes,
                   'sections': len(out_sections)},
        'sections': out_sections,
    }
    with open(HERE + '/catalogue.json', 'w', encoding='utf-8') as f:
        json.dump(catalogue, f, ensure_ascii=False, indent=1)
    print('papers indexed:', total_papers)
    print('unique DOIs:', len(seen_doi))
    print('classes:', total_classes)
    for s in out_sections:
        print(f"  {s['id']:14s} {s['classCount']:4d} classes  {s['paperCount']:5d} papers")
    audio = [(s['id'], e['id']) for s in out_sections for e in s['classes'] if e.get('audio')]
    print('flagship audio classes:', audio)

if __name__ == '__main__':
    main()
