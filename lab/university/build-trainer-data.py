#!/usr/bin/env python3
"""Build trainer-data.json — the phrase sets for the Rosetta-style
listen-and-repeat trainer, one set per language class.

Spanish (Carmen Vega) is the flagship: Lesson 1 re-cut into steps that
build word-by-word into sentences, ending on the line the whole course
exists for — 'Buenas noches, mi amor', for Jillian. Every other
language gets the same shape at starter depth: greetings, your name,
where you're from, the two keys (please / thank you), pleased to meet
you — the phrases each class's own homework already teaches.

For scripts the recognizer returns natively (Devanagari, kana, hanzi,
Arabic, Cyrillic, hangul), the TARGET is the native script — that is
what SpeechRecognition transcribes — and the romanization rides along
as the display line. Audio paths are by convention, filled in here:
  audio/trainer/<classId>/welcome.mp3
  audio/trainer/<classId>/step-<n>.mp3        (the model)
  audio/trainer/<classId>/step-<n>-slow.mp3   (Spanish: generated;
                                               others: engine falls
                                               back to slow playback)
  audio/trainer/<classId>/praise-<n>.mp3
  audio/trainer/<classId>/retry-<n>.mp3
"""
import json, os

def steps(*rows):
    return [{"target": t, "display": d, "meaning": m} for (t, d, m) in rows]

CLASSES = {}

# ---------------- Spanish — the flagship, Lesson 1 in full ----------------
CLASSES["espanol-i-speak-from-zero"] = {
    "lang": "es-ES",
    "welcome": ("Hola, Bill. We do this together now — I say it first, "
                "then you say it back to me. Nothing moves on until it "
                "sounds right. That is how you will actually learn. ¿Listo?"),
    "steps": steps(
        ("Hola", "Hola", "hello — for any hour, any person"),
        ("Buenos días", "Buenos días", "good morning"),
        ("Buenas tardes", "Buenas tardes", "good afternoon"),
        ("Buenas noches", "Buenas noches", "good night / good evening"),
        ("Me llamo", "Me llamo", "my name is… (I call myself…)"),
        ("Me llamo Bill", "Me llamo Bill", "my name is Bill"),
        ("Mucho gusto", "Mucho gusto", "pleased to meet you"),
        ("Por favor", "Por favor", "please — the first key"),
        ("Gracias", "Gracias", "thank you — the second key"),
        ("Soy de Michigan", "Soy de Michigan", "I am from Michigan"),
        ("Soy empresario", "Soy empresario", "I am a businessman"),
        ("Mi prometida se llama Jillian", "Mi prometida se llama Jillian",
         "my fiancée's name is Jillian"),
        ("Mi amor", "Mi amor", "my love — the sweet words begin"),
        ("Mi corazón", "Mi corazón", "my heart — Spanish means it literally"),
        ("Te quiero", "Te quiero", "I love you — the everyday way, at the door"),
        ("Te quiero, Jillian", "Te quiero, Jillian", "I love you, Jillian"),
        ("Buenas noches, mi amor", "Buenas noches, mi amor",
         "good night, my love — tonight's line, for her"),
    ),
    "praise": [
        "¡Perfecto, Bill! You see? A natural.",
        "¡Muy bien! Just like that — say it to her exactly like that.",
        "¡Eso es! That is precisely how it should sound.",
    ],
    "retry": [
        "Casi, casi — almost. Listen to me once more, slowly… and then it is yours.",
        "Ay, so close. Despacio — slowly this time. You have got this, Bill.",
    ],
    "slow_all": True,
}

# ---------------- the other nineteen ----------------
def starter(lang, welcome, rows, praise, retry):
    return {"lang": lang, "welcome": welcome, "steps": steps(*rows),
            "praise": [praise], "retry": [retry], "slow_all": False}

W = ("Welcome. In this room we speak first: I say it, then you say it "
     "back. Nothing moves on until it sounds right. Let us begin.")

