# -*- coding: utf-8 -*-
"""Exolex University — stage B build (2026-11-16).

Merges stageb-content.py (languages shelf, Spanish flagship, six new
authored sections) and stageb-curriculum.py (the full general
curriculum: 26 departments) into catalogue.json, reorders the
catalogue science-first, and gives EVERY class its own professor.

Faculty model (Bill's correction, Nov 16 01:31 EST): a mixed faculty,
like a real university — men and women, many backgrounds, realistic
full names, distinct two-line personalities, voices matched to the
professor (male voices for men, female for women) from the Helio/TTS
catalogue with maximal spread. The stage-A all-female head roster is
rebalanced: nine of the seventeen stage-A heads are now men (their
flagship lessons are re-introduced and re-recorded — see
HEAD_CHANGES / REASSIGN below and the stale-audio deletion at the
end). Bill's Spanish professor stays as specced: Profesora Carmen
Vega, a woman, teaching in the catalogue's Spanish-accented voice.

Deterministic: one seeded RNG drives every generated name, voice,
personality and portrait, so re-running reproduces the same faculty.
"""
import json, re, random, sys, os
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

content = load_mod('stageb_content', os.path.join(HERE, 'stageb-content.py'))
curric = load_mod('stageb_curriculum', os.path.join(HERE, 'stageb-curriculum.py'))

VOICES = json.load(open('/opt/hatch/skills/voice-selector/voice_source.json'))
BY_ID = {v['id']: v for v in VOICES}
DAVE_VOICE = 'avocado_v2:MAI_03'
CARMEN_VOICE = 'avocado_v2:vd3_vd2_r82_rep5k_2694_v068_28k_g5k'  # Determined Mast, F, Spanish accent — low-pitched (Bill, Nov 16 2026: Stately Sailboat was high-pitched/piping, too fast and not sultry enough; Determined Mast is the catalogue's low-pitched Spanish female voice). Synthesize Carmen at --speed 88 (slow clips 76).
assert BY_ID[CARMEN_VOICE]['gender'] == 'F' and BY_ID[CARMEN_VOICE]['accent'] == 'Spanish'

RNG = random.Random(20261116)

# ----------------------------------------------------------------------
# Voice allocator: per-gender shuffled pools, accent-preference queues,
# round-robin refill — maximal spread before any voice repeats.
# ----------------------------------------------------------------------
class VoiceAllocator:
    def __init__(self, exclude_ids):
        self.general = {'F': [], 'M': []}
        self.by_accent = {}
        for v in VOICES:
            g = v['gender']
            if g not in ('F', 'M') or v['id'] == DAVE_VOICE or v['id'] in exclude_ids:
                continue
            self.general[g].append(v)
            self.by_accent.setdefault((g, v['accent']), []).append(v)
            if v['language'] != 'eng':
                self.by_accent.setdefault((g, 'lang:' + v['language']), []).append(v)
        for g in self.general:
            RNG.shuffle(self.general[g])
        for k in self.by_accent:
            RNG.shuffle(self.by_accent[k])
        self.refills = {'F': 0, 'M': 0}

    def _from_general(self, gender):
        if not self.general[gender]:
            pool = [v for v in VOICES if v['gender'] == gender and v['id'] != DAVE_VOICE]
            RNG.shuffle(pool)
            self.general[gender] = pool
            self.refills[gender] += 1
        return self.general[gender].pop(0)

    def take(self, gender, accents=()):
        for a in accents:
            q = self.by_accent.get((gender, a), [])
            while q:
                v = q.pop(0)
                if v in self.general[gender]:
                    self.general[gender].remove(v)
                    return v
        return self._from_general(gender)

def voice_name(v):
    return '%s (%s)' % (v['name'], v['accent'])

# Voices already owned by kept stage-A heads + Carmen: never re-dealt.
KEPT_HEAD_VOICES = {
    'cosmology': 'avocado_v2:isabella', 'particle': 'avocado_v2:Caitlin',
    'condensed': 'avocado_v2:vdc_5', 'geophysics': 'avocado_v2:GrowthMindset',
    'mathematics': 'avocado_v2:paloma', 'french': 'avocado_v2:MAI_01_fr_ca',
    'music': 'avocado_v2:marisol', 'writing': 'avocado_v2:Lily',
}
ALLOC = VoiceAllocator(set(KEPT_HEAD_VOICES.values()) | {CARMEN_VOICE})

def prof_object(name, gender, personality, greeting, portrait, voice):
    return {'name': name, 'gender': gender, 'personality': personality,
            'greeting': greeting, 'voiceId': voice['id'],
            'voiceName': voice_name(voice), 'portrait': portrait}

