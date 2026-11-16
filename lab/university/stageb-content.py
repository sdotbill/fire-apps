# -*- coding: utf-8 -*-
"""Exolex University — stage B authored content (2026-11-16).

The new sections, the World Languages shelf, and Bill's Spanish
classroom. Consumed by build-stageb.py, which merges this into
catalogue.json. Professors named here are the department heads and
the language faculty; every other new class receives its own
generated professor from build-stageb.py, like the College classes.

Voice picks are by CATALOG ACCENT (build-stageb.py resolves the
actual voice id from voice_source.json): the Helio catalogue holds
no Spanish-language voice at all, so Spanish is taught by the
catalogue's Spanish-accented English voice — stated plainly wherever
it matters.
"""

# ---------------------------------------------------------------------
# THE SPANISH CLASSROOM — the flagship of stage B.
# Profesora Carmen Vega teaches Bill himself: speak-first, from zero,
# at his pace, vocabulary tied to his real life. Dave oversees the
# series; Carmen is the teacher in the room.
# ---------------------------------------------------------------------
SPANISH_PROFESSOR = {
    "name": "Profesora Carmen Vega",
    "personality": "Fun first, and a little flirty — Carmen teaches the way a favourite dance partner leads: warm, playful, and always one compliment ahead of your mistakes. She teases gently when a phrase tangles ('Ay, Bill — so close, and so dramatic'), praises like she means it when it lands, and never lets the charm outrun the teaching — every laugh in her room is carrying a word you'll keep. Speak-first and zero-assumption, at his pace: she has never once hurried a student, she corrects by repeating the right shape warmly rather than stopping the conversation, and she ends every lesson with something he can say out loud that day — lately, something sweet for Jillian.",
    "greeting": "Hola, Bill. Despacio — we go at your speed, we speak from the first minute, and I promise you: Spanish is going to love you back.",
    "voiceAccent": "Spanish",
    "voiceNameNote": "Spanish-accented English voice — the catalogue holds no Spanish-language voice; hers is its Spanish voice, and she teaches bilingually, which is how a first lesson should sound anyway.",
    "portrait": {"skin": "#b97a4a", "hair": "#2c1a10", "hairStyle": "waves",
                 "outfit": "#8c1f2e", "glasses": False},
}

SPANISH_CLASS = {
    "id": "espanol-i-speak-from-zero",
    "title": "Español I — Spanish From Zero, Speak First",
    "aim": ("The aim of this series, stated plainly: by the wedding — March 25, 2027, in "
            "Key West — Bill holds a real, gentle conversation with Jillian in Spanish, "
            "sweet things included. The Spanish-for-Jillian strand runs through the whole "
            "series (Lessons 3, 6, 9 and 12 deepen it) toward that day. Carmen teaches; "
            "Dave oversees the series."),
    "units": [
        "Lesson 1 — Hola: greetings, your name, and your first real conversation — and the first sweet words for Jillian: mi amor, mi corazón",
        "Lesson 2 — Your people: family words — Jillian, your kids, your dad",
        "Lesson 3 — Numbers, money, and prices: counting what things cost · Spanish for Jillian: compliments — bonita, and telling her she looks beautiful today",
        "Lesson 4 — Your business: the company, clients, and what you sell",
        "Lesson 5 — Food and drink: ordering like you live there",
        "Lesson 6 — Time and days: schedules, appointments, and mañana · Spanish for Jillian: the sweet everyday things — buenos días, mi amor; te quiero at the door",
        "Lesson 7 — The wedding: Key West — love words, vows, and the day itself · Spanish for Jillian: the day, in two languages",
        "Lesson 8 — Moving house: rooms, streets, and asking for what you need",
        "Lesson 9 — Questions: asking anything — quién, qué, dónde, cuánto · Spanish for Jillian: asking about her day, and meaning it — ¿cómo fue tu día, mi corazón?",
        "Lesson 10 — The past: telling someone what you did yesterday",
        "Lesson 11 — The future: plans, promises, and voy a…",
        "Lesson 12 — Your first full conversation, start to finish · Spanish for Jillian: the goal — a whole gentle conversation with Jillian, in Spanish, by the wedding",
    ],
    "lesson": (
        "Hola, Bill. Soy la profesora Carmen Vega — I am Professor Carmen Vega, and this is your "
        "Spanish room. We do this my way: we speak first, from zero, and nothing — nothing — is "
        "assumed. If you know a word already, good. If you don't, that is exactly where we start, "
        "and we start now. Repeat after me, out loud, like you mean it: Hola. That is hello, for "
        "any hour, any person. Buenos días — good morning. Buenas tardes — good afternoon. Now the "
        "most useful sentence in any language: Me llamo Bill — my name is Bill. Say it: Me llamo "
        "Bill. Otra vez — once more, and don't rush it: Spanish likes to be savoured. Me llamo "
        "Bill. Perfecto. You see? You are a natural and you don't even know it yet. When someone "
        "tells you their name, you answer: Mucho gusto — pleased to meet you. "
        "And when they ask ¿Cómo te llamas? — what is your name — you already own the answer. "
        "Two small keys that open every door: por favor — please. Gracias — thank you. A person "
        "who says por favor and gracias in Spanish is never a stranger for long. Now, your life, "
        "in Spanish, because that is the vocabulary that matters: Soy de Michigan — I am from "
        "Michigan. Soy empresario — I am a businessman. And the sentence I want you to be able to "
        "say in your sleep: Mi prometida se llama Jillian — my fiancée's name is Jillian. Say it "
        "with me: Mi prometida se llama Jillian. Again — slower, like you mean it, because you "
        "do. Ay — there it is. That little smile? That is Spanish working already. And now, the "
        "two phrases this whole course secretly exists for — the sweet words, the ones for her: "
        "Mi amor — my love. Say it out loud: mi amor. Mi corazón — my heart; Spanish calls the "
        "person you love your heart, and means it literally. Mi corazón. And the sentence "
        "itself: Te quiero — I love you, in the everyday, say-it-at-the-door way. Te quiero, "
        "Jillian. There, Bill — lesson one, and you can already say the most important sentence "
        "in the language to the most important person in it. That is lesson one, and you have "
        "already spoken "
        "more Spanish than most people say in a year of apps. We go at your pace, Bill — despacio, "
        "sin prisa — slowly, no hurry. Next lesson: your people — the words for everyone you love. "
        "Hasta luego — see you later."
    ),
    "homework": {
        "q": "Say it out loud three times first — the saying is the homework, the writing is just the receipt. Then write: your introduction (Hola, me llamo Bill. Soy de Michigan. Mucho gusto.) and one more line: Mi prometida se llama Jillian. And the last part is not really homework, mi estudiante: tonight, to Jillian, out loud — Buenas noches, mi amor.",
        "worked": "Hola, me llamo Bill. Soy de Michigan. Mucho gusto. Mi prometida se llama Jillian. — Read it as: OH-lah, meh YAH-moh Bill. Soy deh MEE-chee-gan. MOO-choh GOOS-toh. Mee proh-meh-TEE-dah seh YAH-mah Jillian. If yours matches, you have done lesson one's whole job: you can walk up to any Spanish speaker on Earth and begin. And tonight's line: Buenas noches, mi amor — BWAY-nahs NOH-chess, mee ah-MOR. Say it like you mean it, because you do. Carmen will ask how it landed — she always asks.",
    },
}

