/* Browser verification for the AI & Computing syllabus path and the
   lesson-start wiring (Bill, Nov 16 2026: "I want to be able to do
   the full syllabus for AI and computing — that's where I want to
   start my schooling").
   Drives, in headless Chrome:
     1. the catalogue: the AI & Computing section renders as a
        numbered path (catalogue order, fundamentals first), every
        class "Not started" with a Start door;
     2. a seeded class-grade in dave_lab_log marks Machine Learning I
        Completed on the path after reload;
     3. the AI Fundamentals classroom: entering presents gated step 1
        ready to begin; a WRONG answer holds the step with the
        re-teach; the RIGHT answer lands the big green check and
        advances; the pass is recorded in the log;
     4. the Ask-the-professor box: "lets start lesson 1" STARTS the
        gated lesson (no live-office-hours deflection);
     5. back at the catalogue door, the path now shows AI
        Fundamentals "In progress — 1 step landed / Continue";
     6. a fresh student on AI Fundamentals step 1: the multiple
        choices are on the board BY DEFAULT (Bill, Nov 16 04:16 —
        multiple choice first), exactly the set the generator
        stored from the class's own material; the help button then
        adds a hint from the step's own material; a wrong pick
        holds the step; the right pick advances — and because the
        hint was taken, the log records the pass as ASSISTED.
   Run: NODE_PATH=<owner-lane browser node_modules> node verify-ai-path.cjs <baseUrl>
*/
'use strict';
const puppeteer = require('puppeteer-core');

const BASE = process.argv[2] || 'http://127.0.0.1:8933/';
const EXE = '/home/hatch/.cache/puppeteer/chrome/linux-156.0.8078.47/chrome-linux64/chrome';
const sleep = ms => new Promise(r => setTimeout(r, ms));
let failures = 0;
function check(name, cond, extra) {
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' — ' + extra : ''));
  if (!cond) failures++;
}

const AI_SEC = 'ai-computing';
const AI_FUND = 'ai-fundamentals-what-a-mind-made-of-math-is';
const ML_I = 'machine-learning-i-how-machines-learn-from-data';
const EXPECTED_ORDER = [/AI Fundamentals/, /Machine Learning I/, /^Agents/,
                        /Computing Foundations/, /^Data —/];

async function openSection(page) {
  const det = await page.$('details.section[data-section="' + AI_SEC + '"]');
  if (!det) throw new Error('ai-computing section not rendered');
  const open = await page.evaluate(
    el => el.open, det);
  if (!open) await page.$eval(
    'details.section[data-section="' + AI_SEC + '"] summary',
    el => el.click());
  await sleep(300);
}
const pathRows = page => page.$$eval(
  'details.section[data-section="' + AI_SEC + '"] .pathRow',
  els => els.map(e => ({
    n: e.querySelector('.pnum').textContent.trim(),
    title: e.querySelector('.ct').textContent.trim(),
    prog: e.querySelector('.pprog').textContent.trim(),
    btn: e.querySelector('button').textContent.trim(),
    cls: e.className
  })));