# ----------------------------------------------------------------------
# Stage-A head changes (owner correction): nine sections get new,
# male department heads. Greetings are kept where the recorded
# flagship lesson opens with them, so the lesson needs only its
# name line re-introduced (english/history get a fresh opening).
# ----------------------------------------------------------------------
HEAD_CHANGES = {
    'galactic': dict(
        name='Professor Marcus Webb', gender='M', accents=('American',),
        personality="A field astronomer's patience in a linebacker's frame; he reads a galaxy the way a tracker reads ground — sign first, story second. His favourite question, asked about everything: and what would that look like from inside it?",
        greeting='Pick a star to stand on. Now we can begin.',
        portrait={'skin': '#8d5524', 'hair': '#14100c', 'hairStyle': 'short', 'outfit': '#23365c', 'glasses': False}),
    'astrophysics': dict(
        name='Professor Kenji Nakamura', gender='M', accents=('Japanese', 'American'),
        personality="Quiet, precise, and funny in a dry register that sneaks up on the room; stars are his home territory and he teaches them like neighbours whose habits he has watched for years. He will make you derive a lifetime before he lets you quote one.",
        greeting='Come in — the stars have been waiting politely.',
        portrait={'skin': '#eec39a', 'hair': '#191410', 'hairStyle': 'short', 'outfit': '#9a4a1f', 'glasses': False}),
    'nuclear': dict(
        name='Professor Yusuf Al-Rashid', gender='M', accents=('Middle Eastern', 'British'),
        personality="Measured as a metronome; nothing in his room is approximate that can be made exact. Kind about errors, ruthless about units, and famous for the pause he takes before answering — the answer is always worth it.",
        greeting='Sit. Units on the board before opinions, please.',
        portrait={'skin': '#d9a066', 'hair': '#2c1a10', 'hairStyle': 'short', 'outfit': '#3c3f45', 'glasses': True, 'beard': True}),
    'atomic': dict(
        name='Professor Tomás Herrera', gender='M', accents=('Spanish', 'American'),
        personality="Warm, quick, and precise in equal measure; spectra are sentences he reads aloud until the whole room can read them too. He sets problems that look small and open like trapdoors.",
        greeting='Welcome! Every line of light is a sentence — today we read.',
        portrait={'skin': '#d9a066', 'hair': '#3a2415', 'hairStyle': 'waves', 'outfit': '#1f4d7a', 'glasses': False}),
    'plasma': dict(
        name='Professor Rajan Mehta', gender='M', accents=('Indian',),
        personality="High voltage in every sense; he teaches the fourth state of matter like weather — because it is. He expects courage, rewards it, and keeps a straight face exactly until the discharge makes that impossible.",
        greeting='Mind the discharge. The fourth state does not sit still, and neither do we.',
        portrait={'skin': '#b97a4a', 'hair': '#14100c', 'hairStyle': 'short', 'outfit': '#8c1f2e', 'glasses': False}),
    'mathematical': dict(
        name='Professor Stefan Nowak', gender='M', accents=('German', 'British'),
        personality="Crisp to the point of music; a proof in his room is built like a bridge, in the open, one honest span at a time. 'Almost rigorous' is his only insult, and he has used it twice in a decade.",
        greeting='We begin from definitions. Everything else is negotiation.',
        portrait={'skin': '#f2cfae', 'hair': '#6e6259', 'hairStyle': 'short', 'outfit': '#46536a', 'glasses': True}),
    'designs': dict(
        name='Professor Miguel Santos', gender='M', accents=('Brazilian', 'Spanish'),
        personality="A builder before a talker; every design in his room gets costed, stressed, and asked what it is for. Blueprints are promises — he teaches you to keep them, in pencil first and in public always.",
        greeting="Roll up your sleeves. If we can't build it on paper honestly, we don't build it at all.",
        portrait={'skin': '#d9a066', 'hair': '#2c1a10', 'hairStyle': 'short', 'outfit': '#7a4a1f', 'glasses': False}),
    'english': dict(
        name='Professor James Whitaker', gender='M', accents=('British',),
        personality="Commanding and theatrical in the best way; the canon is his stage and grammar his swordplay. He will expect you to read aloud — well — and he will show you exactly how, line by line, until you can.",
        greeting='Come in, and bring a sentence you love. In this room, we read aloud.',
        portrait={'skin': '#f2cfae', 'hair': '#57493a', 'hairStyle': 'short', 'outfit': '#1f5138', 'glasses': False}),
    'history': dict(
        name='Professor Samuel Adeyemi', gender='M', accents=('Nigerian', 'British'),
        personality="Deep-voiced and steady; he teaches the past as an argument people were having with their own future. Dates are anchors in his room, never the cargo, and every source gets asked who wrote it and why.",
        greeting='Take a seat. The past is about to argue with the present.',
        portrait={'skin': '#8d5524', 'hair': '#14100c', 'hairStyle': 'short', 'outfit': '#5d4630', 'glasses': False}),
}
OLD_HEAD_NAMES = {
    'galactic': 'Mara Ellison', 'astrophysics': 'Naomi Reyes',
    'nuclear': 'Ruth Callahan', 'atomic': 'Aila Korhonen',
    'plasma': 'Zara Okafor', 'mathematical': 'Vera Lindqvist',
    'designs': 'Bea Kowalski', 'english': 'Clara Beaumont',
    'history': 'Margaret Hale',
}
# Flagship-lesson opening replacements for the two heads whose
# greeting changed (the other seven keep their greeting verbatim).
SPECIAL_INTROS = {
    'english': ("Enter, and bring your voice — I am Professor Clara Beaumont, and this is English Grammar and the Sentence.",
                "Come in, and bring a sentence you love. I am Professor James Whitaker, and this is English Grammar and the Sentence."),
    'history': ("Sit down. I am Professor Margaret Hale, and this is World History",
                "Take a seat. The past is about to argue with the present. I am Professor Samuel Adeyemi, and this is World History"),
}