CLASSES["portugues-i-speak-from-zero"] = starter("pt-PT", W, [
    ("Olá", "Olá", "hello — at any hour"),
    ("Bom dia", "Bom dia", "good morning"),
    ("Boa noite", "Boa noite", "good night / good evening"),
    ("O meu nome é Bill", "O meu nome é Bill", "my name is Bill"),
    ("Sou de Michigan", "Sou de Michigan", "I am from Michigan"),
    ("Por favor", "Por favor", "please — the first key"),
    ("Obrigado", "Obrigado", "thank you — a man says obrigado"),
    ("Muito prazer", "Muito prazer", "pleased to meet you"),
], "Muito bem! Very good — exactly right.", "Outra vez, devagar — once more, slowly.")

CLASSES["deutsch-i-speak-from-zero"] = starter("de-DE", W, [
    ("Guten Tag", "Guten Tag", "good day — the greeting that works everywhere"),
    ("Guten Morgen", "Guten Morgen", "good morning"),
    ("Guten Abend", "Guten Abend", "good evening"),
    ("Ich heiße Bill", "Ich heiße Bill", "my name is Bill"),
    ("Ich komme aus Michigan", "Ich komme aus Michigan", "I come from Michigan"),
    ("Bitte", "Bitte", "please — and also you're welcome"),
    ("Danke", "Danke", "thank you"),
    ("Freut mich", "Freut mich", "pleased to meet you"),
], "Sehr gut! Very good — exactly right.", "Noch einmal, langsam — once more, slowly.")

CLASSES["francais-speak-from-zero"] = starter("fr-FR", W, [
    ("Bonjour", "Bonjour", "hello / good day"),
    ("Bonsoir", "Bonsoir", "good evening"),
    ("Je m'appelle Bill", "Je m'appelle Bill", "my name is Bill"),
    ("Je suis de Michigan", "Je suis de Michigan", "I am from Michigan"),
    ("S'il vous plaît", "S'il vous plaît", "please — the first key"),
    ("Merci", "Merci", "thank you — the second key"),
    ("Enchanté", "Enchanté", "pleased to meet you"),
], "Très bien ! Very good — exactly right.", "Encore une fois, lentement — once more, slowly.")

CLASSES["italiano-i-speak-from-zero"] = starter("it-IT", W, [
    ("Buongiorno", "Buongiorno", "good day"),
    ("Buonasera", "Buonasera", "good evening"),
    ("Mi chiamo Bill", "Mi chiamo Bill", "my name is Bill"),
    ("Sono del Michigan", "Sono del Michigan", "I am from Michigan"),
    ("Per favore", "Per favore", "please — the first key"),
    ("Grazie", "Grazie", "thank you — the second key"),
    ("Piacere", "Piacere", "pleased to meet you"),
], "Molto bene! Very good — exactly right.", "Ancora una volta, piano — once more, slowly.")

CLASSES["nederlands-i-speak-from-zero"] = starter("nl-NL", W, [
    ("Hallo", "Hallo", "hello"),
    ("Goedemorgen", "Goedemorgen", "good morning"),
    ("Ik heet Bill", "Ik heet Bill", "my name is Bill"),
    ("Ik kom uit Michigan", "Ik kom uit Michigan", "I come from Michigan"),
    ("Alsjeblieft", "Alsjeblieft", "please — the first key"),
    ("Dank je wel", "Dank je wel", "thank you — the second key"),
    ("Leuk je te ontmoeten", "Leuk je te ontmoeten", "pleased to meet you"),
], "Heel goed! Very good — exactly right.", "Nog een keer, langzaam — once more, slowly.")

