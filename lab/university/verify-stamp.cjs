/* The build-stamp verification (Bill, Nov 16 04:16 EST — his phone
   was served a stale classroom an hour after the fix shipped).
   Proves, in headless Chrome against a local server that mimics
   the live cache headers (Cache-Control: public, max-age=300):
     1. the page runs the stamp minted into index.html, and every
        data fetch (gate-data.json, catalogue.json,
        trainer-data.json) carries it as ?v=;
     2. when the served copy's stamp changes underneath a live
        page — a deploy landing while a phone holds the old tab —
        the page notices on the visibility check and reloads ONCE
        onto the new build (no reload loop);
     3. after the reload, the data fetches carry the NEW stamp.
   Run: NODE_PATH=<owner-lane browser node_modules> node verify-stamp.cjs
*/
'use strict';
const fs = require('fs');
const os = require('os');
const path = require('path');
const http = require('http');
const puppeteer = require('puppeteer-core');

const EXE = '/home/hatch/.cache/puppeteer/chrome/linux-156.0.8078.47/chrome-linux64/chrome';
const sleep = ms => new Promise(r => setTimeout(r, ms));
let failures = 0;
function check(name, ok, extra) {
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (extra ? ' — ' + extra : ''));
  if (!ok) failures++;
}

(async () => {
  /* a throwaway copy of the student-facing files */
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'uni-stamp-'));
  for (const f of fs.readdirSync(__dirname)) {
    if (/\.(html|js|json|css)$/.test(f) &&
        fs.statSync(path.join(__dirname, f)).isFile()) {
      fs.copyFileSync(path.join(__dirname, f), path.join(dir, f));
    }
  }
  const MIME = { '.html': 'text/html', '.js': 'text/javascript',
    '.json': 'application/json', '.css': 'text/css' };
  const server = http.createServer((req, res) => {
    const p = decodeURIComponent(req.url.split('?')[0]);
    const file = path.join(dir, p === '/' ? 'index.html' : p);
    fs.readFile(file, (err, data) => {
      if (err) { res.writeHead(404); res.end('nf'); return; }
      res.writeHead(200, {
        'Content-Type': MIME[path.extname(file)] || 'text/plain',
        'Cache-Control': 'public, max-age=300',
      });
      res.end(data);
    });
  });
  await new Promise(r => server.listen(8941, '127.0.0.1', r));
  const BASE = 'http://127.0.0.1:8941/';

  const browser = await puppeteer.launch({
    executablePath: EXE, headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox',
           '--disable-dev-shm-usage', '--disable-gpu', '--no-first-run',
           '--no-proxy-server', '--window-size=390,844']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 390, height: 844 });
  page.on('pageerror', e => console.log('PAGE ERROR:', e.message));
  const reqs = [];
  page.on('request', r => reqs.push(r.url()));
  let navs = 0;
  page.on('framenavigated', f => { if (f === page.mainFrame()) navs++; });

  await page.goto(BASE, { waitUntil: 'networkidle2', timeout: 60000 });
  const s1 = await page.evaluate(() => window.UNI_BUILD);
  check('the page runs a minted build stamp', !!s1 && s1 !== 'unstamped', s1);
  for (const name of ['gate-data.json', 'catalogue.json', 'trainer-data.json']) {
    check(name + ' is fetched with ?v=<stamp>',
      reqs.some(u => u.includes(name + '?v=' + encodeURIComponent(s1))),
      reqs.filter(u => u.includes(name)).join(' '));
  }

  /* a deploy lands underneath the live page: the served stamp flips */
  const idx = path.join(dir, 'index.html');
  const html = fs.readFileSync(idx, 'utf8');
  if (!html.includes(s1)) throw new Error('stamp not found in served copy');
  fs.writeFileSync(idx, html.split(s1).join('TESTBUILD2'));
  reqs.length = 0;
  const navsBefore = navs;
  await page.evaluate(() => {
    document.dispatchEvent(new Event('visibilitychange'));
  });
  let healed = false;
  for (let i = 0; i < 40 && !healed; i++) {
    await sleep(250);
    healed = await page.evaluate(() => window.UNI_BUILD)
      .then(v => v === 'TESTBUILD2').catch(() => false);
  }
  check('the live page notices the new build and reloads onto it', healed);
  check('the new build\u2019s data fetches carry the NEW stamp',
    reqs.some(u => u.includes('gate-data.json?v=TESTBUILD2')),
    reqs.filter(u => u.includes('gate-data')).join(' '));
  await sleep(3500); /* past the load+1500ms self-check: no loop */
  const navDelta = navs - navsBefore;
  check('exactly one reload — no reload loop', navDelta === 1,
    'navigations after the flip: ' + navDelta);
  const s2 = await page.evaluate(() => window.UNI_BUILD);
  check('the page stays on the new build', s2 === 'TESTBUILD2', s2);

  await browser.close();
  server.close();
  fs.rmSync(dir, { recursive: true, force: true });
  console.log(failures ? `\n${failures} FAILURES` : '\nALL STAMP CHECKS PASSED');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error('VERIFY ERROR:', e); process.exit(2); });