# ----------------------------------------------------------------------
# Founding-class reassignments: nine recorded stage-A classes get
# their own professor (not the section head). Intro seams are exact.
# ----------------------------------------------------------------------
REASSIGN = {
    'geometry-euclids-workshop': dict(
        name='Professor Priya Raman', gender='F', accents=('Indian',),
        personality="A geometer who still draws every figure freehand before she proves anything about it; the compass, she insists, is a thinking tool, not a drawing tool. Patient with stuck students, impatient with unstated assumptions — in her room, what you are given is said out loud.",
        greeting='Straightedge, compass, patience. We build.',
        portrait={'skin': '#b97a4a', 'hair': '#1c1410', 'hairStyle': 'ponytail', 'outfit': '#6d1f2c', 'glasses': False},
        intro=("I am Eleanor Whitfield. This is Geometry — Euclid's Workshop",
               "I am Professor Priya Raman. This is Geometry — Euclid's Workshop")),
    'algebra-the-language-of-unknowns': dict(
        name='Professor Felix Wagner', gender='M', accents=('German',),
        personality="Dry, warm, and quietly delighted by the moment a letter stops frightening a student; he teaches algebra as a language for saying true things about numbers you have not met yet. Every equation in his room gets balanced twice — once on the board, once in words.",
        greeting='Letters are numbers in disguise. Come in.',
        portrait={'skin': '#f2cfae', 'hair': '#8a5a2a', 'hairStyle': 'short', 'outfit': '#2e3d6e', 'glasses': True},
        intro=("Eleanor Whitfield, once more — welcome to Algebra, the language of unknowns.",
               "I am Professor Felix Wagner — welcome to Algebra, the language of unknowns.")),
    'literature-stories-that-built-the-language': dict(
        name='Professor Amara Okafor', gender='F', accents=('Nigerian',),
        personality="A slow reader in a fast century; she teaches a few great books the way they were built to be heard — aloud, at walking pace, with the room arguing back. Her marginalia are famous, and her silences are teaching too.",
        greeting='We read slowly here, and we read aloud.',
        portrait={'skin': '#8d5524', 'hair': '#14100c', 'hairStyle': 'curls', 'outfit': '#1f5138', 'glasses': False},
        intro=("Clara Beaumont. This is Literature — Stories That Built the Language.",
               "I am Professor Amara Okafor. This is Literature — Stories That Built the Language.")),
    'composition-saying-it-plain': dict(
        name='Professor Henry Walsh', gender='M', accents=('Irish', 'British'),
        personality="Smooth, friendly, and merciless about the draft — never about the writer. He believes plain writing is the hardest kind because nothing hides, and he will prove it on your first paragraph, kindly, in pencil.",
        greeting='Bring me your longest sentence. We will set it free.',
        portrait={'skin': '#f6d7b8', 'hair': '#a34d1c', 'hairStyle': 'waves', 'outfit': '#3c3f45', 'glasses': False},
        intro=("I am Clara Beaumont, and this is Composition — Saying It Plain.",
               "I am Professor Henry Walsh, and this is Composition — Saying It Plain.")),
    'francais-ii-conversation-the-passe-compose': dict(
        name='Professor Camille Renaud', gender='F', accents=('lang:fra', 'French'),
        personality="Bright, exact, and completely unshockable by a beginner's mistakes — she has heard them all, and answers each one by handing the sentence back fixed, with a smile. In her room the past tense is a door, and she holds it open.",
        greeting="Re-bonjour. Aujourd'hui, nous parlons d'hier.",
        portrait={'skin': '#eec39a', 'hair': '#7a3b14', 'hairStyle': 'bob', 'outfit': '#4b2a63', 'glasses': False},
        intro=("Madame Marchand, and welcome to Français Two",
               "I am Professor Camille Renaud, and welcome to Français Two")),
    'music-theory-notes-scales-and-why-songs-work': dict(
        name='Professor Jonas Lindberg', gender='M', accents=('Finnish', 'British'),
        personality="A theorist with a performer's timing; he answers 'why does that song work?' at the piano, with his hands, before he allows a single term onto the board. Twelve notes are all we get — he makes that sound like wealth, because it is.",
        greeting='Twelve notes. Everything else is arrangement — come in.',
        portrait={'skin': '#f2cfae', 'hair': '#caa06a', 'hairStyle': 'short', 'outfit': '#26332a', 'glasses': False},
        intro=("Rosa Delgado — welcome to Music Theory",
               "I am Professor Jonas Lindberg — welcome to Music Theory")),
    'rhythm-ear-training': dict(
        name='Professor Keisha Thompson', gender='F', accents=('American',),
        personality="A drummer's discipline with a teacher's grin; her class is attended by feet as much as ears, and she conducts both. Rhythm is the oldest part of music in her room, and nobody hides behind the notes.",
        greeting='Feet first, ears open. We start on the beat.',
        portrait={'skin': '#8d5524', 'hair': '#14100c', 'hairStyle': 'curls', 'outfit': '#b4502e', 'glasses': False},
        intro=("Professor Rosa Delgado. Rhythm and Ear Training",
               "I am Professor Keisha Thompson. Rhythm and Ear Training")),
    'american-history-the-republics-argument-with-itself': dict(
        name='Professor Nathan Cole', gender='M', accents=('American',),
        personality="A storyteller with a cross-examiner's habits; he teaches the republic as the argument it has always been with itself, and he makes both sides of every question stand up and be heard before either is judged. Primary sources first, verdicts last.",
        greeting='The argument started in 1776. It is still going — sit down.',
        portrait={'skin': '#eec39a', 'hair': '#4a2c14', 'hairStyle': 'short', 'outfit': '#5d4630', 'glasses': False},
        intro=("Margaret Hale. American History",
               "I am Professor Nathan Cole. American History")),
    'storytelling-structure-scene-and-voice': dict(
        name='Professor Ingrid Sørensen', gender='F', accents=('Finnish', 'British'),
        personality="A novelist who teaches structure the way engineers teach load — because a story, like a bridge, fails where the weight was never carried. Warm about drafts, exact about skeletons, and incapable of letting a scene end one beat early.",
        greeting='Someone wants something. That is where we start.',
        portrait={'skin': '#f6d7b8', 'hair': '#d8d3c8', 'hairStyle': 'straight', 'outfit': '#2e3d6e', 'glasses': True},
        intro=("June Calloway. Storytelling",
               "I am Professor Ingrid Sørensen. Storytelling")),
}

# ----------------------------------------------------------------------
# Generated faculty: realistic names across many backgrounds.
# ----------------------------------------------------------------------
def BG(f, m, surnames, accents, skins, hairs):
    return {'f': f, 'm': m, 'surnames': surnames, 'accents': accents,
            'skins': skins, 'hairs': hairs}

