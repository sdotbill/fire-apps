# The general classroom gate — build report (Nov 16, 2026)

Bill's order: every Exolex University class works like the language
rooms — the student talks/types an answer back, it is checked against
the class's own material, and the lesson does not go forward until it
lands. Built as a sibling of the listen-and-repeat trainer, reusing
its pattern throughout (step dots, the big green check on the board,
the green voice bar, per-step records in `dave_lab_log`, the quiet
skip). The seam: language classes are NOT in gate-data.json — the
trainer is their gate; every other class is the gate's.

## What was built

- `gate-core.js` — the checker (number with tolerance, exact,
  unit-title by content words, conceptual by keyword groups) and the
  grade bookkeeping. Unit tests: `test-gate.js`, **35/35 pass**.
- `build-gate-data.py` → `gate-data.json` — the generator. Steps come
  only from material the catalogue itself carries: headline values a
  paper's own result line reports; the syllabus's own unit order; and
  every class's own set homework problem as the capstone, keyed by
  keyword groups from the worked answer the catalogue already holds.
  A step whose answer cannot be grounded in the material is not
  generated.
- `gate-ui.js` — the classroom module (self-contained; injects its
  box into the lesson panel). Voice answers via SpeechRecognition
  (en-US) with the green voice bar; typing always available. A miss
  re-teaches the piece a different way and holds the step; a pass
  lands the green check and the professor's praise; skips are
  recorded as skips. The session grade (kind `class-grade`: passed /
  skipped / total / percent / complete) is written to `dave_lab_log`
  on completion or on leaving with progress.
- `index.html` — five wiring lines only (two script tags, the
  `UniGate.enter` hook beside `Trainer.enter`, the `UniGate.leave`
  hook beside `Trainer.leave`). Left uncommitted with the trainer
  build's own uncommitted work, for one joint commit.
- `build-gate-audio.py` — per-step professor voice for the classes
  that already carry a recorded lesson: **275 clips generated, 0
  failed** (teach per step + praise + retry, each in the class
  professor's own roster voice).

## Coverage (of 760 classes)

- **20 language classes** — the listen-and-repeat trainer.
- **740 classes gated here, 3,284 steps** (1,728 unit-order, 740
  capstones, 639 paper-value, 177 DOI/exact).
- **563 full** (3+ substantive steps) · **177 partial** (1–2
  substantive steps) · **0 with none**. Per-class detail:
  `GATE-COVERAGE.md`. The partial classes are the paper classes whose
  results are stated in prose — no `NAME = VALUE` list exists in
  their material to grade against, and no key was invented for them;
  they carry their DOI step and their capstone.

## Hand-checked set

All 38 recorded-lesson classes were reviewed step by step. Generator
fixes from that review: prose-fragment pair names rejected ("…at
epsilon = 0.1" is not a quantity), duplicate values within a class
collapsed to one check, machine-named quantities preferred, capstone
keyword groups noise-filtered with the pass threshold capped at 3.
Nine classes carry hand-written overrides in `gate-overrides.json`:
six College flagships whose lessons state their results in prose
(galactic lensing, Einstein–Cartan torsion tests, globular clusters,
matter & energy, ultracold matter, earth/sky/life) each gained a
number step quoted from the lesson's own stated result; the two
French classes and Music Theory got capstone keys a correct answer
actually contains (the auto-extracted ones were accent-fold fragments
and hyphen-strings).

## Verification

`verify-gate.cjs` — **all 24 browser checks passed**, driving three
real classrooms in headless Chrome:

1. **College flagship** (Cosmology — The Bounce & the Aldred Limit):
   DOI right → advance + green check; value wrong (0.9) → step held,
   re-teach shown, no check; retry right (0.45) → advance; capstone
   skipped → grade panel "2 of 3 steps landed, 1 skipped"; log holds
   gate-step records pass/pass/skip (the missed step with 2 attempts)
   and a complete `class-grade` at 67%, minutes 0 (hours untouched);
   dot states persist across a reload.
2. **Authored** (Numbers & Proof): typed unit title passes, advances,
   and is recorded.
3. **Generated** (Snow Avalanches): typed value passes; the spoken
   value (stubbed recognizer) is heard, shown back, checked, and
   advances, with the green voice bar visible while listening.

Regression: the sibling trainer's own suite still passes untouched —
`test-trainer.js` 28/28 and `verify-trainer.cjs` all browser checks.

Screenshots: `gate-shot-1-flagship.png`, `gate-shot-2-greencheck.png`,
`gate-shot-3-generated.png`.

## Honest remainders

- Per-step professor voice ships for the 32 classes with recorded
  lessons. The other classes present on the board with the
  professor's written praise/re-teaching in the same flow; extending
  the voice catalogue-wide is a generation pass through
  `build-gate-audio.py` (idempotent; paths are written into
  gate-data.json only where the voice is real today).
- Capstone grading is keyword-based by design (the brief's method for
  conceptual answers): thresholds are deliberately fair (at most 3 of
  the groups), the re-teach shows the worked answer's opening move,
  and the recorded skip is the safety valve — a skip is never
  dressed up as a pass.
