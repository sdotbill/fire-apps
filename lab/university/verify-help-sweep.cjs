/* University-wide help sweep (Bill's scope extension, Nov 16 03:11):
   the hint → choices → assisted-pass flow, driven in headless Chrome
   on ONE gated class per section (the section's first gated class in
   catalogue order), plus two targeted samples: a rescued two-step
   class (syllabus-DOI choices) and a single-paper class (guided
   look-up fallback). For every sample: begin → I'm stuck → hint from
   the step's own material → choices (or the honest look-up) → land
   the step → the log records an ASSISTED pass.
   The expected options are computed here from gate-data.json +
   catalogue.json with the same derivation gate-ui.js runs; the
   browser's rendered options must match that set exactly.
   Run: NODE_PATH=<owner-lane browser node_modules> node verify-help-sweep.cjs <baseUrl>
   Writes sweep-results.json; exits non-zero on any failure.
*/
'use strict';
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const BASE = process.argv[2] || 'http://127.0.0.1:8933/';
const EXE = '/home/hatch/.cache/puppeteer/chrome/linux-156.0.8078.47/chrome-linux64/chrome';
const sleep = ms => new Promise(r => setTimeout(r, ms));

const cat = JSON.parse(fs.readFileSync(path.join(__dirname, 'catalogue.json'), 'utf8'));
const gd = JSON.parse(fs.readFileSync(path.join(__dirname, 'gate-data.json'), 'utf8')).classes;
const classObj = {};
cat.sections.forEach(s => s.classes.forEach(c => { classObj[c.id] = c; }));

function answerText(st) {
  if (!st) return null;
  if (st.kind === 'number') return st.disp || String(st.answer);
  if (st.kind === 'keywords') return null;
  return st.answer != null ? String(st.answer) : null;
}
function correctText(st) {
  if (st.kind === 'keywords') {
    return 'An answer built on: ' + st.keywords.map(g => g[0]).join(' · ');
  }
  return answerText(st);
}
function norm(s) { return String(s || '').toLowerCase().replace(/\s+/g, ' ').trim(); }
function expectedOptions(cid, idx) {
  const d = gd[cid], st = d.steps[idx];
  const correct = correctText(st);
  const pool = [], seen = new Set([norm(correct)]);
  const sibs = d.steps.filter((o, i) => i !== idx);
  sibs.sort((a, b) => (b.kind === st.kind ? 1 : 0) - (a.kind === st.kind ? 1 : 0));
  sibs.forEach(o => {
    const t = answerText(o);
    if (!t) return;
    const n = norm(t);
    if (seen.has(n)) return;
    seen.add(n); pool.push(t);
  });
  const cls = classObj[cid];
  if (pool.length < 3 && st.kind === 'exact' &&
      /10\.\d+\//.test(String(st.answer)) && cls && cls.papers) {
    cls.papers.forEach(p => {
      if (pool.length >= 3 || !p.doi) return;
      const n = norm(p.doi);
      if (seen.has(n)) return;
      seen.add(n); pool.push(p.doi);
    });
  }
  if (pool.length < 2 && st.kind === 'number') {
    const want = typeof st.answer === 'number' ? st.answer : parseFloat(st.answer);
    const tol = st.tol || 0.03;
    const text = (st.teach || '') + ' ' + (st.teach2 || '');
    const re = /=\s*(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)/gi;
    let m;
    while ((m = re.exec(text)) !== null && pool.length < 2) {
      const pv = parseFloat(m[1]);
      if (!isNaN(pv) && !isNaN(want) &&
          Math.abs(pv - want) / Math.abs(want || 1) <= tol) continue;
      const n = norm(m[1]);
      if (seen.has(n)) continue;
      seen.add(n); pool.push(m[1]);
    }
  }
  return { correct, allowed: new Set([correct, ...pool.slice(0, 3)]) };
}

/* the plan: first gated class per section + targeted samples.
   An optional third argument re-runs named classes only:
   node verify-help-sweep.cjs <baseUrl> classId1,classId2 */
