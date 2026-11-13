// Makes the Innovation board print pack and checks it.
//   python3 docs/print/innovation-board.py   (first, if you changed the board's words)
//   node docs/print/print.mjs
// innovation-board.pdf: three pages at true size (12x36, 24x36, 12x36 in).
// innovation-print-list.pdf: one US Letter page.
// It fails if any box's text overflows its box, or if the print list runs past one page.
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
let ok = true;

// The board, at true size
await page.goto('file://' + path.join(here, 'innovation-board.html'), { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
const over = await page.evaluate(() =>
  [...document.querySelectorAll('.bx, .bar, .title, .info')].filter(e =>
    e.scrollHeight > e.clientHeight + 1 || e.scrollWidth > e.clientWidth + 1
  ).map(e => `${e.closest('.panel').dataset.panel}: ${(e.querySelector('.lab') || e).textContent.trim().slice(0, 50)}`));
const fonts = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family));
if (!fonts.some(f => /Montserrat/.test(f))) { console.log('Fonts did not load (offline?). Not printing.'); ok = false; }
if (over.length) { console.log('Text does not fit in:\n  ' + over.join('\n  ')); ok = false; }
if (ok) {
  await page.pdf({ path: path.join(here, 'innovation-board.pdf'), printBackground: true, preferCSSPageSize: true });
  console.log('innovation-board.pdf: every box fits');
}

// The print list, one Letter page
await page.goto('file://' + path.join(here, 'innovation-print-list.html'), { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
const pdf = await page.pdf({ path: path.join(here, 'innovation-print-list.pdf'), format: 'Letter', printBackground: true });
const pages = (pdf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
console.log(`innovation-print-list.pdf: ${pages} page${pages === 1 ? '' : 's'}`);
if (pages !== 1) ok = false;

await browser.close();
process.exit(ok ? 0 : 1);
