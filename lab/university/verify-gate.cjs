/* Browser verification for the classroom gate — lesson-first build.
   Bill's model (Nov 16): the class is TAUGHT first — the lesson
   presented in full — and only then do the passing questions run,
   every one drawn from what was just taught.
   Drives real classrooms in headless Chrome:
     1. a College flagship (cosmology — The Bounce & the Aldred
        Limit): lesson first; a WRONG value on the question holds it
        and the re-teach shows the exact passage; the retry passes;
        the capstone is skipped and the skip is recorded; the
        finished set writes a class-grade entry to dave_lab_log;
        states persist across a reload.
     2. an authored class (Numbers & Proof): the end-of-class
        questions ask only what the lesson taught.
     3. a generated paper class (snow avalanches): typed value
        passes, then the VOICE path advances.
     4. AI Fundamentals, read cold — Bill's exact seat (Nov 16):
        the lesson teaches what a model IS before any question; a
        miss brings the exact passage + a different angle; a second
        miss brings the walkthrough; the right answer advances.
     5. a sample of six more classes across sections, driven the
        same way through their lessons.
     6. a node-side containment audit over ALL gated classes: every
        question's answer must be present in that class's taught
        lesson text (independent JS implementation of the rule).
   Run: NODE_PATH=<owner-lane browser node_modules> node verify-gate.cjs <baseUrl>
*/
'use strict';
const fs = require('fs');
const puppeteer = require('puppeteer-core');

const BASE = process.argv[2] || 'http://127.0.0.1:8932/';
const EXE = '/home/hatch/.cache/puppeteer/chrome/linux-156.0.8078.47/chrome-linux64/chrome';
const sleep = ms => new Promise(r => setTimeout(r, ms));
let failures = 0;
function check(name, cond, extra) {
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' — ' + extra : ''));
  if (!cond) failures++;
}
const GATE = JSON.parse(fs.readFileSync('gate-data.json', 'utf8')).classes;

const FAKE_SR = `
  window.__stubHeard = '14.0248';
  class FakeSR {
    constructor() { this.lang = ''; this.interimResults = false; this.maxAlternatives = 1; }
    start() {
      const txt = window.__stubHeard;
      setTimeout(() => {
        if (this.onresult) {
          const r = { isFinal: true, length: 1 };
          r[0] = { transcript: txt, confidence: 0.99 };
          const results = { length: 1 }; results[0] = r;
          this.onresult({ resultIndex: 0, results });
        }
        setTimeout(() => { if (this.onend) this.onend(); }, 150);
      }, 700);
    }
    abort() { if (this.onend) this.onend(); }
    stop() {}
  }
  window.SpeechRecognition = FakeSR;
  window.webkitSpeechRecognition = FakeSR;
`;

async function openClass(page, section, cls) {
  await page.goto(BASE + '#class/' + section + '/' + cls,
    { waitUntil: 'networkidle2', timeout: 60000 });
  await page.waitForSelector('#gateBox', { visible: true, timeout: 20000 });
}
async function answer(page, text) {
  await page.$eval('#gtInput', (el, t) => { el.value = t; }, text);
  await page.click('#gtCheck');
}
const q = page => page.$eval('#gtQ', el => el.textContent);
const status = page => page.$eval('#gtStatus', el => el.textContent);
const logOf = page => page.evaluate(
  () => JSON.parse(localStorage.getItem('dave_lab_log') || '[]'));
const disp = (page, id) => page.$eval('#' + id, el => el.style.display);

/* Walk the lesson phase (if the class opens with one) and click
   Begin on the questions. Returns true if a lesson was presented. */
async function beginQuestions(page, clsId) {
  const lessonVisible = await page.evaluate(
    () => document.getElementById('gtLesson').style.display !== 'none');
  if (lessonVisible) {
    const n = GATE[clsId].lesson.length;
    await page.click('#gtBeginLesson');
    for (let i = 0; i < n; i++) { await page.click('#gtContinue'); await sleep(120); }
    await page.waitForFunction(
      () => document.getElementById('gtBegin').style.display !== 'none',
      { timeout: 15000 });
  }
  await page.click('#gtBegin');
  await sleep(500);
  return lessonVisible;
}