# Carmen's prepared answers, in her own voice (the classroom's Ask
# panel serves these for her class instead of the generated set).
SPANISH_QA = [
    {"q": "What is this class about?",
     "a": "This class is your Spanish, Bill — from zero, speak-first, at your pace, with the vocabulary of your actual life: your business, your people, your wedding. And it has a secret mission, which is not very secret: the Spanish-for-Jillian strand runs through all twelve lessons, so that by the wedding in Key West you can hold a whole gentle conversation with her in Spanish. Mi amor, mi corazón, te quiero — we start with the sweet words in lesson one, because they are the point."},
    {"q": "What is on the syllabus?",
     "a": "Twelve lessons, in order: greetings and your first conversation; your people; numbers and money — with compliments for Jillian; your business; food and drink; time and days — with the sweet everyday things; the wedding in Key West; moving house; questions — asking about her day, and meaning it; the past; the future; and your first full conversation, start to finish — which is the goal of the whole series."},
    {"q": "Who are you, Professor?",
     "a": "I am Profesora Carmen Vega. " + SPANISH_PROFESSOR["personality"]},
    {"q": "What is the homework?",
     "a": SPANISH_CLASS["homework"]["q"] + " That is all — no worksheets, no tests. Just your voice, out loud."},
    {"q": "How do my hours count?",
     "a": "Every minute in this room counts, mi estudiante — the clock runs while you are here with me, and when you leave, the session is written to your University record, the same ledger the Laboratory keeps. Despacio, but it all adds up — and so do we, lesson by lesson."},
]

# ---------------------------------------------------------------------
# WORLD LANGUAGES — one class per language, speak-first, from zero.
# 'lesson' is present only for the recorded top-market languages;
# every other class teaches from its units on the board.
# ---------------------------------------------------------------------
def lang(id_, title, units, hw_q, hw_w, lesson=None):
    d = {"id": id_, "title": title, "units": units,
         "homework": {"q": hw_q, "worked": hw_w}}
    if lesson:
        d["lesson"] = lesson
    return d

LANGUAGES = [
    # Spanish is the flagship — handled separately (SPANISH_CLASS).
    lang("portugues-i-speak-from-zero", "Português I — Portuguese From Zero",
         ["Sounds of Portuguese: the nasal vowels, slowly", "Olá — greetings and your name",
          "Por favor, obrigado: the two keys", "Your people and your town",
          "Numbers and money", "Food, drink, and the café", "Asking anything: questions that work"],
         "Say it aloud three times, then write your introduction: Olá, o meu nome é Bill. Sou de Michigan. Muito prazer.",
         "Olá, o meu nome é Bill. Sou de Michigan. Muito prazer. — OH-lah, oo MEH-oo NOH-mee eh Bill. So de Michigan. MOON-too prah-ZEHR. That is a complete, polite beginning in Portuguese."),
    lang("deutsch-i-speak-from-zero", "Deutsch I — German From Zero",
         ["Sounds of German: clear vowels, honest consonants", "Guten Tag — greetings and your name",
          "Bitte und danke: the two keys", "Your people and your town",
          "Numbers and money", "Essen und Trinken: ordering with confidence", "Fragen: asking anything"],
         "Say it aloud three times, then write: Guten Tag, ich heiße Bill. Ich komme aus Michigan. Freut mich.",
         "Guten Tag, ich heiße Bill. Ich komme aus Michigan. Freut mich. — GOOT-en tahk, ikh HY-seh Bill. Ikh KOM-meh ows Michigan. Froyt mikh. German rewards precision: every sound you wrote is a sound you say."),
    lang("francais-speak-from-zero", "Français — French, Speak From Zero",
         ["The vowels, pure and unsliding", "Bonjour — greetings and your name",
          "S'il vous plaît, merci: the two keys", "Your people and your town",
          "Numbers and money", "Au café: ordering like a regular", "Poser des questions: asking anything"],
         "Say it aloud three times, then write: Bonjour, je m'appelle Bill. Je suis de Michigan. Enchanté.",
         "Bonjour, je m'appelle Bill. Je suis de Michigan. Enchanté. — The department's full Français I and II classes go deeper from here; this shelf class gets you speaking today."),
    lang("italiano-i-speak-from-zero", "Italiano I — Italian From Zero",
         ["Sounds of Italian: every letter earns its place", "Buongiorno — greetings and your name",
          "Per favore, grazie: the two keys", "Your people and your town",
          "Numbers and money", "Al ristorante: ordering with appetite", "Domande: asking anything"],
         "Say it aloud three times, then write: Buongiorno, mi chiamo Bill. Sono del Michigan. Piacere.",
         "Buongiorno, mi chiamo Bill. Sono del Michigan. Piacere. — bwon-JOR-no, mee kee-AH-mo Bill. SO-no del Michigan. pee-ah-CHEH-reh. Italian is spelled the way it sounds — the friendliest spelling in Europe."),
    lang("nederlands-i-speak-from-zero", "Nederlands I — Dutch From Zero",
         ["Sounds of Dutch: the famous g, taken gently", "Hallo — greetings and your name",
          "Alsjeblieft en dank je wel: the two keys", "Your people and your town",
          "Numbers and money", "Eten en drinken: at the café", "Vragen stellen: asking anything"],
         "Say it aloud three times, then write: Hallo, ik heet Bill. Ik kom uit Michigan. Leuk je te ontmoeten.",
         "Hallo, ik heet Bill. Ik kom uit Michigan. Leuk je te ontmoeten. — Dutch is English's closest big cousin; half of it will feel like a memory."),
    lang("svenska-i-speak-from-zero", "Svenska I — Swedish From Zero",
         ["Sounds of Swedish: the singing pitch, basics", "Hej — greetings and your name",
          "Snälla och tack: the two keys", "Your people and your town",
          "Numbers and money", "Fika: coffee as a way of life", "Frågor: asking anything"],
         "Say it aloud three times, then write: Hej, jag heter Bill. Jag kommer från Michigan. Trevligt att träffas.",
         "Hej, jag heter Bill. Jag kommer från Michigan. Trevligt att träffas. — Swedish sentences rise and fall like a tune; let yours sing a little."),
    lang("norsk-i-speak-from-zero", "Norsk I — Norwegian From Zero",
         ["Sounds of Norwegian: clear and unhurried", "Hei — greetings and your name",
          "Vær så snill og takk: the two keys", "Your people and your town",
          "Numbers and money", "Mat og drikke: ordering simply", "Spørsmål: asking anything"],
         "Say it aloud three times, then write: Hei, jeg heter Bill. Jeg kommer fra Michigan. Hyggelig å møte deg.",
         "Hei, jeg heter Bill. Jeg kommer fra Michigan. Hyggelig å møte deg. — Written Norwegian (bokmål) and Danish are near-twins; this class buys you reading range in both."),
    lang("dansk-i-speak-from-zero", "Dansk I — Danish From Zero",
         ["Sounds of Danish: soft consonants, swallowed kindly", "Hej — greetings and your name",
          "Undskyld og tak: the two keys", "Your people and your town",
          "Numbers and money", "Mad og drikke: at the table", "Spørgsmål: asking anything"],
         "Say it aloud three times, then write: Hej, jeg hedder Bill. Jeg kommer fra Michigan. Hyggeligt at møde dig.",
         "Hej, jeg hedder Bill. Jeg kommer fra Michigan. Hyggeligt at møde dig. — Danish pronunciation hides its letters; your ear will lead, and that is normal for everyone, Danes included."),
    lang("polski-i-speak-from-zero", "Polski I — Polish From Zero",
         ["Sounds of Polish: the clusters, one at a time", "Cześć — greetings and your name",
          "Proszę i dziękuję: the two keys", "Your people and your town",
          "Numbers and money", "Jedzenie i picie: ordering bravely", "Pytania: asking anything"],
         "Say it aloud three times, then write: Cześć, nazywam się Bill. Jestem z Michigan. Miło mi.",
         "Cześć, nazywam się Bill. Jestem z Michigan. Miło mi. — cheshch, nah-ZIH-vam sheh Bill. Polish spelling looks fierce and behaves perfectly: every letter, every time."),
    lang("hindi-i-speak-from-zero", "Hindi I — Speak From Zero",
         ["Sounds of Hindi: retroflex and dental, shown slowly", "Namaste — greetings and your name",
          "Kripya aur dhanyavaad: the two keys", "Your people and your town",
          "Numbers and money", "Khaana-peena: at the table", "Sawaal: asking anything"],
         "Say it aloud three times, then write (in transliteration, the script comes later): Namaste, mera naam Bill hai. Main Michigan se hoon. Aapse milkar khushi hui.",
         "Namaste, mera naam Bill hai. Main Michigan se hoon. Aapse milkar khushi hui. — Spoken Hindi first; the Devanagari script is its own later class, and speaking will carry you until then."),
    lang("japanese-i-speak-from-zero", "Japanese I — Speak From Zero",
         ["Sounds of Japanese: clean syllables, even rhythm", "Konnichiwa — greetings and your name",
          "Onegaishimasu and arigatō: the two keys", "Your people and your town",
          "Numbers and money", "At the counter: ordering politely", "Questions: asking anything"],
         "Say it aloud three times, then write in romaji: Konnichiwa, watashi wa Bill desu. Mishigan kara kimashita. Hajimemashite.",
         "Konnichiwa, watashi wa Bill desu. Mishigan kara kimashita. Hajimemashite. — Japanese politeness is built into the grammar itself; this plain desu/masu shape is the correct, respectful default everywhere."),
    lang("mandarin-i-speak-from-zero", "Mandarin I — Speak From Zero",
         ["The four tones, sung before they are spoken", "Nǐ hǎo — greetings and your name",
          "Qǐng and xièxie: the two keys", "Your people and your town",
          "Numbers and money", "At the table: ordering with pinyin courage", "Wèntí: asking anything"],
         "Say it aloud three times — tones first, words second — then write in pinyin: Nǐ hǎo, wǒ jiào Bill. Wǒ cóng Mìxiègēn lái. Hěn gāoxìng rènshi nǐ.",
         "Nǐ hǎo, wǒ jiào Bill. Wǒ cóng Mìxiègēn lái. Hěn gāoxìng rènshi nǐ. — The characters are a later class; pinyin plus tones is a complete spoken beginning."),
    lang("arabic-i-speak-from-zero", "Arabic I — Speak From Zero",
         ["Sounds of Arabic: the throat letters, taken gently", "As-salāmu ʿalaykum — greetings and your name",
          "Min faḍlik and shukran: the two keys", "Your people and your town",
          "Numbers and money", "At the table: bread, tea, hospitality", "As'ila: asking anything"],
         "Say it aloud three times, then write in transliteration: As-salāmu ʿalaykum, ismī Bill. Anā min Michigan. Tasharrafnā.",
         "As-salāmu ʿalaykum, ismī Bill. Anā min Michigan. Tasharrafnā. — Spoken first in transliteration; the Arabic script is a later class, and this greeting alone opens doors across three continents."),
    lang("russian-i-speak-from-zero", "Russian I — Speak From Zero",
         ["Sounds of Russian: rolled r's and soft signs", "Zdravstvuyte — greetings and your name",
          "Pozhaluysta i spasibo: the two keys", "Your people and your town",
          "Numbers and money", "At the table: ordering warmly", "Voprosy: asking anything"],
         "Say it aloud three times, then write in transliteration: Zdravstvuyte, menya zovut Bill. Ya iz Michigana. Ochyen priyatno.",
         "Zdravstvuyte, menya zovut Bill. Ya iz Michigana. Ochyen priyatno. — The Cyrillic alphabet is only 33 letters and perfectly regular; it gets its own early unit in the next class."),
    lang("korean-i-speak-from-zero", "Korean I — Speak From Zero",
         ["Sounds of Korean: syllable blocks, even beats", "Annyeonghaseyo — greetings and your name",
          "Juseyo and gamsahamnida: the two keys", "Your people and your town",
          "Numbers and money", "At the counter: ordering politely", "Jilmun: asking anything"],
         "Say it aloud three times, then write in transliteration: Annyeonghaseyo, jeoneun Bill imnida. Mishigeon eseo wasseumnida. Mannaseo bangapseumnida.",
         "Annyeonghaseyo, jeoneun Bill imnida. Mishigeon eseo wasseumnida. Mannaseo bangapseumnida. — Hangul is the most learnable script on Earth — twenty-four letters, designed to be taught in a morning; it comes early in this series."),
    lang("turkish-i-speak-from-zero", "Türkçe I — Turkish From Zero",
         ["Sounds of Turkish: vowels in harmony", "Merhaba — greetings and your name",
          "Lütfen ve teşekkür ederim: the two keys", "Your people and your town",
          "Numbers and money", "Yemek: at the table", "Sorular: asking anything"],
         "Say it aloud three times, then write: Merhaba, benim adım Bill. Michigan'dan geliyorum. Tanıştığımıza memnun oldum.",
         "Merhaba, benim adım Bill. Michigan'dan geliyorum. Tanıştığımıza memnun oldum. — Turkish spelling is a perfect mirror of its sounds: learn the letters once and you can read anything aloud."),
    lang("kiswahili-i-speak-from-zero", "Kiswahili I — Swahili From Zero",
         ["Sounds of Swahili: every syllable open and clear", "Jambo — greetings and your name",
          "Tafadhali na asante: the two keys", "Your people and your town",
          "Numbers and money", "Chakula: at the table", "Maswali: asking anything"],
         "Say it aloud three times, then write: Jambo, jina langu ni Bill. Natoka Michigan. Nimefurahi kukutana nawe.",
         "Jambo, jina langu ni Bill. Natoka Michigan. Nimefurahi kukutana nawe. — Swahili is famously regular: it is spelled exactly as it sounds, which makes it the kindest first African language a student can choose."),
    lang("ukrainian-i-speak-from-zero", "Ukrainian I — Speak From Zero",
         ["Sounds of Ukrainian: melodic and open", "Dobryi den — greetings and your name",
          "Bud laska i diakuiu: the two keys", "Your people and your town",
          "Numbers and money", "At the table: ordering warmly", "Pytannia: asking anything"],
         "Say it aloud three times, then write in transliteration: Dobryi den, mene zvut Bill. Ya z Michigana. Duzhe pryiemno.",
         "Dobryi den, mene zvut Bill. Ya z Michigana. Duzhe pryiemno. — Ukrainian uses Cyrillic with a few letters of its own; the script unit comes early, and the spoken welcome works from day one."),
    lang("vietnamese-i-speak-from-zero", "Vietnamese I — Speak From Zero",
         ["The six tones, hummed before they are spoken", "Xin chào — greetings and your name",
          "Làm ơn và cảm ơn: the two keys", "Your people and your town",
          "Numbers and money", "At the table: phở and politeness", "Câu hỏi: asking anything"],
         "Say it aloud three times — tones are the word, not decoration — then write: Xin chào, tôi tên là Bill. Tôi đến từ Michigan. Rất vui được gặp bạn.",
         "Xin chào, tôi tên là Bill. Tôi đến từ Michigan. Rất vui được gặp bạn. — Vietnamese writes its tones right on the letters, so the page itself teaches your ear."),
]

