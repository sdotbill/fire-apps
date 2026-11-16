/* Exolex University — language trainer core (Rosetta-style listen & repeat).
   Pure logic, no DOM: speech normalization, the pronunciation gate, and
   mastery bookkeeping against the SAME lab log the classrooms already
   write ('dave_lab_log'). The University page loads this file; the
   headless test runs the identical code in Node.

   The gate (Bill's spec, Nov 16 2026): the professor models a phrase,
   the student says it back, the recognizer's transcript is checked
   against the target, and the lesson does NOT advance on a miss.
   Accent-tolerant: diacritics are folded (á→a, ñ→n is NOT folded —
   ñ is a different letter in Spanish and the fold below only strips
   combining marks after NFD, which turns ñ into n + tilde... so ñ IS
   folded to n. That is deliberate: a recognizer that hears "ano" for
   "año" has still heard the phrase; the gate judges the phrase, not
   the orthography.) */
(function (global) {
  'use strict';

  /* ---------- normalization ---------- */
  function normalizeSpeech(s) {
    var t = String(s == null ? '' : s).toLowerCase();
    try { t = t.normalize('NFD').replace(/[̀-ͯ]/g, ''); } catch (e) {}
    t = t.replace(/[^\p{L}\p{N}\s]/gu, ' ');
    return t.replace(/\s+/g, ' ').trim();
  }

  /* ---------- edit distance / similarity ---------- */
  function levenshtein(a, b) {
    if (a === b) return 0;
    if (!a.length) return b.length;
    if (!b.length) return a.length;
    var prev = [], cur = [], i, j;
    for (j = 0; j <= b.length; j++) prev[j] = j;
    for (i = 1; i <= a.length; i++) {
      cur[0] = i;
      for (j = 1; j <= b.length; j++) {
        cur[j] = Math.min(
          prev[j] + 1,
          cur[j - 1] + 1,
          prev[j - 1] + (a.charAt(i - 1) === b.charAt(j - 1) ? 0 : 1)
        );
      }
      var tmp = prev; prev = cur; cur = tmp;
    }
    return prev[b.length];
  }

  function similarity(a, b) {
    if (!a && !b) return 1;
    if (!a || !b) return 0;
    var d = levenshtein(a, b);
    return 1 - d / Math.max(a.length, b.length);
  }

  /* ---------- the gate ----------
     gradeAttempt(target, heard) -> {pass, score, why}
     Pass rules, in order:
       1. exact normalized match;
       2. the heard text contains the whole target (recognizers add
          filler around a correct phrase);
       3. whole-string similarity >= 0.85;
       4. multi-word targets: every target word heard (each at >= 0.8
          similarity to some heard word), allowing ONE missing word on
          targets of 4+ words.
     Short single words (<= 4 normalized chars) pass only on rule 1/2 —
     "hola" vs "ola" is a real miss the student should retry. */
  function gradeAttempt(target, heard) {
    var t = normalizeSpeech(target);
    var h = normalizeSpeech(heard);
    if (!t) return { pass: false, score: 0, why: 'no-target' };
    if (!h) return { pass: false, score: 0, why: 'nothing-heard' };
    if (h === t) return { pass: true, score: 1, why: 'exact' };
    if ((' ' + h + ' ').indexOf(' ' + t + ' ') !== -1)
      return { pass: true, score: 0.97, why: 'contained' };
    var sim = similarity(t, h);
    var tWords = t.split(' '), hWords = h.split(' ');
    if (tWords.length === 1 && t.length <= 4)
      return { pass: false, score: sim, why: 'short-word' };
    if (sim >= 0.85) return { pass: true, score: sim, why: 'similar' };
    if (tWords.length >= 2) {
      var missing = 0;
      for (var i = 0; i < tWords.length; i++) {
        var best = 0;
        for (var j = 0; j < hWords.length; j++)
          best = Math.max(best, similarity(tWords[i], hWords[j]));
        if (best < 0.8) missing++;
      }
      var allowed = tWords.length >= 4 ? 1 : 0;
      if (missing <= allowed)
        return { pass: true, score: Math.max(sim, 0.86), why: 'word-match' };
    }
    return { pass: false, score: sim, why: 'miss' };
  }

  /* ---------- mastery, in the existing lab log ----------
     One entry per mastered phrase, minutes: 0 — the log's minute
     totals (the student's hours) are untouched; the entry carries the
     phrase so the record shows WHAT was mastered, in which class. */
  var LOG_KEY = 'dave_lab_log';

  function masteryEntry(opts) {
    return {
      date: opts.date,
      minutes: 0,
      stations: ['university'],
      stepsCompleted: 1,
      classId: opts.classId,
      classTitle: opts.classTitle,
      kind: 'phrase-mastery',
      phrase: opts.phrase,
      selfChecked: !!opts.selfChecked
    };
  }

  function loadMastered(storage, classId) {
    var out = {};
    try {
      var raw = storage.getItem(LOG_KEY);
      var log = raw ? JSON.parse(raw) : [];
      if (!Array.isArray(log)) return out;
      log.forEach(function (e) {
        if (e && e.kind === 'phrase-mastery' && e.classId === classId && e.phrase)
          out[e.phrase] = true;
      });
    } catch (e) {}
    return out;
  }

  function recordMastery(storage, opts) {
    try {
      var raw = storage.getItem(LOG_KEY);
      var log = raw ? JSON.parse(raw) : [];
      if (!Array.isArray(log)) log = [];
      log.push(masteryEntry(opts));
      storage.setItem(LOG_KEY, JSON.stringify(log));
      return true;
    } catch (e) { return false; }
  }

  var api = {
    LOG_KEY: LOG_KEY,
    normalizeSpeech: normalizeSpeech,
    levenshtein: levenshtein,
    similarity: similarity,
    gradeAttempt: gradeAttempt,
    masteryEntry: masteryEntry,
    loadMastered: loadMastered,
    recordMastery: recordMastery
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.LangTrainer = api;
})(typeof window !== 'undefined' ? window : globalThis);
