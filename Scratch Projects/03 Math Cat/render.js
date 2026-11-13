// Renders both TV decks to docs/scratch/math-cat/ (and a PNG of each slide for checking):
//   slides.html -> slides.pdf   Math Cat: set up, the six missions, then the finished code
//   lesson.html -> lesson.pdf   Asking and Operators, the short lesson taught before Math Cat
//   node "Scratch Projects/03 Math Cat/render.js" [folder for PNGs]
// Playwright must be installed. Each PDF is 1280 x 720, one slide per page.
const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const here = __dirname;
  const site = path.join(here, '..', '..', 'docs', 'scratch', 'math-cat');
  const pngs = process.argv[2];
  const browser = await chromium.launch();
  for (const [src, pdf, prefix] of [['slides.html', 'slides.pdf', 'slide'], ['lesson.html', 'lesson.pdf', 'lesson']]) {
    const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
    await page.goto('file://' + path.join(here, src));
    await page.waitForSelector('body[data-ready="1"]');
    await page.evaluate(() => document.fonts.ready);
    if (pngs) {
      const n = await page.locator('section.slide').count();
      for (let i = 0; i < n; i++) await page.locator('section.slide').nth(i).screenshot({ path: path.join(pngs, `${prefix}-${i + 1}.png`) });
    }
    const out = path.join(site, pdf);
    await page.pdf({ path: out, width: '1280px', height: '720px', printBackground: true, preferCSSPageSize: true });
    await page.close();
    console.log('wrote', out);
  }
  await browser.close();
})();