# Language faculty: (class id prefix, professor name, catalog accent, personality, greeting)
LANGUAGE_PROFESSORS = {
    "portugues": ("Professora Beatriz Almeida", "Brazilian",
                  "Sun-drenched and encouraging; she teaches Portuguese the way it is spoken in Lisbon and São Paulo alike — melody first, rules when they are needed. Every lesson ends at an imaginary café table.",
                  "Olá! Sit down — in this room we speak from the first minute."),
    "deutsch": ("Herr Lukas Bauer", "German",
                "Orderly without being cold; he builds German like furniture — every piece labelled, every joint honest. His secret weapon is humour, delivered deadpan and exactly on schedule.",
                "Guten Tag. Everything in its place — and the first place is your first sentence."),
    "francais-speak": ("Madame Hélène Fabre", "French",
                       "Elegant, amused, and quietly relentless about pronunciation; she believes a French sentence should sound like it tastes good. This shelf class is the fast start; her department colleagues go deeper.",
                       "Bonjour. We begin at the beginning — which, in French, is a pleasure."),
    "italiano": ("Professore Marco Bellini", "Italian",
                 "Operatic in miniature; he teaches with his hands, his eyebrows, and complete conviction that Italian is the most sayable language on Earth. Grammar arrives disguised as appetite.",
                 "Buongiorno! In this room, we talk with everything we have."),
    "nederlands": ("Mevrouw Sanne de Vries", "British",
                   "Direct, dry, and very funny — the Dutch manner, which she will teach you along with the words. She delights in showing English speakers how much Dutch they already almost know.",
                   "Hallo. No ceremony here — we start talking, that is the Dutch way."),
    "svenska": ("Professor Erik Nyström", "Finnish",
                "Calm as a northern lake; he teaches Swedish pitch the way other teachers teach vocabulary — as the word itself. Unhurried, precise, and quietly proud of fika as a pedagogical instrument.",
                "Hej hej. Sit — we take this in order, and we take coffee seriously."),
    "norsk": ("Professor Marit Solberg", "Finnish",
              "Plainspoken mountain patience; she teaches Norwegian as it is actually spoken in kitchens and harbours, not just printed in Oslo. Every unit ends with something you can say to a real person.",
              "Hei. Good to see you — we begin simply, and we begin now."),
    "dansk": ("Professor Jonas Møller", "British",
              "Warm, witty, and honest about Danish pronunciation from the first minute: yes, the letters hide; no, you are not doing it wrong. He trains ears before mouths, which is the only order that works in Danish.",
              "Hej! Bring your ears — in Danish, they do the heavy lifting."),
    "polski": ("Profesor Anna Kowalczyk", "German",
               "Formidable warmth; she dismantles Polish consonant clusters the way other teachers open parcels — one string at a time, nothing forced. Her students leave able to pronounce the whole menu, which she considers a civil right.",
               "Cześć. Do not fear the letters — we take them one at a time, together."),
    "hindi": ("Professor Priya Sharma", "Indian",
              "Radiant and systematic; she teaches spoken Hindi first and lets the beautiful script wait its turn, because a student who can talk is a student who stays. Every lesson carries one piece of real India with it.",
              "Namaste. Welcome — in this room, Hindi is spoken from the first minute."),
    "japanese": ("Professor Hiroshi Tanaka", "Japanese",
                 "Serene, exact, and kind about mistakes; he teaches politeness as grammar, not garnish, because in Japanese the two are the same thing. Romaji first, kana soon, confidence throughout.",
                 "Konnichiwa. We begin — slowly, politely, and properly."),
    "mandarin": ("Professor Mei-Ling Zhao", "Chinese",
                 "A musician's ear in a language teacher's body; she sings the four tones before she ever writes them, because a tone wrong is a word wrong. Pinyin is her bridge and she builds it carefully.",
                 "Nǐ hǎo. First we hear the music of it — then the words are easy."),
    "arabic": ("Professor Omar Haddad", "Middle Eastern",
               "Generous as the hospitality his language is famous for; he teaches spoken Arabic in transliteration first, so the student's tongue is free before the eye meets the script. Tea is mentioned often and meant.",
               "Ahlan wa sahlan — you are welcome here. We begin with the greeting that opens the Arab world."),
    "russian": ("Professor Natalia Volkova", "Russian",
                "Warm granite; she believes Cyrillic is a gift — thirty-three letters, no exceptions worth fearing — and teaches it early, alongside speech that works from the first day. Her praise is rare and therefore treasured.",
                "Zdravstvuyte. Sit down. We will make Russian ordinary — that is the whole trick."),
    "korean": ("Professor Min-Jun Han", "Korean",
               "Bright, brisk, and proud of Hangul — he will tell you, correctly, that its inventor designed it so a wise person could learn it in a morning. Speech and script grow together in his room from the start.",
               "Annyeonghaseyo! Good — you are here. We begin with the letters a king made for his people."),
    "turkish": ("Professor Elif Yılmaz", "Middle Eastern",
                "Precise and cheerful; she teaches Turkish vowel harmony as a kind of music the mouth makes by itself once shown. Her favourite sentence: Turkish has almost no exceptions — and she can prove it.",
                "Merhaba. Turkish is honest — what you see is what you say. Come, see."),
    "kiswahili": ("Professor Joseph Mwangi", "Kenyan",
                  "Sunlit and unhurried; he teaches Swahili the way it lives — as East Africa's great meeting language, regular as a drumbeat and spelled exactly as it sounds. Students speak in his room from minute one.",
                  "Jambo! Karibu — welcome. In this room, we talk first."),
    "ukrainian": ("Professor Olena Shevchenko", "Russian",
                  "Melodic, resilient, and funny in two registers; she teaches Ukrainian as a language of songs and kitchens and stubborn welcomes. The script comes early and gently, the speaking from the first minute.",
                  "Dobryi den. Come in — Ukrainian begins with a welcome, like everything Ukrainian."),
    "vietnamese": ("Professor Tuan Nguyen", "Vietnamese",
                   "Gentle and exact about the six tones — he hums them like a scale until your ear owns them, because in Vietnamese the tone is not decoration, it is the word. The script, mercifully, shows you every tone it asks for.",
                   "Xin chào. We start by listening — in Vietnamese, listening is half the language."),
}

