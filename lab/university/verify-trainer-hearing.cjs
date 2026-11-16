/* Browser verification for the trainer HEARING fix (Nov 16, 2026).
   The live failure: a student saying "hola" correctly, forever —
   the recognizer returns "ola" (the h is silent) and the old gate
   failed it by design; nothing showed what was heard; no typing
   route existed; SR errors looped "say it again" without end.
   Scenarios, all in the REAL Spanish classroom, SR stubbed:
     A clean pass ('hola')          — heard line + advance + green check
     B mis-hearing variant ('ola')  — passes, advances
     C mis-hearing variant ('holla')— passes, advances
     D typing route                 — wrong type holds, right type passes,
                                      log entry carries typed:true
     E SR 'no-speech' x2            — auto-switch to typing with one plain
                                      line, then a typed answer passes
     F getUserMedia DENIED          — SR pass still lands; typing row present
   Run: NODE_PATH=<owner-lane browser node_modules> node verify-trainer-hearing.cjs <baseUrl>
*/
'use strict';
const puppeteer = require('puppeteer-core');

const BASE = process.argv[2] || 'http://127.0.0.1:8932/';
const URL_ES = BASE + '#class/languages/espanol-i-speak-from-zero';
const EXE = '/home/hatch/.cache/puppeteer/chrome/linux-156.0.8078.47/chrome-linux64/chrome';
const sleep = ms => new Promise(r => setTimeout(r, ms));
let failures = 0;
function check(name, cond, extra) {
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' — ' + extra : ''));
  if (!cond) failures++;
}

const SR_STUB = `
  window.__srMode = window.__srMode || 'value';   /* value | error | silent */
  window.__stubHeard = window.__stubHeard || 'hola';
  window.__stubError = window.__stubError || 'no-speech';
  class FakeSR {
    constructor() { this.lang = ''; this.interimResults = false; this.maxAlternatives = 1; }
    start() {
      const mode = window.__srMode;
      if (mode === 'silent') return;              /* never answers: mic path idles */
      setTimeout(() => {
        if (mode === 'error') {
          if (this.onerror) this.onerror({ error: window.__stubError });
          setTimeout(() => { if (this.onend) this.onend(); }, 60);
          return;
        }
        if (this.onresult) {
          const txt = window.__stubHeard;
          const r = { isFinal: true, length: 1 };
          r[0] = { transcript: txt, confidence: 0.99 };
          const results = { length: 1 }; results[0] = r;
          this.onresult({ resultIndex: 0, results });
        }
        setTimeout(() => { if (this.onend) this.onend(); }, 120);
      }, 400);
    }
    abort() { if (this.onend) this.onend(); }
    stop() {}
  }
  window.SpeechRecognition = FakeSR;
  window.webkitSpeechRecognition = FakeSR;
`;

async function openClass(browser, setupJs) {
  const ctx = await browser.createBrowserContext();
  const page = await ctx.newPage();
  await page.setViewport({ width: 1280, height: 1000 });
  page.on('pageerror', e => console.log('PAGE ERROR:', e.message));
  await page.evaluateOnNewDocument(SR_STUB);
  if (setupJs) await page.evaluateOnNewDocument(setupJs);
  await page.goto(URL_ES, { waitUntil: 'networkidle2', timeout: 60000 });
  await page.waitForSelector('#trainerBox', { visible: true, timeout: 20000 });
  await page.waitForFunction(
    () => document.getElementById('trPhrase').textContent === 'Hola',
    { timeout: 20000 });
  return { ctx, page };
}

async function beginAndReachPhrase(page, timeout) {
  await page.click('#trBegin');
  await page.waitForFunction(
    () => document.getElementById('trPhrase').textContent !== 'Hola',
    { timeout: timeout || 45000 });
}