CLASSES["svenska-i-speak-from-zero"] = starter("sv-SE", W, [
    ("Hej", "Hej", "hello"),
    ("God morgon", "God morgon", "good morning"),
    ("Jag heter Bill", "Jag heter Bill", "my name is Bill"),
    ("Jag kommer från Michigan", "Jag kommer från Michigan", "I come from Michigan"),
    ("Snälla", "Snälla", "please — the first key"),
    ("Tack", "Tack", "thank you — the second key"),
    ("Trevligt att träffas", "Trevligt att träffas", "pleased to meet you"),
], "Mycket bra! Very good — exactly right.", "En gång till, långsamt — once more, slowly.")

CLASSES["norsk-i-speak-from-zero"] = starter("nb-NO", W, [
    ("Hei", "Hei", "hello"),
    ("God morgen", "God morgen", "good morning"),
    ("Jeg heter Bill", "Jeg heter Bill", "my name is Bill"),
    ("Jeg kommer fra Michigan", "Jeg kommer fra Michigan", "I come from Michigan"),
    ("Vær så snill", "Vær så snill", "please — the first key"),
    ("Takk", "Takk", "thank you — the second key"),
    ("Hyggelig å møte deg", "Hyggelig å møte deg", "pleased to meet you"),
], "Veldig bra! Very good — exactly right.", "En gang til, sakte — once more, slowly.")

CLASSES["dansk-i-speak-from-zero"] = starter("da-DK", W, [
    ("Hej", "Hej", "hello"),
    ("Godmorgen", "Godmorgen", "good morning"),
    ("Jeg hedder Bill", "Jeg hedder Bill", "my name is Bill"),
    ("Jeg kommer fra Michigan", "Jeg kommer fra Michigan", "I come from Michigan"),
    ("Tak", "Tak", "thank you"),
    ("Mange tak", "Mange tak", "thank you very much"),
    ("Hyggeligt at møde dig", "Hyggeligt at møde dig", "pleased to meet you"),
], "Meget godt! Very good — exactly right.", "En gang til, langsomt — once more, slowly.")

CLASSES["polski-i-speak-from-zero"] = starter("pl-PL", W, [
    ("Cześć", "Cześć", "hello"),
    ("Dzień dobry", "Dzień dobry", "good day"),
    ("Nazywam się Bill", "Nazywam się Bill", "my name is Bill"),
    ("Jestem z Michigan", "Jestem z Michigan", "I am from Michigan"),
    ("Proszę", "Proszę", "please — the first key"),
    ("Dziękuję", "Dziękuję", "thank you — the second key"),
    ("Miło mi", "Miło mi", "pleased to meet you"),
], "Bardzo dobrze! Very good — exactly right.", "Jeszcze raz, powoli — once more, slowly.")

CLASSES["hindi-i-speak-from-zero"] = starter("hi-IN", W, [
    ("नमस्ते", "नमस्ते · Namaste", "hello — the greeting with respect built in"),
    ("मेरा नाम बिल है", "मेरा नाम बिल है · Mera naam Bill hai", "my name is Bill"),
    ("मैं मिशिगन से हूँ", "मैं मिशिगन से हूँ · Main Michigan se hoon", "I am from Michigan"),
    ("कृपया", "कृपया · Kripya", "please — the first key"),
    ("धन्यवाद", "धन्यवाद · Dhanyavaad", "thank you — the second key"),
    ("आपसे मिलकर खुशी हुई", "आपसे मिलकर खुशी हुई · Aapse milkar khushi hui", "pleased to meet you"),
], "बहुत अच्छा! Very good — exactly right.", "एक बार और, धीरे — once more, slowly.")

CLASSES["japanese-i-speak-from-zero"] = starter("ja-JP", W, [
    ("こんにちは", "こんにちは · Konnichiwa", "good afternoon — the all-day greeting"),
    ("おはようございます", "おはようございます · Ohayō gozaimasu", "good morning, with respect"),
    ("わたしはビルです", "わたしはビルです · Watashi wa Bill desu", "I am Bill"),
    ("ミシガンからきました", "ミシガンからきました · Mishigan kara kimashita", "I come from Michigan"),
    ("おねがいします", "おねがいします · Onegaishimasu", "please — the first key"),
    ("ありがとうございます", "ありがとうございます · Arigatō gozaimasu", "thank you — the second key"),
    ("はじめまして", "はじめまして · Hajimemashite", "pleased to meet you"),
], "とてもよくできました! Very good — exactly right.", "もう一度、ゆっくり — once more, slowly.")