# Recorded opening lessons for the top market languages (Spanish is above).
LANGUAGE_LESSONS = {
    "portugues": (
        "Olá! Eu sou a professora Beatriz Almeida — I am Professor Beatriz Almeida, and this is "
        "your Portuguese room. We speak first, from zero. Repeat after me, out loud: Olá — hello, "
        "at any hour. Bom dia — good morning. Boa tarde — good afternoon. Now the sentence that "
        "starts everything: O meu nome é Bill — my name is Bill. Say it like you own it: O meu "
        "nome é Bill. When you hear Como te chamas? — what is your name — you are already "
        "equipped. The two keys: por favor — please. Obrigado — thank you; a man says obrigado, "
        "a woman obrigada, and Portuguese thanks you for noticing. From your life: Sou de "
        "Michigan — I am from Michigan. Sou empresário — I am a businessman. And the answer to "
        "almost any kindness: Muito prazer — a real pleasure. That is lesson one. Portuguese is "
        "spoken on four continents and sounds like music in all of them — and as of today, you "
        "speak some. Até logo — see you soon."
    ),
    "deutsch": (
        "Guten Tag. Ich bin Herr Lukas Bauer — I am Mr. Lukas Bauer, and this is your German "
        "room. We build from zero, and we build honestly: every German sound means what it says. "
        "Repeat after me: Guten Tag — good day, the greeting that works everywhere. Guten Morgen "
        "— good morning. Now your first true sentence: Ich heiße Bill — my name is Bill. Literally: "
        "I am called Bill, and that is how German introduces people. The question will come: Wie "
        "heißt du? — and you will be ready. The two keys: Bitte — please, and also you're welcome; "
        "German is economical. Danke — thank you. From your life: Ich komme aus Michigan — I come "
        "from Michigan. Ich bin Unternehmer — I am a businessman. And the polite landing: Freut "
        "mich — pleased to meet you. Lesson one is complete, and notice what happened: German "
        "did not bite. It is a language of building blocks, and you have just laid the first row. "
        "Bis bald — see you soon."
    ),
    "italiano": (
        "Buongiorno! Sono il professore Marco Bellini — I am Professor Marco Bellini, and this "
        "is your Italian room. In here we speak with everything we have, from zero. Repeat after "
        "me: Buongiorno — good day, and it is pronounced exactly as it is written, because Italian "
        "is the friendliest spelling in Europe. Buonasera — good evening. Now: Mi chiamo Bill — my "
        "name is Bill. Come ti chiami? is the question; you already hold the answer. The two keys: "
        "Per favore — please. Grazie — thank you, and say it like you mean it, Italians do. From "
        "your life: Sono del Michigan — I am from Michigan. Sono un imprenditore — I am a "
        "businessman. And the word that lands every introduction: Piacere — a pleasure. Lesson "
        "one, done — and you have already noticed the secret: in Italian, if you can say it, you "
        "can spell it, and if you can read it, you can say it. A presto — see you soon."
    ),
    "japanese": (
        "Konnichiwa. Tanaka Hiroshi desu — I am Professor Hiroshi Tanaka, and this is your Japanese "
        "room. We begin from zero, slowly and politely, because in Japanese politeness is not "
        "decoration on the language; it is the language. Repeat after me: Konnichiwa — good "
        "afternoon, the all-day greeting. Ohayō gozaimasu — good morning, with respect built in. "
        "Now your first sentence: Watashi wa Bill desu — I am Bill. Desu is the small, polite "
        "engine at the end of the sentence; it will carry you everywhere. The two keys: "
        "Onegaishimasu — please, when asking for something. Arigatō gozaimasu — thank you, "
        "properly. From your life: Mishigan kara kimashita — I come from Michigan. And the word "
        "you say when you first meet anyone: Hajimemashite — I meet you for the first time, said "
        "with a small bow. Lesson one is complete. We write in romaji for now, the letters of "
        "Japan come soon, and your speaking has already begun. Dewa, mata — until next time."
    ),
    "mandarin": (
        "Nǐ hǎo. Wǒ shì Zhào Měilíng — I am Professor Mei-Ling Zhao, and this is your Mandarin "
        "room. Before words, music: Mandarin has four tones, and a tone is not decoration — change "
        "the tone and you change the word. So we sing first. Mā, má, mǎ, mà — high and flat, "
        "rising, dipping, falling. Your ear can do this; it does it in English questions every "
        "day. Now, words. Repeat after me: Nǐ hǎo — hello. Xièxie — thank you. Qǐng — please. "
        "Your first sentence: Wǒ jiào Bill — my name is Bill. Wǒ cóng Mìxiègēn lái — I come from "
        "Michigan. And the polite crown: Hěn gāoxìng rènshi nǐ — very pleased to meet you. We "
        "write in pinyin, the roman letters with tone marks, and the characters wait for a later "
        "class — speaking carries you first. Lesson one is complete: you have greeted, thanked, "
        "named yourself, and placed yourself on the map, in the most spoken language on Earth. "
        "Zàijiàn — goodbye, and we will meet again."
    ),
}

