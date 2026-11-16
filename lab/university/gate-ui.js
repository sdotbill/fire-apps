/* Exolex University — the general classroom gate (UI).
   Bill's law (Nov 16 2026), generalised from the language trainer to
   EVERY class: the professor presents a piece of the lesson, poses
   the check from that same material, the student answers OUT LOUD or
   by typing, the answer is checked (gate-core.js), and the lesson
   does NOT advance on a miss — the professor re-teaches the piece a
   different way and the student tries again. A pass lands the big
   green check on the board, exactly as in the language rooms. The
   session's grade — steps passed, skips counted as skips, never as
   passes — is written to the lab log when the set is finished or the
   student leaves. One small, quiet "skip for now" exists so a checker
   quirk can never trap anyone.

   This file is self-contained: it injects its own styles and its own
   box into the lesson panel, and index.html calls UniGate.enter /
   UniGate.leave beside the Trainer's hooks. Language classes are not
   in gate-data.json — the listen-and-repeat trainer is their gate. */
(function () {
  'use strict';
  var G = window.GateCore;
  var storage = window.localStorage;

  var CSS = [
    '#gtDots{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0 4px}',
    '#gtDots .dot{width:14px;height:14px;border-radius:50%;border:2px solid var(--gold);background:transparent;cursor:pointer;padding:0}',
    '#gtDots .dot.cur{background:var(--gold-hi)}',
    '#gtDots .dot.done{background:#46a35a;border-color:#46a35a}',
    '#gtDots .dot.skipped{background:repeating-linear-gradient(45deg,#fff,#fff 2px,#cbbd8d 2px,#cbbd8d 4px)}',
    '#gtTeach{font-size:1.02rem;line-height:1.5;margin:8px 0 0}',
    '#gtWhy{color:var(--ink-soft);font-size:.9rem;margin:4px 0 6px}',
    '#gtQ{font-size:1.25rem;font-weight:bold;color:var(--gold-deep);margin:10px 0 6px;line-height:1.35}',
    '#gtWave{width:100%;height:56px;background:#26332a;border-radius:6px;display:none}',
    '#gtHeard{min-height:1.3em;font-style:italic;color:var(--ink-soft);margin-top:6px}',
    '#gtStatus{min-height:1.5em;font-size:1.02rem;margin:6px 0 10px}',
    '#gtStatus.good{color:#2e7d3b;font-weight:bold}',
    '#gtStatus.bad{color:#a33b2e}',
    '#gtInput{width:100%;min-height:56px;padding:10px 12px;font-family:inherit;font-size:1rem;border:1px solid var(--gold);border-radius:4px;background:#fff}',
    '#gtBtns{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}',
    '#gtFoot{display:flex;justify-content:space-between;align-items:baseline;margin-top:10px;gap:10px}',
    '#gtProgress{font-size:.85rem;color:var(--ink-soft)}',
    '#gtSkip{font-size:.8rem;color:var(--ink-soft);white-space:nowrap}',
    '#gtGrade{border:1px solid #46a35a;background:#f2f9f2;border-radius:6px;padding:12px 16px;margin-top:12px}',
    '#gtHint{display:none;border:1px solid var(--gold);background:#fdf6dd;border-radius:6px;padding:10px 14px;margin:10px 0 0;font-size:.96rem}',
    '#gtWalk{display:none;border:1px solid #4a6b8a;background:#eef4fa;border-radius:6px;padding:10px 14px;margin:10px 0 0;font-size:.96rem;line-height:1.5}',
    '#gtWalk b{color:#33536e}',
    '#gtLesson{border:1px solid var(--gold);background:#fffdf4;border-radius:6px;padding:12px 16px;margin:10px 0 0}',
    '#gtLessonMeta{font-size:.82rem;color:var(--ink-soft);letter-spacing:.04em;text-transform:uppercase;margin-bottom:6px}',
    '#gtLessonText{font-size:1.05rem;line-height:1.55}',
    '#gtLessonBtns{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;align-items:baseline}',
    '#gtToQuestions{font-size:.82rem;color:var(--ink-soft)}',
    '#gtRef{display:none;border:1px solid var(--line);background:#fffdf4;border-radius:6px;padding:10px 14px;margin:10px 0 0;font-size:.95rem;line-height:1.5;max-height:320px;overflow:auto}',
    '#gtRef p{margin:0 0 8px}',
    '#gtChoices{display:none;margin:10px 0 0}',
    '#gtChoices .gtChoice{display:block;width:100%;text-align:left;margin:6px 0;background:var(--panel);border:1px solid var(--gold);color:var(--ink);border-radius:6px;padding:9px 14px;font-family:inherit;font-size:.98rem;cursor:pointer}',
    '#gtChoices .gtChoice:hover:not(:disabled){background:var(--gold);color:#fff}',
    '#gtChoices .gtChoice:disabled{opacity:.45;cursor:default}',
    '.gtSep{border:0;border-top:1px solid var(--line);margin:18px 0 10px}'
  ].join('\n');

  var HTML =
    '<h3 id="gtTitle">First the lesson — then the questions</h3>' +
    '<p>First, your professor <b>teaches the lesson</b> — the ' +
    'class\u2019s real material, presented in order, the whole of it. ' +
    'Then come the <b>questions</b>: every one drawn from what was ' +
    'just taught, and nothing else — nobody is expected to just know ' +
    'an answer that was not taught. <b>Say your answer out loud or ' +
    'type it.</b> It is checked against the lesson, and the class ' +
    '<b>does not move on</b> until it lands: miss, and your professor ' +
    'shows you the exact passage again, taught a different way. Your ' +
    'grade is recorded in your University record — passes, and skips ' +
    'counted as skips. Miss the same question twice and your ' +
    'professor <b>walks it through</b> — the reasoning, step by ' +
    'step, until the answer follows — then it is still yours to say. ' +
    'Most questions also offer <b>choices to pick from</b> — every ' +
    'choice built from this class\u2019s own lesson. Picking is a ' +
    'normal way to answer and counts in full; answering out loud ' +
    'or by typing is always there instead. (The class\u2019s set ' +
    'problem is the one exception: that one you work in your own ' +
    'words.) Stuck is still allowed: <b>I\u2019m stuck — help me</b> ' +
    'gives a hint drawn from the material itself — and a question ' +
    'landed after taking the hint counts too, with your record ' +
    'saying so, as an assisted pass.</p>' +
    '<div id="gtLesson" style="display:none">' +
      '<div id="gtLessonMeta"></div>' +
      '<div id="gtLessonText"></div>' +
      '<div id="gtLessonBtns">' +
        '<button class="act" id="gtBeginLesson">Begin — your professor teaches</button>' +
        '<button class="act" id="gtContinue" style="display:none">Continue \u2192</button>' +
        '<button class="ghost" id="gtHearLesson" style="display:none">\uD83D\uDD0A Hear this part</button>' +
        '<a href="#" id="gtToQuestions" style="display:none">skip the lesson — straight to the questions \u2192</a>' +
      '</div>' +
    '</div>' +
    '<div id="gtRef"></div>' +
    '<div id="gtDots"></div>' +
    '<div id="gtTeach"></div>' +
    '<div id="gtWhy"></div>' +
    '<div id="gtQ"></div>' +
    '<canvas id="gtWave" width="640" height="56"></canvas>' +
    '<div id="gtHeard"></div>' +
    '<textarea id="gtInput" style="display:none" placeholder="Your answer — say it, or type it here."></textarea>' +
    '<div id="gtBtns">' +
      '<button class="act" id="gtBegin">Begin — work through it</button>' +
      '<button class="act" id="gtCheck" style="display:none">Check my answer</button>' +
      '<button class="ghost" id="gtMic" style="display:none">\uD83C\uDFA4 Answer out loud</button>' +
      '<button class="ghost" id="gtHear" style="display:none">\uD83D\uDD0A Hear that again</button>' +
      '<button class="ghost" id="gtHelp" style="display:none">I\u2019m stuck — help me</button>' +
      '<button class="ghost" id="gtRefBtn" style="display:none">\uD83D\uDCD6 The lesson</button>' +
    '</div>' +
    '<div id="gtStatus"></div>' +
    '<div id="gtHint"></div>' +
    '<div id="gtWalk"></div>' +
    '<div id="gtChoices"></div>' +
    '<div id="gtFoot"><span id="gtProgress"></span>' +
    '<a href="#" id="gtSkip" style="display:none">skip for now \u2192</a></div>' +
    '<div id="gtGrade" style="display:none"></div>' +
    '<audio id="gtAudio" preload="auto" style="display:none"></audio>' +
    '<hr class="gtSep">';

  var GATE_DATA = null, pendingEnter = null;
  /* the build stamp (index.html's x-uni-build) versions every data
     fetch, so a new build is never served from an old cache entry */
  var VQ = (window.UNI_BUILD && window.UNI_BUILD !== 'unstamped')
    ? '?v=' + encodeURIComponent(window.UNI_BUILD) : '';
  fetch('gate-data.json' + VQ).then(function (r) { return r.ok ? r.json() : null; })
    .then(function (j) {
      if (j && j.classes) GATE_DATA = j.classes;
      if (GATE_DATA && pendingEnter) {
        var p = pendingEnter; pendingEnter = null;
        enter(p.section, p.cls, p.prof);
      }
    })
    .catch(function () { /* no gate data: classrooms stay as they were */ });

  var box = null;
  function $(id) { return document.getElementById(id); }
  function ensureBox() {
    if (box) return box;
    var st = document.createElement('style');
    st.textContent = CSS;
    document.head.appendChild(st);
    box = document.createElement('div');
    box.id = 'gateBox';
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

  /* ---------------- state ---------------- */
  var data = null, gCls = null, gProf = null;
  var phase = 'questions';   /* 'lesson' first, then 'questions' */
  var lessonIdx = 0, lessonStarted = false;
  var idx = 0, attempts = 0, sessionAttempts = 0, praiseCount = 0;
  var helpLevel = 0;   /* per step: 0 none · 1 hint shown · 2 choices shown */
  var walkIdx = -1;    /* the step the walkthrough is shown for (-1: none) */
  var states = {}, started = false, busy = false, dirty = false, gradeWritten = false;
  var stream = null, actx = null, analyser = null, waveRAF = null;
  var rec = null, listening = false, heardFinal = null;

  function step() { return data.steps[idx]; }
  function profFirst() {
    var nm = String((gProf && gProf.name) || '').replace(/^(Professor|Profesora|Professore|Professora|Madame|Herr|Mevrouw)\s+/, '');
    return nm.split(/\s+/)[0] || 'your professor';
  }
  function setStatus(msg, kind) {
    var s = $('gtStatus');
    s.textContent = msg;
    s.className = kind || '';
    s.id = 'gtStatus';
  }
  function showBoardCheck() { var b = $('trBoardCheck'); if (b) b.classList.add('on'); }
  function hideBoardCheck() { var b = $('trBoardCheck'); if (b) b.classList.remove('on'); }

  function playClip(src) {
    return new Promise(function (resolve) {
      if (!src) { resolve(); return; }
      var a = $('gtAudio');
      a.pause();
      a.src = src;
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

  /* ---------------- the green bar (the student's voice) ---------------- */
  function startWave() {
    if (!analyser) return;
    var cv = $('gtWave'), ctx = cv.getContext('2d');
    var arr = new Uint8Array(analyser.frequencyBinCount);
    cancelAnimationFrame(waveRAF);
    (function draw() {
      waveRAF = requestAnimationFrame(draw);
      analyser.getByteFrequencyData(arr);
      ctx.fillStyle = '#26332a'; ctx.fillRect(0, 0, cv.width, cv.height);
      var bars = 48, bw = cv.width / bars;
      for (var i = 0; i < bars; i++) {
        var v = arr[Math.floor(i * arr.length / (bars * 2))] / 255;
        var h = Math.max(3, v * (cv.height - 8));
        ctx.fillStyle = '#57d977';
        ctx.fillRect(i * bw + 1, (cv.height - h) / 2, bw - 2, h);
      }
    })();
  }
  function idleWave() {
    cancelAnimationFrame(waveRAF);
    var cv = $('gtWave');
    if (!cv) return;
    var ctx = cv.getContext('2d');
    ctx.fillStyle = '#26332a'; ctx.fillRect(0, 0, cv.width, cv.height);
    ctx.fillStyle = 'rgba(87,217,119,.45)';
    ctx.fillRect(0, cv.height / 2 - 1, cv.width, 2);
  }
  function getMic() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia)
      return Promise.reject(new Error('no-mic-api'));
    return navigator.mediaDevices.getUserMedia({ audio: true }).then(function (s) {
      stream = s;
      var AC = window.AudioContext || window.webkitAudioContext;
      if (AC) {
        actx = new AC();
        analyser = actx.createAnalyser();
        analyser.fftSize = 2048;
        actx.createMediaStreamSource(s).connect(analyser);
      }
    });
  }

  /* ---------------- dots + progress ---------------- */
  function renderDots() {
    var host = $('gtDots');
    host.innerHTML = '';
    data.steps.forEach(function (st, i) {
      var d = document.createElement('button');
      d.className = 'dot' +
        (states[i] === 'pass' ? ' done' : states[i] === 'skip' ? ' skipped' : '') +
        (i === idx ? ' cur' : '');
      d.title = 'Step ' + (i + 1);
      d.setAttribute('aria-label', 'Step ' + (i + 1) + ' of ' + data.steps.length);
      d.addEventListener('click', function () { if (started && !busy) showStep(i); });
      host.appendChild(d);
    });
  }
  function renderProgress() {
    var g = G.gradeFor(states, data.steps.length);
    $('gtProgress').textContent = 'Question ' + (idx + 1) + ' of ' + data.steps.length +
      ' · ' + g.passed + ' landed' +
      (g.skipped ? ' · ' + g.skipped + (g.skipped === 1 ? ' skip' : ' skips') : '') +
      (attempts ? ' · ' + attempts + (attempts === 1 ? ' try' : ' tries') + ' on this one' : '');
  }

  /* ---------------- the lesson phase ----------------
     Bill's model: the class is TAUGHT first — the lesson passages
     presented in order, read or heard — and only then do the
     questions begin. A student with recorded progress in the class
     enters at the questions (the lesson stays one tap away, in the
     reference panel); a first-time student gets the lesson, with a
     quiet skip door for anyone who has already read it elsewhere. */
  var QIDS = ['gtDots', 'gtTeach', 'gtWhy', 'gtQ', 'gtWave', 'gtHeard',
    'gtInput', 'gtBtns', 'gtStatus', 'gtHint', 'gtWalk', 'gtChoices',
    'gtFoot', 'gtGrade'];
  function setQuestionChrome(show) {
    QIDS.forEach(function (id) {
      var el = $(id);
      if (el) el.style.display = show ? '' : 'none';
    });
    if (!show) { var r = $('gtRef'); if (r) r.style.display = 'none'; }
  }
  function hasLesson() { return !!(data && data.lesson && data.lesson.length); }
  function showLessonChunk() {
    var chunks = data.lesson;
    var ch = chunks[lessonIdx];
    $('gtLessonMeta').textContent = 'The lesson — part ' + (lessonIdx + 1) +
      ' of ' + chunks.length;
    $('gtLessonText').textContent = ch.teach;
    $('gtBeginLesson').style.display = lessonStarted ? 'none' : '';
    $('gtContinue').style.display = lessonStarted ? '' : 'none';
    $('gtContinue').textContent = lessonIdx + 1 < chunks.length
      ? 'Continue \u2192' : 'Begin the questions \u2192';
    $('gtHearLesson').style.display = (lessonStarted && ch.audio) ? '' : 'none';
    $('gtToQuestions').style.display = '';
  }
  function playLessonChunk() {
    if (!hasLesson()) return Promise.resolve();
    return playClip(data.lesson[lessonIdx].audio);
  }
  function beginLesson() {
    if (lessonStarted) return;
    lessonStarted = true;
    showLessonChunk();
    playLessonChunk();
  }
  function continueLesson() {
    if (!lessonStarted) { beginLesson(); return; }
    if (lessonIdx + 1 < data.lesson.length) {
      lessonIdx++;
      showLessonChunk();
      playLessonChunk();
    } else if (data.steps.length) {
      toQuestions();
    } else {
      /* a lesson-only class (none in the current build, but the
         data format allows it): the lesson is the whole sitting */
      $('gtLessonMeta').textContent = 'The lesson — complete';
      $('gtContinue').style.display = 'none';
      $('gtHearLesson').style.display = 'none';
      $('gtToQuestions').style.display = 'none';
    }
  }
  function toQuestions() {
    if (!data.steps.length) return;
    phase = 'questions';
    $('gtLesson').style.display = 'none';
    setQuestionChrome(true);
    /* restore the pre-Begin pattern of the question controls */
    $('gtInput').style.display = 'none';
    $('gtGrade').style.display = 'none';
    $('gtHint').style.display = 'none';
    $('gtWalk').style.display = 'none';
    $('gtChoices').style.display = 'none';
    $('gtWave').style.display = 'none';
    ['gtCheck', 'gtMic', 'gtHear', 'gtSkip', 'gtHelp', 'gtRefBtn']
      .forEach(function (id) { $(id).style.display = 'none'; });
    $('gtBegin').style.display = '';
    $('gtBegin').textContent = 'Begin — ' + profFirst() + ' asks the questions';
    showStep(idx);
  }
  function toggleRef() {
    var r = $('gtRef');
    if (r.style.display !== 'none') { r.style.display = 'none'; return; }
    r.innerHTML = '';
    var h = document.createElement('p');
    var hb = document.createElement('b');
    hb.textContent = 'The lesson, for reference — everything the questions draw on:';
    h.appendChild(hb);
    r.appendChild(h);
    data.lesson.forEach(function (ch) {
      var p = document.createElement('p');
      p.textContent = ch.teach;
      r.appendChild(p);
    });
    r.style.display = '';
  }

  /* ---------------- the step flow ---------------- */
  function showStep(i, keepHeard) {
    idx = i; attempts = 0;
    hideBoardCheck();
    var st = step();
    $('gtTeach').textContent = st.teach;
    $('gtWhy').textContent = st.why || '';
    $('gtQ').textContent = st.q;
    /* arriving from a check keeps the receipt of what was just
       answered on screen; navigating by hand starts the step clean */
    if (!keepHeard) $('gtHeard').textContent = '';
    $('gtInput').value = '';
    $('gtHear').style.display = (started && st.audio) ? '' : 'none';
    /* help starts fresh on every step */
    helpLevel = 0;
    choicesShown = false;
    walkIdx = -1;
    var wk = $('gtWalk');
    wk.style.display = 'none'; wk.innerHTML = '';
    var hint = $('gtHint'), ch = $('gtChoices'), hb = $('gtHelp');
    hint.style.display = 'none'; hint.innerHTML = '';
    ch.style.display = 'none'; ch.innerHTML = '';
    hb.textContent = 'I\u2019m stuck — help me';
    hb.style.display = (started && states[i] !== 'pass') ? '' : 'none';
    renderDots(); renderProgress();
    /* multiple choice is a normal way to answer: the step's choice
       set is on the board from the moment the student is working */
    showDefaultChoices();
    if (states[i] === 'pass') {
      setStatus('This one is landed \u2713 — say it again to keep it warm, or tap another dot.', 'good');
    } else if (states[i] === 'skip') {
      setStatus('You skipped this one for now — it is still here to land, and landing it is what counts.', '');
    } else if (started) {
      setStatus(profFirst() + ' is waiting on your answer.', '');
    } else {
      setStatus('Read the piece, then tap Begin when you are ready to answer.', '');
    }
  }

  function check(text) {
    if (busy || !started) return;
    var said = (text !== undefined ? text : $('gtInput').value).trim();
    if (!said) {
      setStatus('Give it a real try first — even a rough one. That is what gets checked.', '');
      return;
    }
    busy = true;
    attempts++; sessionAttempts++;
    var res = G.checkAnswer(step(), said);
    $('gtHeard').textContent = 'Your answer: \u201C' + said + '\u201D';
    renderProgress();
    /* a pass after the I'm-stuck hint was taken is recorded as
       assisted, honestly; the choices alone are a normal way to
       answer and never make a pass assisted */
    if (res.pass) onPass(helpLevel >= 1);
    else onMiss(res);
  }

  function onPass(assisted) {
    var isNew = states[idx] !== 'pass';
    if (isNew) {
      states[idx] = 'pass';
      dirty = true;
      G.recordStep(storage, {
        date: new Date().toISOString(), classId: gCls.id, classTitle: gCls.title,
        step: idx, status: 'pass', attempts: attempts,
        assisted: !!assisted
      });
    }
    showBoardCheck();   /* the big green check lands WITH the praise */
    var pi = praiseCount++ % data.praise.length;
    setStatus(data.praise[pi] + (assisted
      ? ' That one landed with help — it counts, and your record says so: an assisted pass.'
      : ''), 'good');
    renderDots(); renderProgress();
    playClip(data.praiseAudio && data.praiseAudio[pi]).then(function () {
      busy = false;
      advance();
    });
  }

  /* the walkthrough: after the SECOND miss on a step, the professor
     stops re-asking and teaches the reasoning itself — how the
     answer follows, step by step, from the step's own material.
     The student still has to produce the answer; the walkthrough
     never passes the step for them. (Bill, Nov 16: "the re-teach
     claims to show a different side but never actually gives it" —
     the walkthrough IS the side, given.) */
  function showWalk() {
    var st = step();
    if (!st.walk || walkIdx === idx) return;
    walkIdx = idx;
    var wk = $('gtWalk');
    wk.innerHTML = '';
    var b = document.createElement('b');
    b.textContent = profFirst() + ' walks it through — how the answer follows: ';
    wk.appendChild(b);
    wk.appendChild(document.createTextNode(st.walk));
    wk.style.display = '';
  }

  function onMiss(res) {
    hideBoardCheck();
    var ri = (attempts - 1) % data.retry.length;
    setStatus(data.retry[ri] + ' ' + profFirst() + ' teaches it again, another way:', 'bad');
    /* the re-teach: the same piece, a different way in — then retry */
    $('gtTeach').textContent = step().teach2 || step().teach;
    /* a second miss earns the walkthrough, on the board immediately */
    if (attempts >= 2) showWalk();
    renderProgress();
    playClip(data.retryAudio && data.retryAudio[ri]).then(function () {
      busy = false;
      setStatus(data.retry[ri] + ' Try again — it does not move on until it lands.' +
        (walkIdx === idx
          ? ' The walkthrough is on the board: read how the answer follows, then say it yourself — it still has to come from you.'
          : ' Stuck? The help button under the question is there any time: a hint first, then choices.'), 'bad');
    });
  }

  /* ---------------- choices + help (Bill, Nov 16 03:07 + 04:16) ----
     MULTIPLE CHOICE IS A NORMAL WAY TO ANSWER (04:16): every step
     that carries an honest choice set shows it by default — the
     options are prebuilt by the generator from the class's own
     taught material (step.choices, with the correct text stored as
     step.mcAnswer) and picking the right one is a full, unassisted
     pass. The runtime derivation below remains as a fallback for
     any step the generator could not prebuild. HELP is separate:
     the I'm-stuck button gives a HINT drawn from the step's own
     material (its re-teach chunk, nothing invented), and a pass
     landed after the hint — by picking, speaking, or typing — is
     an ASSISTED pass, recorded as one. */
  function answerText(st) {
    if (!st) return null;
    if (st.kind === 'number') return st.disp || String(st.answer);
    if (st.kind === 'keywords') return null;   /* no single answer string */
    return st.answer != null ? String(st.answer) : null;
  }
  function correctText(st) {
    /* the generator stores the correct choice text on the step
       itself (mcAnswer) beside its prebuilt choices */
    if (st.mcAnswer) return st.mcAnswer;
    if (st.kind === 'keywords') {
      /* fallback derivation: a keyword step's correct choice is
         its own key ideas — the terms its worked answer stands on */
      return 'An answer built on: ' + st.keywords.map(function (g) {
        return g[0];
      }).join(' · ');
    }
    return answerText(st);
  }
  function normForChoice(s) {
    return String(s || '').toLowerCase().replace(/\s+/g, ' ').trim();
  }
  function buildChoices() {
    var st = step();
    /* the class's set problem is worked in the student's own
       words — no choice set is ever derived for it (the generator
       stores none either) */
    if (st.capstone) return [];
    var correct = correctText(st);
    var pool = [], seen = {};
    seen[normForChoice(correct)] = true;
    /* same-kind siblings first (a value among values, a title among
       titles), then the class's other answers — all its own material */
    var sibs = data.steps.filter(function (o, i) { return i !== idx; });
    sibs.sort(function (a, b) {
      return (b.kind === st.kind ? 1 : 0) - (a.kind === st.kind ? 1 : 0);
    });
    sibs.forEach(function (o) {
      /* a keyword step's "answer", for choice purposes, is its idea
         set — the terms its material stands on. A class of keyword
         questions thus offers its own idea sets as the choices:
         real material from this class, only one set answers this
         question. */
      var t = o.kind === 'keywords' ? correctText(o) : answerText(o);
      if (!t) return;
      var n = normForChoice(t);
      if (seen[n]) return;
      seen[n] = true;
      pool.push(t);
    });
    /* Top-up 1 — a DOI step in a paper class: the class's own
       SYLLABUS is part of the class, and its other papers' DOIs are
       the honest plausible set for "what is this paper's DOI". The
       two-step partial classes (DOI step + capstone) have no sibling
       answers at all; their syllabuses carry the rescue. */
    if (pool.length < 3 && st.kind === 'exact' &&
        /10\.\d+\//.test(String(st.answer)) && gCls && gCls.papers) {
      gCls.papers.forEach(function (p) {
        if (pool.length >= 3 || !p.doi) return;
        var n = normForChoice(p.doi);
        if (seen[n]) return;
        seen[n] = true;
        pool.push(p.doi);
      });
    }
    /* Top-up 2 — a value step gone thin: its own teach chunk states
       the paper's headline values in a row ("A = x; B = y; …"). The
       sibling values in that same statement are the step's own
       material, in the material's own printed form. */
    if (pool.length < 2 && st.kind === 'number') {
      var want = typeof st.answer === 'number' ? st.answer : G.parseNumber(st.answer);
      var tol = st.tol || 0.03;
      var text = (st.teach || '') + ' ' + (st.teach2 || '');
      var m, re = /=\s*(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)/gi;
      while ((m = re.exec(text)) !== null && pool.length < 2) {
        var pv = parseFloat(m[1]);
        if (!isNaN(pv) && want !== null && want !== undefined &&
            Math.abs(pv - want) / Math.abs(want || 1) <= tol) continue;
        var n2 = normForChoice(m[1]);
        if (seen[n2]) continue;
        seen[n2] = true;
        pool.push(m[1]);
      }
    }
    var opts = [{ t: correct, ok: true }].concat(
      pool.slice(0, 3).map(function (t) { return { t: t, ok: false }; }));
    /* a plain shuffle — position teaches nothing */
    for (var i = opts.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = opts[i]; opts[i] = opts[j]; opts[j] = tmp;
    }
    return opts;
  }
  function showHint() {
    helpLevel = 1;
    var st = step();
    var hint = $('gtHint');
    hint.innerHTML = '';
    var b = document.createElement('b');
    b.textContent = 'Hint — from the material itself: ';
    hint.appendChild(b);
    hint.appendChild(document.createTextNode(st.teach2 || st.teach || ''));
    hint.style.display = '';
    if (choicesShown) {
      /* the choices are already on the board — the hint completes
         the help kit for this step */
      $('gtHelp').style.display = 'none';
      setStatus('There is the piece again, the other way in — and ' +
        'the choices are on the board. Land it.', '');
    } else {
      $('gtHelp').textContent = 'Still stuck — show me the choices';
      setStatus('There is the piece again, the other way in. Try once ' +
        'more — or take the choices below the hint.', '');
    }
  }
  var choicesShown = false;
  function renderChoices(opts, viaHelp) {
    var host = $('gtChoices');
    host.innerHTML = '';
    var head = document.createElement('p');
    head.style.margin = '0 0 4px';
    head.innerHTML = viaHelp
      ? '<b>Pick the one the material supports.</b> Every choice ' +
        'here is real material from this class — only one answers ' +
        'this question. Landing it after the hint is recorded as ' +
        'an assisted pass.'
      : '<b>Pick your answer</b> — or answer out loud, or type it ' +
        'below, instead. Every choice here is real material from ' +
        'this class\u2019s own lesson, and picking the right one ' +
        'counts in full.';
    host.appendChild(head);
    opts.forEach(function (o) {
      var btn = document.createElement('button');
      btn.className = 'gtChoice';
      btn.textContent = o.t;
      btn.addEventListener('click', function () { pickChoice(btn, o.ok); });
      host.appendChild(btn);
    });
    host.style.display = '';
    choicesShown = true;
    if (viaHelp) $('gtHelp').style.display = 'none';
  }
  function storedChoices() {
    var st = step();
    if (!st.choices || st.choices.length < 2) return null;
    var correct = correctText(st);
    return st.choices.map(function (t) {
      return { t: t, ok: t === correct };
    });
  }
  /* the default presentation: a step with an honest choice set
     shows it as soon as the student is working on the step */
  function showDefaultChoices() {
    if (!started || states[idx] === 'pass') return;
    var opts = storedChoices() || buildChoices();
    if (opts.length >= 2) renderChoices(opts, false);
  }
  function showChoices() {
    var opts = storedChoices() || buildChoices();
    if (opts.length < 2) { showLookup(); return; }
    helpLevel = 2;
    renderChoices(opts, true);
    setStatus('Choices are up. Pick the one the material supports.', '');
  }
  /* No honest choice set exists for this step (its class carries no
     sibling answers and no syllabus rescue): help becomes a guided
     look-up in the class's own materials instead of a fabricated
     pick. helpLevel still goes to 2, so a pass typed after the
     look-up is recorded as assisted — the student was shown where
     the answer lives. */
  function showLookup() {
    helpLevel = 2;
    choicesShown = true;
    var st = step();
    var host = $('gtChoices');
    host.innerHTML = '';
    var p = document.createElement('p');
    p.style.margin = '0 0 4px';
    var where = st.kind === 'exact'
      ? 'This step\u2019s answer is printed on the class\u2019s own ' +
        'Syllabus card. Open the Syllabus tab above, find it there, ' +
        'and type it here.'
      : 'This step\u2019s answer is in the piece itself — the hint ' +
        'above states the material again, the other way in. Read ' +
        'the answer out of it and type it here.';
    p.innerHTML = '<b>No set of choices can be honestly built for ' +
      'this step</b> — this class carries no other answers to pick ' +
      'from, and invented options would be fabrication. ' + where +
      ' Landing it after the look-up is recorded as an assisted ' +
      'pass, honestly.';
    host.appendChild(p);
    host.style.display = '';
    $('gtHelp').style.display = 'none';
    setStatus('Help, the honest form for this step: look it up in ' +
      'the class\u2019s own material, then type it.', '');
  }
  function pickChoice(btn, ok) {
    if (busy || !started) return;
    attempts++; sessionAttempts++;
    renderProgress();
    if (!ok) {
      btn.disabled = true;
      /* a second miss on the step earns the walkthrough, however
         the misses arrived — picked, spoken, or typed */
      if (attempts >= 2) showWalk();
      setStatus('Not that one — it is real material from this ' +
        'class, but it answers a different question. Look at the ' +
        'piece once more and pick the one this question\u2019s ' +
        'material supports.' +
        (walkIdx === idx
          ? ' The walkthrough is on the board: read how the answer follows.'
          : ''), 'bad');
      return;
    }
    busy = true;
    $('gtChoices').style.display = 'none';
    choicesShown = false;
    /* picking is a normal way to answer — assisted only when the
       hint was taken first */
    onPass(helpLevel >= 1);
  }
  function onHelp() {
    if (!started || busy || states[idx] === 'pass') return;
    if (helpLevel === 0) showHint();
    else if (helpLevel === 1 && !choicesShown) showChoices();
  }
  /* assisted passes recorded for this class, among its passed steps */
  function assistedCount() {
    var n = 0;
    try {
      var log = JSON.parse(storage.getItem('dave_lab_log') || '[]');
      var seen = {};
      log.forEach(function (e) {
        if (e && e.kind === 'gate-step' && e.classId === gCls.id &&
            e.status === 'pass' && e.assisted) seen[e.step] = true;
      });
      Object.keys(seen).forEach(function (k) {
        if (states[k] === 'pass') n++;
      });
    } catch (e) { /* the count is a courtesy; the entries stand */ }
    return n;
  }

  function advance() {
    var total = data.steps.length;
    for (var k = 1; k <= total; k++) {
      var j = (idx + k) % total;
      if (!states[j]) { showStep(j, true); return; }
    }
    complete();
  }

  function writeGrade(complete) {
    if (gradeWritten || !dirty) return;
    gradeWritten = true;
    G.recordGrade(storage, {
      date: new Date().toISOString(), classId: gCls.id, classTitle: gCls.title,
      states: states, total: data.steps.length,
      attempts: sessionAttempts, complete: complete,
      assisted: assistedCount()
    });
  }

  function complete() {
    renderDots(); renderProgress();
    writeGrade(true);
    var g = G.gradeFor(states, data.steps.length);
    var panel = $('gtGrade');
    panel.style.display = '';
    panel.innerHTML = '';
    var h = document.createElement('div');
    h.innerHTML = '<b>Set complete \u2014 your grade is in your University record.</b>';
    panel.appendChild(h);
    var p = document.createElement('p');
    p.style.margin = '6px 0 0';
    var assistedN = assistedCount();
    p.textContent = g.passed + ' of ' + g.total + ' questions landed' +
      (g.skipped ? ', ' + g.skipped + ' skipped (counted as skips, never as passes)' : '') +
      (assistedN ? ', ' + assistedN + ' landed with help (recorded as assisted passes)' : '') +
      ' \u2014 ' + g.percent + '%. ' +
      (g.percent === 100
        ? 'Every question earned. That is the whole lesson, proven in session.'
        : 'Revisit a striped dot any time to land what was skipped \u2014 the grade updates when you do.');
    panel.appendChild(p);
    setStatus('Every question in this set is resolved. Well worked.', 'good');
    showBoardCheck();
  }

  /* ---------------- speech: answering out loud ---------------- */
  function startListening() {
    if (listening || busy || !started) return;
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
      setStatus('This browser can\u2019t listen \u2014 Chrome and Edge can. Typing is the door here, and it counts exactly the same.', '');
      $('gtMic').style.display = 'none';
      return;
    }
    rec = new SR();
    rec.lang = 'en-US';
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
      if (interim) $('gtHeard').textContent = '\u2026 ' + interim;
    };
    rec.onerror = function (ev) {
      listening = false; idleWave();
      $('gtWave').style.display = 'none';
      if (ev.error === 'not-allowed' || ev.error === 'service-not-allowed') {
        setStatus('The microphone is off for this page \u2014 typing is the door here, and it counts exactly the same.', '');
        $('gtMic').style.display = 'none';
      } else if (ev.error === 'no-speech') {
        setStatus('I didn\u2019t hear anything \u2014 tap \u201CAnswer out loud\u201D and say it like you mean it.', '');
      } else {
        setStatus('The listening hiccupped (' + ev.error + ') \u2014 type it, or tap the mic and try again.', '');
      }
    };
    rec.onend = function () {
      var was = listening;
      listening = false; idleWave();
      $('gtWave').style.display = 'none';
      if (heardFinal) {
        var hf = heardFinal; heardFinal = null;
        $('gtInput').value = hf;
        check(hf);
      } else if (was) {
        setStatus('I didn\u2019t catch that \u2014 say it once more, or type it below.', '');
      }
    };
    try {
      rec.start();
      listening = true;
      $('gtWave').style.display = 'block';
      startWave();
      setStatus(profFirst() + ' is listening \u2014 answer now.', '');
    } catch (e) { listening = false; }
  }

  /* ---------------- session control ---------------- */
  function begin() {
    if (started) return;
    started = true;
    $('gtBegin').style.display = 'none';
    $('gtInput').style.display = '';
    $('gtCheck').style.display = '';
    $('gtSkip').style.display = '';
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SR) $('gtMic').style.display = '';
    if (step().audio) $('gtHear').style.display = '';
    /* the help door is on the step from the FIRST attempt — visible,
       not discovered later (Bill, Nov 16) */
    $('gtHelp').style.display = states[idx] !== 'pass' ? '' : 'none';
    /* the lesson stays one tap away while the questions run */
    if (hasLesson()) $('gtRefBtn').style.display = '';
    getMic().catch(function () { /* mic unavailable: typing still works */ });
    /* the opening clip shares one audio element with every later
       clip, so this promise can resolve late — when the RETRY clip
       ends, not the opening one. If the student has already
       answered by then, the check flow owns the board: a late
       showStep here would reset the attempt count mid-question
       (a fast first miss lost its attempt — Nov 16 verification). */
    var stamp = sessionAttempts;
    playClip(step().audio).then(function () {
      if (sessionAttempts === stamp) showStep(idx);
    });
  }

  function enter(section, cls, prof) {
    ensureBox();
    leave();
    if (!GATE_DATA) {
      pendingEnter = { section: section, cls: cls, prof: prof };
      box.style.display = 'none';
      return false;
    }
    if (!GATE_DATA[cls.id] || !G) {
      box.style.display = 'none';
      return false;
    }
    data = GATE_DATA[cls.id]; gCls = cls; gProf = prof;
    states = G.loadStepStates(storage, cls.id);
    sessionAttempts = 0; praiseCount = 0;
    started = false; busy = false; dirty = false; gradeWritten = false;
    box.style.display = '';
    $('gtTitle').textContent = 'First the lesson \u2014 then the questions, with ' + profFirst();
    var firstOpen = data.steps.findIndex(function (s, i) { return !states[i]; });
    idx = firstOpen === -1 ? 0 : firstOpen;
    var hasProgress = Object.keys(states).length > 0;
    if (hasLesson() && !hasProgress && data.steps.length) {
      /* first time in this class: the lesson is taught first */
      phase = 'lesson';
      lessonIdx = 0; lessonStarted = false;
      setQuestionChrome(false);
      $('gtBegin').style.display = 'none';
      $('gtLesson').style.display = '';
      showLessonChunk();
    } else {
      phase = 'questions';
      $('gtLesson').style.display = 'none';
      setQuestionChrome(true);
      $('gtBegin').style.display = '';
      $('gtBegin').textContent = 'Begin \u2014 ' + profFirst() + ' asks the questions';
      ['gtCheck', 'gtMic', 'gtHear', 'gtSkip', 'gtHelp', 'gtRefBtn'].forEach(function (id) { $(id).style.display = 'none'; });
      $('gtInput').style.display = 'none';
      $('gtGrade').style.display = 'none';
      $('gtWave').style.display = 'none';
      showStep(idx);
    }
    return true;
  }

  /* start(): begin the current class's lesson from outside the box
     (the Ask-the-professor box routes "start lesson 1" here). Returns
     true when a live gate lesson owns this classroom — started now,
     or already under way — and false when this class has no gate
     (a language room, or the data has not landed yet). */
  function start() {
    if (!data || !box || box.style.display === 'none') return false;
    if (phase === 'lesson') { beginLesson(); return true; }
    if (!started) begin();
    return true;
  }

  function leave() {
    if (data && gCls && dirty) writeGrade(
      G.gradeFor(states, data.steps.length).resolved === data.steps.length);
    hideBoardCheck();
    if (rec) { try { rec.abort(); } catch (e) {} rec = null; }
    listening = false;
    if (stream) { stream.getTracks().forEach(function (t) { t.stop(); }); stream = null; }
    if (actx) { try { actx.close(); } catch (e) {} actx = null; analyser = null; }
    cancelAnimationFrame(waveRAF);
    var a = $('gtAudio');
    if (a) { a.pause(); a.removeAttribute('src'); }
    started = false; busy = false;
    phase = 'questions'; lessonIdx = 0; lessonStarted = false;
    var lp = $('gtLesson'); if (lp) lp.style.display = 'none';
    var rp = $('gtRef'); if (rp) rp.style.display = 'none';
    data = null; gCls = null;
    if (box) box.style.display = 'none';
  }

  function wire() {
    $('gtBeginLesson').addEventListener('click', beginLesson);
    $('gtContinue').addEventListener('click', continueLesson);
    $('gtHearLesson').addEventListener('click', function () { playLessonChunk(); });
    $('gtToQuestions').addEventListener('click', function (e) {
      e.preventDefault();
      if (phase === 'lesson') toQuestions();
    });
    $('gtRefBtn').addEventListener('click', toggleRef);
    $('gtBegin').addEventListener('click', begin);
    $('gtCheck').addEventListener('click', function () { check(); });
    $('gtMic').addEventListener('click', startListening);
    $('gtHelp').addEventListener('click', onHelp);
    $('gtHear').addEventListener('click', function () { if (!busy) playClip(step().audio); });
    $('gtSkip').addEventListener('click', function (e) {
      e.preventDefault();
      if (!started || busy) return;
      if (states[idx] !== 'pass' && states[idx] !== 'skip') {
        states[idx] = 'skip';
        dirty = true;
        G.recordStep(storage, {
          date: new Date().toISOString(), classId: gCls.id, classTitle: gCls.title,
          step: idx, status: 'skip', attempts: attempts
        });
      } else if (states[idx] === 'skip') {
        /* already recorded — just move on */
      } else {
        return; /* a landed step is not skippable */
      }
      setStatus('Skipped for now \u2014 recorded as a skip. It stays on the board until you land it.', '');
      renderDots(); renderProgress();
      advance();
    });
  }

  window.UniGate = { enter: enter, leave: leave, start: start };
})();
