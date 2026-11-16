// Headless render check for the University pages (portrait build, Nov 2026).
// Usage: node shot-check.js <hash-route> <outfile>
const puppeteer = require('/home/hatch/workspace/your_files/dave-4-public-app-2026-11-08/owner-lane/browser/node_modules/puppeteer-core');
(async () => {
  const route = process.argv[2];
  const out = process.argv[3];
  const browser = await puppeteer.launch({
    executablePath: '/home/hatch/.cache/puppeteer/chrome/linux-156.0.8078.47/chrome-linux64/chrome',
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });
  await page.goto('http://127.0.0.1:8791/lab/university/' + route,
    { waitUntil: 'networkidle0', timeout: 60000 });
  await new Promise(r => setTimeout(r, 2500));
  const info = await page.evaluate(() => {
    const card = document.getElementById('profCard');
    const bodyText = document.body.innerText || '';
    const img = card && card.querySelector('img.pphoto');
    return {
      cardHTML: card ? card.innerHTML.slice(0, 300) : null,
      hasPhoto: !!img,
      imgLoaded: img ? (img.complete && img.naturalWidth > 0) : false,
      hasMono: !!(card && card.querySelector('.pmono')),
      hasSVG: !!(card && card.querySelector('svg')),
      voiceLines: (bodyText.match(/Voice:/g) || []).length,
    };
  });
  console.log(JSON.stringify(info, null, 1));
  if (out) await page.screenshot({ path: out });
  await browser.close();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
