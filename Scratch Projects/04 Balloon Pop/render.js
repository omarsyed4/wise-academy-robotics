// Renders both TV decks to docs/scratch/balloon-pop/ (and a PNG of each slide for checking):
//   lesson.html -> lesson.pdf   Clicks, Sounds and Looks, the short lesson taught before Balloon Pop
//   slides.html -> slides.pdf   Balloon Pop: set up, the four missions, then the finished code
//   node "Scratch Projects/04 Balloon Pop/render.js" [folder for PNGs]
// Playwright must be installed. Each PDF is 1280 x 720, one slide per page.
const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const here = __dirname;
  const site = path.join(here, '..', '..', 'docs', 'scratch', 'balloon-pop');
  const pngs = process.argv[2];
  const browser = await chromium.launch();
  for (const [src, pdf, prefix] of [['lesson.html', 'lesson.pdf', 'lesson'], ['slides.html', 'slides.pdf', 'slide']]) {
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