CLASSES["mandarin-i-speak-from-zero"] = starter("zh-CN", W, [
    ("你好", "你好 · Nǐ hǎo", "hello"),
    ("早上好", "早上好 · Zǎoshang hǎo", "good morning"),
    ("我叫比尔", "我叫比尔 · Wǒ jiào Bill", "my name is Bill"),
    ("我从密歇根来", "我从密歇根来 · Wǒ cóng Mìxiègēn lái", "I come from Michigan"),
    ("请", "请 · Qǐng", "please — the first key"),
    ("谢谢", "谢谢 · Xièxie", "thank you — the second key"),
    ("很高兴认识你", "很高兴认识你 · Hěn gāoxìng rènshi nǐ", "pleased to meet you"),
], "非常好! Very good — exactly right.", "再来一次，慢慢说 — once more, slowly.")

CLASSES["arabic-i-speak-from-zero"] = starter("ar-SA", W, [
    ("السلام عليكم", "السلام عليكم · As-salāmu ʿalaykum", "peace be upon you — the greeting"),
    ("صباح الخير", "صباح الخير · Ṣabāḥ al-khayr", "good morning"),
    ("اسمي بيل", "اسمي بيل · Ismī Bill", "my name is Bill"),
    ("أنا من ميشيغان", "أنا من ميشيغان · Anā min Michigan", "I am from Michigan"),
    ("من فضلك", "من فضلك · Min faḍlik", "please — the first key"),
    ("شكراً", "شكراً · Shukran", "thank you — the second key"),
    ("تشرفنا", "تشرفنا · Tasharrafnā", "pleased to meet you"),
], "أحسنت! Very good — exactly right.", "مرة أخرى، ببطء — once more, slowly.")

CLASSES["russian-i-speak-from-zero"] = starter("ru-RU", W, [
    ("Здравствуйте", "Здравствуйте · Zdravstvuyte", "hello — the formal, all-day greeting"),
    ("Доброе утро", "Доброе утро · Dobroe utro", "good morning"),
    ("Меня зовут Билл", "Меня зовут Билл · Menya zovut Bill", "my name is Bill"),
    ("Я из Мичигана", "Я из Мичигана · Ya iz Michigana", "I am from Michigan"),
    ("Пожалуйста", "Пожалуйста · Pozhaluysta", "please — the first key"),
    ("Спасибо", "Спасибо · Spasibo", "thank you — the second key"),
    ("Очень приятно", "Очень приятно · Ochyen priyatno", "pleased to meet you"),
], "Очень хорошо! Very good — exactly right.", "Ещё раз, медленно — once more, slowly.")

CLASSES["korean-i-speak-from-zero"] = starter("ko-KR", W, [
    ("안녕하세요", "안녕하세요 · Annyeonghaseyo", "hello — polite, all-day"),
    ("저는 빌입니다", "저는 빌입니다 · Jeoneun Bill imnida", "I am Bill"),
    ("미시간에서 왔습니다", "미시간에서 왔습니다 · Michigan-eseo wasseumnida", "I come from Michigan"),
    ("주세요", "주세요 · Juseyo", "please — the first key"),
    ("감사합니다", "감사합니다 · Gamsahamnida", "thank you — the second key"),
    ("만나서 반갑습니다", "만나서 반갑습니다 · Mannaseo bangapseumnida", "pleased to meet you"),
], "아주 잘했어요! Very good — exactly right.", "한 번 더, 천천히 — once more, slowly.")