# ---------------------------------------------------------------------
# NEW SECTIONS — authored founding classes.
# Each section: dept-head professor (teaches the flagship class),
# classes with units + homework; the flagship carries the recorded
# opening 'lesson'. Non-flagship classes get their own generated
# professors from build-stageb.py.
# ---------------------------------------------------------------------
def cls(id_, title, units, hw_q, hw_w, lesson=None):
    d = {"id": id_, "title": title, "units": units,
         "homework": {"q": hw_q, "worked": hw_w}}
    if lesson:
        d["lesson"] = lesson
    return d

NEW_SECTIONS = [
    {
        "id": "ai-computing", "name": "AI & Computing",
        "group": "Science, Technology & AI",
        "professor": {
            "name": "Professor David Kim",
            "personality": "A systems thinker with a teacher's patience; he refuses mystique in both directions — AI is neither magic nor menace in his room, it is machinery whose workings can be shown. He draws the diagram before he names the thing.",
            "greeting": "Come in. We take the machine apart by understanding it — no magic allowed, in either direction.",
            "voiceAccent": "American",
            "portrait": {"skin": "#eec39a", "hair": "#14100c", "hairStyle": "short", "outfit": "#26332a", "glasses": True},
        },
        "classes": [
            cls("ai-fundamentals-what-a-mind-made-of-math-is",
                "AI Fundamentals — What a Mind Made of Math Is",
                ["What 'artificial intelligence' actually names", "Data, parameters, and training: the three ingredients",
                 "What a model is — a function with a memory of examples", "Prediction as the core act",
                 "Where AI is strong, where it is brittle, and why", "The honest vocabulary: no magic, no menace"],
                "In your own words, one paragraph: what is a model, and what did training do to it? Use one example from your own life where prediction — not understanding — was enough.",
                "A model is a function — a machine for turning inputs into outputs — whose internal settings (parameters) were adjusted, over millions of examples, until its predictions matched reality often enough to be useful. Training is that adjustment. A spam filter never understood a word of your email; prediction was enough, and knowing the difference between the two is the whole first lesson.",
                "Come in. I am Professor David Kim, and this is AI Fundamentals. Before anything else, we clear the fog: artificial intelligence is not magic, and it is not a mind in a box. It is machinery — mathematics, running at enormous scale, on data. Here is the whole secret in one sentence: a model is a function that was shown so many examples that its guesses became good. Training is the showing. Prediction is the act. Everything else — the chatbots, the image makers, the agents you will meet in this department's later classes — is those three ideas, arranged with increasing cleverness. In this class we learn the honest vocabulary: data, parameters, training, inference — and we learn where these systems are strong, where they are brittle, and why both are true at once. You will leave able to read any headline about AI and know, within a sentence or two, whether it is reporting or theatre. That is a citizen's skill now, and it starts here."),
            cls("machine-learning-i-how-machines-learn-from-data",
                "Machine Learning I — How Machines Learn From Data",
                ["Examples in, rules out: the inversion of programming", "Features and labels: what the machine is shown",
                 "The loss function: a number that says 'wrong, this much'", "Gradient descent: walking downhill in the dark",
                 "Overfitting: memorising instead of learning", "Test data: the exam the model has never seen"],
                "Explain overfitting to a friend using a student and an exam. Two or three sentences, no jargon you cannot unpack.",
                "Overfitting is the student who memorised last year's exam answers instead of learning the subject: perfect on the questions already seen, helpless on new ones. The cure is the same in both cases — hold back questions the learner has never seen, and grade on those."),
            cls("agents-ai-that-acts-tools-memory-and-work",
                "Agents — AI That Acts: Tools, Memory, and Work",
                ["From answering to acting: what makes an agent", "Tools: hands for a model — search, code, messages",
                 "Memory: short-term context and the long record", "Planning in loops: act, observe, adjust",
                 "Permission and latitude: who decides what the agent may do", "Failure modes of agents, and the guardrails that hold"],
                "Name one job in your own life you would hand to an agent, and the exact point where you would want it to stop and ask you. Why there?",
                "There is no single right answer — the worked answer is the shape of one: the job is delegable where its steps are checkable and reversible; the stop-point belongs where an action becomes irreversible, spends money, speaks in your name, or touches another person's rights. Drawing that line, task by task, is the actual skill of working with agents."),
            cls("computing-foundations-how-computers-actually-work",
                "Computing Foundations — How Computers Actually Work",
                ["Bits and the audacity of counting with two fingers", "The processor: a very fast, very literal clerk",
                 "Memory and storage: the desk and the filing cabinet", "Programs: instructions all the way down",
                 "Networks: computers talking, and what can go wrong", "Files, formats, and where your data actually lives"],
                "A computer is 'just' counting with electricity — write four sentences on what has to be added to counting before you get a word processor. Keep every claim checkable.",
                "Counting gives you numbers; you must add representation (numbers standing for letters, colours, sounds by agreed codes), stored instructions (the program as data the machine can fetch), conditional branching (do this if that), and input/output (a way for the world to reach the counting and the counting to reach the world). A word processor is those four, wearing a friendly face."),
            cls("data-where-it-lives-and-what-it-proves",
                "Data — Where It Lives and What It Proves",
                ["What counts as data, and what is just noise with confidence", "Tables, records, and the humble spreadsheet",
                 "Samples and populations: asking some to learn about all", "Correlation, causation, and the gap between them",
                 "Charts that tell the truth and charts that lean", "Your own data: who holds it, and what it can prove"],
                "Find one chart — anywhere — that leans: a cut axis, a cherry-picked range, a missing denominator. Describe in three sentences what it wants you to believe and what it hides.",
                "The worked answer is a method, not a chart: name the claim, then ask three questions — what is the denominator, what range was chosen and what was left outside it, and does the axis start where honesty starts? A chart that survives all three has earned your belief; one that fails any has told you what it is."),
        ],
    },
    {
        "id": "architecture", "name": "Architecture",
        "group": "Science, Technology & AI",
        "professor": {
            "name": "Professor Ada Whitmore",
            "personality": "An architect who still draws by hand first; she believes a building is an argument about how people should live, made in load-bearing material. Exact about structure, romantic about light, and incapable of letting a vague plan leave the room.",
            "greeting": "Come in, and look up. Every ceiling you have ever stood under was a decision — we learn to make them.",
            "voiceAccent": "British",
            "portrait": {"skin": "#eec39a", "hair": "#57493a", "hairStyle": "bun", "outfit": "#6d4c2a", "glasses": True},
        },
        "classes": [
            cls("architecture-i-seeing-like-an-architect",
                "Architecture I — Seeing Like an Architect",
                ["The architect's eye: proportion, rhythm, scale", "Plan, section, elevation: the three honest views",
                 "Structure and skin: what holds it up, what meets the weather", "Light as a building material",
                 "How people move: circulation and the life inside the plan", "Reading a real building, start to finish"],
                "Take one building you know well. In five sentences: what holds it up, where does the light come in, and how do people move through it? You are reading it now, not just remembering it.",
                "The worked answer is the reading itself, in order: name the structure (posts and beams? load-bearing walls? a frame?), name the light (which faces, which openings, what hours), name the path (door to stair to room). A building you can describe in those three sentences is a building you have begun to see like an architect.",
                "Come in, and look up. I am Professor Ada Whitmore, and this is Architecture One — Seeing Like an Architect. Before we draw a single line, we learn to see, because most people have lived their whole lives inside buildings they have never actually looked at. A building is three things at once: a structure that stands up, a skin that keeps the weather out, and a set of decisions about how people will live and move inside it. In this class you will learn the architect's three honest views — the plan, from above; the section, cut through; the elevation, face on — and you will learn to ask of any building the questions that unlock it: What holds it up? Where does the light come in? How do people move? Architecture is the most public art and the slowest technology we have; a building is an argument about how life should go, made in material that outlives the arguer. By the end of this class, no building will ever be invisible to you again."),
            cls("structures-how-buildings-stand",
                "Structures — How Buildings Stand",
                ["Loads: the weight of everything, including snow and people", "Compression and tension: push and pull",
                 "Beams, columns, and the betrayal of the long span", "The arch and the dome: compression made beautiful",
                 "Frames, trusses, and the skeleton idea", "Foundations: arguing with the ground"],
                "A beam sags more in the middle than at the ends. In your own words: where is the top of the beam being squeezed, where is the bottom being stretched, and why does that tell you what material the beam wants to be?",
                "The top fibres are in compression (squeezed), the bottom in tension (stretched), and the middle depth barely works at all — which is why steel, strong in tension, carries the bottom of a concrete beam as rebar, and why an I-beam puts its material at the top and bottom edges where the work is."),
            cls("the-blueprint-reading-and-drawing-plans",
                "The Blueprint — Reading and Drawing Plans",
                ["Scale: the drawing as a promise at a ratio", "The plan view: walls as lines, doors as swings",
                 "Sections and elevations: the other two truths", "Symbols and conventions: the shared shorthand",
                 "Dimensions: numbers that someone will build from", "From sketch to set: how a drawing becomes a document"],
                "Draw the plan of one room you know — walls, door swing, windows, furniture — at any consistent scale, and dimension the two longest walls. It does not need to be beautiful. It needs to be true.",
                "There is no single worked drawing; the check is threefold: the door swing clears what it must clear, the furniture fits the walls it stands against, and your two dimensions agree with the proportions you drew. If all three hold, you have read and written your first true plan."),
            cls("design-studio-i-your-first-building",
                "Design Studio I — Your First Building",
                ["The brief: what this building must do, and for whom", "Site: sun, wind, slope, and neighbours",
                 "Bubble diagrams: relationships before rooms", "From bubbles to plan: giving ideas walls",
                 "The model: card, foam, and honest failure", "The review: presenting, defending, improving"],
                "Write the brief for your building in five lines: who it serves, what must happen inside it, what the site gives and forbids, and the one thing it must feel like. The studio builds from this page.",
                "A good brief is short enough to pin above the drawing board and specific enough to argue with: 'A workshop for one boat-builder, on a sloped lot facing south; building and storing inside; the lot gives sun and a view, forbids nothing but the neighbour's light; it must feel like a place where work is honoured.' Every later decision gets tested against those five lines."),
            cls("history-of-building-pyramids-to-skyscrapers",
                "History of Building — Pyramids to Skyscrapers",
                ["Stone on stone: Egypt, Greece, and the post-and-lintel world", "Rome: concrete, the arch, and building an empire",
                 "The Gothic wager: height and light on a skeleton of stone", "Iron and the industrial century",
                 "Steel, elevators, and the skyscraper bargain", "The modern argument: what a building owes its street"],
                "Pick one leap — the arch, Gothic structure, iron, or steel-and-elevator — and write four sentences: what became possible that was impossible the year before, and what did it cost?",
                "Take the arch: before it, openings were limited to what a single stone lintel could span; after it, Rome could roof baths, bridge rivers, and stack aqueducts across valleys. The cost was skill and centring — every arch is built twice, once in timber to hold it up while it learns to stand. Each leap in this course has that shape: a new possibility, paid for in a new kind of knowledge."),
        ],
    },
    {
        "id": "biology", "name": "Biology & Life Sciences",
        "group": "Science, Technology & AI",
        "professor": {
            "name": "Professor Sylvia Anand",
            "personality": "A field biologist's wonder disciplined by a lab scientist's standards; she teaches life from the cell outward and never lets a beautiful story outrun the evidence for it. Her specimens are real and her questions are alive.",
            "greeting": "Come in — everything in this room was once alive, including the subject. Especially the subject.",
            "voiceAccent": "Indian",
            "portrait": {"skin": "#b97a4a", "hair": "#1c1410", "hairStyle": "ponytail", "outfit": "#2e5d33", "glasses": False},
        },
        "classes": [
            cls("biology-i-the-cell-where-life-starts",
                "Biology I — The Cell, Where Life Starts",
                ["The cell: life's smallest self-running unit", "The membrane: a border with customs officers",
                 "Energy: mitochondria and the currency of ATP", "DNA to protein: the central workflow",
                 "Division: how one cell becomes two, faithfully", "Specialisation: how identical instructions build a body"],
                "In four sentences: why is a cell compared to a city, and where does the comparison break? Both halves matter.",
                "The comparison works for division of labour — power stations (mitochondria), borders (membrane), a library of plans (DNA). It breaks at intention: no mayor, no plan-reader with a mind; the city's order emerges from chemistry obeying physics, and that emergence, not the metaphor, is the wonder.",
                "Come in. I am Professor Sylvia Anand, and this is Biology One — the cell, where life starts. Every living thing you have ever seen — the oak, the whale, the person beside you — is either one cell or a society of them, and everything life does, it does first inside this microscopic room. In this class we take the cell apart respectfully: the membrane, a border that decides what may pass; the mitochondria, burning fuel into the currency every process spends; and the great central workflow — DNA read into RNA, RNA built into protein, proteins doing nearly all the actual work of being alive. Then the miracle of bookkeeping: how a cell copies three billion letters of instruction and divides, faithfully, into two. Understand the cell and the rest of biology — organs, species, ecosystems — becomes the same story at larger scale. We begin, as life did, small."),
            cls("genetics-dna-inheritance-and-variation",
                "Genetics — DNA, Inheritance, and Variation",
                ["Genes and alleles: the instruction and its editions", "Dominant, recessive, and the honest complications",
                 "Meiosis: shuffling the deck on purpose", "Mutations: copying errors and their long consequences",
                 "Reading a genome: what a sequence can and cannot tell you", "Genetic medicine: promise, evidence, and hype"],
                "Two parents, both carriers of a recessive trait neither shows. What fraction of their children would show it, on average — and why does 'on average' matter in a real family of three?",
                "One in four, on average: each child independently has a 1/4 chance of receiving both recessive copies. 'On average' matters because three children are not a statistic — a real family could have none, or all three; probability governs crowds, not cradles."),
            cls("evolution-the-story-written-in-species",
                "Evolution — The Story Written in Species",
                ["Variation first: the raw material", "Selection: the environment as editor",
                 "Deep time and the fossil record's honest gaps", "Speciation: when one story becomes two",
                 "Evidence lines: fossils, anatomy, embryos, molecules", "Evolution in the present tense: microbes, moths, and medicine"],
                "In your own words: why is 'survival of the fittest' a misleading summary, and what four-word replacement does this class use instead?",
                "It misleads because 'fittest' suggests the strongest or best, when the mechanism only requires heritable differences in reproductive success — the class's replacement is 'descent with modification, filtered': descent with modification names the process, and the filter is any environment, not a contest with a winner's podium."),
            cls("ecology-living-systems-and-how-they-hold",
                "Ecology — Living Systems and How They Hold Together",
                ["Energy flow: sun to grass to grazer to grave", "Food webs: nobody eats alone",
                 "Cycles: water, carbon, nitrogen, round and round", "Populations: growth, limits, and the carrying question",
                 "Keystone species: small numbers, enormous leverage", "Disturbance and resilience: what 'holding together' means"],
                "Pick one species and list what it eats, what eats it, and one thing that would change for three other species if it vanished. That web is the lesson.",
                "The worked answer is the method worked once: the bee — eats nectar and pollen, is eaten by birds and spiders; vanish it, and the flowering plants it pollinates set less seed, the birds lose both prey and the seeds the plants would have made, and the grazers meet thinner meadows. Three species, three different kinds of debt — that is a food web thinking."),
        ],
    },
    {
        "id": "health", "name": "Health & Medicine",
        "group": "Science, Technology & AI",
        "professor": {
            "name": "Professor Jonathan Meyer",
            "personality": "A clinician-teacher: calm, plain-spoken, and allergic to both panic and miracle cures. He teaches the body as a system its owner should understand, and he is exact about the line between knowledge and diagnosis — this classroom informs; it never treats.",
            "greeting": "Come in. You live in the subject of this class — let us learn how it works.",
            "voiceAccent": "German",
            "portrait": {"skin": "#f6d7b8", "hair": "#5c5340", "hairStyle": "short", "outfit": "#1f4d7a", "glasses": True},
        },
        "classes": [
            cls("health-i-your-body-owners-manual",
                "Health I — Your Body, Owner's Manual",
                ["The systems at a glance: one body, eleven crews", "The heart and the plumbing: pressure, flow, return",
                 "Lungs and blood: the gas exchange", "The immune system: an army with a memory",
                 "Signals: hormones, nerves, and feedback loops", "Numbers worth knowing: what the common tests measure"],
                "Pick one feedback loop in your body — temperature, blood sugar, or thirst — and describe it in four sentences: the sensor, the signal, the response, and what 'back to normal' means.",
                "Blood sugar, worked: sensors in the pancreas read glucose; the signal is insulin (or its opposite, glucagon); the response is cells taking up sugar or the liver releasing it; 'back to normal' is a range, not a point — the loop hunts around a setting, which is why healthy numbers wobble instead of pinning.",
                "Come in. I am Professor Jonathan Meyer, and this is Health One — your body, owner's manual. You are the only person who will live in your body for its entire service life, and most owners are never given the manual. This class is the manual. We walk the systems the way a good mechanic walks a machine: the heart and its plumbing, pressure and flow; the lungs and the blood, trading gases at a border thinner than paper; the immune system, an army with a memory, which is why vaccines work; and the signals — nerves for speed, hormones for reach — that hold the whole enterprise in feedback loops tuned like thermostats. Two rules in my room. First: knowledge here is for understanding, never for self-diagnosis — a classroom informs, it does not treat. Second: every claim gets its evidence asked after. Bodies are systems, and systems can be learned. We begin."),
            cls("first-aid-what-to-do-before-help-arrives",
                "First Aid — What To Do Before Help Arrives",
                ["The first minute: assess, shout, send", "Bleeding: pressure, elevation, tourniquets — the real order",
                 "Choking: the blocked airway, adult and child", "The unconscious person: recovery position and CPR's shape",
                 "Burns, breaks, and bites: the common three", "The kit: what a home should actually hold"],
                "Write, from memory, the order of actions for finding an adult collapsed and unresponsive — five steps, in order. Then check it against the unit. The order is the lesson.",
                "One: check response and shout for help. Two: send someone specific to call emergency services and fetch a defibrillator. Three: open the airway, check breathing for no more than ten seconds. Four: if not breathing normally, start compressions — hard, fast, centre of the chest. Five: use the defibrillator the moment it arrives, and follow its voice. Every step exists because the minutes before help arrives are the minutes that decide."),
            cls("nutrition-fuel-repair-and-the-long-game",
                "Nutrition — Fuel, Repair, and the Long Game",
                ["Macros honestly: protein, fat, carbohydrate, and what each is FOR", "Micronutrients: small doses, large consequences",
                 "Energy balance without mythology", "Reading a label like a detective",
                 "Fad diets: the anatomy of a recurring miracle", "Eating for decades: the unglamorous evidence"],
                "Take one food label and write three sentences: what it wants you to notice, what it mentions quietly, and what it cannot tell you at all.",
                "Labels shout the fashionable virtue (low fat! high protein!), mention the sugar or sodium quietly in the small grid, and cannot tell you the only thing that finally matters — what the rest of your day and decade of eating looks like. A label describes a food; health describes a pattern."),
            cls("medicine-how-healing-works-and-doctors-think",
                "Medicine — How Healing Works, and How Doctors Think",
                ["Diagnosis as detective work: hypothesis and test", "The evidence ladder: anecdote to trial",
                 "How drugs work: keys, locks, and side effects as logic", "Surgery: repair under anaesthesia's truce",
                 "Prevention: the medicine nobody notices", "Talking with doctors: questions that get answers"],
                "A friend swears a remedy worked because they took it and got better. Write the two questions this class teaches you to ask — kindly, but exactly.",
                "First: what would have happened without it — most illnesses improve on their own, so recovery after a remedy is the weakest evidence there is. Second: has it been tested against doing nothing (or against a placebo) in people like you? The questions are kind because they protect your friend; they are exact because 'it worked for me' has launched a thousand useless cures."),
        ],
    },
    {
        "id": "trades", "name": "Trades & Applied Skills",
        "group": "Science, Technology & AI",
        "professor": {
            "name": "Professor Carla Mendes",
            "personality": "Thirty years on job sites in her voice; she teaches trades the way they are learned — safety first, principles always, hands on everything. Contemptuous of corner-cutting, generous with tricks of the trade, and firm that a good tradesperson is an applied physicist who gets wet.",
            "greeting": "Boots on. In this department we learn it the way the work teaches it — safely, and for real.",
            "voiceAccent": "Brazilian",
            "portrait": {"skin": "#d9a066", "hair": "#3a2415", "hairStyle": "ponytail", "outfit": "#8a6508", "glasses": False},
        },
        "classes": [
            cls("plumbing-i-water-in-water-out",
                "Plumbing I — Water In, Water Out",
                ["The two systems: supply under pressure, drainage by gravity", "Pipe materials and what each is for",
                 "Valves, traps, and vents: the small parts that run the show", "Reading a leak: where water has been",
                 "The plumber's core tools and what 'hand-tight plus a quarter' means", "Safety and law: permits, shutoffs, and knowing your limits"],
                "A sink drains slowly and gurgles. In three sentences: what is the gurgle telling you, and which part of the system — supply, trap, or vent — do you suspect first, and why?",
                "The gurgle is air being pulled through the trap's water seal — the drain is asking for air it should be getting from the vent. Suspect the vent (or a partial blockage making the drain behave like one): supply is pressurised and silent about drainage, the trap holds water by design, but a starved vent makes every drain in the line breathe through its traps.",
                "Boots on. I am Professor Carla Mendes, and this is Plumbing One — water in, water out. Every building you will ever enter is quietly running two rivers: one under pressure, bringing clean water to every tap, and one with no pressure at all, coaxing waste away downhill — and the whole craft lives in understanding that those two systems obey opposite rules. Supply is force; drainage is persuasion. In this class you will learn the parts that run the show: the trap, which keeps sewer gas out of your kitchen with nothing but a cup of standing water; the vent, which lets drains breathe; the shutoff, which you will locate in any house within a minute before I am done with you. We learn it the way the work teaches it: principles first, hands on everything, safety always — water is patient and electricity is not the only thing in a wall that can hurt you. A good plumber is an applied physicist who gets wet. Let us get to work."),
            cls("electrical-i-circuits-safety-and-the-panel",
                "Electrical I — Circuits, Safety, and the Panel",
                ["Voltage, current, resistance: the water analogy and its limits", "The circuit: a loop or it is nothing",
                 "The panel: breakers as guardians", "Grounding and GFCI: safety written in copper",
                 "Wire, load, and heat: why sizes matter", "The rules that keep you alive: test, lock, verify"],
                "A breaker keeps tripping on one circuit. In three sentences: what is the breaker telling you, and why is 'replace it with a bigger breaker' the one answer that can burn a house down?",
                "The breaker is reporting that the circuit draws more current than its wires can safely carry — it is a guardian tripping on purpose. A bigger breaker silences the guardian while the wires, sized for the smaller current, overheat inside the walls. The fix is to find the overload or the fault, never to fire the messenger."),
            cls("carpentry-i-measure-cut-join",
                "Carpentry I — Measure, Cut, Join",
                ["Wood: grain, movement, and why boards cup", "Measuring and marking: the pencil is a precision instrument",
                 "Saws and the honest cut", "Joints: where carpentry becomes joinery",
                 "Fasteners: nails, screws, glue — and choosing", "Squareness: the diagonal test that never lies"],
                "You measure both diagonals of a rectangular frame and they differ by a centimetre. What does the frame look like, and which corner do you push?",
                "The frame is a parallelogram — racked out of square. Push the corner at the end of the LONGER diagonal toward the other side: shortening the long diagonal until the two agree makes all four corners true at once. Equal diagonals are the definition of rectangular; carpenters trust them more than their eyes."),
            cls("automotive-i-how-a-car-works-and-what-breaks",
                "Automotive I — How a Car Works and What Breaks",
                ["The four strokes: what the engine is actually doing", "The supporting cast: cooling, lubrication, electrical",
                 "Brakes and tyres: where the car meets physics", "Sounds, smells, and leaks: the diagnostic senses",
                 "Maintenance that matters and maintenance theatre", "Reading a mechanic's invoice like an owner"],
                "A car overheats only in traffic, never on the highway. In three sentences: what does that pattern point to, and why does the highway hide it?",
                "It points at airflow, not coolant: at highway speed the road itself forces air through the radiator, masking a dead or weak cooling fan; in traffic the fan is the only airflow there is, so its failure shows. Patterns are diagnoses half-finished — when a fault happens is often what the fault is."),
            cls("the-house-systems-heating-cooling-keeping-a-home-alive",
                "The House Systems — Heating, Cooling, and Keeping a Home Alive",
                ["The furnace and the heat pump: moving heat versus making it", "Ducts and airflow: the forgotten half of comfort",
                 "The thermostat: a negotiator, not a switch", "Insulation and air sealing: the cheapest fuel",
                 "Water heaters, sump pumps, and the basement cast", "The seasonal walk: what to check before each season checks you"],
                "Two identical houses, one with heating bills half the other's. List the three likeliest reasons, in the order a professional would check them.",
                "Air sealing first — holes to the attic and outside leak heated air continuously and cost little to close. Insulation second — thin attic insulation is the classic silent bill. The equipment third — an old or oversized furnace wastes fuel, but it is checked last because the first two are cheaper and more common. Envelope before machinery: that order is the trade's whole wisdom in one line."),
        ],
    },
    {
        "id": "business", "name": "Business & Economics",
        "group": "Arts, Letters & Enterprise",
        "professor": {
            "name": "Professor Andre Boateng",
            "personality": "A founder who has signed both sides of a payroll; he teaches business as arithmetic plus character — the numbers must work and the word must hold. Warm about ambition, ruthless about fuzzy thinking, and famous for asking 'and then what happens?'",
            "greeting": "Come in. Bring your ambitions — we are going to give them arithmetic.",
            "voiceAccent": "Nigerian",
            "portrait": {"skin": "#8d5524", "hair": "#14100c", "hairStyle": "short", "outfit": "#5c2a54", "glasses": False},
        },
        "classes": [
            cls("business-i-what-a-business-is-from-the-ground-up",
                "Business I — What a Business Is, From the Ground Up",
                ["The exchange at the centre: value for money, both sides glad", "Customers: who they are and what they actually buy",
                 "Costs, price, and the margin between them", "Cash flow: profit's faster, stricter sibling",
                 "The legal shapes: sole trader, partnership, company", "Records: the memory a business keeps of itself"],
                "A business is profitable on paper and still dies. In three sentences: what kills it, and what number should its owner have watched every week?",
                "Cash flow kills it: profit can sit in unpaid invoices and stock on shelves while rent, wages, and suppliers demand actual money on actual dates. The number to watch weekly is cash — what is in the account, what is owed in, what is owed out, and when. Profit is an opinion at year-end; cash is a fact every Friday.",
                "Come in. I am Professor Andre Boateng, and this is Business One — what a business is, from the ground up. Strip away the logos and the language and a business is one honest exchange: something of value, made or done, traded for money, with both sides glad it happened. Everything else is machinery around that exchange — finding the customers, setting the price, watching the costs, and above all watching the cash, because businesses rarely die of unpopularity; they die of an empty account on a Friday with wages due. In this class we build the whole picture plainly: what a customer actually buys (it is never quite the object), the margin between cost and price where a business lives, the legal shapes a business can wear, and the records it must keep — a business that cannot remember itself cannot be run, sold, or saved. Ambition is welcome here. Arithmetic is compulsory. Let us begin."),
            cls("economics-i-scarcity-prices-and-why-markets-move",
                "Economics I — Scarcity, Prices, and Why Markets Move",
                ["Scarcity: the first fact", "Supply and demand: the two curves that run the world",
                 "Price as a signal, not a verdict", "Elasticity: how much, when the price moves",
                 "Money: what it is when everyone agrees", "Booms, busts, and the stories we tell about them"],
                "A frost ruins half the orange crop. Trace, in four steps, what happens to the price of orange juice, what juice-makers do next, and what orange growers plant next year.",
                "Price rises — the same demand chasing half the fruit. Juice-makers stretch supply: blends, imports, smaller cartons at the old price. Some drinkers switch to apple. And growers, seeing high prices, plant more trees — which fruit in several years, possibly into a glut. That four-beat rhythm — signal, scramble, substitution, investment — is most of economics in one orange."),
            cls("money-and-the-books-accounting-without-tears",
                "Money & the Books — Accounting Without Tears",
                ["Double entry: every coin has two stories", "The three statements: position, performance, cash",
                 "Assets, liabilities, equity: the grammar of the balance sheet", "Revenue is not cash, and other expensive confusions",
                 "Taxes: the appointment every business keeps", "Reading your own books monthly: the owner's habit"],
                "Your business is owed $10,000 for work delivered and owes $6,000 to suppliers. Are you 'up $4,000'? Answer in three sentences, carefully.",
                "On paper, your position improved by $4,000 — an asset (receivable) exceeds the liability (payable). But you are up zero dollars of cash, and if the $6,000 falls due before the $10,000 arrives, you are in trouble while 'up'. The books tell both truths at once; the skill is reading the second one in time."),
            cls("selling-the-honest-craft-of-the-deal",
                "Selling — The Honest Craft of the Deal",
                ["Selling as diagnosis: find the problem before the pitch", "Listening ratios: two ears, one mouth",
                 "The honest pitch: true claims, plainly made", "Objections: information, not combat",
                 "Closing: asking, cleanly, once", "After the sale: the reputation that sells next time"],
                "A customer says 'it's too expensive.' Write the two sentences a graduate of this class says next — no discounts, no pressure, and the conversation still alive at the end of them.",
                "First: 'Tell me what you were hoping it would do for you — I want to be sure we're pricing the right thing.' Second: 'If it does that, measured in your numbers, what is it worth over a year?' The price has not moved; the comparison has — from a number against nothing, to a number against the value the customer themselves stated."),
        ],
    },
]
