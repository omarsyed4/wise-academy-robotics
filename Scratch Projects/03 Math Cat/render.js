// Renders slides.html to docs/scratch/math-cat/slides.pdf (and a PNG of each slide for checking).
//   node "Scratch Projects/03 Math Cat/render.js" [folder for PNGs]
// Playwright must be installed. The PDF is 1280 x 720, one slide per page.
const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const here = __dirname;
  const out = path.join(here, '..', '..', 'docs', 'scratch', 'math-cat', 'slides.pdf');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto('file://' + path.join(here, 'slides.html'));
  await page.waitForSelector('body[data-ready="1"]');
  await page.evaluate(() => document.fonts.ready);
  const pngs = process.argv[2];
  if (pngs) {
    const n = await page.locator('section.slide').count();
    for (let i = 0; i < n; i++) await page.locator('section.slide').nth(i).screenshot({ path: path.join(pngs, `slide-${i + 1}.png`) });
  }
  await page.pdf({ path: out, width: '1280px', height: '720px', printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log('wrote', out);
})();