BACKGROUNDS = [
    BG(['Mary','Susan','Karen','Patricia','Jennifer','Linda','Elizabeth','Barbara','Sarah','Jessica','Emily','Hannah','Megan','Rachel','Lauren','Nicole','Amanda','Stephanie','Rebecca','Catherine'],
       ['James','John','Robert','Michael','William','David','Richard','Joseph','Thomas','Charles','Daniel','Matthew','Anthony','Mark','Steven','Paul','Andrew','Kenneth','George','Edward'],
       ['Smith','Johnson','Williams','Brown','Jones','Miller','Davis','Wilson','Moore','Taylor','Anderson','Jackson','White','Harris','Martin','Clark','Lewis','Walker','Hall','Allen','Young','King','Wright','Scott','Adams','Baker','Carter','Mitchell','Roberts','Turner','Phillips','Campbell','Parker','Evans','Edwards','Collins','Stewart','Morris','Rogers','Reed','Cook','Morgan'],
       ['American','British'], ['#f6d7b8','#f2cfae','#eec39a'], ['#3a2415','#57493a','#8a5a2a','#caa06a','#6e6259','#a34d1c','#2c1a10']),
    BG(['Denise','Angela','Pamela','Jasmine','Imani','Nia','Regina','Tanya','Valerie','Yolanda','Camille','Ebony','Faith','Grace','Monique','Shanice','Brianna','Aaliyah','Latoya','Hope'],
       ['Andre','Brandon','Calvin','Darnell','Elijah','Franklin','Gregory','Harold','Isaiah','Jamal','Keith','Lamar','Nathaniel','Otis','Preston','Quentin','Reginald','Terrence','Dwayne','Jerome'],
       ['Washington','Jefferson','Booker','Douglass','Freeman','Banks','Grant','Hughes','Jenkins','Marshall','Owens','Parks','Simmons','Tate','Vaughn','Wells','Brooks','Coleman','Bryant','Foster','Graham','Henry','Lawson','Perkins'],
       ['American','Southern American'], ['#8d5524','#6f4420','#5d3a1a'], ['#14100c','#1c1410']),
    BG(['Ana','Lucía','Marta','Elena','Isabel','Sofía','Valentina','Camila','Fernanda','Gabriela','Mariana','Natalia','Alejandra','Daniela','Carolina'],
       ['Carlos','José','Luis','Jorge','Fernando','Alejandro','Rafael','Diego','Andrés','Javier','Manuel','Ricardo','Eduardo','Francisco','Antonio','Pedro','Héctor','Óscar','Raúl','Enrique'],
       ['García','Rodríguez','Martínez','López','González','Pérez','Sánchez','Ramírez','Torres','Flores','Rivera','Vásquez','Morales','Jiménez','Ortiz','Castillo','Guerrero','Delgado','Navarro'],
       ['Spanish','American'], ['#d9a066','#b97a4a','#eec39a'], ['#2c1a10','#3a2415','#14100c']),
    BG(['Ananya','Deepika','Kavita','Meera','Nisha','Pooja','Radha','Shreya','Sunita','Vidya','Aisha','Farah','Lakshmi','Divya','Ritu','Anita','Geeta','Rekha','Sita','Maya'],
       ['Arjun','Vikram','Rohan','Amit','Sanjay','Rajesh','Kiran','Nikhil','Aditya','Pranav','Varun','Deepak','Manoj','Suresh','Harish','Anand','Ravi','Vijay','Ashok','Rahul'],
       ['Patel','Sharma','Khan','Singh','Kumar','Gupta','Reddy','Iyer','Nair','Rao','Ahmed','Das','Chatterjee','Banerjee','Krishnan','Menon','Pillai','Verma','Joshi','Malhotra','Chandra'],
       ['Indian'], ['#b97a4a','#8d5524','#d9a066'], ['#14100c','#1c1410']),
    BG(['Wei','Jing','Li','Na','Xia','Yan','Fang','Hui','Lei','Min','Ping','Juan','Tao','Xue','Ying'],
       ['Wei','Qiang','Lei','Tao','Jun','Hao','Peng','Bo','Chao','Feng','Jian','Ming','Yong','Bin','Kai'],
       ['Wang','Li','Zhang','Liu','Chen','Yang','Huang','Zhao','Wu','Zhou','Xu','Sun','Hu','Zhu','Gao','Lin','He','Guo','Ma','Luo'],
       ['Chinese','Singaporean'], ['#f2cfae','#eec39a'], ['#14100c','#191410']),
    BG(['Sakura','Hana','Aiko','Keiko','Noriko','Yumi','Akiko','Emi','Rina','Kaori','Maki','Yoko','Tomoko','Sachiko','Junko'],
       ['Takeshi','Satoshi','Masahiro','Kazuo','Takashi','Yoshio','Akira','Shinji','Daisuke','Ryota','Kenta','Shota','Yuta','Naoki','Hiro'],
       ['Sato','Suzuki','Takahashi','Watanabe','Ito','Yamamoto','Kobayashi','Kato','Yoshida','Yamada','Sasaki','Yamaguchi','Matsumoto','Inoue','Kimura','Hayashi','Shimizu','Nakamura'],
       ['Japanese','American'], ['#f2cfae','#eec39a'], ['#14100c','#191410']),
    BG(['Ji-Eun','Seo-Yeon','Min-Ji','Hae-Won','Soo-Jin','Eun-Ji','Hye-Jin','Mi-Kyung','Young-Hee','Ji-Yeon','Su-A','Ye-Jin','Da-Eun','Chae-Won','Ji-Min'],
       ['Ji-Hoon','Sung-Min','Jae-Hyun','Dong-Hyun','Min-Ho','Jun-Seok','Tae-Yang','Woo-Jin','Hyun-Woo','Sang-Chul','Kyung-Min','Young-Jae','Seung-Ho','Jin-Woo','Chang-Min'],
       ['Kim','Lee','Park','Choi','Jung','Cho','Yoon','Shin','Lim','Bae','Kwon','Moon','Seo','Hwang','Ahn','Yang','Song','Hong'],
       ['Korean','American'], ['#f2cfae','#eec39a'], ['#14100c']),
    BG(['Fatima','Maryam','Noor','Huda','Rania','Samira','Yasmin','Dalia','Leila','Amal','Sana','Rana','Dina','Hala','Mona'],
       ['Ahmed','Khalid','Tariq','Samir','Karim','Bilal','Faisal','Nabil','Rami','Hassan','Ibrahim','Yusuf','Adel','Walid','Tarek'],
       ['Khalil','Aziz','Rahman','Saleh','Nasser','Habib','Mansour','Farouk','Barakat','Saad','Rahal','Antoun','Haddad','Awad','Daher','Karam','Sleiman'],
       ['Middle Eastern','British'], ['#d9a066','#b97a4a','#eec39a'], ['#2c1a10','#14100c','#3a2415']),
    BG(['Adaeze','Ngozi','Zainab','Halima','Chiamaka','Efua','Akosua','Zuri','Folasade','Achieng','Wanjiru','Njeri','Funke','Yetunde','Baraka'],
       ['Kofi','Kwame','Chidi','Emeka','Tunde','Babatunde','Sekou','Amadou','Jelani','Kito','Oluwaseun','Chukwu','Kojo','Yaw','Tendai'],
       ['Okonkwo','Eze','Mensah','Diallo','Traore','Ndiaye','Kamara','Bello','Sule','Adeleke','Asante','Quartey','Onyema','Kariuki','Otieno','Wafula','Banda','Phiri','Dube','Ncube'],
       ['Nigerian','Kenyan','South African'], ['#8d5524','#6f4420','#5d3a1a'], ['#14100c']),
    BG(['Katarzyna','Agnieszka','Magdalena','Ivana','Olga','Tatiana','Irina','Anastasia','Milena','Zofia','Hanna','Eliska','Vesna','Dragana','Svetlana'],
       ['Piotr','Tomasz','Andrzej','Ivan','Dmitri','Alexei','Nikolai','Milos','Jan','Pavel','Grzegorz','Boris','Stanisław','Marek','Krzysztof'],
       ['Wisniewski','Wozniak','Kozlov','Petrov','Sokolov','Volkov','Horvat','Novak','Dvorak','Svoboda','Kral','Nagy','Toth','Kowalczyk','Zielinski','Kaminski','Lewandowski'],
       ['German','Russian','British'], ['#f6d7b8','#f2cfae'], ['#57493a','#8a5a2a','#caa06a','#3a2415','#6e6259']),
    BG(['Sari','Dewi','Putri','Ratna','Wulan','Ayu','Indah','Fitri','Thao','Huong','Mai','Trang','Phuong','Lestari','Rahayu'],
       ['Budi','Agus','Joko','Bambang','Dedi','Minh','Duc','Hung','Thanh','Eko','Heru','Slamet','Wahyu','Taufik','Rizky'],
       ['Wijaya','Saputra','Rahmawati','Santoso','Prasetyo','Hartono','Tran','Le','Pham','Hoang','Vu','Dang','Bui','Do','Ho','Ngo'],
       ['Indonesian','Vietnamese','Singaporean'], ['#d9a066','#b97a4a','#eec39a'], ['#14100c','#1c1410']),
    BG(['Sigrid','Elin','Maja','Freya','Annika','Solveig','Birgit','Ingrid','Astrid','Liv','Kari','Tuula','Aino','Sanna','Helmi'],
       ['Lars','Anders','Sven','Magnus','Henrik','Nils','Oscar','Frej','Eero','Juhani','Mikko','Antti','Ville','Onni','Armas'],
       ['Andersson','Karlsson','Nilsson','Eriksson','Larsson','Olsson','Persson','Svensson','Gustafsson','Hansen','Larsen','Andersen','Pedersen','Nilsen','Korhonen','Laine','Makela','Saarinen','Lehtonen'],
       ['Finnish','British'], ['#f6d7b8','#f2cfae'], ['#caa06a','#d8d3c8','#8a5a2a','#57493a']),
    BG(['Francesca','Chiara','Alessandra','Valentina','Eleni','Konstantina','Inês','Francisca','Giorgia','Federica','Silvia','Roberta','Athena','Dimitra','Calliope'],
       ['Alessandro','Francesco','Lorenzo','Matteo','Nikos','Georgios','Dimitrios','João','Tiago','Luca','Giovanni','Andrea','Stefano','Paulo','Ricardo'],
       ['Rossi','Russo','Greco','Marino','Moretti','Conti','Papadopoulos','Georgiou','Nikolaidis','Oliveira','Costa','Ferreira','Pereira','Carvalho','Ribeiro','Almeida','Bianchi','Romano'],
       ['Italian','Brazilian','British'], ['#eec39a','#d9a066','#f2cfae'], ['#2c1a10','#3a2415','#57493a','#14100c']),
]
BG_BY_KEY = {'anglo': BACKGROUNDS[0], 'blackam': BACKGROUNDS[1], 'hispanic': BACKGROUNDS[2],
             'southasian': BACKGROUNDS[3], 'chinese': BACKGROUNDS[4], 'japanese': BACKGROUNDS[5],
             'korean': BACKGROUNDS[6], 'middleeast': BACKGROUNDS[7], 'african': BACKGROUNDS[8],
             'easteuro': BACKGROUNDS[9], 'seasia': BACKGROUNDS[10], 'scandi': BACKGROUNDS[11],
             'mediterranean': BACKGROUNDS[12]}

