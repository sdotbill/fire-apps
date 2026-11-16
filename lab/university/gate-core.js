/* Exolex University — the general classroom gate core.
   Pure logic, no DOM: the answer checker and the grade bookkeeping
   for EVERY non-language class, built to the same pattern as the
   language trainer (trainer-core.js). Bill's law (Nov 16 2026): every
   class lets the student talk or type an answer back, the answer is
   checked against the class's own material, and the lesson does NOT
   advance on a miss — the professor re-teaches the piece another way
   and the student tries again. Assessment happens in-session, while
   the student is there; the grade is written to the same lab log the
   classrooms already use ('dave_lab_log').

   Check kinds:
     number   — a value the class material itself reports; parsed out
                of whatever the student typed or said, compared with a
                relative tolerance.
     exact    — a short factual string (a DOI, a name); normalized
                equality or containment, plus an accept list.
     title    — a unit title from the class's own syllabus, matched by
                content words (the student need not reproduce the
                punctuation, only the substance).
     keywords — a conceptual answer (the class's own set problem);
                keyword GROUPS drawn from the worked answer in the
                material; a pass needs `need` of the groups present. */
(function (global) {
  'use strict';

  /* ---------- normalization ---------- */
  function normalizeText(s) {
    var t = String(s == null ? '' : s).toLowerCase();
    try { t = t.normalize('NFD').replace(/[̀-ͯ]/g, ''); } catch (e) {}
    t = t.replace(/[^\p{L}\p{N}.\s]/gu, ' ');
    return t.replace(/\s+/g, ' ').trim();
  }

  var SUPERSCRIPTS = { '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4',
    '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁻': '-' };

  /* Parse the first number out of free text. Handles 1.227e13,
     1.227 × 10^13, 1.227 x 10^13, 1.227*10¹³, 12,270,000,000,000,
     plain decimals and integers. Returns null when there is none. */
  function parseNumber(s) {
    if (s == null) return null;
    var t = String(s).replace(/10([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)/g, function (_, run) {
      return '10^' + run.split('').map(function (ch) {
        return SUPERSCRIPTS[ch] !== undefined ? SUPERSCRIPTS[ch] : ch;
      }).join('');
    }).replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]/g, function (ch) {
      return SUPERSCRIPTS[ch] !== undefined ? SUPERSCRIPTS[ch] : ch;
    });
    t = t.replace(/,/g, '');
    var m = t.match(/(-?\d+(?:\.\d+)?)\s*(?:×|x|\*)\s*10\s*\^\s*(-?\d+)/);
    if (m) return parseFloat(m[1]) * Math.pow(10, parseInt(m[2], 10));
    m = t.match(/-?\d+(?:\.\d+)?(?:\s*[eE]\s*[+-]?\d+)?/);
    if (!m) return null;
    var v = parseFloat(m[0].replace(/\s+/g, ''));
    return isNaN(v) ? null : v;
  }

  /* ---------- the checker ---------- */
  function checkNumber(step, answer) {
    var want = typeof step.answer === 'number' ? step.answer : parseNumber(step.answer);
    var got = parseNumber(answer);
    if (want === null || want === undefined || isNaN(want))
      return { pass: false, score: 0, why: 'no-key' };
    if (got === null) return { pass: false, score: 0, why: 'no-number-heard' };
    var tol = step.tol || 0.03;
    var ok;
    if (want === 0) ok = (got === 0);
    else ok = Math.abs(got - want) / Math.abs(want) <= tol;
    var score = ok ? 1 : Math.max(0, 1 - Math.abs(got - want) / Math.abs(want || 1));
    return { pass: ok, score: score, why: ok ? 'number' : 'number-off', got: got, want: want };
  }

  function checkExact(step, answer) {
    var a = normalizeText(answer);
    if (!a) return { pass: false, score: 0, why: 'empty' };
    var targets = [step.answer].concat(step.accept || []);
    for (var i = 0; i < targets.length; i++) {
      var t = normalizeText(targets[i]);
      if (!t) continue;
      if (a === t) return { pass: true, score: 1, why: 'exact' };
      /* containment either way, but a one-word target must match whole */
      if (t.indexOf(' ') !== -1 && (' ' + a + ' ').indexOf(' ' + t + ' ') !== -1)
        return { pass: true, score: 0.97, why: 'contained' };
      if (a.indexOf(' ') !== -1 && (' ' + t + ' ').indexOf(' ' + a + ' ') !== -1 &&
          a.replace(/ /g, '').length >= 4)
        return { pass: true, score: 0.95, why: 'contained-rev' };
    }
    return { pass: false, score: 0, why: 'miss' };
  }

  var STOP = { the: 1, and: 1, a: 1, an: 1, of: 1, to: 1, in: 1, on: 1,
    for: 1, with: 1, is: 1, are: 1, its: 1, it: 1, by: 1, at: 1, from: 1,
    or: 1, as: 1, how: 1, why: 1, what: 1, when: 1, your: 1, you: 1 };

  function contentWords(s) {
    return normalizeText(s).split(' ').filter(function (w) {
      return w.length >= 3 && !STOP[w];
    });
  }

  function checkTitle(step, answer) {
    var want = contentWords(step.answer);
    var got = contentWords(answer);
    if (!want.length || !got.length) return { pass: false, score: 0, why: 'empty' };
    var gotSet = {};
    got.forEach(function (w) { gotSet[w] = 1; });
    var hit = 0;
    want.forEach(function (w) { if (gotSet[w]) hit++; });
    var need = Math.max(1, Math.ceil(want.length * 0.75));
    var precision = hit / got.length;
    var ok = hit >= need && precision >= 0.45;
    return { pass: ok, score: hit / want.length, why: ok ? 'title' : 'title-miss',
             hit: hit, need: need };
  }

  function checkKeywords(step, answer) {
    var a = ' ' + normalizeText(answer) + ' ';
    var groups = step.keywords || [];
    if (!groups.length) return { pass: false, score: 0, why: 'no-key' };
    var hit = 0;
    groups.forEach(function (g) {
      var found = g.some(function (syn) {
        return a.indexOf(' ' + normalizeText(syn) + ' ') !== -1 ||
               a.indexOf(normalizeText(syn)) !== -1;
      });
      if (found) hit++;
    });
    var need = step.need || Math.max(1, Math.ceil(groups.length / 2));
    var ok = hit >= need;
    return { pass: ok, score: hit / groups.length, why: ok ? 'keywords' : 'keywords-miss',
             hit: hit, need: need };
  }

  function checkAnswer(step, answer) {
    if (!step) return { pass: false, score: 0, why: 'no-step' };
    switch (step.kind) {
      case 'number': return checkNumber(step, answer);
      case 'exact': return checkExact(step, answer);
      case 'title': return checkTitle(step, answer);
      case 'keywords': return checkKeywords(step, answer);
      default: return { pass: false, score: 0, why: 'bad-kind' };
    }
  }

  /* ---------- grade bookkeeping, in the existing lab log ----------
     Per-step records (kind 'gate-step', minutes 0 — the student's
     hours are untouched, exactly as the trainer's mastery entries)
     and one grade entry per gate session (kind 'class-grade').
     Skips are recorded as skips, never as passes. */
  var LOG_KEY = 'dave_lab_log';

  function loadLog(storage) {
    try {
      var raw = storage.getItem(LOG_KEY);
      var log = raw ? JSON.parse(raw) : [];
      return Array.isArray(log) ? log : [];
    } catch (e) { return []; }
  }

  function append(storage, entry) {
    try {
      var log = loadLog(storage);
      log.push(entry);
      storage.setItem(LOG_KEY, JSON.stringify(log));
      return true;
    } catch (e) { return false; }
  }

  function recordStep(storage, opts) {
    return append(storage, {
      date: opts.date, minutes: 0, stations: ['university'], stepsCompleted: 0,
      classId: opts.classId, classTitle: opts.classTitle,
      kind: 'gate-step', step: opts.step, status: opts.status,
      attempts: opts.attempts || 0
    });
  }

  /* step states for one class: {index: 'pass'|'skip'} — a pass always
     outranks a skip recorded earlier for the same step. */
  function loadStepStates(storage, classId) {
    var out = {};
    loadLog(storage).forEach(function (e) {
      if (e && e.kind === 'gate-step' && e.classId === classId &&
          typeof e.step === 'number') {
        if (e.status === 'pass') out[e.step] = 'pass';
        else if (e.status === 'skip' && out[e.step] !== 'pass') out[e.step] = 'skip';
      }
    });
    return out;
  }

  function gradeFor(states, total) {
    var passed = 0, skipped = 0;
    Object.keys(states).forEach(function (k) {
      if (states[k] === 'pass') passed++;
      else if (states[k] === 'skip') skipped++;
    });
    return {
      passed: passed, skipped: skipped, total: total,
      resolved: passed + skipped,
      percent: total ? Math.round(100 * passed / total) : 0
    };
  }

  function recordGrade(storage, opts) {
    var g = gradeFor(opts.states, opts.total);
    return append(storage, {
      date: opts.date, minutes: 0, stations: ['university'], stepsCompleted: g.passed,
      classId: opts.classId, classTitle: opts.classTitle,
      kind: 'class-grade',
      passed: g.passed, skipped: g.skipped, total: g.total,
      attempts: opts.attempts || 0,
      percent: g.percent, complete: !!opts.complete
    });
  }

  var api = {
    LOG_KEY: LOG_KEY,
    normalizeText: normalizeText,
    parseNumber: parseNumber,
    contentWords: contentWords,
    checkAnswer: checkAnswer,
    recordStep: recordStep,
    loadStepStates: loadStepStates,
    gradeFor: gradeFor,
    recordGrade: recordGrade
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.GateCore = api;
})(typeof window !== 'undefined' ? window : globalThis);
