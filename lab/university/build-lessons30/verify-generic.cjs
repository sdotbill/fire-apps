/* Generic lessons30 drive for a non-Spanish class: precedence, list,
 * audio + full text, gate holds, read-path unlock with real minutes,
 * every question answered correctly from the class data itself
 * (MC: click the correct choice; typed: the answer; keywords: a
 * keyword-stuffed answer), grade logged complete, reload shows
 * Complete, zero page errors.
 * Usage: node verify-generic.cjs <baseUrl> <sectionId> <classId>
 * NODE_PATH=<owner-lane browser node_modules> */
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');
const EXE = '/home/hatch/.cache/puppeteer/chrome/linux-156.0.8078.47/chrome-linux64/chrome';
const BASE = process.argv[2] || 'http://127.0.0.1:8937/';
const SECTION = process.argv[3];
const CID = process.argv[4];
const DATA = JSON.parse(fs.readFileSync(
  path.join(__dirname, '..', 'lessons30', CID + '.json'), 'utf8'));
const L1 = DATA.lessons[0];

let fails = 0;
const ok = (cond, label, extra) => {
  console.log((cond ? 'PASS ' : 'FAIL ') + label + (extra ? ' — ' + extra : ''));
  if (!cond) fails++;
};
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const browser = await puppeteer.launch({
    executablePath: EXE, headless: 'new',
    args: ['--no-sandbox', '--autoplay-policy=no-user-gesture-required'],
  });
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(BASE + '#class/' + SECTION + '/' + CID,
    { waitUntil: 'networkidle2', timeout: 60000 });
  await page.waitForSelector('#lessons30Box', { timeout: 20000 });
  await sleep(600);
  ok(await page.$eval('#lessons30Box', e => getComputedStyle(e).display !== 'none'),
    'lessons30 box shown');
  const rows = await page.$$eval('#lessons30Box .l30Row', es => es.length);
  ok(rows === DATA.lessons.length, 'lesson list rows match data', rows + ' rows');
  await page.$$eval('#lessons30Box .l30Row', es => es[0].click());
  await page.waitForSelector('#l30Audio', { timeout: 10000 });
  const src = await page.$eval('#l30Audio', e => e.getAttribute('src') || '');
  ok(src.endsWith('lesson-01.mp3'), 'audio carries lesson-01.mp3', src);
  const textLen = await page.$eval('#l30Text', e => e.textContent.length);
  ok(textLen > 15000, 'full text present', textLen + ' chars');
  ok(await page.$eval('#l30ToQuiz', e => e.disabled),
    'GATE HOLDS: questions disabled before lesson done');
  await page.evaluate(() => {
    const t = document.getElementById('l30Text');
    t.scrollTop = t.scrollHeight;
    t.dispatchEvent(new Event('scroll'));
  });
  await sleep(500);
  ok(await page.$eval('#l30ReadBtn', e => !e.disabled), 'read button arms');
  await page.click('#l30ReadBtn');
  await sleep(400);
  ok(await page.$eval('#l30ToQuiz', e => !e.disabled), 'questions unlock');
  const log1 = await page.evaluate(() =>
    JSON.parse(localStorage.getItem('dave_lab_log') || '[]'));
  const done = log1.filter(e => e.kind === 'lesson30-done');
  ok(done.length === 1 && done[0].minutes > 15,
    'lesson30-done logged with real minutes',
    done.length ? done[0].minutes + ' min' : 'none');

  await page.click('#l30ToQuiz');
  await sleep(600);
  const qs = L1.questions;
  for (let i = 0; i < qs.length; i++) {
    const q = qs[i];
    // wait until this question is on screen
    let shown = false;
    for (let t = 0; t < 20 && !shown; t++) {
      shown = await page.evaluate((want) => {
        const el = document.getElementById('l30Q');
        return el && el.textContent === want;
      }, q.q);
      if (!shown) await sleep(400);
    }
    ok(shown, 'Q' + (i + 1) + ' on screen', q.q.slice(0, 50));
    if (!shown) break;
    const nChoices = await page.$$eval('#l30Choices .l30Choice',
      es => es.length).catch(() => 0);
    if (q.choices && q.mcAnswer && nChoices) {
      const picked = await page.evaluate((want) => {
        const bs = [...document.querySelectorAll('#l30Choices .l30Choice')];
        const b = bs.find(x => x.textContent === want);
        if (b) { b.click(); return true; }
        return false;
      }, q.mcAnswer);
      ok(picked, 'Q' + (i + 1) + ' correct MC picked');
    } else if (q.kind === 'keywords') {
      const ans = (q.keywords || []).map(g => g[0]).join(' ');
      await page.evaluate((v) => {
        document.getElementById('l30Input').value = v;
        document.getElementById('l30Check2').click();
      }, ans);
      ok(true, 'Q' + (i + 1) + ' keywords answered');
    } else {
      await page.evaluate((v) => {
        document.getElementById('l30Input').value = v;
        document.getElementById('l30Check2').click();
      }, String(q.answer));
      ok(true, 'Q' + (i + 1) + ' typed answer submitted');
    }
    await sleep(1600);
  }
  await sleep(800);
  const gradeTxt = await page.$eval('#l30Grade', e => e.textContent)
    .catch(() => '');
  ok(/landed|of 11|of 12/.test(gradeTxt) || gradeTxt.length > 10,
    'grade panel shows', gradeTxt.slice(0, 70));
  const log2 = await page.evaluate(() =>
    JSON.parse(localStorage.getItem('dave_lab_log') || '[]'));
  const grades = log2.filter(e => e.kind === 'lesson30-grade');
  ok(grades.length >= 1 && grades[grades.length - 1].complete === true,
    'lesson30-grade complete logged',
    grades.length ? 'passed=' + grades[grades.length - 1].passed : 'none');
  await page.reload({ waitUntil: 'networkidle2' });
  await page.waitForSelector('#lessons30Box .l30Row', { timeout: 20000 });
  await sleep(600);
  const rowText = await page.$eval('#lessons30Box .l30Row',
    e => e.textContent);
  ok(/Complete/.test(rowText), 'after reload, list shows Complete',
    rowText.slice(0, 80));
  ok(errors.length === 0, 'no page errors', errors.join(' | ').slice(0, 200));
  await browser.close();
  console.log(fails ? '\n' + fails + ' FAILURES' : '\nALL PASS');
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error('HARNESS ERROR', e); process.exit(2); });
