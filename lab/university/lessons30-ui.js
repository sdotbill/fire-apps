/* Exolex University — the 30-minute lesson room.
   Bill's law (Nov 16 2026, stated twice, corrected once): every class
   is a REAL class. The professor teaches a full lesson — about thirty
   minutes of audio in the professor's own voice, with the complete
   lesson text beside the player to read along with or re-read — and
   ONLY when the lesson is finished do the questions open: more than
   five of them, plain language, multiple choice wherever an honest
   choice set exists, easy to hard, every answer drawn from the lesson
   itself. There is no skipping the lesson to reach the questions.
   Re-reading the lesson while answering is allowed and encouraged —
   that is learning, not cheating.

   Data: lessons30/<classId>.json (built by build-lessons30/), one
   file per class: { lessons: [ { n, title, audio, minutes, words,
   paragraphs[], phrases[]?, questions[] } ] }. Questions carry the
   gate's step shape, so GateCore checks them and the grade lands in
   the same lab log (kinds lesson30-done / lesson30-step /
   lesson30-grade — kept distinct from the old gate's entries so the
   two builds never corrupt each other's records).

   This module is self-contained like gate-ui.js: it injects its own
   styles and box into the lesson panel, and index.html calls
   UniLessons30.enter / .leave / .start beside the Trainer and
   UniGate hooks. When a class has 30-minute lessons, this room takes
   precedence: the trainer box and the old gate box stay hidden. */
