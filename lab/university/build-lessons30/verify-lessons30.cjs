/* Browser verification for the 30-minute lesson room.
   Bill's law (Nov 16 2026): the class is TAUGHT first — a full
   ~30-minute lesson, audio + complete text — and only when the
   lesson is finished do the questions open. No skipping.

   Drives the Spanish flagship (Carmen Vega, Lesson 1) end to end in
   headless Chrome against a locally served copy:
     1. the lessons30 room takes precedence (trainer box hidden),
        the lesson list renders with honest states;
     2. the lesson view carries the audio player, the FULL text, and
        the speak-along phrases; the questions button is DISABLED —
        the gate holds;
     3. the read-through path: scrolling the text to the end arms
        "I've read the whole lesson"; confirming it opens the gate
        and writes a lesson30-done entry (minutes > 0) to the log;
     4. a phrase is mastered by typing it (green check + a
        phrase-mastery entry);
     5. the quiz: a correct MC pick passes in full; a typed miss
        shows the re-teach; the right answer then passes; Help marks
        the next pass assisted; a skip is recorded as a skip;
     6. finishing writes a lesson30-grade (complete) and the list
        shows the lesson Complete after a reload.
   Run: NODE_PATH=<owner-lane browser node_modules> node \
        build-lessons30/verify-lessons30.cjs <baseUrl> */
'use strict';
const fs = require('fs');
const puppeteer = require('puppeteer-core');

const BASE = process.argv[2] || 'http://127.0.0.1:8937/';
const EXE = '/home/hatch/.cache/puppeteer/chrome/linux-156.0.8078.47/chrome-linux64/chrome';
const sleep = ms => new Promise(r => setTimeout(r, ms));
let failures = 0;
function check(name, cond, extra) {
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' — ' + extra : ''));
  if (!cond) failures++;
}

const DATA = JSON.parse(fs.readFileSync('lessons30/espanol-i-speak-from-zero.json', 'utf8'));
const L1 = DATA.lessons[0];