const q = page => page.$eval('#gtQ', el => el.textContent);
const logOf = page => page.evaluate(
  () => JSON.parse(localStorage.getItem('dave_lab_log') || '[]'));

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

  /* ============ 1. the path renders, in order, all unstarted ============ */
  await page.goto(BASE, { waitUntil: 'networkidle2', timeout: 60000 });
  await page.waitForSelector('details.section[data-section="' + AI_SEC + '"]',
    { timeout: 20000 });
  await openSection(page);
  let rows = await pathRows(page);
  check('path has 5 classes', rows.length === 5, String(rows.length));
  check('path is numbered 1–5 in order',
    rows.map(r => r.n).join(',') === '1,2,3,4,5', rows.map(r => r.n).join(','));
  check('path order is the catalogue order (fundamentals first)',
    rows.every((r, i) => EXPECTED_ORDER[i].test(r.title)),
    rows.map(r => r.title).join(' | '));
  check('every class starts unstarted, with a Start door',
    rows.every(r => r.prog === 'Not started' && r.btn === 'Start →'),
    rows.map(r => r.prog + '/' + r.btn).join(' | '));

  /* ============ 2. a completed grade shows on the path ============ */
  await page.evaluate((mlId) => {
    const log = JSON.parse(localStorage.getItem('dave_lab_log') || '[]');
    log.push({
      date: new Date().toISOString(), minutes: 0, stations: ['university'],
      stepsCompleted: 4, classId: mlId,
      classTitle: 'Machine Learning I — How Machines Learn From Data',
      kind: 'class-grade', passed: 4, skipped: 0, total: 4,
      attempts: 5, percent: 100, complete: true
    });
    localStorage.setItem('dave_lab_log', JSON.stringify(log));
  }, ML_I);
  await page.reload({ waitUntil: 'networkidle2' });
  await page.waitForSelector('details.section[data-section="' + AI_SEC + '"]',
    { timeout: 20000 });
  await openSection(page);
  rows = await pathRows(page);
  check('Machine Learning I shows Completed from the record',
    /✓ Completed/.test(rows[1].prog) && rows[1].btn === 'Review the lesson →',
    rows[1].prog + ' / ' + rows[1].btn);
  check('AI Fundamentals still Not started',
    rows[0].prog === 'Not started', rows[0].prog);

  /* ============ 3. AI Fundamentals: the gated lesson ============ */
  await page.goto(BASE + '#class/' + AI_SEC + '/' + AI_FUND,
    { waitUntil: 'networkidle2', timeout: 60000 });
  await page.waitForSelector('#gateBox', { visible: true, timeout: 20000 });
  /* lesson-first (Bill's law, Nov 16): the class is TAUGHT before
     any question exists on the page */
  const lessonShown = await page.$eval('#gtLesson',
    el => el.style.display !== 'none');
  const lessonPart1 = await page.$eval('#gtLessonText', el => el.textContent);
  check('entering the class presents the LESSON first',
    lessonShown && /a model is a function/.test(lessonPart1),
    lessonPart1.slice(0, 70));
  await page.screenshot({ path: 'ai-shot-1-lesson-presented.png' });
  await page.click('#gtBeginLesson');
  for (let i = 0; i < 5; i++) { await page.click('#gtContinue'); await sleep(150); }
  await page.waitForFunction(
    () => document.getElementById('gtBegin').style.display !== 'none',
    { timeout: 15000 });
  const beginVisible = await page.$eval('#gtBegin',
    el => el.style.display !== 'none');
  check('after the lesson, the questions door is showing', beginVisible);
  await page.click('#gtBegin');
  await sleep(600);
  const q0 = await q(page);
  check('question 1 asks only what the lesson taught (what a model is)',
    /what is a model/.test(q0), q0.slice(0, 70));

  /* wrong answer: HOLD + re-teach, no green check */
  await page.$eval('#gtInput', el => { el.value = 'quantum bananas from outer space'; });
  await page.click('#gtCheck');
  await page.waitForFunction(
    () => /teaches it again/.test(document.getElementById('gtStatus').textContent),
    { timeout: 15000 });
  check('wrong answer holds the question (no advance)',
    /what is a model/.test(await q(page)));
  const checkOnMiss = await page.evaluate(
    () => document.getElementById('trBoardCheck').classList.contains('on'));
  check('no green check on a miss', !checkOnMiss);

  /* right answer: green check + advance */
  await page.waitForFunction(
    () => /Try again/.test(document.getElementById('gtStatus').textContent),
    { timeout: 30000 });
  let checkSeen = false;
  const watcher = (async () => {
    for (let i = 0; i < 80 && !checkSeen; i++) {
      const on = await page.evaluate(
        () => document.getElementById('trBoardCheck').classList.contains('on')
      ).catch(() => false);
      if (on) {
        checkSeen = true;
        await page.screenshot({ path: 'ai-shot-2-greencheck.png' });
      }
      await sleep(150);
    }
  })();
  await page.$eval('#gtInput',
    el => { el.value = 'A model is a function that was shown so many examples that its guesses became good'; });
  await page.click('#gtCheck');
  await page.waitForFunction(
    () => /Question 2 of/.test(document.getElementById('gtProgress').textContent),
    { timeout: 30000 });
  check('right answer advances to question 2', true);
  await watcher;
  check('big green check appeared on the board', checkSeen);
  const log1 = await logOf(page);
  check('the pass is recorded in the University record',
    log1.some(e => e.kind === 'gate-step' && e.classId === AI_FUND &&
      e.step === 0 && e.status === 'pass'));

  /* ============ 4. the Ask box: "lets start lesson 1" ============ */
  await page.reload({ waitUntil: 'networkidle2' });
  await page.waitForSelector('#gateBox', { visible: true, timeout: 20000 });
  await sleep(400);
  await page.click('.deskbar button[data-panel="ask"]');
  await page.$eval('#askInput', el => { el.value = 'lets start lesson 1'; });
  await page.click('#btnAsk');
  await sleep(800);
  const lessonOpen = await page.$eval('#panel-lesson',
    el => el.classList.contains('open'));
  check('ask intent switches to the lesson panel', lessonOpen);
  const inputShown = await page.$eval('#gtInput',
    el => el.style.display !== 'none');
  const checkShown = await page.$eval('#gtCheck',
    el => el.style.display !== 'none');
  check('ask intent STARTS the gated lesson (answer box + check live)',
    inputShown && checkShown);
  const askText = await page.$eval('#askLog', el => el.textContent);
  check('no live-office-hours deflection',
    !/live office hours/.test(askText), askText.slice(0, 90));
  check('the professor answers as a beginning, not a refusal',
    /Then we begin/.test(askText));

  /* ============ 5. the path reflects the work, live ============ */
  await page.click('#backDoor');
  await sleep(500);
  await openSection(page);
  rows = await pathRows(page);
  check('AI Fundamentals now In progress — 1 step landed, Continue door',
    /In progress — 1 step landed/.test(rows[0].prog) &&
    rows[0].btn === 'Continue →',
    rows[0].prog + ' / ' + rows[0].btn);
  check('Machine Learning I still Completed',
    /✓ Completed/.test(rows[1].prog), rows[1].prog);
  await page.screenshot({ path: 'ai-shot-3-path-progress.png' });

  /* ============ 6. stuck → hint → choices → assisted pass ============ */
  const ctx = browser.createBrowserContext
    ? await browser.createBrowserContext()
    : await browser.createIncognitoBrowserContext();
  const hp = await ctx.newPage();
  await hp.setViewport({ width: 1280, height: 1000 });
  hp.on('pageerror', e => console.log('PAGE ERROR (help):', e.message));
  await hp.goto(BASE + '#class/' + AI_SEC + '/' + AI_FUND,
    { waitUntil: 'networkidle2', timeout: 60000 });
  await hp.waitForSelector('#gateBox', { visible: true, timeout: 20000 });
  /* lesson first, then the questions */
  await hp.click('#gtBeginLesson');
  for (let i = 0; i < 5; i++) { await hp.click('#gtContinue'); await sleep(150); }
  await hp.waitForFunction(
    () => document.getElementById('gtBegin').style.display !== 'none',
    { timeout: 15000 });
  await hp.click('#gtBegin');
  /* the gate presents the question when the professor's opening
     clip ends — wait for the stuck button to actually be on it */
  await hp.waitForFunction(
    () => document.getElementById('gtHelp').style.display !== 'none',
    { timeout: 30000 });
  check('the stuck button is on the step', true);
  /* MULTIPLE CHOICE FIRST (Bill, Nov 16 04:16): the choices are on
     the board by default, before any help is asked for — read the
     expected set from the served gate data, never hardcoded */
  const STEP0 = await hp.evaluate(async (cid) => {
    const d = await (await fetch('gate-data.json')).json();
    const s = d.classes[cid].steps[0];
    return { choices: s.choices || [], mcAnswer: s.mcAnswer || null };
  }, AI_FUND);
  const CORRECT = STEP0.mcAnswer;
  await hp.waitForFunction(
    () => document.getElementById('gtChoices').style.display !== 'none' &&
      document.querySelectorAll('#gtChoices .gtChoice').length >= 2,
    { timeout: 10000 });
  const opts = await hp.$$eval('#gtChoices .gtChoice',
    els => els.map(e => e.textContent));
  check('choices are shown BY DEFAULT (multiple choice first)',
    opts.length >= 3 && opts.indexOf(CORRECT) !== -1, opts.join(' | '));
  check('the rendered choices are exactly the stored set — the ' +
    'class\u2019s own material, nothing fabricated',
    opts.slice().sort().join('\n') === STEP0.choices.slice().sort().join('\n'),
    opts.join(' | '));
  await hp.click('#gtHelp');
  await hp.waitForFunction(
    () => document.getElementById('gtHint').style.display !== 'none',
    { timeout: 10000 });
  const hintText = await hp.$eval('#gtHint', el => el.textContent);
  check('the hint is drawn from the step\u2019s own material',
    /Hint — from the material itself/.test(hintText) && hintText.length > 60,
    hintText.slice(0, 80));
  check('with the choices already up, the hint completes the help kit',
    await hp.$eval('#gtHelp', el => el.style.display === 'none'));
  await hp.screenshot({ path: 'ai-shot-4-help-choices.png' });
  /* a wrong pick: held, that choice disabled, no advance */
  await hp.evaluate((correct) => {
    const btns = Array.from(document.querySelectorAll('#gtChoices .gtChoice'));
    btns.find(b => b.textContent !== correct).click();
  }, CORRECT);
  await hp.waitForFunction(
    () => /Not that one/.test(document.getElementById('gtStatus').textContent),
    { timeout: 10000 });
  check('a wrong pick holds the step', /what is a model/.test(await q(hp)));
  /* the right pick: advance, recorded as an ASSISTED pass */
  let assistedNoteSeen = false;
  const noteWatch = (async () => {
    for (let i = 0; i < 80 && !assistedNoteSeen; i++) {
      const t = await hp.evaluate(
        () => document.getElementById('gtStatus').textContent).catch(() => '');
      if (/assisted pass/.test(t)) assistedNoteSeen = true;
      await sleep(150);
    }
  })();
  await hp.evaluate((correct) => {
    const btns = Array.from(document.querySelectorAll('#gtChoices .gtChoice'));
    btns.find(b => b.textContent === correct).click();
  }, CORRECT);
  await hp.waitForFunction(
    () => /Question 2 of/.test(document.getElementById('gtProgress').textContent),
    { timeout: 30000 });
  check('the right pick advances the lesson', true);
  await noteWatch;
  check('the student is told it landed as an assisted pass', assistedNoteSeen);
  const hlog = await logOf(hp);
  const hstep = hlog.find(e => e.kind === 'gate-step' &&
    e.classId === AI_FUND && e.step === 0);
  check('the log records the pass as ASSISTED (honest grading)',
    !!hstep && hstep.status === 'pass' && hstep.assisted === true,
    hstep ? JSON.stringify(hstep) : 'missing');
  await ctx.close();

  await browser.close();
  console.log(failures ? `\n${failures} FAILURES` : '\nALL AI-PATH BROWSER CHECKS PASSED');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error('VERIFY ERROR:', e.message); process.exit(2); });