(async () => {
  const browser = await puppeteer.launch({
    executablePath: EXE, headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage',
           '--disable-gpu', '--no-first-run', '--no-proxy-server',
           '--use-fake-device-for-media-stream', '--use-fake-ui-for-media-stream',
           '--autoplay-policy=no-user-gesture-required', '--window-size=1280,1000']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 1000 });
  page.on('pageerror', e => console.log('PAGE ERROR:', e.message));
  await page.evaluateOnNewDocument(FAKE_SR);

  /* ============ 1. College flagship: the bounce ============ */
  await openClass(page, 'cosmology', 'the-bounce-the-aldred-limit');
  check('the flagship opens with the LESSON, before any question',
    await disp(page, 'gtLesson') !== 'none' &&
    await disp(page, 'gtDots') === 'none');
  const part1 = await page.$eval('#gtLessonText', el => el.textContent);
  check('lesson part 1 opens the class (professor, title, the frame in order)',
    /Professor/.test(part1) && /Bounce/.test(part1), part1.slice(0, 60));
  const lessonShown = await beginQuestions(page, 'the-bounce-the-aldred-limit');
  check('the full lesson was presented before the questions', lessonShown);
  const dots = await page.$$eval('#gtDots .dot', els => els.length);
  check('flagship has 2 end-of-class questions (untaught checks are gone)',
    dots === 2, String(dots));
  await page.screenshot({ path: 'gate-shot-1-flagship.png' });

  /* question 0 — the eps_mid value: wrong first */
  const q0 = await q(page);
  check('question 0 asks a value the lesson taught', /eps_mid/.test(q0),
    q0.slice(0, 60));
  let checkSeen = false;
  const watcher = (async () => {
    for (let i = 0; i < 60 && !checkSeen; i++) {
      const on = await page.evaluate(
        () => document.getElementById('trBoardCheck').classList.contains('on')
      ).catch(() => false);
      if (on) { checkSeen = true; await page.screenshot({ path: 'gate-shot-2-greencheck.png' }); }
      await sleep(150);
    }
  })();
  await answer(page, '0.9');
  await page.waitForFunction(
    () => /Not yet/.test(document.getElementById('gtStatus').textContent),
    { timeout: 15000 });
  const qMiss = await q(page);
  check('wrong value holds the question (no advance)', /eps_mid/.test(qMiss),
    qMiss.slice(0, 60));
  const teach2 = await page.$eval('#gtTeach', el => el.textContent);
  check('miss brings the re-teach: the exact passage, value stated plainly',
    /eps_mid = 0.45/.test(teach2), teach2.slice(0, 80));
  const checkOnMiss = await page.evaluate(
    () => document.getElementById('trBoardCheck').classList.contains('on'));
  check('no green check on a miss', !checkOnMiss);

  /* retry — right value: advance to the capstone */
  await page.waitForFunction(
    () => /Try again/.test(document.getElementById('gtStatus').textContent),
    { timeout: 30000 });
  await answer(page, '0.45');
  await page.waitForFunction(
    () => /Question 2 of 2/.test(document.getElementById('gtProgress').textContent),
    { timeout: 30000 });
  check('retry with the right value advances', true);
  await watcher;
  check('big green check appeared on the board', checkSeen);

  /* capstone — skip: recorded as a skip, set completes, grade lands */
  await page.click('#gtSkip');
  await page.waitForFunction(
    () => document.getElementById('gtGrade').style.display !== 'none',
    { timeout: 15000 });
  const gradeText = await page.$eval('#gtGrade', el => el.textContent);
  check('grade panel reports 1 landed + 1 skip',
    /1 of 2 questions landed/.test(gradeText) && /1 skipped/.test(gradeText),
    gradeText.slice(0, 110));
  const log1 = await logOf(page);
  const steps1 = log1.filter(e => e.kind === 'gate-step' &&
    e.classId === 'the-bounce-the-aldred-limit');
  check('gate-step records: pass, skip',
    steps1.map(e => e.status).join(',') === 'pass,skip',
    steps1.map(e => e.status).join(','));
  check('the missed question recorded its attempts',
    steps1[0] && steps1[0].attempts === 2,
    steps1[0] ? String(steps1[0].attempts) : 'missing');
  const grade1 = log1.find(e => e.kind === 'class-grade' &&
    e.classId === 'the-bounce-the-aldred-limit');
  check('class-grade entry written, complete, 50%',
    !!grade1 && grade1.complete === true && grade1.passed === 1 &&
    grade1.skipped === 1 && grade1.percent === 50,
    grade1 ? JSON.stringify(grade1) : 'missing');
  check('grade entry keeps hours untouched (minutes 0)', grade1 && grade1.minutes === 0);

  /* persistence: dots survive a reload in their recorded states,
     and a returning student enters at the questions */
  await page.reload({ waitUntil: 'networkidle2' });
  await page.waitForSelector('#gateBox', { visible: true, timeout: 20000 });
  await sleep(500);
  const dotCls = await page.$$eval('#gtDots .dot', els => els.map(e => e.className));
  check('states persist after reload (done, skipped)',
    /done/.test(dotCls[0]) && /skipped/.test(dotCls[1]),
    dotCls.join(' | '));
  check('returning student goes straight to the questions',
    await disp(page, 'gtLesson') === 'none');

  /* ============ 2. Authored class: Numbers & Proof ============ */
  await openClass(page, 'mathematics', 'numbers-proof-foundations-of-mathematics');
  await beginQuestions(page, 'numbers-proof-foundations-of-mathematics');
  const qA = await q(page);
  check('end-of-class question asks only what the lesson taught, ' +
    'in plain language',
    /in your own words/i.test(qA), qA.slice(0, 70));
  const glossStep = GATE['numbers-proof-foundations-of-mathematics'].steps[0];
  await answer(page, glossStep.keywords.map(g => g[0]).join(' '));
  await page.waitForFunction(
    () => /Question 2 of/.test(document.getElementById('gtProgress').textContent),
    { timeout: 30000 });
  check('an answer built on the taught definition passes and advances', true);
  const log2 = await logOf(page);
  check('authored pass recorded in the log',
    log2.some(e => e.kind === 'gate-step' &&
      e.classId === 'numbers-proof-foundations-of-mathematics' && e.status === 'pass'));

  /* ============ 3. Generated paper class: snow avalanches ============ */
  await openClass(page, 'particle',
    'snow-avalanches-slab-fracture-and-powder-clouds-release-fracture');
  await beginQuestions(page,
    'snow-avalanches-slab-fracture-and-powder-clouds-release-fracture');
  const qG = await q(page);
  check('generated question asks a value the lesson stated',
    /runout beyond beta point/.test(qG), qG.slice(0, 70));
  await answer(page, '197.61');
  await page.waitForFunction(
    () => /flexural response speed/.test(document.getElementById('gtQ').textContent),
    { timeout: 30000 });
  check('typed value passes and advances', true);
  let waveSeen = false;
  const waveWatch = (async () => {
    for (let i = 0; i < 40 && !waveSeen; i++) {
      const d = await page.evaluate(
        () => document.getElementById('gtWave').style.display).catch(() => 'none');
      if (d === 'block') waveSeen = true;
      await sleep(80);
    }
  })();
  await page.click('#gtMic');
  await page.waitForFunction(
    () => /release volume/.test(document.getElementById('gtQ').textContent),
    { timeout: 30000 });
  check('spoken value is heard, checked, and advances', true);
  await waveWatch;
  check('green voice bar showed while listening', waveSeen);
  const heard = await page.$eval('#gtHeard', el => el.textContent);
  check('student is shown what was heard', /14\.0248/.test(heard), heard.slice(0, 60));
  await page.screenshot({ path: 'gate-shot-3-generated.png' });

  /* ============ 4. AI Fundamentals, read cold (Bill's seat) ====
     The class he was stuck in: the old first question asked which
     unit comes next — an answer nowhere in the teaching. Now the
     lesson teaches what a model IS first; the questions come at
     the end and draw only on the lesson; a miss brings the exact
     passage plus a different angle; a second miss brings the
     walkthrough; the help door is visible from the first attempt. */
  const AI = 'ai-fundamentals-what-a-mind-made-of-math-is';
  await openClass(page, 'ai-computing', AI);
  check('AI Fundamentals opens with the lesson, not a question',
    await disp(page, 'gtLesson') !== 'none' &&
    await disp(page, 'gtDots') === 'none');
  const aiPart1 = await page.$eval('#gtLessonText', el => el.textContent);
  check('the lesson teaches what a model is, before any question',
    /a model is a function/.test(aiPart1), aiPart1.slice(0, 70));
  await page.screenshot({ path: 'gate-shot-5-lesson.png' });
  await beginQuestions(page, AI);
  check('help door visible from the FIRST attempt',
    await disp(page, 'gtHelp') !== 'none');
  const qAI = await q(page);
  check('first question is on the taught material (what a model is)',
    /what is a model/.test(qAI), qAI.slice(0, 70));
  const teachAI = await page.$eval('#gtTeach', el => el.textContent);
  await answer(page, 'a robot that thinks like a person');
  await page.waitForFunction(
    () => /Not yet/.test(document.getElementById('gtStatus').textContent),
    { timeout: 15000 });
  check('a wrong answer holds the question', true);
  const teach2AI = await page.$eval('#gtTeach', el => el.textContent);
  check('the re-teach shows the exact taught passage, a different presentation',
    teach2AI !== teachAI && /exact passage/.test(teach2AI) &&
    /a model is a function/.test(teach2AI), teach2AI.slice(0, 80));
  check('no walkthrough after only one miss',
    await disp(page, 'gtWalk') === 'none');
  await page.waitForFunction(
    () => /Try again/.test(document.getElementById('gtStatus').textContent),
    { timeout: 30000 });
  await answer(page, 'a machine that dreams');
  await page.waitForFunction(
    () => document.getElementById('gtWalk').style.display !== 'none',
    { timeout: 30000 });
  const walkAI = await page.$eval('#gtWalk', el => el.textContent);
  check('second miss: the professor walks it through, reasoning to the answer',
    /step by step/.test(walkAI) && /function/.test(walkAI), walkAI.slice(0, 80));
  await page.screenshot({ path: 'gate-shot-4-walkthrough.png' });
  await page.waitForFunction(
    () => /Try again/.test(document.getElementById('gtStatus').textContent),
    { timeout: 30000 });
  await answer(page,
    'A model is a function that was shown so many examples that its guesses became good');
  await page.waitForFunction(
    () => /Question 2 of 4/.test(document.getElementById('gtProgress').textContent),
    { timeout: 30000 });
  check('the taught answer lands the question and advances', true);
  const logAI = await logOf(page);
  const aiStep = logAI.find(e => e.kind === 'gate-step' &&
    e.classId === AI && e.step === 0);
  check('the pass is recorded with its 3 attempts',
    !!aiStep && aiStep.status === 'pass' && aiStep.attempts === 3,
    aiStep ? JSON.stringify(aiStep) : 'missing');

  /* ============ 5. Six-class sample across sections ============
     First gated class of six different sections, each in a fresh
     profile: lesson presented first, then question 1 driven
     wrong -> held -> right -> advance. Proves the machinery is
     general, not flagship-only. */
  const CAT = JSON.parse(fs.readFileSync('catalogue.json', 'utf8'));
  function rightAnswer(st) {
    if (st.kind === 'number') return String(st.answer);
    if (st.kind === 'exact') return st.answer;
    if (st.kind === 'keywords') return st.keywords.map(g => g[0]).join(' ');
    return st.answer || '';
  }
  const sampleSecs = ['cosmology', 'galactic', 'particle', 'nuclear',
    'mathematical', 'geophysics'];
  for (const secId of sampleSecs) {
    const sec = CAT.sections.find(s => s.id === secId);
    const cls = sec.classes.find(c => GATE[c.id] && GATE[c.id].steps.length);
    const ctx = await browser.createBrowserContext();
    const p2 = await ctx.newPage();
    await p2.setViewport({ width: 1280, height: 1000 });
    p2.on('pageerror', e => console.log('PAGE ERROR (' + secId + '):', e.message));
    await p2.evaluateOnNewDocument(FAKE_SR);
    await openClass(p2, secId, cls.id);
    await beginQuestions(p2, cls.id);
    const st = GATE[cls.id].steps[0];
    const qBefore = await q(p2);
    await answer(p2, st.kind === 'number' ? '424242' : 'I have not learned this yet');
    await p2.waitForFunction(
      () => /Not yet/.test(document.getElementById('gtStatus').textContent),
      { timeout: 20000 });
    check('sample ' + secId + ': a wrong answer holds question 1',
      (await q(p2)) === qBefore);
    await p2.waitForFunction(
      () => /Try again/.test(document.getElementById('gtStatus').textContent),
      { timeout: 45000 });
    await answer(p2, rightAnswer(st));
    await p2.waitForFunction(
      () => /Question 2 of/.test(document.getElementById('gtProgress').textContent) ||
            document.getElementById('gtGrade').style.display !== 'none',
      { timeout: 30000 });
    check('sample ' + secId + ': the taught answer advances (' +
      cls.id.slice(0, 34) + ')', true);
    await ctx.close();
  }

  /* ============ 6. Containment audit over ALL classes =========
     Independent JS implementation of Bill's law: a question ships
     only if its answer is present in the class's taught lesson.
     Numbers are extracted from the lesson text (plain, e-notation,
     and x10^ forms); keyword questions need their required idea
     groups present; nothing else may exist. */
  const SUP = { '\u2070': '0', '\u00B9': '1', '\u00B2': '2', '\u00B3': '3',
    '\u2074': '4', '\u2075': '5', '\u2076': '6', '\u2077': '7',
    '\u2078': '8', '\u2079': '9', '\u207B': '-' };
  function extractNumbers(text) {
    let t = String(text);
    Object.keys(SUP).forEach(k => { t = t.split(k).join(SUP[k]); });
    t = t.replace(/(\d+(?:\.\d+)?)\s*(?:×|x|\*)\s*10\s*\^\s*(-?\d+)/g, '$1e$2');
    const out = [];
    const re = /-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?/g;
    let m;
    while ((m = re.exec(t))) { const v = parseFloat(m[0]); if (isFinite(v)) out.push(v); }
    return out;
  }
  const WORDNUM = { zero: 0, one: 1, two: 2, three: 3, four: 4, five: 5,
    six: 6, seven: 7, eight: 8, nine: 9, ten: 10, first: 1, second: 2 };
  let audited = 0, auditBad = [];
  for (const [cid, entry] of Object.entries(GATE)) {
    const lessonText = (entry.lesson || []).map(c => c.teach).join(' ');
    const norm = lessonText.toLowerCase();
    const nums = extractNumbers(lessonText);
    for (const st of entry.steps) {
      audited++;
      let ok = true, why = '';
      if (st.kind === 'number') {
        ok = nums.some(v => Math.abs(v - st.answer) <=
          Math.max(0.02, Math.abs(st.answer) * 0.03));
        if (!ok) {
          const w = Object.keys(WORDNUM).find(k => WORDNUM[k] === st.answer);
          if (w && new RegExp('\\b' + w + '\\b').test(norm)) ok = true;
        }
        why = 'value ' + st.answer + ' not in lesson';
      } else if (st.kind === 'keywords') {
        const hit = st.keywords.filter(g =>
          g.some(a => norm.includes(a.toLowerCase()))).length;
        ok = hit >= st.need; why = 'only ' + hit + ' of ' + st.need + ' idea groups in lesson';
      } else if (st.kind === 'exact') {
        ok = norm.includes(st.answer.toLowerCase()); why = 'answer not in lesson';
      } else {
        ok = false; why = 'untaught step kind survives: ' + st.kind;
      }
      if (!ok) auditBad.push(cid + ' [' + st.kind + ']: ' + why);
    }
  }
  check('containment audit: every question\u2019s answer is in its class\u2019s lesson',
    auditBad.length === 0,
    audited + ' questions audited, ' + auditBad.length + ' failures' +
    (auditBad.length ? ' — first: ' + auditBad[0] : ''));

  /* ============ 6b. the MC audit: every stored choice set ======
     For every question carrying choices: the marked answer must be
     among them, and every distractor must itself come from the
     lesson — a value the lesson prints, clearly outside grading
     tolerance of the answer, or text the lesson contains. */
  let mcSets = 0, mcBad = [];
  for (const [cid, c] of Object.entries(GATE)) {
    const lessonText = (c.lesson || []).map(x => x.teach).join('\n');
    const lessonNorm = lessonText.toLowerCase()
      .replace(/[^a-z0-9. ]/g, ' ').replace(/\s+/g, ' ');
    const lessonNums = extractNumbers(lessonText);
    for (const st of c.steps) {
      if (!st.choices) continue;
      mcSets++;
      if (!st.mcAnswer || !st.choices.includes(st.mcAnswer))
        mcBad.push(cid + ': marked answer not among the choices');
      if (st.choices.length < 2 || st.choices.length > 4)
        mcBad.push(cid + ': choice count ' + st.choices.length);
      if (new Set(st.choices).size !== st.choices.length)
        mcBad.push(cid + ': duplicate choices');
      for (const t of st.choices) {
        if (t === st.mcAnswer) continue;
        if (st.kind === 'number') {
          const v = extractNumbers(t)[0];
          const rel = st.answer === 0 ? (v === 0 ? 0 : 9)
            : Math.abs(v - st.answer) / Math.abs(st.answer);
          if (!(rel > Math.max(0.06, 2 * (st.tol || 0.03))))
            mcBad.push(cid + ': distractor within tolerance: ' + t);
          if (!lessonNums.some(x => Math.abs(x - v) <=
              Math.max(0.02, Math.abs(v) * 0.03)))
            mcBad.push(cid + ': distractor value not in lesson: ' + t);
        } else if (st.kind === 'keywords') {
          const nt = t.toLowerCase().replace(/[^a-z0-9. ]/g, ' ')
            .replace(/\s+/g, ' ').trim();
          /* verbatim lesson text, or — for a hand-authored option —
             a list built purely from the lesson's own vocabulary:
             every content word present in the lesson */
          const words = nt.split(' ')
            .map(w => w.replace(/^\.+|\.+$/g, ''))
            .filter(w => w.length >= 3);
          if (!lessonNorm.includes(nt) &&
              !(words.length && words.every(w => lessonNorm.includes(w))))
            mcBad.push(cid + ': distractor text not in lesson: ' +
              t.slice(0, 40));
        }
      }
    }
  }
  check('MC audit: every distractor comes from the lesson ' +
    '(' + mcSets + ' choice sets)',
    mcBad.length === 0,
    mcSets + ' sets audited, ' + mcBad.length + ' failures' +
    (mcBad.length ? ' — first: ' + mcBad[0] : ''));

  /* ============ 6c. plumbing, cold — Bill's screenshot class ====
     The class from his 04:14 EST screenshot: it must now open on
     the lesson, ask plainly, show the choices BY DEFAULT, and a
     right pick must land as a plain (unassisted) pass. The gate
     data request must carry the build stamp (?v=). A reload in the
     same context — the warm-cache return — must serve the same
     new build. */
  const pp = await browser.newPage();
  await pp.setViewport({ width: 390, height: 844 });
  const gateReqs = [];
  pp.on('request', r => {
    if (/gate-data\.json/.test(r.url())) gateReqs.push(r.url());
  });
  pp.on('pageerror', e => console.log('PAGE ERROR (plumbing):', e.message));
  await pp.goto(BASE + '#class/trades/plumbing-i-water-in-water-out',
    { waitUntil: 'networkidle2', timeout: 60000 });
  await pp.waitForSelector('#gateBox', { visible: true, timeout: 20000 });
  const PC = GATE['plumbing-i-water-in-water-out'];
  check('plumbing opens on its lesson (lesson first)',
    await disp(pp, 'gtLesson') !== 'none');
  check('plumbing data: the killed order question is GONE',
    !JSON.stringify(PC).includes('which unit comes next'),
    PC.steps.map(s => s.q).join(' | ').slice(0, 120));
  check('plumbing data: lesson first, then plain questions',
    PC.lesson.length >= 3 && /in your own words/i.test(PC.steps[0].q),
    PC.steps[0].q);
  await pp.click('#gtBeginLesson');
  for (let i = 0; i < 12; i++) {
    const done = await pp.evaluate(() =>
      document.getElementById('gtBegin').style.display !== 'none');
    if (done) break;
    await pp.click('#gtContinue'); await sleep(200);
  }
  await pp.click('#gtBegin');
  await pp.waitForFunction(
    () => document.querySelectorAll('#gtChoices .gtChoice').length >= 2,
    { timeout: 20000 });
  const pOpts = await pp.$$eval('#gtChoices .gtChoice',
    els => els.map(e => e.textContent));
  check('plumbing: choices on the board BY DEFAULT, before any help',
    pOpts.length >= 2 && pOpts.includes(PC.steps[0].mcAnswer),
    pOpts.join(' | '));
  check('plumbing: gate data fetched with the build stamp (?v=)',
    gateReqs.some(u => /gate-data\.json\?v=/.test(u)), gateReqs.join(' '));
  await pp.evaluate((correct) => {
    const b = Array.from(document.querySelectorAll('#gtChoices .gtChoice'))
      .find(x => x.textContent !== correct);
    b.click();
  }, PC.steps[0].mcAnswer);
  await sleep(400);
  check('plumbing: a wrong pick holds the question',
    /Question 1 of/.test(await pp.$eval('#gtProgress',
      el => el.textContent)));
  await pp.evaluate((correct) => {
    const b = Array.from(document.querySelectorAll('#gtChoices .gtChoice'))
      .find(x => x.textContent === correct);
    b.click();
  }, PC.steps[0].mcAnswer);
  await pp.waitForFunction(
    () => /Question 2 of/.test(
      document.getElementById('gtProgress').textContent),
    { timeout: 20000 });
  const plog = await logOf(pp);
  const pstep = plog.find(e => e.kind === 'gate-step' &&
    e.classId === 'plumbing-i-water-in-water-out' && e.step === 0);
  check('plumbing: the right pick is a PLAIN pass (picking is not assisted)',
    !!pstep && pstep.status === 'pass' && !pstep.assisted,
    pstep ? JSON.stringify(pstep) : 'missing');
  await pp.reload({ waitUntil: 'networkidle2', timeout: 60000 });
  await pp.waitForSelector('#gateBox', { visible: true, timeout: 20000 });
  /* a returning student goes straight to their questions — what
     must hold on the warm-cache return is that the question in
     front of them is the NEW build's plain question, not the
     killed one */
  await pp.waitForFunction(
    () => /Question 2 of/.test(
      document.getElementById('gtProgress').textContent),
    { timeout: 20000 });
  check('plumbing, warm-cache return: still the new build\u2019s questions',
    (await q(pp)) === PC.steps[1].q, await q(pp));
  await pp.close();

  await browser.close();
  console.log(failures === 0 ? 'ALL CHECKS PASSED' : failures + ' CHECK(S) FAILED');
  process.exit(failures === 0 ? 0 : 1);
})().catch(e => { console.error('ERROR', e); process.exit(2); });