(async () => {
  const browser = await puppeteer.launch({
    executablePath: EXE, headless: true,
    args: ['--no-sandbox', '--autoplay-policy=no-user-gesture-required']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1100, height: 900 });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(BASE + 'index.html#class/languages/espanol-i-speak-from-zero',
    { waitUntil: 'networkidle0', timeout: 60000 });
  await sleep(2500);

  /* 1 — the room takes precedence, list renders */
  const list = await page.evaluate(() => {
    const box = document.getElementById('lessons30Box');
    const tb = document.getElementById('trainerBox');
    const rows = document.querySelectorAll('#l30List .l30Row');
    return {
      boxShown: !!box && box.style.display !== 'none',
      trainerHidden: !tb || tb.style.display === 'none',
      rows: rows.length,
      firstRow: rows.length ? rows[0].textContent : ''
    };
  });
  check('lessons30 box shown', list.boxShown);
  check('trainer box hidden (precedence)', list.trainerHidden);
  check('lesson list has rows', list.rows >= 1, list.rows + ' rows');
  check('row names Lesson 1', /Lesson 1/.test(list.firstRow));

  /* 2 — lesson view: audio, full text, phrases, gate holds */
  await page.evaluate(() => {
    document.querySelector('#l30List .l30Row').click();
  });
  await sleep(600);
  const lv = await page.evaluate(() => {
    const au = document.getElementById('l30Audio');
    const tx = document.getElementById('l30Text');
    return {
      audioSrc: au ? au.getAttribute('src') : null,
      audioShown: !!au && au.style.display !== 'none',
      textStart: tx ? tx.textContent.slice(0, 60) : '',
      textLen: tx ? tx.textContent.length : 0,
      phrases: document.querySelectorAll('.l30Phrase').length,
      quizDisabled: document.getElementById('l30ToQuiz').disabled,
      readDisabled: document.getElementById('l30ReadBtn').disabled
    };
  });
  check('audio player carries lesson-01.mp3', /lesson-01\.mp3/.test(lv.audioSrc || ''), lv.audioSrc);
  check('audio player visible', lv.audioShown);
  check('full text present', lv.textLen > 15000, lv.textLen + ' chars');
  check('text opens with Carmen', /Carmen Vega/.test(lv.textStart));
  check('speak-along phrases render', lv.phrases >= 8, lv.phrases + ' phrases');
  check('GATE HOLDS: questions disabled before lesson done', lv.quizDisabled === true);
  check('read-confirm starts disabled', lv.readDisabled === true);

  /* 3 — read-through path opens the gate */
  await page.evaluate(() => {
    const tx = document.getElementById('l30Text');
    tx.scrollTop = tx.scrollHeight;
    tx.dispatchEvent(new Event('scroll'));
  });
  await sleep(300);
  const armed = await page.evaluate(() =>
    !document.getElementById('l30ReadBtn').disabled);
  check('scroll-to-end arms the read button', armed);
  await page.evaluate(() => document.getElementById('l30ReadBtn').click());
  await sleep(300);
  const after = await page.evaluate(() => {
    const log = JSON.parse(localStorage.getItem('dave_lab_log') || '[]');
    const done = log.filter(e => e.kind === 'lesson30-done');
    return {
      quizEnabled: !document.getElementById('l30ToQuiz').disabled,
      doneBar: document.getElementById('l30DoneBar').style.display !== 'none',
      doneEntries: done.length,
      minutes: done.length ? done[0].minutes : 0,
      via: done.length ? done[0].via : null
    };
  });
  check('questions unlock after read-through', after.quizEnabled);
  check('done bar shows', after.doneBar);
  check('lesson30-done logged once', after.doneEntries === 1);
  check('done entry carries real minutes', after.minutes > 15, after.minutes + ' min');
  check('done via read', after.via === 'read');

  /* 4 — a phrase mastered by typing */
  const phr = await page.evaluate(() => {
    const row = document.querySelector('.l30Phrase');
    const input = row.querySelector('input');
    const btns = row.querySelectorAll('button');
    input.value = 'Hola';
    btns[btns.length - 1].click();
    return { mark: row.querySelector('.l30Mark').style.display };
  });
  await sleep(200);
  const mastery = await page.evaluate(() => {
    const log = JSON.parse(localStorage.getItem('dave_lab_log') || '[]');
    return log.filter(e => e.kind === 'phrase-mastery' && e.phrase === 'Hola').length;
  });
  check('typed phrase passes (green check)', phr.mark === 'inline');
  check('phrase-mastery logged', mastery === 1);

  /* 5 — the quiz */
  await page.evaluate(() => document.getElementById('l30ToQuiz').click());
  await sleep(500);
  const q1 = await page.evaluate(() => ({
    q: document.getElementById('l30Q').textContent,
    choices: document.querySelectorAll('#l30Choices .l30Choice').length
  }));
  check('quiz opens on question 1', q1.q === L1.questions[0].q, q1.q.slice(0, 50));
  check('MC choices render by default', q1.choices >= 3, q1.choices + ' choices');
  /* correct pick passes in full */
  await page.evaluate(() => {
    const want = 'good morning';
    document.querySelectorAll('#l30Choices .l30Choice').forEach(b => {
      if (b.textContent === want) b.click();
    });
  });
  await sleep(400);
  const p1 = await page.evaluate(() => ({
    checkShown: document.getElementById('l30Check').style.display !== 'none',
    status: document.getElementById('l30QStatus').textContent
  }));
  check('correct MC pick passes', p1.checkShown, p1.status.slice(0, 40));
  await sleep(1200);
  /* Q2: typed miss -> re-teach; then correct typed answer passes */
  const q2txt = await page.evaluate(() =>
    document.getElementById('l30Q').textContent);
  check('advanced to question 2', q2txt === L1.questions[1].q);
  await page.evaluate(() => {
    document.getElementById('l30Input').value = 'Buenas noches';
    document.getElementById('l30Check2').click();
  });
  await sleep(300);
  const miss = await page.evaluate(() => ({
    hintShown: document.getElementById('l30Hint').style.display !== 'none',
    status: document.getElementById('l30QStatus').textContent
  }));
  check('miss shows the re-teach', miss.hintShown, miss.status.slice(0, 40));
  await page.evaluate(() => {
    document.getElementById('l30Input').value = 'Hola';
    document.getElementById('l30Check2').click();
  });
  await sleep(1500);
  /* Q3: help first, then pick the correct choice -> assisted pass */
  await page.evaluate(() => document.getElementById('l30Help').click());
  await sleep(300);
  await page.evaluate(() => {
    document.querySelectorAll('#l30Choices .l30Choice').forEach(b => {
      if (b.textContent === 'the letter h') b.click();
    });
  });
  await sleep(1500);
  const assisted = await page.evaluate(() => {
    const log = JSON.parse(localStorage.getItem('dave_lab_log') || '[]');
    const steps = log.filter(e => e.kind === 'lesson30-step');
    return {
      passes: steps.filter(e => e.status === 'pass').length,
      assisted: steps.filter(e => e.assisted).length
    };
  });
  check('three passes logged', assisted.passes === 3, JSON.stringify(assisted));
  check('help pass recorded assisted', assisted.assisted === 1);
  /* Q4: skip it — recorded as a skip, never a pass */
  await page.evaluate(() => document.getElementById('l30Skip').click());
  await sleep(400);
  /* finish the rest with correct typed answers / picks */
  for (let i = 4; i < L1.questions.length; i++) {
    const st = L1.questions[i];
    const done = await page.evaluate((st) => {
      const qEl = document.getElementById('l30Q');
      if (!qEl || qEl.textContent !== st.q) return 'not-on-question';
      if (st.choices && st.choices.length && st.mcAnswer) {
        let clicked = false;
        document.querySelectorAll('#l30Choices .l30Choice').forEach(b => {
          if (b.textContent === String(st.mcAnswer)) { b.click(); clicked = true; }
        });
        return clicked ? 'picked' : 'no-choice-found';
      }
      const inp = document.getElementById('l30Input');
      inp.value = 'llamo call myself name hand offer stranger';
      document.getElementById('l30Check2').click();
      return 'typed';
    }, st);
    check('Q' + (i + 1) + ' answered (' + done + ')', done === 'picked' || done === 'typed');
    await sleep(1500);
  }
  await sleep(600);
  const grade = await page.evaluate(() => {
    const log = JSON.parse(localStorage.getItem('dave_lab_log') || '[]');
    const grades = log.filter(e => e.kind === 'lesson30-grade');
    const steps = log.filter(e => e.kind === 'lesson30-step');
    return {
      gradeShown: document.getElementById('l30Grade').style.display !== 'none',
      grades: grades.length,
      complete: grades.length ? grades[grades.length - 1].complete : null,
      passed: grades.length ? grades[grades.length - 1].passed : 0,
      skipped: steps.filter(e => e.status === 'skip').length
    };
  });
  check('grade panel shows', grade.gradeShown);
  check('lesson30-grade written, complete', grade.grades >= 1 && grade.complete === true);
  check('grade counts 11 passes', grade.passed === 11, 'passed=' + grade.passed);
  check('one skip recorded as skip', grade.skipped === 1);

  /* 6 — persistence: reload shows the lesson complete */
  await page.reload({ waitUntil: 'networkidle0' });
  await sleep(2500);
  const afterReload = await page.evaluate(() => {
    const row = document.querySelector('#l30List .l30Row');
    return row ? row.textContent : '';
  });
  check('after reload, list shows Complete', /Complete/.test(afterReload),
    afterReload.slice(0, 80));

  check('no page errors', errors.length === 0, errors.slice(0, 2).join(' | '));
  await browser.close();
  console.log(failures ? ('\n' + failures + ' FAILURES') : '\nALL PASS');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error('VERIFY CRASH', e); process.exit(2); });