CLASSES["turkish-i-speak-from-zero"] = starter("tr-TR", W, [
    ("Merhaba", "Merhaba", "hello"),
    ("Günaydın", "Günaydın", "good morning"),
    ("Benim adım Bill", "Benim adım Bill", "my name is Bill"),
    ("Michigan'dan geliyorum", "Michigan'dan geliyorum", "I come from Michigan"),
    ("Lütfen", "Lütfen", "please — the first key"),
    ("Teşekkür ederim", "Teşekkür ederim", "thank you — the second key"),
    ("Tanıştığımıza memnun oldum", "Tanıştığımıza memnun oldum", "pleased to meet you"),
], "Çok güzel! Very good — exactly right.", "Bir daha, yavaş — once more, slowly.")

CLASSES["kiswahili-i-speak-from-zero"] = starter("sw-KE", W, [
    ("Jambo", "Jambo", "hello"),
    ("Habari za asubuhi", "Habari za asubuhi", "good morning"),
    ("Jina langu ni Bill", "Jina langu ni Bill", "my name is Bill"),
    ("Natoka Michigan", "Natoka Michigan", "I come from Michigan"),
    ("Tafadhali", "Tafadhali", "please — the first key"),
    ("Asante", "Asante", "thank you — the second key"),
    ("Nimefurahi kukutana nawe", "Nimefurahi kukutana nawe", "pleased to meet you"),
], "Vizuri sana! Very good — exactly right.", "Tena, pole pole — once more, slowly.")

CLASSES["ukrainian-i-speak-from-zero"] = starter("uk-UA", W, [
    ("Добрий день", "Добрий день · Dobryi den", "good day — the greeting"),
    ("Мене звуть Білл", "Мене звуть Білл · Mene zvut Bill", "my name is Bill"),
    ("Я з Мічигану", "Я з Мічигану · Ya z Michigana", "I am from Michigan"),
    ("Будь ласка", "Будь ласка · Bud laska", "please — the first key"),
    ("Дякую", "Дякую · Diakuiu", "thank you — the second key"),
    ("Дуже приємно", "Дуже приємно · Duzhe pryiemno", "pleased to meet you"),
], "Дуже добре! Very good — exactly right.", "Ще раз, повільно — once more, slowly.")

CLASSES["vietnamese-i-speak-from-zero"] = starter("vi-VN", W, [
    ("Xin chào", "Xin chào", "hello"),
    ("Chào buổi sáng", "Chào buổi sáng", "good morning"),
    ("Tôi tên là Bill", "Tôi tên là Bill", "my name is Bill"),
    ("Tôi đến từ Michigan", "Tôi đến từ Michigan", "I come from Michigan"),
    ("Làm ơn", "Làm ơn", "please — the first key"),
    ("Cảm ơn", "Cảm ơn", "thank you — the second key"),
    ("Rất vui được gặp bạn", "Rất vui được gặp bạn", "pleased to meet you"),
], "Rất tốt! Very good — exactly right.", "Một lần nữa, chậm thôi — once more, slowly.")

# ---- wire the conventional audio paths ----
for cid, data in CLASSES.items():
    base = "audio/trainer/%s/" % cid
    data["audioBase"] = base
    data["welcomeAudio"] = base + "welcome.mp3"
    for i, st in enumerate(data["steps"]):
        st["audio"] = base + "step-%d.mp3" % i
        if data.get("slow_all"):
            st["slowAudio"] = base + "step-%d-slow.mp3" % i
    data["praiseAudio"] = [base + "praise-%d.mp3" % i for i in range(len(data["praise"]))]
    data["retryAudio"] = [base + "retry-%d.mp3" % i for i in range(len(data["retry"]))]

out = {
    "generated": "build-trainer-data.py — phrase sets for the listen-and-repeat trainer",
    "classes": CLASSES,
}
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "trainer-data.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("trainer-data.json:", len(CLASSES), "classes,",
      sum(len(c["steps"]) for c in CLASSES.values()), "steps")