MANNERS = ['unhurried and exact', 'warm and quick', 'dry-humoured and precise',
           'plainspoken and immovable', 'bright and brisk', 'measured and methodical',
           'expansive and curious', 'quiet and relentless', 'sunny and hands-on',
           'crisp and formal', 'easygoing and sharp', 'deliberate and kind',
           'wry and well-read', 'calm and thorough', 'energetic and exacting',
           'gentle and rigorous']
HABITS = ['builds every lesson around one real example before any definition is allowed',
          'asks the room to predict first, and only then shows the answer',
          "keeps a notebook of the class's mistakes and teaches from it the following week",
          'refuses to move on while a single honest question is still standing',
          'draws the diagram before {p} names the thing',
          'sets problems that look small and open like trapdoors',
          'reads the primary source aloud before trusting any summary of it',
          'ends every session five minutes early, for the questions students were afraid to ask',
          'grades generously and explains mercilessly',
          'makes the class derive it once before anyone is allowed to quote it',
          'tells the field story first and the theory immediately after',
          'writes the units on the board before opinions, every time',
          "learns every student's name by the second meeting, and uses them",
          'treats a wrong answer as data, never as a verdict',
          'brings one object from the real world to every single class',
          'slows down exactly where the textbooks speed up']
SIGNATURES = ["{S} favourite sentence is: show me.",
              "Students leave {p} room able to explain the idea to a stranger, which {s} counts as the only real grade.",
              "{S} office door carries a hand-written sign: stuck is a place, not a person.",
              "Once a term, {s} teaches a whole session from the class's own questions and nothing else.",
              "{S} motto, written on the board in week one and never erased: the subject is learnable, and so are you.",
              "Colleagues send {o} their hardest teaching problems, because {p} explanations have a reputation for landing.",
              "{S} keeps the last word of every lesson for what the subject is for — not just how it works.",
              "Examinations in {p} room are open-book, because {s} is testing thinking, not storage.",
              "{S} has one unbreakable rule: nobody apologises for a question.",
              "The classes {s} teaches tend to run long, because the room keeps asking for one more example.",
              "{S} believes the worked example is a moral act: nobody should have to guess what good looks like.",
              "Every syllabus {s} writes ends with the same line: bring your curiosity; the rest is provided."]
GREETINGS = ["Come in. {Subj} starts with a question, and today it is a good one.",
             "Welcome. In this room, {subj} is learned by doing it, not by watching it.",
             "Sit down, open your notebook — {subj} rewards the prepared.",
             "In, in. {Subj} waits for no one, and neither do we.",
             "Good to see you. Today {subj} earns its keep.",
             "Come in and take a seat — {subj} first, opinions after.",
             "Welcome to {subj}. We start where the subject starts: at the beginning.",
             "Mind the threshold. {Subj} is bigger inside than it looks.",
             "Come in. {Subj} is a craft here, and crafts are learned by hand.",
             "Settle in — {subj} repays attention like few things on Earth."]
