// ARC CORE BOOK renderer: HTML -> PDF (Chromium via Playwright).
// usage: node render_pdf.js <doc.html> <out.pdf>
// Playwright is resolved from NODE_PATH, a local install, or the CI/container global path.
const path = require('path');
function loadPlaywright() {
  const candidates = ['playwright', '/opt/node22/lib/node_modules/playwright', '/usr/lib/node_modules/playwright'];
  for (const c of candidates) { try { return require(c); } catch (e) { /* try next */ } }
  throw new Error('playwright not found (set NODE_PATH or npm i playwright)');
}
(async () => {
  const [html, out] = process.argv.slice(2);
  if (!html || !out) throw new Error('usage: node render_pdf.js <doc.html> <out.pdf>');
  const { chromium } = loadPlaywright();
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(html));
  await page.evaluate(() => document.fonts.ready);
  // Source audit: overflow:hidden page shells and flow columns are forbidden (see v0.9 patch).
  const audit = await page.evaluate(() => {
    const issues = [];
    document.querySelectorAll('.s,.imp,.adv,.chk,.ex').forEach((n, i) => {
      if (n.scrollHeight - n.clientHeight > 2) issues.push({ i, type: 'BLOCK_OVERFLOW', cls: n.className });
    });
    document.querySelectorAll('[style*="column-count"]').forEach((n) => issues.push({ type: 'CORE_TWO_COLUMN_FLOW', cls: n.className }));
    return issues;
  });
  if (audit.length) { console.error('ARC_CORE_BOOK_SOURCE_PREFLIGHT HOLD ' + JSON.stringify(audit.slice(0, 10))); process.exitCode = 2; }
  await page.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await browser.close();
})().catch((e) => { console.error(String(e.message).slice(0, 400)); process.exit(1); });
