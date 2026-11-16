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
    '#gtChoices{display:none;margin:10px 0 0}',
    '#gtChoices .gtChoice{display:block;width:100%;text-align:left;margin:6px 0;background:var(--panel);border:1px solid var(--gold);color:var(--ink);border-radius:6px;padding:9px 14px;font-family:inherit;font-size:.98rem;cursor:pointer}',
    '#gtChoices .gtChoice:hover:not(:disabled){background:var(--gold);color:#fff}',
    '#gtChoices .gtChoice:disabled{opacity:.45;cursor:default}',
    '.gtSep{border:0;border-top:1px solid var(--line);margin:18px 0 10px}'
  ].join('\n');

  var HTML =
    '<h3 id="gtTitle">Work it with your professor — answer, and earn each step</h3>' +
    '<p>Your professor presents a piece of the lesson, then asks you ' +
    'about it — a problem to solve, a value to produce, a question to ' +
    'answer. <b>Say your answer out loud or type it.</b> It is checked ' +
    'against the class\u2019s own material, and the lesson <b>does not ' +
    'move on</b> until it lands: miss, and your professor teaches the ' +
    'piece again, a different way. Your grade for the set is recorded ' +
    'in your University record — passes, and skips counted as skips. ' +
    'Stuck is allowed: <b>I\u2019m stuck — help me</b> first gives a ' +
    'hint drawn from the material itself, then choices to pick from. ' +
    'A step landed through the choices counts — and your record says ' +
    'so, as an assisted pass.</p>' +
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
    '</div>' +
    '<div id="gtStatus"></div>' +
    '<div id="gtHint"></div>' +
    '<div id="gtChoices"></div>' +
    '<div id="gtFoot"><span id="gtProgress"></span>' +
    '<a href="#" id="gtSkip" style="display:none">skip for now \u2192</a></div>' +
    '<div id="gtGrade" style="display:none"></div>' +
    '<audio id="gtAudio" preload="auto" style="display:none"></audio>' +
    '<hr class="gtSep">';

  var GATE_DATA = null, pendingEnter = null;
  fetch('gate-data.json').then(function (r) { return r.ok ? r.json() : null; })
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
  var idx = 0, attempts = 0, sessionAttempts = 0, praiseCount = 0;
  var helpLevel = 0;   /* per step: 0 none · 1 hint shown · 2 choices shown */
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
    $('gtProgress').textContent = 'Step ' + (idx + 1) + ' of ' + data.steps.length +
      ' · ' + g.passed + ' landed' +
      (g.skipped ? ' · ' + g.skipped + (g.skipped === 1 ? ' skip' : ' skips') : '') +
      (attempts ? ' · ' + attempts + (attempts === 1 ? ' try' : ' tries') + ' on this one' : '');
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
    var hint = $('gtHint'), ch = $('gtChoices'), hb = $('gtHelp');
    hint.style.display = 'none'; hint.innerHTML = '';
    ch.style.display = 'none'; ch.innerHTML = '';
    hb.textContent = 'I\u2019m stuck — help me';
    hb.style.display = (started && states[i] !== 'pass') ? '' : 'none';
    renderDots(); renderProgress();
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
    /* a pass after the choices were shown was landed with the answer
       set in front of the student — recorded as assisted, honestly */
    if (res.pass) onPass(helpLevel >= 2);
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

  function onMiss(res) {
    hideBoardCheck();
    var ri = (attempts - 1) % data.retry.length;
    setStatus(data.retry[ri] + ' ' + profFirst() + ' teaches it again, another way:', 'bad');
    /* the re-teach: the same piece, a different way in — then retry */
    $('gtTeach').textContent = step().teach2 || step().teach;
    renderProgress();
    playClip(data.retryAudio && data.retryAudio[ri]).then(function () {
      busy = false;
      setStatus(data.retry[ri] + ' Try again — it does not move on until it lands.', 'bad');
    });
  }

  /* ---------------- help: hint, then choices (Bill, Nov 16 03:07) ----
     A stuck student can ask for help. Level 1 is a HINT drawn from
     the step's own material — its re-teach chunk, nothing invented.
     Level 2 is MULTIPLE CHOICE: the correct answer plus distractors
     drawn from the SAME class's other steps' own answers — real
     material, never fabricated facts. Landing a step through the
     choices is an ASSISTED pass, recorded as one. */
  function answerText(st) {
    if (!st) return null;
    if (st.kind === 'number') return st.disp || String(st.answer);
    if (st.kind === 'keywords') return null;   /* no single answer string */
    return st.answer != null ? String(st.answer) : null;
  }
  function correctText(st) {
    if (st.kind === 'keywords') {
      /* the capstone's correct choice is its own key ideas — the
         terms its worked answer stands on, from its own key */
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
      var t = answerText(o);
      if (!t) return;
      var n = normForChoice(t);
      if (seen[n]) return;
      seen[n] = true;
      pool.push(t);
    });
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
    $('gtHelp').textContent = 'Still stuck — show me the choices';
    setStatus('There is the piece again, the other way in. Try once ' +
      'more — or take the choices below the hint.', '');
  }
  function showChoices() {
    helpLevel = 2;
    var host = $('gtChoices');
    host.innerHTML = '';
    var head = document.createElement('p');
    head.style.margin = '0 0 4px';
    head.innerHTML = '<b>Pick the one the material supports.</b> ' +
      'Every choice here is real material from this class — only one ' +
      'answers this step. Landing it this way is recorded as an ' +
      'assisted pass.';
    host.appendChild(head);
    buildChoices().forEach(function (o) {
      var btn = document.createElement('button');
      btn.className = 'gtChoice';
      btn.textContent = o.t;
      btn.addEventListener('click', function () { pickChoice(btn, o.ok); });
      host.appendChild(btn);
    });
    host.style.display = '';
    $('gtHelp').style.display = 'none';
    setStatus('Choices are up. Pick the one the material supports.', '');
  }
  function pickChoice(btn, ok) {
    if (busy || !started) return;
    attempts++; sessionAttempts++;
    renderProgress();
    if (!ok) {
      btn.disabled = true;
      setStatus('Not that one — it belongs to another step of this ' +
        'class. Look at the hint once more and pick the one this ' +
        'step\u2019s material supports.', 'bad');
      return;
    }
    busy = true;
    $('gtChoices').style.display = 'none';
    onPass(true);
  }
  function onHelp() {
    if (!started || busy || states[idx] === 'pass') return;
    if (helpLevel === 0) showHint();
    else if (helpLevel === 1) showChoices();
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
    p.textContent = g.passed + ' of ' + g.total + ' steps landed' +
      (g.skipped ? ', ' + g.skipped + ' skipped (counted as skips, never as passes)' : '') +
      (assistedN ? ', ' + assistedN + ' landed with help (recorded as assisted passes)' : '') +
      ' \u2014 ' + g.percent + '%. ' +
      (g.percent === 100
        ? 'Every step earned. That is the whole lesson, proven in session.'
        : 'Revisit a striped dot any time to land what was skipped \u2014 the grade updates when you do.');
    panel.appendChild(p);
    setStatus('Every step in this set is resolved. Well worked.', 'good');
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
    getMic().catch(function () { /* mic unavailable: typing still works */ });
    playClip(step().audio).then(function () { showStep(idx); });
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
    $('gtTitle').textContent = 'Work it with ' + profFirst() + ' \u2014 answer, and earn each step';
    $('gtBegin').style.display = '';
    $('gtBegin').textContent = 'Begin \u2014 ' + profFirst() + ' presents the first piece';
    ['gtCheck', 'gtMic', 'gtHear', 'gtSkip', 'gtHelp'].forEach(function (id) { $(id).style.display = 'none'; });
    $('gtInput').style.display = 'none';
    $('gtGrade').style.display = 'none';
    $('gtWave').style.display = 'none';
    var firstOpen = data.steps.findIndex(function (s, i) { return !states[i]; });
    idx = firstOpen === -1 ? 0 : firstOpen;
    showStep(idx);
    return true;
  }

  /* start(): begin the current class's lesson from outside the box
     (the Ask-the-professor box routes "start lesson 1" here). Returns
     true when a live gate lesson owns this classroom — started now,
     or already under way — and false when this class has no gate
     (a language room, or the data has not landed yet). */
  function start() {
    if (!data || !box || box.style.display === 'none') return false;
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
    data = null; gCls = null;
    if (box) box.style.display = 'none';
  }

  function wire() {
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
