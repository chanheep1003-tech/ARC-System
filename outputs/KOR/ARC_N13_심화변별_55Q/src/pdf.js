const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  for (const [src, dst] of [['student.html', process.argv[2]], ['key.html', process.argv[3]], ['explain.html', process.argv[4]]]) {
    await p.goto('file://' + path.join(__dirname, src));
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: dst, format: 'A4', preferCSSPageSize: true, printBackground: true });
  }
  await b.close();
})();