OUTFITS = ['#14524a', '#23365c', '#9a4a1f', '#5c2a54', '#3c3f45', '#1f4d7a',
           '#2e5d33', '#8c1f2e', '#8a6508', '#46536a', '#7a4a1f', '#6d1f2c',
           '#1f5138', '#4b2a63', '#b4502e', '#5d4630', '#2e3d6e', '#26332a']
F_STYLES = ['bob', 'waves', 'straight', 'curls', 'bun', 'ponytail']
M_STYLES = ['short', 'straight', 'waves']

USED_NAMES = set()
USED_PERSONALITIES = set()

def bare(name):
    return re.sub(r'^(Professor|Professora|Professore|Profesor|Profesora|Madame|Herr|Frau|Mevrouw)\s+', '', name)

def fill_pronouns(text, gender):
    s = 'she' if gender == 'F' else 'he'
    return (text.replace('{S}', s.capitalize()).replace('{s}', s)
                .replace('{o}', 'her' if gender == 'F' else 'him')
                .replace('{p}', 'her' if gender == 'F' else 'his'))

def gen_personality(subject, gender):
    for _ in range(300):
        text = ('A %s teacher of %s who %s. %s' % (
            RNG.choice(MANNERS), subject, RNG.choice(HABITS), RNG.choice(SIGNATURES)))
        text = fill_pronouns(text, gender)
        if text not in USED_PERSONALITIES:
            USED_PERSONALITIES.add(text)
            return text
    raise RuntimeError('personality pool exhausted')

def gen_portrait(bg, gender):
    p = {'skin': RNG.choice(bg['skins']), 'hair': RNG.choice(bg['hairs']),
         'hairStyle': RNG.choice(F_STYLES if gender == 'F' else M_STYLES),
         'outfit': RNG.choice(OUTFITS), 'glasses': RNG.random() < 0.3}
    if gender == 'M' and RNG.random() < 0.35:
        p['beard'] = True
    return p

def gen_professor(section_name):
    subject = re.split(r'\s+[—(]', section_name)[0].strip()
    gender = 'F' if RNG.random() < 0.535 else 'M'
    bg = RNG.choice(BACKGROUNDS)
    for _ in range(200):
        full = '%s %s' % (RNG.choice(bg['f' if gender == 'F' else 'm']),
                          RNG.choice(bg['surnames']))
        if full not in USED_NAMES:
            break
    USED_NAMES.add(full)
    accents = list(bg['accents']); RNG.shuffle(accents)
    voice = ALLOC.take(gender, tuple(accents))
    greeting = RNG.choice(GREETINGS).replace('{Subj}', subject).replace(
        '{subj}', subject[0].lower() + subject[1:])
    return prof_object('Professor ' + full, gender,
                       gen_personality(subject, gender), greeting,
                       gen_portrait(bg, gender), voice)

# ----------------------------------------------------------------------
# Assembly
# ----------------------------------------------------------------------
GROUP_OVERRIDE = {
    'designs': 'Science, Technology & AI', 'mathematics': 'Science, Technology & AI',
    'ai-computing': 'Science, Technology & AI', 'architecture': 'Science, Technology & AI',
    'biology': 'Science, Technology & AI', 'health': 'Science, Technology & AI',
    'trades': 'Science, Technology & AI', 'computer-science': 'Science, Technology & AI',
    'languages': 'Languages of the World', 'french': 'Languages of the World',
    'chemistry': 'Natural & Physical Sciences', 'statistics': 'Natural & Physical Sciences',
    'earth-sciences': 'Natural & Physical Sciences', 'engineering': 'Engineering',
    'psychology': 'Social Sciences', 'sociology': 'Social Sciences',
    'anthropology': 'Social Sciences', 'political-science': 'Social Sciences',
    'geography': 'Social Sciences', 'economics': 'Social Sciences',
    'philosophy': 'Humanities', 'linguistics': 'Humanities', 'classics': 'Humanities',
    'religious-studies': 'Humanities',
    'nursing': 'Health & Human Services', 'public-health': 'Health & Human Services',
    'social-work': 'Health & Human Services', 'kinesiology': 'Health & Human Services',
    'education': 'Education, Law & Public Life', 'law': 'Education, Law & Public Life',
    'criminal-justice': 'Education, Law & Public Life',
    'agriculture': 'Agriculture & Natural Resources',
    'english': 'Arts, Letters & Enterprise', 'music': 'Arts, Letters & Enterprise',
    'history': 'Arts, Letters & Enterprise', 'writing': 'Arts, Letters & Enterprise',
    'business': 'Arts, Letters & Enterprise', 'communications': 'Arts, Letters & Enterprise',
    'art-design': 'Arts, Letters & Enterprise', 'theatre-film': 'Arts, Letters & Enterprise',
}
ORDER = ['cosmology', 'galactic', 'astrophysics', 'particle', 'nuclear', 'atomic',
         'condensed', 'plasma', 'geophysics', 'mathematical',
         'designs', 'mathematics', 'ai-computing', 'architecture', 'biology',
         'health', 'trades', 'computer-science',
         'languages', 'french',
         'chemistry', 'statistics', 'earth-sciences', 'engineering',
         'psychology', 'sociology', 'anthropology', 'political-science',
         'geography', 'economics',
         'philosophy', 'linguistics', 'classics', 'religious-studies',
         'nursing', 'public-health', 'social-work', 'kinesiology',
         'education', 'law', 'criminal-justice', 'agriculture',
         'english', 'music', 'history', 'writing', 'business',
         'communications', 'art-design', 'theatre-film']
FOUNDATION_SECTIONS = {'mathematics', 'english', 'french', 'music', 'history', 'writing'}

def slugify(text):
    s = re.sub(r'[^a-z0-9]+', '-', text.lower().replace('&', ' and ')).strip('-')
    return s[:80].strip('-')

cat = json.load(open(os.path.join(HERE, 'catalogue.json')))
sections = {}

