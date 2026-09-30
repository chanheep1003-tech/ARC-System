// Usage: node render_pdf.js <input.html> <output.pdf>
// Renders an HTML file to an A4 PDF with Chromium; also reports console errors and pre-export overflow audit.
const path = require('path');
const { chromium } = require(process.env.PW_CORE || 'playwright-core');
const CHROME = process.env.CHROME_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
(async () => {
  const [inp, out] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox', '--font-render-hinting=none'] });
  const page = await browser.newPage();
  const errs = [];
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  page.on('requestfailed', r => errs.push('requestfailed: ' + r.url()));
  await page.goto('file://' + path.resolve(inp), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const audit = await page.evaluate(() => {
    const cols = getComputedStyle(document.querySelector('[data-product="arc-core"]') || document.body).columnCount;
    const fam = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight);
    return { columnCount: cols, loadedFonts: [...new Set(fam)].slice(0, 20) };
  });
  await page.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  console.log(JSON.stringify({ out, errs, audit }));
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
