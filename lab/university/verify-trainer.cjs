/* Browser verification for the language trainer (Rosetta-style).
   Drives the REAL Spanish classroom in headless Chrome:
   - fake media device supplies the microphone (waveform must animate)
   - SpeechRecognition is stubbed with a controllable transcript so the
     GATE can be exercised deterministically: pass advances + the big
     green check lands; miss holds the phrase and re-models slowly.
   - mastery must land in localStorage 'dave_lab_log' and persist.
   A second pass deletes SpeechRecognition to prove the self-check
   fallback renders and records.
   Run: NODE_PATH=<owner-lane browser node_modules> node verify-trainer.cjs <baseUrl>
*/
'use strict';
const puppeteer = require('puppeteer-core');

const BASE = process.argv[2] || 'http://127.0.0.1:8931/';
const URL_ES = BASE + '#class/languages/espanol-i-speak-from-zero';
const EXE = '/home/hatch/.cache/puppeteer/chrome/linux-156.0.8078.47/chrome-linux64/chrome';
const sleep = ms => new Promise(r => setTimeout(r, ms));
let failures = 0;
function check(name, cond, extra) {
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' — ' + extra : ''));
  if (!cond) failures++;
}

const FAKE_SR = `
  window.__stubHeard = 'hola';
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

async function canvasStats(page) {
  return page.evaluate(() => {
    const cv = document.getElementById('trWave');
    const ctx = cv.getContext('2d');
    const d = ctx.getImageData(0, 0, cv.width, cv.height).data;
    let green = 0;
    for (let i = 0; i < d.length; i += 4) {
      if (d[i + 1] > 150 && d[i] < 140 && d[i + 2] < 170) green++;
    }
    return { green, dataUrl: cv.toDataURL() };
  });
}

(async () => {
  const browser = await puppeteer.launch({
    executablePath: EXE, headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage',
           '--disable-gpu', '--no-first-run', '--no-proxy-server',
           '--ignore-certificate-errors',
           '--use-fake-device-for-media-stream', '--use-fake-ui-for-media-stream',
           '--autoplay-policy=no-user-gesture-required', '--window-size=1280,1000']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 1000 });
  page.on('pageerror', e => console.log('PAGE ERROR:', e.message));
  await page.evaluateOnNewDocument(FAKE_SR);
  await page.goto(URL_ES, { waitUntil: 'networkidle2', timeout: 60000 });

  await page.waitForSelector('#trainerBox', { visible: true, timeout: 20000 });
  check('trainer renders in the Spanish classroom', true);
  const phrase0 = await page.$eval('#trPhrase', el => el.textContent);
  check('first phrase is Hola', phrase0 === 'Hola', phrase0);
  const meaning0 = await page.$eval('#trMeaning', el => el.textContent);
  check('meaning shown under the phrase', /hello/.test(meaning0), meaning0);
  const dots = await page.$$eval('#trDots .dot', els => els.length);
  check('17 step dots for Lesson 1', dots === 17, String(dots));
  await page.screenshot({ path: 'trainer-shot-1-step.png' });

  /* ---- PASS flow: 'hola' must land the green check and advance ---- */
  let checkSeen = false, waveAnim = false, waveGreen = 0;
  const watcher = (async () => {
    let prev = null;
    for (let i = 0; i < 220 && !checkSeen; i++) {
      const st = await page.evaluate(() => ({
        on: document.getElementById('trBoardCheck').classList.contains('on'),
        status: document.getElementById('trStatus').textContent
      })).catch(() => ({ on: false, status: '' }));
      if (st.on) {
        checkSeen = true;
        await page.evaluate(() => window.scrollTo(0, 0));
        await sleep(200);
        await page.screenshot({ path: 'trainer-shot-2-greencheck.png' });
      }
      if (/is listening/.test(st.status)) {
        const a = await canvasStats(page);
        await sleep(260);
        const b = await canvasStats(page);
        if (a.dataUrl !== b.dataUrl) waveAnim = true;
        waveGreen = Math.max(waveGreen, a.green, b.green);
      }
      await sleep(180);
    }
  })();
  await page.click('#trBegin');
  await page.waitForFunction(
    () => document.getElementById('trPhrase').textContent === 'Buenos días',
    { timeout: 60000 });
  check('PASS advances to phrase 2', true);
  await watcher;
  check('big green check appeared on the board during praise', checkSeen);
  check('waveform bar animated while listening (fake mic)', waveAnim, 'max green px ' + waveGreen);
  check('waveform actually shows voice energy (green pixels)', waveGreen > 300, String(waveGreen));
  const status1 = await page.$eval('#trStatus', el => el.textContent);
  const log1 = await page.evaluate(() => JSON.parse(localStorage.getItem('dave_lab_log') || '[]'));
  const hola = log1.find(e => e.kind === 'phrase-mastery' && e.phrase === 'Hola');
  check('mastery for Hola written to dave_lab_log', !!hola, hola ? hola.classId : 'missing');
  check('mastery entry keeps hours untouched (minutes 0)', hola && hola.minutes === 0);

  /* ---- MISS flow: garbage must HOLD the phrase ---- */
  await page.evaluate(() => { window.__stubHeard = 'banana pancake seven'; });
  await page.waitForFunction(
    () => /Not yet/.test(document.getElementById('trStatus').textContent),
    { timeout: 45000 });
  const phraseMiss = await page.$eval('#trPhrase', el => el.textContent);
  check('MISS holds the phrase (no advance)', phraseMiss === 'Buenos días', phraseMiss);
  const checkOnMiss = await page.evaluate(
    () => document.getElementById('trBoardCheck').classList.contains('on'));
  check('no green check on a miss', !checkOnMiss);
  const heardShown = await page.$eval('#trHeard', el => el.textContent);
  check('student is shown what was heard', /banana pancake seven/.test(heardShown), heardShown);

  /* ---- recovery: after the slow re-model, a good attempt passes ---- */
  await page.evaluate(() => { window.__stubHeard = 'buenos días'; });
  await page.waitForFunction(
    () => document.getElementById('trPhrase').textContent === 'Buenas tardes',
    { timeout: 60000 });
  check('retry after miss passes and advances', true);

  /* ---- persistence: mastered dots survive a reload ---- */
  await page.reload({ waitUntil: 'networkidle2' });
  await page.waitForSelector('#trainerBox', { visible: true, timeout: 20000 });
  await sleep(800);
  const dotClasses = await page.$$eval('#trDots .dot', els => els.map(e => e.className));
  check('mastered phrases persist after reload',
    /done/.test(dotClasses[0]) && /done/.test(dotClasses[1]), dotClasses.slice(0, 3).join(' | '));
  const resumePhrase = await page.$eval('#trPhrase', el => el.textContent);
  check('trainer resumes at first unmastered phrase', resumePhrase === 'Buenas tardes', resumePhrase);

  /* ---- FALLBACK: no SpeechRecognition -> self-check mode ----
     Isolated browser context: page 1's localStorage already carries
     mastery, and the fallback flow must start from phrase 1. */
  const ctx2 = await browser.createBrowserContext();
  const page2 = await ctx2.newPage();
  await page2.setViewport({ width: 1280, height: 1000 });
  await page2.evaluateOnNewDocument(() => {
    window.SpeechRecognition = undefined;
    window.webkitSpeechRecognition = undefined;
  });
  await page2.goto(URL_ES, { waitUntil: 'networkidle2', timeout: 60000 });
  await page2.waitForSelector('#trainerBox', { visible: true, timeout: 20000 });
  const fbStart = await page2.$eval('#trPhrase', el => el.textContent);
  check('fallback run starts at phrase 1 (fresh record)', fbStart === 'Hola', fbStart);
  await page2.click('#trBegin');
  await page2.waitForFunction(
    () => document.getElementById('trFallbackNote').style.display !== 'none',
    { timeout: 20000 });
  const fbText = await page2.$eval('#trFallbackNote', el => el.textContent);
  check('fallback states plainly why (browser cannot listen)', /Chrome and Edge/.test(fbText), fbText.slice(0, 60) + '…');
  await page2.waitForFunction(
    () => document.getElementById('trRecord').style.display !== 'none',
    { timeout: 30000 });
  check('self-check offers recording', true);
  await page2.click('#trRecord');
  await sleep(1200);
  await page2.click('#trRecord'); // stop
  await page2.waitForFunction(
    () => document.getElementById('trYes').style.display !== 'none',
    { timeout: 15000 });
  check('own recording plays back and self-grade buttons appear', true);
  await page2.screenshot({ path: 'trainer-shot-3-fallback.png' });
  await page2.click('#trYes');
  await page2.waitForFunction(
    () => document.getElementById('trPhrase').textContent === 'Buenos días',
    { timeout: 30000 });
  const log2 = await page2.evaluate(() => JSON.parse(localStorage.getItem('dave_lab_log') || '[]'));
  const selfEntry = log2.find(e => e.kind === 'phrase-mastery' && e.phrase === 'Hola');
  check('self-check mastery logged, flagged selfChecked',
    !!selfEntry && selfEntry.selfChecked === true);

  await browser.close();
  console.log(failures ? `\n${failures} FAILURES` : '\nALL BROWSER CHECKS PASSED');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error('VERIFY ERROR:', e.message); process.exit(2); });
