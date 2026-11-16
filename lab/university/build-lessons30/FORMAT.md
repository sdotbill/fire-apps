# The 30-minute lesson format — writer spec

Every lesson is a REAL class: the professor teaches for about thirty
minutes, in their own voice, and the student listens (or reads the full
text, which sits beside the player). Only when the lesson is finished do
the questions unlock. These files are the source of truth; the pipeline
(assemble.py → audit → synth.py) turns them into the live class.

## The script file

Path: `scripts/<classId>/lesson-NN.txt` (NN = 01, 02, …)

- Line 1: `# <lesson title>` — the syllabus lesson/unit title.
- Then the lesson itself: plain spoken prose, one paragraph per block,
  paragraphs separated by a blank line. No markdown, no bullet lists,
  no brackets, no stage directions — every character is spoken aloud.
- Length: 4,200–4,800 words (about 25,000–28,000 characters). That is
  ~30 minutes of speech. Teach honestly: if the material is genuinely
  thinner, a shorter lesson ships at its honest length — never pad.
- Structure, in order:
  1. Welcome: the professor greets the student, names the lesson, and
     says plainly what it teaches and why it is worth knowing.
  2. The material, in syllabus order. Every idea is explained in plain
     language, then anchored with a concrete example from the student's
     real life or the class's own material. New terms are defined the
     first time they appear. The teacher checks understanding as she
     goes ("so if X, then Y — hold onto that").
  3. Where the class has something to *do* (a phrase to say, a problem
     shape to recognise), a short guided try-it moment inside the
     teaching — the doing is taught, not tested, here.
  4. A recap: the lesson's key points, said once more, in order.
  5. Close: the professor tells the student what comes next — the
     questions on this lesson — and reminds them the full text stays
     open beside the questions; going back to read is learning, not
     cheating.
- Voice: the professor's own personality from the catalogue, warm and
  human. First person. Contractions. No lecture-hall stiffness, no
  hype, no shorthand, no internal vocabulary of any kind.
- Speakable text: write numbers and symbols the way they should be
  heard ("twenty-five", "x squared" spelled as words where needed).
  Avoid characters the TTS chokes on (ø, ʿ, ʾ). Spanish accents
  (á, é, í, ó, ú, ñ, ¿, ¡) are fine in Carmen's lessons.

## Spanish lessons (Carmen Vega) — extra rules

- Teach the way Lesson 1 already does: Spanish first, English support
  right beside it ("Buenas tardes — good afternoon"). The student is a
  beginner; every Spanish phrase is translated the first time it is
  used in each lesson.
- The speak-along phrases are part of the teaching, woven into the
  script ("Say it with me: …"), AND listed again at the end of the
  file after a line containing exactly `=== PHRASES ===`, one per line:
  `Target phrase | English meaning` — 6 to 10 phrases per lesson.
  These become the listen-and-repeat practice inside the lesson.
- The Spanish-for-Jillian strand runs through Lessons 3, 6, 9 and 12
  (and Lesson 1 seeded it): keep it sweet, tasteful, and aimed at the
  wedding — March 25, 2027, Key West.
- Carmen's voice is locked: Determined Mast, speed 88. Writers do not
  choose voices; the pipeline reads them from the catalogue.

## The questions file

Path: `questions/<classId>/lesson-NN.json` — a JSON array of 10–12
question objects (never fewer than 8 surviving the audit):

```json
{
  "q": "A full, plain-language question sentence?",
  "kind": "exact | keywords | number",
  "answer": "the answer (string for exact, number for number)",
  "accept": ["other honest forms of the same answer"],
  "keywords": [["group", "words"], ["second", "group"]],
  "need": 2,
  "choices": ["correct choice", "distractor", "distractor", "distractor"],
  "mcAnswer": "the correct choice, exactly as it appears in choices",
  "teach": "One line of context: From the lesson: …",
  "teach2": "The exact passage from the lesson that teaches this, quoted, plus one sentence explaining it a different way.",
  "walk": "Walk it through step by step: (1) … (2) … (3) … so the answer is …",
  "rank": 1
}
```

Rules (the audit enforces them mechanically; failures are dropped and
reported, never shipped):

- CONTAINMENT: the answer must be in the lesson script — for `exact`,
  the answer or an accept form appears in the text; for `number`, the
  value appears among the lesson's numbers; for `keywords`, every
  keyword group has a word in the text. The correct MC choice must
  appear in the lesson text too.
- DISTRACTORS: real material from the SAME lesson (other phrases,
  other values, other concepts the lesson taught) — plausible, but
  wrong for this question. Never invented facts, never jokes.
- PLAIN LANGUAGE: full sentences a normal person understands. No
  shorthand, no syllabus-speak ("which unit comes next" is banned
  forever), no question whose answer is a title or a DOI.
- ORDER: rank 1 = recall of a headline fact, rank 2 = understanding,
  rank 3 = applying/combining. The set runs easy to hard.
- `teach2` must quote the lesson: include a verbatim run of at least
  60 characters from the script.
- Spanish questions: ask about what the lesson taught — meanings of
  phrases, which phrase fits a moment, what Carmen explained. Choices
  are phrases/meanings from the lesson. Questions are asked in English
  (the student is a beginner); the answers are the Spanish taught.