const onlyArg = process.argv[3] || '';
const plan = [];
cat.sections.forEach(s => {
  const first = s.classes.find(c => gd[c.id]);
  if (first) plan.push({ section: s.id, sectionName: s.name, classId: first.id, why: 'section sample' });
});
[['cosmology', 'founding-papers-re-read', 'rescued two-step class (syllabus choices)'],
 ['designs', 'house-record', 'single-paper class (look-up fallback)']
].forEach(([sec, cid, why]) => {
  if (gd[cid] && !plan.some(p => p.classId === cid)) {
    const s = cat.sections.find(x => x.id === sec);
    plan.push({ section: sec, sectionName: s ? s.name : sec, classId: cid, why });
  }
});

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
  let pageErrors = 0;
  page.on('pageerror', e => { pageErrors++; console.log('PAGE ERROR:', e.message); });

  const runPlan = onlyArg
    ? plan.filter(p => onlyArg.split(',').indexOf(p.classId) !== -1)
    : plan;
  const results = [];
  for (const item of runPlan) {
    const sec = classObj[item.classId]._section || cat.sections.find(s => s.id === item.section);
    const r = { section: item.section, classId: item.classId, why: item.why, ok: false, mode: '', detail: '' };
    try {
      const exp = expectedOptions(item.classId, 0);
      await page.goto(BASE, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.evaluate(() => localStorage.clear());
      await page.goto(BASE + '#class/' + item.section + '/' + item.classId,
        { waitUntil: 'networkidle2', timeout: 60000 });
      await page.waitForSelector('#gateBox', { visible: true, timeout: 20000 });
      await page.click('#gtBegin');
      /* the step is presented when the professor's spoken piece
         ends — a recorded step clip can run past two minutes, so
         this wait is sized to the longest clip, not to impatience */
      await page.waitForFunction(
        () => document.getElementById('gtHelp').style.display !== 'none',
        { timeout: 240000 });
      await page.click('#gtHelp');
      await page.waitForFunction(
        () => document.getElementById('gtHint').style.display !== 'none',
        { timeout: 10000 });
      const hint = await page.$eval('#gtHint', el => el.textContent);
      if (!/Hint — from the material itself/.test(hint) || hint.length < 40)
        throw new Error('hint not honestly present: ' + hint.slice(0, 60));
      await page.click('#gtHelp');
      await sleep(600);
      const choiceTexts = await page.$$eval('#gtChoices .gtChoice',
        els => els.map(e => e.textContent));
      const boxText = await page.$eval('#gtChoices', el => el.textContent);
      if (choiceTexts.length) {
        r.mode = 'choices ×' + choiceTexts.length;
        if (choiceTexts.indexOf(exp.correct) === -1)
          throw new Error('correct option missing: ' + choiceTexts.join(' | '));
        const alien = choiceTexts.filter(t => !exp.allowed.has(t));
        if (alien.length) throw new Error('options outside the class material: ' + alien.join(' | '));
        await page.evaluate((correct) => {
          Array.from(document.querySelectorAll('#gtChoices .gtChoice'))
            .find(b => b.textContent === correct).click();
        }, exp.correct);
      } else if (/No set of choices can be honestly built/.test(boxText)) {
        r.mode = 'look-up fallback';
        const st = gd[item.classId].steps[0];
        const typed = st.kind === 'keywords' ? null : String(st.answer);
        if (typed === null) throw new Error('look-up fallback on a keywords step — cannot type-verify');
        await page.$eval('#gtInput', (el, t) => { el.value = t; }, typed);
        await page.click('#gtCheck');
      } else {
        throw new Error('neither choices nor the look-up appeared');
      }
      await page.waitForFunction(
        () => /Step 2 of/.test(document.getElementById('gtProgress').textContent) ||
              document.getElementById('gtGrade').style.display !== 'none',
        { timeout: 30000 });
      const log = await page.evaluate(
        () => JSON.parse(localStorage.getItem('dave_lab_log') || '[]'));
      const entry = log.find(e => e.kind === 'gate-step' &&
        e.classId === item.classId && e.step === 0);
      if (!entry || entry.status !== 'pass' || entry.assisted !== true)
        throw new Error('assisted pass not in the log: ' + JSON.stringify(entry || null));
      r.ok = true;
      r.detail = 'hint ✓ · ' + r.mode + ' · assisted pass logged';
    } catch (e) {
      r.detail = e.message.slice(0, 160);
    }
    results.push(r);
    console.log((r.ok ? 'PASS ' : 'FAIL ') + r.section + ' — ' + r.classId +
      ' (' + r.why + ') — ' + r.detail);
  }

  await browser.close();
  fs.writeFileSync(path.join(__dirname, 'sweep-results.json'),
    JSON.stringify(results, null, 1));
  const fails = results.filter(r => !r.ok);
  console.log('\nSWEEP: ' + (results.length - fails.length) + '/' + results.length +
    ' sections passed · page errors: ' + pageErrors);
  process.exit(fails.length ? 1 : 0);
})().catch(e => { console.error('SWEEP ERROR:', e.message); process.exit(2); });