(function () {
  'use strict';
  var G = window.GateCore;
  var LT = window.LangTrainer;
  var storage = window.localStorage;
  var LOG_KEY = 'dave_lab_log';

  var CSS = [
    '#l30List .l30Row{display:block;width:100%;text-align:left;margin:8px 0;background:var(--panel);border:1px solid var(--gold);color:var(--ink);border-radius:6px;padding:11px 14px;font-family:inherit;font-size:1rem;cursor:pointer}',
    '#l30List .l30Row:hover{background:#fdf6dd}',
    '#l30List .l30Meta{font-size:.85rem;color:var(--ink-soft);margin-top:2px}',
    '#l30List .l30State{font-size:.85rem;font-weight:bold;color:#2e7d3b}',
    '#l30List .l30State.open{color:#8a6d1f}',
    '#l30Meta{font-size:.82rem;color:var(--ink-soft);letter-spacing:.04em;text-transform:uppercase;margin-bottom:6px}',
    '#l30Text{border:1px solid var(--gold);background:#fffdf4;border-radius:6px;padding:14px 18px;font-size:1.06rem;line-height:1.6;max-height:46vh;overflow:auto}',
    '#l30Text p{margin:0 0 12px}',
    '#l30Audio{width:100%;margin:10px 0 4px}',
    '#l30DoneBar{display:none;border:1px solid #46a35a;background:#f2f9f2;border-radius:6px;padding:10px 14px;margin:10px 0 0}',
    '#l30Phrases{margin:14px 0 0}',
    '.l30Phrase{border:1px solid var(--line);border-radius:6px;padding:10px 14px;margin:8px 0;background:#fff}',
    '.l30Phrase .l30Target{font-size:1.3rem;font-weight:bold;color:var(--gold-deep)}',
    '.l30Phrase .l30Meaning{color:var(--ink-soft);font-size:.95rem}',
    '.l30Phrase .l30Row2{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px;align-items:center}',
    '.l30Phrase input{flex:1;min-width:160px;padding:8px 10px;font-family:inherit;font-size:1rem;border:1px solid var(--gold);border-radius:4px}',
    '.l30Phrase .l30Heard{font-style:italic;color:var(--ink-soft);min-height:1.2em}',
    '.l30Phrase .l30Mark{font-size:1.5rem;color:#46a35a;font-weight:bold;display:none}',
    '#l30Dots{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0 4px}',
    '#l30Dots .dot{width:14px;height:14px;border-radius:50%;border:2px solid var(--gold);background:transparent;padding:0}',
    '#l30Dots .dot.cur{background:var(--gold-hi)}',
    '#l30Dots .dot.done{background:#46a35a;border-color:#46a35a}',
    '#l30Dots .dot.skipped{background:repeating-linear-gradient(45deg,#fff,#fff 2px,#cbbd8d 2px,#cbbd8d 4px)}',
    '#l30Teach{font-size:1.02rem;line-height:1.5;margin:8px 0 0}',
    '#l30Q{font-size:1.25rem;font-weight:bold;color:var(--gold-deep);margin:10px 0 6px;line-height:1.35}',
    '#l30Heard{min-height:1.3em;font-style:italic;color:var(--ink-soft);margin-top:6px}',
    '#l30Status{min-height:1.5em;font-size:1.02rem;margin:6px 0 10px}',
    '#l30Status.good{color:#2e7d3b;font-weight:bold}',
    '#l30Status.bad{color:#a33b2e}',
    '#l30Input{width:100%;min-height:56px;padding:10px 12px;font-family:inherit;font-size:1rem;border:1px solid var(--gold);border-radius:4px;background:#fff}',
    '#l30Btns{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}',
    '#l30Foot{display:flex;justify-content:space-between;align-items:baseline;margin-top:10px;gap:10px}',
    '#l30Progress{font-size:.85rem;color:var(--ink-soft)}',
    '#l30Skip{font-size:.8rem;color:var(--ink-soft);white-space:nowrap}',
    '#l30Grade{display:none;border:1px solid #46a35a;background:#f2f9f2;border-radius:6px;padding:12px 16px;margin-top:12px}',
    '#l30Hint{display:none;border:1px solid var(--gold);background:#fdf6dd;border-radius:6px;padding:10px 14px;margin:10px 0 0;font-size:.96rem;line-height:1.5}',
    '#l30Walk{display:none;border:1px solid #4a6b8a;background:#eef4fa;border-radius:6px;padding:10px 14px;margin:10px 0 0;font-size:.96rem;line-height:1.5}',
    '#l30Ref{display:none;border:1px solid var(--line);background:#fffdf4;border-radius:6px;padding:10px 14px;margin:10px 0 0;font-size:.98rem;line-height:1.55;max-height:340px;overflow:auto}',
    '#l30Ref p{margin:0 0 8px}',
    '#l30Choices{display:none;margin:10px 0 0}',
    '#l30Choices .l30Choice{display:block;width:100%;text-align:left;margin:6px 0;background:var(--panel);border:1px solid var(--gold);color:var(--ink);border-radius:6px;padding:9px 14px;font-family:inherit;font-size:.98rem;cursor:pointer}',
    '#l30Choices .l30Choice:hover:not(:disabled){background:var(--gold);color:#fff}',
    '#l30Choices .l30Choice:disabled{opacity:.45;cursor:default}',
    '#l30Check{font-size:2.2rem;color:#46a35a;font-weight:bold;display:none;line-height:1}',
    '.l30Sep{border:0;border-top:1px solid var(--line);margin:18px 0 10px}'
  ].join('\n');

  var HTML =
    '<h3 id="l30Title">The full lesson — first the class, then the questions</h3>' +
    '<p id="l30Intro">Your professor teaches this lesson in full — ' +
    'about thirty minutes, in their own voice, with the whole lesson ' +
    'written out beside the player so you can read along, or read it ' +
    'instead. <b>Finish the lesson first</b> — listen to the end, or ' +
    'read it through and say so — and only then do the questions ' +
    'open. Every question is drawn from the lesson you just had, ' +
    'nothing else, and the lesson text stays open beside them: going ' +
    'back to read is learning. Most questions offer <b>choices to ' +
    'pick from</b>; answering out loud or by typing is always there ' +
    'too. Miss, and your professor teaches that piece again a ' +
    'different way; miss twice, and they walk it through with you.</p>' +
    '<div id="l30List"></div>' +
    '<div id="l30Lesson" style="display:none">' +
      '<div id="l30Meta"></div>' +
      '<h3 id="l30LessonTitle" style="margin:4px 0 6px"></h3>' +
      '<audio id="l30Audio" controls preload="metadata"></audio>' +
      '<div id="l30Text" tabindex="0"></div>' +
      '<div id="l30Phrases"></div>' +
      '<div id="l30Btns">' +
        '<button class="act" id="l30ReadBtn" disabled>I\u2019ve read the whole lesson</button>' +
        '<button class="act" id="l30ToQuiz" disabled>Answer the questions \u2192</button>' +
        '<a href="#" id="l30BackList">\u2190 all lessons</a>' +
      '</div>' +
      '<div id="l30Status"></div>' +
      '<div id="l30DoneBar"></div>' +
    '</div>' +
    '<div id="l30Quiz" style="display:none">' +
      '<div id="l30Dots"></div>' +
      '<div id="l30Teach"></div>' +
      '<div id="l30Q"></div>' +
      '<div id="l30Choices"></div>' +
      '<textarea id="l30Input" placeholder="Your answer — say it, or type it here."></textarea>' +
      '<div id="l30Btns2" style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px">' +
        '<button class="act" id="l30Check2">Check my answer</button>' +
        '<button class="ghost" id="l30Mic">\uD83C\uDFA4 Answer out loud</button>' +
        '<button class="ghost" id="l30Help">I\u2019m stuck — help me</button>' +
        '<button class="ghost" id="l30RefBtn">\uD83D\uDCD6 The lesson</button>' +
        '<span id="l30Check"></span>' +
      '</div>' +
      '<div id="l30Heard"></div>' +
      '<div id="l30QStatus"></div>' +
      '<div id="l30Hint"></div>' +
      '<div id="l30Walk"></div>' +
      '<div id="l30Ref"></div>' +
      '<div id="l30Foot"><span id="l30Progress"></span>' +
      '<a href="#" id="l30Skip">skip for now \u2192</a></div>' +
      '<div id="l30Grade"></div>' +
      '<div style="margin-top:10px"><a href="#" id="l30BackList2">\u2190 all lessons</a></div>' +
    '</div>' +
    '<audio id="l30Clip" preload="auto" style="display:none"></audio>' +
    '<hr class="l30Sep">';

  var VQ = (window.UNI_BUILD && window.UNI_BUILD !== 'unstamped')
    ? '?v=' + encodeURIComponent(window.UNI_BUILD) : '';

  var box = null;
  function $(id) { return document.getElementById(id); }
  function ensureBox() {
    if (box) return box;
    var st = document.createElement('style');
    st.textContent = CSS;
    document.head.appendChild(st);
    box = document.createElement('div');
    box.id = 'lessons30Box';
    box.style.display = 'none';
    box.innerHTML = HTML;
    var panel = $('panel-lesson');
    var trainerBox = $('trainerBox');
    if (panel && trainerBox && trainerBox.nextSibling) {
      panel.insertBefore(box, trainerBox.nextSibling);
    } else if (panel) {
      panel.insertBefore(box, panel.firstChild);
    }
    wire();
    return box;
  }

  /* ---------------- lab log ---------------- */
  function loadLog() {
    try {
      var raw = storage.getItem(LOG_KEY);
      var log = raw ? JSON.parse(raw) : [];
      return Array.isArray(log) ? log : [];
    } catch (e) { return []; }
  }
  function append(entry) {
    try {
      var log = loadLog();
      log.push(entry);
      storage.setItem(LOG_KEY, JSON.stringify(log));
      return true;
    } catch (e) { return false; }
  }
  function today() { return new Date().toISOString().slice(0, 10); }
  function lessonDone(classId, n) {
    var found = false;
    loadLog().forEach(function (e) {
      if (e && e.kind === 'lesson30-done' && e.classId === classId &&
          e.lesson === n) found = true;
    });
    return found;
  }
  function stepStates(classId, n) {
    var out = {};
    loadLog().forEach(function (e) {
      if (e && e.kind === 'lesson30-step' && e.classId === classId &&
          e.lesson === n && typeof e.step === 'number') {
        if (e.status === 'pass') out[e.step] = 'pass';
        else if (e.status === 'skip' && out[e.step] !== 'pass') out[e.step] = 'skip';
      }
    });
    return out;
  }
  function recordStep(status, assisted) {
    append({
      date: today(), minutes: 0, stations: ['university'], stepsCompleted: 0,
      classId: cur.cls.id, classTitle: cur.cls.title,
      kind: 'lesson30-step', lesson: curLesson.n, step: qIdx,
      status: status, attempts: qAttempts,
      assisted: !!assisted
    });
  }
  function recordGrade(complete) {
    var st = stepStates(cur.cls.id, curLesson.n);
    var passed = 0, skipped = 0;
    Object.keys(st).forEach(function (k) {
      if (st[k] === 'pass') passed++;
      else if (st[k] === 'skip') skipped++;
    });
    var total = curLesson.questions.length;
    append({
      date: today(), minutes: 0, stations: ['university'],
      stepsCompleted: passed,
      classId: cur.cls.id, classTitle: cur.cls.title,
      kind: 'lesson30-grade', lesson: curLesson.n,
      passed: passed, skipped: skipped, total: total,
      attempts: qSessionAttempts,
      percent: total ? Math.round(100 * passed / total) : 0,
      complete: !!complete
    });
  }

  /* ---------------- state ---------------- */
  var DATA = {};          /* classId -> lessons30 class data */
  var FETCHING = {};
  var cur = null;         /* {section, cls, prof, data} */
  var curLesson = null;
  var phase = 'list';     /* list | lesson | quiz */
  var qIdx = 0, qAttempts = 0, qSessionAttempts = 0, qHelp = 0;
  var qStates = {}, qDirty = false, qGradeWritten = false;
  var rec = null, listening = false, heardFinal = null;
  var phraseRec = null, phraseListening = false;

  function profFirst() {
    var nm = String((cur && cur.prof && cur.prof.name) || '')
      .replace(/^(Professor|Profesora|Professore|Professora|Madame|Herr|Mevrouw)\s+/, '');
    return nm.split(/\s+/)[0] || 'your professor';
  }
  function setStatus(msg, kind) {
    var s = $('l30Status');
    if (s) { s.textContent = msg; s.className = kind || ''; s.id = 'l30Status'; }
  }
  function setQStatus(msg, kind) {
    var s = $('l30QStatus');
    if (s) {
      s.textContent = msg;
      s.style.color = kind === 'good' ? '#2e7d3b' : (kind === 'bad' ? '#a33b2e' : '');
      s.style.fontWeight = kind === 'good' ? 'bold' : '';
      s.style.minHeight = '1.5em'; s.style.fontSize = '1.02rem'; s.style.margin = '6px 0 10px';
    }
  }
  function playClip(src) {
    return new Promise(function (resolve) {
      if (!src) { resolve(); return; }
      var a = $('l30Clip');
      a.pause(); a.src = src;
      var done = function () {
        a.removeEventListener('ended', done);
        a.removeEventListener('error', done);
        resolve();
      };
      a.addEventListener('ended', done);
      a.addEventListener('error', done);
      var p = a.play();
      if (p && p.catch) p.catch(function () { resolve(); });
    });
  }

  /* ---------------- the lesson list ---------------- */
  function showList() {
    phase = 'list';
    curLesson = null;
    $('l30List').style.display = '';
    $('l30Lesson').style.display = 'none';
    $('l30Quiz').style.display = 'none';
    var host = $('l30List');
    host.innerHTML = '';
    cur.data.lessons.forEach(function (ls) {
      var done = lessonDone(cur.cls.id, ls.n);
      var st = stepStates(cur.cls.id, ls.n);
      var passed = 0, skipped = 0;
      Object.keys(st).forEach(function (k) {
        if (st[k] === 'pass') passed++;
        else if (st[k] === 'skip') skipped++;
      });
      var total = (ls.questions || []).length;
      var b = document.createElement('button');
      b.className = 'l30Row';
      var state;
      if (total && passed + skipped >= total) state = '<span class="l30State">\u2713 Complete — ' + passed + ' of ' + total + ' questions landed' + (skipped ? ', ' + skipped + ' skipped' : '') + '</span>';
      else if (done) state = '<span class="l30State open">Lesson finished — questions open (' + passed + ' of ' + total + ' landed)</span>';
      else state = '<span class="l30State open">Not started</span>';
      var dispTitle = String(ls.title || '').replace(/^Lesson\s+\d+\s*[—–-]\s*/, '');
      b.innerHTML = '<b>Lesson ' + ls.n + ' — ' + dispTitle + '</b>' +
        '<div class="l30Meta">About ' + Math.round(ls.minutes || 30) +
        ' minutes \u00B7 ' + total + ' questions after the lesson</div>' +
        '<div>' + state + '</div>';
      b.addEventListener('click', function () { openLesson(ls); });
      host.appendChild(b);
    });
  }

  /* ---------------- one lesson: listen / read ---------------- */
  function openLesson(ls) {
    curLesson = ls;
    phase = 'lesson';
    $('l30List').style.display = 'none';
    $('l30Quiz').style.display = 'none';
    $('l30Lesson').style.display = '';
    $('l30Meta').textContent = 'Lesson ' + ls.n + ' of ' +
      cur.data.lessons.length + ' \u00B7 about ' + Math.round(ls.minutes || 30) +
      ' minutes \u00B7 ' + (ls.words || 0).toLocaleString() + ' words';
    $('l30LessonTitle').textContent =
      String(ls.title || '').replace(/^Lesson\s+\d+\s*[—–-]\s*/, '');
    var au = $('l30Audio');
    au.pause();
    if (ls.audio) { au.src = ls.audio; au.style.display = ''; }
    else au.style.display = 'none';
    var tx = $('l30Text');
    tx.innerHTML = '';
    (ls.paragraphs || []).forEach(function (p) {
      var el = document.createElement('p');
      el.textContent = p;
      tx.appendChild(el);
    });
    tx.scrollTop = 0;
    renderPhrases(ls);
    refreshLessonGate();
    setStatus('', '');
    tx.onscroll = function () {
      if (tx.scrollTop + tx.clientHeight >= tx.scrollHeight - 48) {
        var rb = $('l30ReadBtn');
        if (rb && !lessonDone(cur.cls.id, curLesson.n)) rb.disabled = false;
      }
    };
  }

  function refreshLessonGate() {
    if (!curLesson) return;
    var done = lessonDone(cur.cls.id, curLesson.n);
    $('l30ToQuiz').disabled = !done;
    $('l30ReadBtn').disabled = true;
    var bar = $('l30DoneBar');
    if (done) {
      bar.style.display = '';
      bar.innerHTML = '<b>Lesson finished \u2713</b> — the questions are ' +
        'open. The lesson text stays right here, and it stays open ' +
        'beside the questions too.';
    } else {
      bar.style.display = 'none';
    }
  }

  function finishLesson(via) {
    if (!curLesson || lessonDone(cur.cls.id, curLesson.n)) return;
    append({
      date: today(), minutes: Math.round(curLesson.minutes || 0),
      stations: ['university'], stepsCompleted: 0,
      classId: cur.cls.id, classTitle: cur.cls.title,
      kind: 'lesson30-done', lesson: curLesson.n, via: via
    });
    refreshLessonGate();
    setStatus('That is the lesson, whole. When you are ready, the ' +
      'questions are below — every one of them comes from what ' +
      profFirst() + ' just taught.', 'good');
  }

  /* -------- speak-along practice (language lessons) -------- */
  function renderPhrases(ls) {
    var host = $('l30Phrases');
    host.innerHTML = '';
    if (!ls.phrases || !ls.phrases.length || !LT) return;
    var head = document.createElement('h4');
    head.textContent = 'Say it with ' + profFirst() + ' — the speaking practice';
    head.style.margin = '6px 0 2px';
    host.appendChild(head);
    var note = document.createElement('p');
    note.style.color = 'var(--ink-soft)';
    note.textContent = 'Hear her say it, then say it yourself — out ' +
      'loud, or typed. Nothing moves on until it lands.';
    host.appendChild(note);
    var mastered = LT.loadMastered(storage, cur.cls.id);
    ls.phrases.forEach(function (ph) {
      var row = document.createElement('div');
      row.className = 'l30Phrase';
      var mark = document.createElement('span');
      mark.className = 'l30Mark';
      mark.textContent = ' \u2713';
      if (mastered[ph.target]) mark.style.display = 'inline';
      var t = document.createElement('span');
      t.className = 'l30Target';
      t.textContent = ph.display || ph.target;
      var m = document.createElement('div');
      m.className = 'l30Meaning';
      m.textContent = ph.meaning || '';
      var heard = document.createElement('div');
      heard.className = 'l30Heard';
      var r2 = document.createElement('div');
      r2.className = 'l30Row2';
      var bHear = document.createElement('button');
      bHear.className = 'ghost';
      bHear.textContent = '\uD83D\uDD0A Hear her say it';
      bHear.addEventListener('click', function () { playClip(ph.audio); });
      var bSlow = document.createElement('button');
      bSlow.className = 'ghost';
      bSlow.textContent = 'Slowly';
      bSlow.addEventListener('click', function () { playClip(ph.slowAudio || ph.audio); });
      var bMic = document.createElement('button');
      bMic.className = 'act';
      bMic.textContent = '\uD83C\uDFA4 Your turn — say it';
      var inp = document.createElement('input');
      inp.type = 'text';
      inp.placeholder = '…or type it here';
      var bType = document.createElement('button');
      bType.className = 'ghost';
      bType.textContent = 'Check what I typed';
      var pass = function (viaTyped) {
        mark.style.display = 'inline';
        heard.textContent = 'That\u2019s it. \u2713';
        LT.recordMastery(storage, {
          date: today(), classId: cur.cls.id, classTitle: cur.cls.title,
          phrase: ph.target, selfChecked: false, typed: !!viaTyped
        });
      };
      var grade = function (text) {
        var g = LT.gradeAttempt(ph.target, text, ph.variants);
        if (g.pass) pass(false);
        else heard.textContent = 'It heard: \u201C' + text + '\u201D — not ' +
          'yet. Hear her once more, then say it like you mean it.';
      };
      bMic.addEventListener('click', function () {
        phraseListen(ph, heard, grade);
      });
      bType.addEventListener('click', function () {
        var v = inp.value.trim();
        if (!v) { heard.textContent = 'Type it first — then check it.'; return; }
        var g = LT.gradeAttempt(ph.target, v, ph.variants);
        if (g.pass) pass(true);
        else heard.textContent = 'Not yet — compare it letter by letter ' +
          'with the line above, and try once more.';
      });
      r2.appendChild(bHear);
      if (ph.slowAudio) r2.appendChild(bSlow);
      r2.appendChild(bMic);
      r2.appendChild(inp);
      r2.appendChild(bType);
      var top = document.createElement('div');
      top.appendChild(t);
      top.appendChild(mark);
      row.appendChild(top);
      row.appendChild(m);
      row.appendChild(r2);
      row.appendChild(heard);
      host.appendChild(row);
    });
  }

  function phraseListen(ph, heardEl, gradeFn) {
    if (phraseListening) return;
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
      heardEl.textContent = 'This browser can\u2019t listen — type it ' +
        'instead; it counts exactly the same.';
      return;
    }
    phraseRec = new SR();
    phraseRec.lang = (cur.data && cur.data.lang) || 'es-ES';
    phraseRec.interimResults = true;
    phraseRec.maxAlternatives = 3;
    var final = null;
    phraseRec.onresult = function (ev) {
      var interim = '';
      for (var i = ev.resultIndex; i < ev.results.length; i++) {
        var r = ev.results[i];
        if (r.isFinal) {
          for (var j = 0; j < r.length; j++) {
            var g = LT.gradeAttempt(ph.target, r[j].transcript, ph.variants);
            if (g.pass) { final = r[j].transcript; break; }
          }
          if (!final) final = r[0].transcript;
        } else interim += r[0].transcript;
      }
      if (interim) heardEl.textContent = '\u2026 ' + interim;
    };
    phraseRec.onerror = function (ev) {
      phraseListening = false;
      if (ev.error === 'not-allowed' || ev.error === 'service-not-allowed') {
        heardEl.textContent = 'The microphone is off for this page — ' +
          'typing counts exactly the same.';
      } else if (ev.error !== 'aborted') {
        heardEl.textContent = 'It heard nothing that time — try once more, or type it.';
      }
    };
    phraseRec.onend = function () {
      phraseListening = false;
      if (final) { var f = final; final = null; gradeFn(f); }
    };
    try {
      phraseRec.start();
      phraseListening = true;
      heardEl.textContent = profFirst() + ' is listening — say it now.';
    } catch (e) { phraseListening = false; }
  }

  /* ---------------- the questions ---------------- */
  function openQuiz() {
    if (!curLesson || !lessonDone(cur.cls.id, curLesson.n)) return;
    phase = 'quiz';
    qStates = stepStates(cur.cls.id, curLesson.n);
    qDirty = false; qGradeWritten = false; qSessionAttempts = 0;
    qIdx = 0;
    while (qIdx < curLesson.questions.length && qStates[qIdx]) qIdx++;
    if (qIdx >= curLesson.questions.length) qIdx = 0;
    $('l30Lesson').style.display = 'none';
    $('l30List').style.display = 'none';
    $('l30Quiz').style.display = '';
    $('l30Grade').style.display = 'none';
    showQuestion();
  }

  function qStep() { return curLesson.questions[qIdx]; }

  function renderDots() {
    var host = $('l30Dots');
    host.innerHTML = '';
    curLesson.questions.forEach(function (q, i) {
      var d = document.createElement('span');
      d.className = 'dot' + (i === qIdx ? ' cur' : '') +
        (qStates[i] === 'pass' ? ' done' : '') +
        (qStates[i] === 'skip' ? ' skipped' : '');
      host.appendChild(d);
    });
    var passed = 0;
    Object.keys(qStates).forEach(function (k) { if (qStates[k] === 'pass') passed++; });
    $('l30Progress').textContent = 'Question ' + (qIdx + 1) + ' of ' +
      curLesson.questions.length + ' \u00B7 ' + passed + ' landed';
  }

  function showQuestion() {
    var st = qStep();
    if (!st) { finishQuiz(); return; }
    qAttempts = 0; qHelp = 0;
    renderDots();
    $('l30Teach').textContent = st.teach || '';
    $('l30Q').textContent = st.q || '';
    $('l30Input').value = '';
    $('l30Heard').textContent = '';
    $('l30Check').style.display = 'none';
    setQStatus('', '');
    $('l30Hint').style.display = 'none';
    $('l30Walk').style.display = 'none';
    $('l30Ref').style.display = 'none';
    renderChoices(false);
  }

  function correctText(st) {
    if (st.kind === 'number') return st.mcAnswer != null ? String(st.mcAnswer) : String(st.disp || st.answer);
    if (st.kind === 'keywords') return null;
    return st.mcAnswer != null ? String(st.mcAnswer) : String(st.answer || '');
  }

  function renderChoices(viaHelp) {
    var host = $('l30Choices');
    host.innerHTML = '';
    var st = qStep();
    if (!st || !st.choices || st.choices.length < 2) {
      host.style.display = 'none';
      return;
    }
    var correct = correctText(st);
    var head = document.createElement('p');
    head.style.margin = '0 0 4px';
    head.innerHTML = viaHelp
      ? '<b>Pick the one the lesson supports.</b> Every choice here is ' +
        'real material from this lesson — only one answers this ' +
        'question. Landing it after help is recorded as an assisted pass.'
      : '<b>Pick your answer</b> — or answer out loud, or type it ' +
        'below, instead. Every choice here is real material from this ' +
        'lesson, and picking the right one counts in full.';
    host.appendChild(head);
    /* stable shuffle so the correct choice is not always first */
    var opts = st.choices.slice();
    for (var i = opts.length - 1; i > 0; i--) {
      var j = (qIdx * 7 + i * 3) % (i + 1);
      var tmp = opts[i]; opts[i] = opts[j]; opts[j] = tmp;
    }
    opts.forEach(function (t) {
      var btn = document.createElement('button');
      btn.className = 'l30Choice';
      btn.textContent = t;
      btn.addEventListener('click', function () {
        if (correct != null && String(t) === correct) onPass(qHelp > 0);
        else { btn.disabled = true; onMiss('choice'); }
      });
      host.appendChild(btn);
    });
    host.style.display = '';
  }

  function onPass(assisted) {
    qStates[qIdx] = 'pass';
    qDirty = true;
    recordStep('pass', assisted);
    $('l30Check').style.display = 'inline';
    setQStatus(assisted
      ? 'Landed — with help, and the record says so. That still counts.'
      : 'That\u2019s it. \u2713', 'good');
    renderDots();
    setTimeout(function () {
      qIdx++;
      while (qIdx < curLesson.questions.length && qStates[qIdx] === 'pass') qIdx++;
      if (qIdx >= curLesson.questions.length) finishQuiz();
      else showQuestion();
    }, 1100);
  }

  function onMiss(how) {
    qAttempts++;
    qSessionAttempts++;
    var st = qStep();
    if (how !== 'choice') {
      var heard = $('l30Input').value.trim();
      if (heard) $('l30Heard').textContent = 'It heard / you wrote: \u201C' + heard + '\u201D';
    }
    if (qAttempts >= 2 && st.walk) {
      var w = $('l30Walk');
      w.innerHTML = '<b>Walk it through with ' + profFirst() + ':</b> ' +
        st.walk.replace(/</g, '&lt;');
      w.style.display = '';
      setQStatus('Not yet — walk it through below, then say it yourself.', 'bad');
    } else {
      setQStatus('Not yet. Here is that piece of the lesson again, ' +
        'taught another way:', 'bad');
    }
    if (st.teach2) {
      var h = $('l30Hint');
      h.textContent = st.teach2;
      h.style.display = '';
    }
  }

  function check(text) {
    var st = qStep();
    if (!st || qStates[qIdx] === 'pass') return;
    var res = G.checkAnswer(st, text);
    if (res.pass) onPass(qHelp > 0);
    else onMiss('text');
  }

  function finishQuiz() {
    recordGrade(true);
    qGradeWritten = true;
    var st = stepStates(cur.cls.id, curLesson.n);
    var passed = 0, skipped = 0, total = curLesson.questions.length;
    Object.keys(st).forEach(function (k) {
      if (st[k] === 'pass') passed++;
      else if (st[k] === 'skip') skipped++;
    });
    var g = $('l30Grade');
    g.style.display = '';
    g.innerHTML = '<b>Lesson ' + curLesson.n + ' — the questions are ' +
      'done.</b><br>' + passed + ' of ' + total + ' landed' +
      (skipped ? ', ' + skipped + ' skipped (counted as skips, never as passes)' : '') +
      '. The grade is in your University record. The lesson above ' +
      'stays open — re-read it any time.';
    setQStatus('', '');
    renderDots();
  }

  /* ---------------- quiz speech ---------------- */
  function startListening() {
    if (listening) return;
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
      setQStatus('This browser can\u2019t listen — Chrome and Edge can. ' +
        'Typing counts exactly the same.', '');
      $('l30Mic').style.display = 'none';
      return;
    }
    rec = new SR();
    rec.lang = (cur.data && cur.data.lang) || 'en-US';
    rec.interimResults = true;
    rec.maxAlternatives = 1;
    heardFinal = null;
    rec.onresult = function (ev) {
      var interim = '';
      for (var i = ev.resultIndex; i < ev.results.length; i++) {
        var r = ev.results[i];
        if (r.isFinal) heardFinal = r[0].transcript;
        else interim += r[0].transcript;
      }
      if (interim) $('l30Heard').textContent = '\u2026 ' + interim;
    };
    rec.onerror = function (ev) {
      listening = false;
      if (ev.error === 'not-allowed' || ev.error === 'service-not-allowed') {
        setQStatus('The microphone is off for this page — typing counts exactly the same.', '');
        $('l30Mic').style.display = 'none';
      } else if (ev.error === 'no-speech') {
        setQStatus('I didn\u2019t hear anything — tap the mic and say it like you mean it.', '');
      } else if (ev.error !== 'aborted') {
        setQStatus('The listening hiccupped (' + ev.error + ') — type it, or try the mic again.', '');
      }
    };
    rec.onend = function () {
      listening = false;
      if (heardFinal) {
        var hf = heardFinal; heardFinal = null;
        $('l30Input').value = hf;
        check(hf);
      }
    };
    try {
      rec.start();
      listening = true;
      setQStatus(profFirst() + ' is listening — answer now.', '');
    } catch (e) { listening = false; }
  }

  /* ---------------- wiring ---------------- */
  function wire() {
    $('l30Audio').addEventListener('ended', function () { finishLesson('audio'); });
    $('l30Audio').addEventListener('error', function () {
      if (curLesson && !lessonDone(cur.cls.id, curLesson.n)) {
        setStatus('The recording would not play here — read the lesson ' +
          'text through instead; the read-through opens the questions ' +
          'just the same.', '');
      }
    });
    $('l30ReadBtn').addEventListener('click', function () { finishLesson('read'); });
    $('l30ToQuiz').addEventListener('click', openQuiz);
    $('l30BackList').addEventListener('click', function (e) { e.preventDefault(); backToList(); });
    $('l30BackList2').addEventListener('click', function (e) { e.preventDefault(); backToList(); });
    $('l30Check2').addEventListener('click', function () {
      var v = $('l30Input').value.trim();
      if (v) check(v);
      else setQStatus('Say it out loud, pick a choice, or type your answer first.', '');
    });
    $('l30Mic').addEventListener('click', startListening);
    $('l30Help').addEventListener('click', function () {
      var st = qStep();
      if (!st) return;
      qHelp = 1;
      if (st.teach2) {
        var h = $('l30Hint');
        h.textContent = st.teach2;
        h.style.display = '';
      }
      renderChoices(true);
      setQStatus('Help is up — the passage is above, and the choices ' +
        'are this lesson\u2019s own material. Landing it now is ' +
        'recorded as an assisted pass.', '');
    });
    $('l30RefBtn').addEventListener('click', function () {
      var r = $('l30Ref');
      if (r.style.display !== 'none') { r.style.display = 'none'; return; }
      r.innerHTML = '';
      (curLesson.paragraphs || []).forEach(function (p) {
        var el = document.createElement('p');
        el.textContent = p;
        r.appendChild(el);
      });
      r.style.display = '';
    });
    $('l30Skip').addEventListener('click', function (e) {
      e.preventDefault();
      if (qStates[qIdx] === 'pass') return;
      qStates[qIdx] = 'skip';
      qDirty = true;
      recordStep('skip', false);
      qIdx++;
      if (qIdx >= curLesson.questions.length) finishQuiz();
      else showQuestion();
    });
  }

  function backToList() {
    if (phase === 'quiz' && qDirty && !qGradeWritten) recordGrade(false);
    var au = $('l30Audio');
    if (au) au.pause();
    showList();
  }

  /* ---------------- enter / leave / start ---------------- */
  function fetchClass(cid, cb) {
    if (DATA[cid]) { cb(DATA[cid]); return; }
    if (FETCHING[cid]) { FETCHING[cid].push(cb); return; }
    FETCHING[cid] = [cb];
    fetch('lessons30/' + encodeURIComponent(cid) + '.json' + VQ)
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) {
        var cbs = FETCHING[cid] || [];
        delete FETCHING[cid];
        if (j && j.lessons && j.lessons.length) DATA[cid] = j;
        cbs.forEach(function (f) { f(DATA[cid] || null); });
      })
      .catch(function () {
        var cbs = FETCHING[cid] || [];
        delete FETCHING[cid];
        cbs.forEach(function (f) { f(null); });
      });
  }

  function enter(section, cls, prof) {
    fetchClass(cls.id, function (data) {
      if (!data) return;           /* not a 30-minute class (yet) */
      ensureBox();
      cur = { section: section, cls: cls, prof: prof, data: data };
      /* this room takes precedence over the trainer and the old gate */
      var tb = $('trainerBox'); if (tb) tb.style.display = 'none';
      var gb = $('gateBox'); if (gb) gb.style.display = 'none';
      var bp = $('btnPlay'); if (bp) bp.style.display = 'none';
      var la = $('lessonAudio'); if (la) { la.pause(); la.style.display = 'none'; }
      var li = $('lessonIntro');
      if (li) li.textContent = 'This class now teaches the full ' +
        'way: a complete lesson of about thirty minutes with ' +
        profFirst() + ', then the questions. It is all in the lesson ' +
        'panel below.';
      box.style.display = '';
      showList();
    });
  }

  function leave() {
    if (phase === 'quiz' && qDirty && !qGradeWritten && cur && curLesson) {
      recordGrade(false);
    }
    if (rec) { try { rec.abort(); } catch (e) {} rec = null; }
    if (phraseRec) { try { phraseRec.abort(); } catch (e) {} phraseRec = null; }
    listening = false; phraseListening = false;
    if (box) {
      var au = $('l30Audio');
      if (au) au.pause();
      box.style.display = 'none';
    }
    cur = null; curLesson = null; phase = 'list';
  }

  function start() {
    if (!box || box.style.display === 'none' || !cur) return false;
    box.scrollIntoView({ block: 'start', behavior: 'smooth' });
    if (phase === 'list') {
      var first = null;
      cur.data.lessons.forEach(function (ls) {
        if (first) return;
        var st = stepStates(cur.cls.id, ls.n);
        var passed = 0;
        Object.keys(st).forEach(function (k) { if (st[k] === 'pass') passed++; });
        if (!lessonDone(cur.cls.id, ls.n) || passed < (ls.questions || []).length) first = ls;
      });
      if (first) openLesson(first);
    }
    return true;
  }

  window.UniLessons30 = { enter: enter, leave: leave, start: start };
})();
