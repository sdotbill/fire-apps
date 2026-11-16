/* Browser verification for the general classroom gate.
   Drives three real classrooms in headless Chrome:
     1. a College flagship (cosmology — The Bounce & the Aldred Limit):
        right answer advances + the big green check lands; a WRONG
        value holds the step and the re-teach appears; the capstone is
        skipped and the skip is recorded as a skip; the finished set
        writes a class-grade entry to dave_lab_log.
     2. an authored class (Numbers & Proof): a unit-order answer typed
        in full advances.
     3. a generated paper class (snow avalanches): a typed value
        passes, then the VOICE path — SpeechRecognition stubbed with
        the correct value — fills, checks, and advances.
   Run: NODE_PATH=<owner-lane browser node_modules> node verify-gate.cjs <baseUrl>
*/
'use strict';
const puppeteer = require('puppeteer-core');

const BASE = process.argv[2] || 'http://127.0.0.1:8932/';
const EXE = '/home/hatch/.cache/puppeteer/chrome/linux-156.0.8078.47/chrome-linux64/chrome';
const sleep = ms => new Promise(r => setTimeout(r, ms));
let failures = 0;
function check(name, cond, extra) {
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' — ' + extra : ''));
  if (!cond) failures++;
}

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
  check('gate renders in the flagship classroom', true);
  const dots = await page.$$eval('#gtDots .dot', els => els.length);
  check('flagship has 3 gated steps', dots === 3, String(dots));
  await page.screenshot({ path: 'gate-shot-1-flagship.png' });
  await page.click('#gtBegin');
  await sleep(600);

  /* step 0 — DOI, typed right: advance + green check */
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
  const q0 = await q(page);
  check('step 0 asks the DOI', /DOI/.test(q0), q0.slice(0, 60));
  await answer(page, '10.5281/zenodo.24147907');
  await page.waitForFunction(
    () => /eps_mid/.test(document.getElementById('gtQ').textContent),
    { timeout: 30000 });
  check('right answer advances to the value step', true);
  await watcher;
  check('big green check appeared on the board', checkSeen);

  /* step 1 — wrong value: HOLD + re-teach */
  await answer(page, '0.9');
  await page.waitForFunction(
    () => /Not yet/.test(document.getElementById('gtStatus').textContent),
    { timeout: 15000 });
  const qMiss = await q(page);
  check('wrong value holds the step (no advance)', /eps_mid/.test(qMiss), qMiss.slice(0, 60));
  const teach2 = await page.$eval('#gtTeach', el => el.textContent);
  check('miss brings the re-teach (value stated plainly)', /eps_mid = 0.45/.test(teach2),
    teach2.slice(0, 80));
  const checkOnMiss = await page.evaluate(
    () => document.getElementById('trBoardCheck').classList.contains('on'));
  check('no green check on a miss', !checkOnMiss);

  /* retry — right value: advance to the capstone. Wait until the
     re-teach clip has finished and the gate invites the retry
     (the gate is busy while the professor is speaking). */
  await page.waitForFunction(
    () => /Try again/.test(document.getElementById('gtStatus').textContent),
    { timeout: 30000 });
  await answer(page, '0.45');
  await page.waitForFunction(
    () => /Binary-Pulsar/.test(document.getElementById('gtQ').textContent),
    { timeout: 30000 });
  check('retry with the right value advances', true);

  /* capstone — skip: recorded as a skip, set completes, grade lands */
  await page.click('#gtSkip');
  await page.waitForFunction(
    () => document.getElementById('gtGrade').style.display !== 'none',
    { timeout: 15000 });
  const gradeText = await page.$eval('#gtGrade', el => el.textContent);
  check('grade panel reports 2 landed + 1 skip',
    /2 of 3 steps landed/.test(gradeText) && /1 skipped/.test(gradeText), gradeText.slice(0, 110));
  const log1 = await logOf(page);
  const steps1 = log1.filter(e => e.kind === 'gate-step' &&
    e.classId === 'the-bounce-the-aldred-limit');
  check('gate-step records: pass, pass, skip',
    steps1.map(e => e.status).join(',') === 'pass,pass,skip',
    steps1.map(e => e.status).join(','));
  check('the missed step recorded its attempts', steps1[1] && steps1[1].attempts === 2,
    steps1[1] ? String(steps1[1].attempts) : 'missing');
  const grade1 = log1.find(e => e.kind === 'class-grade' &&
    e.classId === 'the-bounce-the-aldred-limit');
  check('class-grade entry written, complete, 67%',
    !!grade1 && grade1.complete === true && grade1.passed === 2 &&
    grade1.skipped === 1 && grade1.percent === 67,
    grade1 ? JSON.stringify(grade1) : 'missing');
  check('grade entry keeps hours untouched (minutes 0)', grade1 && grade1.minutes === 0);

  /* persistence: dots survive a reload in their recorded states */
  await page.reload({ waitUntil: 'networkidle2' });
  await page.waitForSelector('#gateBox', { visible: true, timeout: 20000 });
  await sleep(500);
  const dotCls = await page.$$eval('#gtDots .dot', els => els.map(e => e.className));
  check('states persist after reload (done, done, skipped)',
    /done/.test(dotCls[0]) && /done/.test(dotCls[1]) && /skipped/.test(dotCls[2]),
    dotCls.join(' | '));

  /* ============ 2. Authored class: Numbers & Proof ============ */
  await openClass(page, 'mathematics', 'numbers-proof-foundations-of-mathematics');
  await page.click('#gtBegin');
  await sleep(500);
  const qA = await q(page);
  check('authored step asks the unit order', /Counting and the natural numbers/.test(qA),
    qA.slice(0, 70));
  await answer(page, 'Integers, rationals, and why fractions behave');
  await page.waitForFunction(
    () => /Step 2 of 5/.test(document.getElementById('gtProgress').textContent),
    { timeout: 30000 });
  check('typed unit title passes and advances', true);
  const log2 = await logOf(page);
  check('authored pass recorded in the log',
    log2.some(e => e.kind === 'gate-step' &&
      e.classId === 'numbers-proof-foundations-of-mathematics' && e.status === 'pass'));

  /* ============ 3. Generated paper class: snow avalanches ============ */
  await openClass(page, 'particle',
    'snow-avalanches-slab-fracture-and-powder-clouds-release-fracture');
  await page.click('#gtBegin');
  await sleep(500);
  const qG = await q(page);
  check('generated step asks a headline value', /runout beyond beta point/.test(qG),
    qG.slice(0, 70));
  await answer(page, '197.61');
  await page.waitForFunction(
    () => /flexural response speed/.test(document.getElementById('gtQ').textContent),
    { timeout: 30000 });
  check('typed value passes and advances', true);
  /* voice path: the stubbed recognizer says the value out loud */
  let waveSeen = false;
  const waveWatch = (async () => {
    for (let i = 0; i < 40 && !waveSeen; i++) {
      const disp = await page.evaluate(
        () => document.getElementById('gtWave').style.display).catch(() => 'none');
      if (disp === 'block') waveSeen = true;
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

  await browser.close();
  console.log(failures ? `\n${failures} FAILURES` : '\nALL GATE BROWSER CHECKS PASSED');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error('VERIFY ERROR:', e.message); process.exit(2); });