# Seed uniqueness sets with every authored personality.
for s in cat['sections']:
    USED_PERSONALITIES.add(s['professor']['personality'])
    USED_NAMES.add(bare(s['professor']['name']))
for spec in list(HEAD_CHANGES.values()) + list(REASSIGN.values()):
    USED_PERSONALITIES.add(spec['personality']); USED_NAMES.add(bare(spec['name']))
for name, _a, pers, _g in content.LANGUAGE_PROFESSORS.values():
    USED_PERSONALITIES.add(pers); USED_NAMES.add(bare(name))
USED_PERSONALITIES.add(content.SPANISH_PROFESSOR['personality'])
USED_NAMES.add(bare(content.SPANISH_PROFESSOR['name']))
for s in content.NEW_SECTIONS:
    USED_PERSONALITIES.add(s['professor']['personality'])
    USED_NAMES.add(bare(s['professor']['name']))

STALE_AUDIO = []

# --- existing sections: heads, flagships, reassignments, generated ---
for s in cat['sections']:
    sid = s['id']
    if sid in GROUP_OVERRIDE:
        s['group'] = GROUP_OVERRIDE[sid]
    if sid in HEAD_CHANGES:
        spec = HEAD_CHANGES[sid]
        voice = ALLOC.take(spec['gender'], spec['accents'])
        head = prof_object(spec['name'], spec['gender'], spec['personality'],
                           spec['greeting'], spec['portrait'], voice)
    else:
        head = dict(s['professor']); head['gender'] = 'F'
    s['professor'] = head
    if sid in FOUNDATION_SECTIONS:
        flagship = s['classes'][0]
    else:
        flagship = next(c for c in s['classes'] if c.get('audio'))
    for cls in s['classes']:
        if cls is flagship:
            cls['professor'] = head
            if sid in HEAD_CHANGES and cls.get('lesson'):
                if sid in SPECIAL_INTROS:
                    old_t, new_t = SPECIAL_INTROS[sid]
                    assert old_t in cls['lesson'], (sid, 'special intro seam')
                    cls['lesson'] = cls['lesson'].replace(old_t, new_t, 1)
                else:
                    old_full = 'Professor ' + OLD_HEAD_NAMES[sid]
                    assert cls['lesson'].count(old_full) == 1, (sid, 'intro name count')
                    cls['lesson'] = cls['lesson'].replace(old_full, head['name'], 1)
                STALE_AUDIO.append(cls['audio'])
        elif cls['id'] in REASSIGN:
            spec = REASSIGN[cls['id']]
            voice = ALLOC.take(spec['gender'], spec['accents'])
            cls['professor'] = prof_object(spec['name'], spec['gender'],
                                           spec['personality'], spec['greeting'],
                                           spec['portrait'], voice)
            old_t, new_t = spec['intro']
            assert old_t in cls['lesson'], (cls['id'], 'reassign seam')
            cls['lesson'] = cls['lesson'].replace(old_t, new_t, 1)
            STALE_AUDIO.append(cls['audio'])
        else:
            cls['professor'] = gen_professor(s['name'])
    sections[sid] = s

# --- the Languages of the World shelf ---
LANG_GENDER = {'portugues': 'F', 'deutsch': 'M', 'francais-speak': 'F',
               'italiano': 'M', 'nederlands': 'F', 'svenska': 'M', 'norsk': 'F',
               'dansk': 'M', 'polski': 'F', 'hindi': 'F', 'japanese': 'M',
               'mandarin': 'F', 'arabic': 'M', 'russian': 'F', 'korean': 'M',
               'turkish': 'F', 'kiswahili': 'M', 'ukrainian': 'F', 'vietnamese': 'M'}
LANG_BG = {'portugues': 'mediterranean', 'deutsch': 'easteuro',
           'francais-speak': 'anglo', 'italiano': 'mediterranean',
           'nederlands': 'scandi', 'svenska': 'scandi', 'norsk': 'scandi',
           'dansk': 'scandi', 'polski': 'easteuro', 'hindi': 'southasian',
           'japanese': 'japanese', 'mandarin': 'chinese', 'arabic': 'middleeast',
           'russian': 'easteuro', 'korean': 'korean', 'turkish': 'middleeast',
           'kiswahili': 'african', 'ukrainian': 'easteuro', 'vietnamese': 'seasia'}

carmen = prof_object(content.SPANISH_PROFESSOR['name'], 'F',
                     content.SPANISH_PROFESSOR['personality'],
                     content.SPANISH_PROFESSOR['greeting'],
                     content.SPANISH_PROFESSOR['portrait'], BY_ID[CARMEN_VOICE])
carmen['voiceNote'] = content.SPANISH_PROFESSOR['voiceNameNote']
lang_section = {'id': 'languages', 'name': 'Languages of the World',
                'group': 'Languages of the World', 'professor': carmen,
                'note': ('The standing principle of this shelf: any language a '
                         'student asks for gets a classroom. These twenty rooms '
                         'are the start, not the limit — the shelf grows on request.'),
                'classes': []}
sc = dict(content.SPANISH_CLASS)
sc.update({'source': 'founding curriculum', 'count': 0, 'papers': [],
           'audio': 'audio/espanol-i-speak-from-zero.mp3', 'professor': carmen})
if getattr(content, 'SPANISH_QA', None):
    sc['qa'] = content.SPANISH_QA
lang_section['classes'].append(sc)

for entry in content.LANGUAGES:
    key = next((k for k in content.LANGUAGE_PROFESSORS
                if entry['id'].startswith(k) or
                (k == 'francais-speak' and entry['id'].startswith('francais'))), None)
    assert key, entry['id']
    pname, accent, pers, greet = content.LANGUAGE_PROFESSORS[key]
    gender = LANG_GENDER[key]
    accents = ('lang:fra', 'French') if key == 'francais-speak' else (accent,)
    voice = ALLOC.take(gender, accents)
    prof = prof_object(pname, gender, pers, greet,
                       gen_portrait(BG_BY_KEY[LANG_BG[key]], gender), voice)
    nc = dict(entry)
    nc.update({'source': 'founding curriculum', 'count': 0, 'papers': [],
               'professor': prof})
    if key in content.LANGUAGE_LESSONS:
        nc['lesson'] = content.LANGUAGE_LESSONS[key]
        nc['audio'] = 'audio/%s.mp3' % entry['id']
    lang_section['classes'].append(nc)