async function masteryLog(page) {
  return page.evaluate(() => {
    try {
      const log = JSON.parse(localStorage.getItem('dave_lab_log') || '[]');
      return log.filter(e => e && e.kind === 'phrase-mastery');
    } catch (e) { return []; }
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

  /* ---- A: clean pass ---- */
  {
    const { ctx, page } = await openClass(browser,
      `window.__srMode = 'value'; window.__stubHeard = 'hola';`);
    check('A: typing row is rendered', await page.$('#trType') !== null);
    await page.click('#trBegin');
    await page.waitForFunction(
      () => /It heard: “hola”/.test(document.getElementById('trHeard').textContent),
      { timeout: 45000 });
    check('A: heard line shows the transcript at grade time', true);
    await page.waitForFunction(
      () => document.getElementById('trPhrase').textContent !== 'Hola',
      { timeout: 45000 });
    check('A: clean "hola" advances to Buenos días', true);
    const log = await masteryLog(page);
    check('A: mastery logged, not typed',
      log.some(e => e.phrase === 'Hola' && e.typed === false), JSON.stringify(log));
    await ctx.close();
  }

  /* ---- B: 'ola' — the exact transcript that looped Bill ---- */
  {
    const { ctx, page } = await openClass(browser,
      `window.__srMode = 'value'; window.__stubHeard = 'ola';`);
    await page.click('#trBegin');
    await page.waitForFunction(
      () => /It heard: “ola”/.test(document.getElementById('trHeard').textContent),
      { timeout: 45000 });
    check('B: heard line shows "ola"', true);
    await page.waitForFunction(
      () => document.getElementById('trPhrase').textContent !== 'Hola',
      { timeout: 45000 });
    check('B: mis-heard "ola" passes and advances', true);
    await ctx.close();
  }

  /* ---- C: 'holla' ---- */
  {
    const { ctx, page } = await openClass(browser,
      `window.__srMode = 'value'; window.__stubHeard = 'holla';`);
    await beginAndReachPhrase(page);
    check('C: mis-heard "holla" passes and advances', true);
    await ctx.close();
  }

  /* ---- D: typing route ---- */
  {
    const { ctx, page } = await openClass(browser,
      `window.__srMode = 'silent';`);
    await page.click('#trBegin');
    await sleep(2500); /* welcome plays; mic path idles on the silent stub */
    await page.type('#trType', 'gracias');
    await page.click('#trTypeGo');
    await sleep(600);
    let phrase = await page.$eval('#trPhrase', el => el.textContent);
    check('D: typed WRONG word holds the phrase', phrase === 'Hola', phrase);
    let heard = await page.$eval('#trHeard', el => el.textContent);
    check('D: typed attempt is shown back', /You typed: “gracias”/.test(heard), heard);
    await page.evaluate(() => { document.getElementById('trType').value = ''; });
    await page.type('#trType', 'hola');
    await page.click('#trTypeGo');
    await page.waitForFunction(
      () => document.getElementById('trPhrase').textContent !== 'Hola',
      { timeout: 20000 });
    check('D: typed "hola" passes and advances', true);
    const log = await masteryLog(page);
    check('D: mastery logged as typed',
      log.some(e => e.phrase === 'Hola' && e.typed === true), JSON.stringify(log));
    await ctx.close();
  }

  /* ---- E: SR error twice -> auto typing fallback ---- */
  {
    const { ctx, page } = await openClass(browser,
      `window.__srMode = 'error'; window.__stubError = 'no-speech';`);
    await page.click('#trBegin');
    /* first listen auto-starts after the model clip and errors */
    await page.waitForFunction(
      () => /It heard: \(nothing at all\)/.test(document.getElementById('trHeard').textContent),
      { timeout: 45000 });
    check('E: first empty outcome shows "It heard: (nothing at all)"', true);
    await page.waitForSelector('#trSay', { visible: true, timeout: 10000 });
    await sleep(1500); /* let the recognizer fully end before the next tap */
    await page.click('#trSay');
    await page.waitForFunction(
      () => {
        const n = document.getElementById('trFallbackNote');
        return n && n.style.display !== 'none' && /switch to typing/.test(n.textContent);
      }, { timeout: 20000 });
    check('E: second empty outcome switches to typing with one plain line', true);
    await page.type('#trType', 'hola');
    await page.click('#trTypeGo');
    await page.waitForFunction(
      () => document.getElementById('trPhrase').textContent !== 'Hola',
      { timeout: 20000 });
    check('E: typed answer passes after the fallback', true);
    await ctx.close();
  }

  /* ---- F: microphone denied — SR and typing unblocked ---- */
  {
    const { ctx, page } = await openClass(browser, `
      window.__srMode = 'value'; window.__stubHeard = 'hola';
      if (navigator.mediaDevices) {
        navigator.mediaDevices.getUserMedia = () => Promise.reject(new Error('denied'));
      }
    `);
    await beginAndReachPhrase(page);
    check('F: with the mic denied, the SR pass still lands', true);
    check('F: typing row present with the mic denied',
      await page.$('#trType') !== null);
    await ctx.close();
  }

  await browser.close();
  console.log(failures ? failures + ' FAILURES' : 'ALL HEARING CHECKS PASS');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error('HARNESS ERROR:', e.message); process.exit(2); });
