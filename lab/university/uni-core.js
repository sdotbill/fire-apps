/* Exolex University — shared logic core (stage A).
   Pure data + functions, no DOM. The University page loads this file,
   and the headless verifier runs the identical code in Node: the board
   segmenter, the board-lesson builder for classes without a recorded
   lesson, the prepared-answer set, and the classroom session log —
   which writes into the SAME localStorage log the Lab room uses
   ('dave_lab_log'), in the same entry shape, extended with classId /
   classTitle. The room's summarizeLog ignores the extra fields, so
   totals keep reading correctly there and on the dashboard Lab desk. */
(function (global) {
  'use strict';

  var LOG_KEY = 'dave_lab_log';

  /* ---------- board segments ---------- */
  function boardSegments(text) {
    var clean = String(text || '').replace(/\s+/g, ' ').trim();
    if (!clean) return [];
    var sentences = clean.match(/[^.!?]+[.!?]+["']?|\S[^.!?]*$/g) || [clean];
    var segs = [], buf = '';
    sentences.forEach(function (s) {
      s = s.trim();
      if (!s) return;
      if (buf && (buf.length + s.length > 190 || /^(First|Next|And then),/.test(s))) {
        segs.push(buf); buf = s;
      } else {
        buf = buf ? buf + ' ' + s : s;
      }
    });
    if (buf) segs.push(buf);
    return segs;
  }

  /* ---------- a board lesson for classes without a recorded one ----------
     Built from the class's real syllabus data only: titles and the
     index's own result lines. Nothing is paraphrased into existence —
     a paper without an abstracted result is presented as exactly that. */
  function buildBoardLesson(cls, section, prof) {
    var parts = [];
    parts.push(prof.greeting + ' I am ' + prof.name + ', and this is ' +
      cls.title + ' — a class in ' + section.name + ' at Exolex University.');
    if (cls.units) {
      parts.push('The syllabus, in order: ' + cls.units.join(' · ') + '.');
    } else {
      parts.push('The syllabus is real: ' + cls.count + ' papers from the ' +
        'Aldred corpus, every one deposited and citable, and in this room ' +
        'we read them for what they actually claim.');
      var walk = cls.papers.slice(0, 3);
      var lead = ['First, ', 'Next, ', 'And then, '];
      walk.forEach(function (p, i) {
        if (p.r) {
          parts.push(lead[i] + p.t + '. Its stated result: ' + p.r);
        } else {
          parts.push(lead[i] + p.t + '. Its result is read from the ' +
            'deposit itself — the index carries the title and the DOI, ' +
            'and the paper carries the numbers.');
        }
      });
    }
    parts.push('That is the shape of this class. Your homework is waiting ' +
      'on your desk.');
    return parts.join(' ');
  }

  /* ---------- prepared answers ----------
     Stage A honesty rule: these are prepared answers, written from the
     class's real data, and the page labels them as prepared. Live
     questions need a worker route that can carry a professor persona;
     until then, an unmatched question gets the plain truth, below. */
  var LIVE_NOTE = 'That one needs live office hours, which arrive with ' +
    'the University\u2019s next stage — tonight I answer the questions on ' +
    'the cards, and I answer them properly.';

  function preparedAnswers(cls, section, prof) {
    /* A class may carry its own authored answer set (cls.qa) — written
       in its professor's own voice. Bill's Spanish classroom does. */
    if (cls.qa && cls.qa.length) return cls.qa;
    var about, syllabus;
    if (cls.units) {
      about = cls.title + ' is a founding-curriculum class in ' +
        section.name + ', taught by ' + prof.name + '. It runs ' +
        cls.units.length + ' units, in order, and every session in this ' +
        'room is logged to your University record.';
      syllabus = 'The units, in order: ' + cls.units.join(' · ') + '.';
    } else {
      about = cls.title + ' is a class in ' + section.name + ', taught ' +
        'by ' + prof.name + '. Its syllabus is ' + cls.count +
        ' real papers from the Aldred corpus — deposited, citable, and ' +
        'read in this room for what they actually claim.';
      syllabus = 'The first papers on the syllabus: ' +
        cls.papers.slice(0, 5).map(function (p) { return p.t; }).join(' · ') +
        (cls.count > 5 ? ' · — and ' + (cls.count - 5) + ' more, all on the syllabus card.' : '.');
    }
    return [
      { q: 'What is this class about?', a: about },
      { q: 'What is on the syllabus?', a: syllabus },
      { q: 'Who are you, Professor?', a: 'I am ' + prof.name + '. ' + prof.personality },
      { q: 'What is the homework?', a: cls.homework.q },
      { q: 'How do my hours count?', a: 'Time in this classroom is real ' +
        'University time. The clock runs only while you are here with the ' +
        'room in front of you, and when you leave, the session — the date, ' +
        'the minutes, and this class\u2019s name — is written to your Lab ' +
        'log, the same ledger the Laboratory keeps. Credit follows work ' +
        'that can be shown.' }
    ];
  }

  function matchAnswer(question, cls, section, prof) {
    var q = String(question || '').toLowerCase();
    if (!q) return null;
    var set = preparedAnswers(cls, section, prof);
    function pick(i) { return set[i].a; }
    if (/syllabus|reading|papers|units|books/.test(q)) return pick(1);
    if (/homework|assignment|problem|exercise/.test(q)) return pick(3);
    if (/who are you|your name|about you|professor/.test(q)) return pick(2);
    if (/hour|credit|log|record|count/.test(q)) return pick(4);
    if (/about|what is this|subject|topic/.test(q)) return pick(0);
    return null;
  }

  /* ---------- the classroom session log (same ledger as the Lab) ------- */
  function loadLog(storage) {
    try {
      var raw = storage.getItem(LOG_KEY);
      if (!raw) return [];
      var parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
      return [];
    }
  }

  function makeClassEntry(opts) {
    return {
      date: opts.date,
      minutes: Math.round((opts.minutes || 0) * 10) / 10,
      stations: ['university'],
      stepsCompleted: 0,
      classId: opts.classId,
      classTitle: opts.classTitle
    };
  }

  function appendEntry(storage, entry) {
    var log = loadLog(storage);
    log.push(entry);
    storage.setItem(LOG_KEY, JSON.stringify(log));
    return log;
  }

  function formatMinutes(mins) {
    var m = Math.round(mins || 0);
    if (m < 60) return m + ' min';
    var h = Math.floor(m / 60), rem = m % 60;
    return h + ' h ' + (rem < 10 ? '0' : '') + rem + ' min';
  }

  function summarizeLog(log) {
    var total = 0;
    (log || []).forEach(function (e) { total += e.minutes || 0; });
    return { sessions: (log || []).length,
             totalMinutes: Math.round(total * 10) / 10 };
  }

  var api = {
    LOG_KEY: LOG_KEY,
    LIVE_NOTE: LIVE_NOTE,
    boardSegments: boardSegments,
    buildBoardLesson: buildBoardLesson,
    preparedAnswers: preparedAnswers,
    matchAnswer: matchAnswer,
    loadLog: loadLog,
    makeClassEntry: makeClassEntry,
    appendEntry: appendEntry,
    formatMinutes: formatMinutes,
    summarizeLog: summarizeLog
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.UniCore = api;
})(typeof window !== 'undefined' ? window : globalThis);