sections['languages'] = lang_section

# --- six new authored sections ---
HEAD_GENDER_NEW = {'ai-computing': 'M', 'architecture': 'F', 'biology': 'F',
                   'health': 'M', 'trades': 'F', 'business': 'M'}
for s in content.NEW_SECTIONS:
    hp = s['professor']
    gender = HEAD_GENDER_NEW[s['id']]
    voice = ALLOC.take(gender, (hp['voiceAccent'],))
    head = prof_object(hp['name'], gender, hp['personality'], hp['greeting'],
                       hp['portrait'], voice)
    sec = {'id': s['id'], 'name': s['name'],
           'group': GROUP_OVERRIDE.get(s['id'], s['group']),
           'professor': head, 'classes': []}
    for i, c in enumerate(s['classes']):
        assert isinstance(c['homework'], dict)
        nc = {'id': c['id'], 'title': c['title'], 'source': 'founding curriculum',
              'count': 0, 'papers': [], 'units': c['units'], 'homework': c['homework']}
        if c.get('lesson'):
            nc['lesson'] = c['lesson']
            nc['audio'] = 'audio/%s.mp3' % c['id']
        nc['professor'] = head if i == 0 else gen_professor(s['name'])
        sec['classes'].append(nc)
    sections[s['id']] = sec

# --- the full general curriculum ---
used_class_ids = set()
for s in sections.values():
    for c in s['classes']:
        used_class_ids.add(c['id'])
for d in curric.DEPARTMENTS:
    sec = {'id': d['id'], 'name': d['name'], 'group': GROUP_OVERRIDE[d['id']],
           'classes': []}
    head = None
    for i, course in enumerate(d['courses']):
        assert 'title' in course and 'units' in course, course
        title, units = course['title'], course['units']
        cid = slugify(d['id'] + '-' + title)
        base, n = cid, 2
        while cid in used_class_ids:
            cid = '%s-%d' % (base, n); n += 1
        used_class_ids.add(cid)
        nc = {'id': cid, 'title': title, 'source': 'founding curriculum',
              'count': 0, 'papers': [], 'units': units,
              'homework': {'q': d['homework'][0].replace('{unit}', units[0]).replace('{course}', title),
                           'worked': d['homework'][1].replace('{unit}', units[0]).replace('{course}', title)}}
        if i == 0:
            head = gen_professor(d['name'])
            nc['professor'] = head
        else:
            nc['professor'] = gen_professor(d['name'])
        sec['classes'].append(nc)
    sec['professor'] = head
    sections[d['id']] = sec

# --- order, counts, totals ---
ordered = [sections[sid] for sid in ORDER]
assert len(ordered) == 50, len(ordered)
total_classes = 0
total_papers = 0
roster = []
gender_count = {'F': 0, 'M': 0}
head_gender = {'F': 0, 'M': 0}
for s in ordered:
    s['classCount'] = len(s['classes'])
    s['paperCount'] = sum(c.get('count', 0) for c in s['classes'])
    total_classes += s['classCount']
    total_papers += s['paperCount']
    head_gender[s['professor']['gender']] += 1
    for c in s['classes']:
        p = c['professor']
        gender_count[p['gender']] += 1
        roster.append({'classId': c['id'], 'classTitle': c['title'],
                       'sectionId': s['id'], 'sectionName': s['name'],
                       'name': p['name'], 'gender': p['gender'],
                       'voiceId': p['voiceId'], 'voiceName': p['voiceName'],
                       'personality': p['personality'], 'greeting': p['greeting']})
names = [r['name'] for r in roster]
assert len(names) == len(set(names)), 'professor names not unique'
assert total_papers == 7170, total_papers

cat['generated'] = '2026-11-16 (stage B)'
cat['sources'] = ['MASTER-INDEX.md', 'INDEX-SUPPLEMENT-2026-11-14.md',
                  'founding curriculum (authored, stage A)',
                  'stage B authored curriculum — the Languages of the World shelf, six new departments, and the full general curriculum']
cat['totals'] = {'papers': total_papers, 'classes': total_classes,
                 'sections': len(ordered), 'professors': len(set(names))}
cat['sections'] = ordered
with open(os.path.join(HERE, 'catalogue.json'), 'w') as f:
    json.dump(cat, f, indent=1, ensure_ascii=False)

prof_file = {
    'note': ('Exolex University — section registry and department heads (stage B, '
             '2026-11-16). The faculty is mixed, like a real university: every one '
             'of the %d classes has its OWN professor (see roster.json) — the '
             'professors listed here are the department heads, who teach their '
             "sections' flagship classes. Voices are drawn from the Helio/TTS "
             "catalogue (1,218 voices: 770 male, 447 female), matched to each "
             "professor's gender and, where the catalogue allows, accent. Dave's "
             'own voice (avocado_v2:MAI_03) is never used for a professor. '
             'Portraits are stylised figures drawn in the page from the portrait '
             'parameters — no photographs, no real people.' % total_classes),
    'sections': [{'group': s['group'], 'id': s['id'], 'name': s['name'],
                  'professor': s['professor']} for s in ordered],
}
with open(os.path.join(HERE, 'professors.json'), 'w') as f:
    json.dump(prof_file, f, indent=1, ensure_ascii=False)

with open(os.path.join(HERE, 'roster.json'), 'w') as f:
    json.dump({'note': 'Exolex University — per-class faculty roster (stage B, 2026-11-16). '
                       'One professor per class; department heads teach their flagship class.',
               'professors': roster}, f, indent=1, ensure_ascii=False)

# Stale recordings whose professor changed: delete so gen-audio re-records.
for rel in STALE_AUDIO:
    path = os.path.join(HERE, rel)
    if os.path.exists(path):
        os.remove(path)
print('classes:', total_classes, '| sections:', len(ordered), '| papers:', total_papers)
print('faculty gender:', gender_count, '| heads gender:', head_gender)
print('distinct professors:', len(set(names)))
print('stale audio deleted (to re-record):', len(STALE_AUDIO))
for rel in STALE_AUDIO:
    print('  stale:', rel)
from collections import Counter
vc = Counter(r['voiceId'] for r in roster)
print('max voice repeats:', vc.most_common(3))
print('voice pool refills:', ALLOC.refills)
