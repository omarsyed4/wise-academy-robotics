// Writes a quiz into the website with the answers hashed.
//
//   node scripts/build-quiz.mjs [admin/quiz-bank.json]
//
// The bank (questions, answers, explanations) is coach-only: keep it in admin/, which is gitignored.
// The page gets the questions and options in plain text, but each answer only as
// sha256(salt|question id|answer text), so the page source doesn't give the answers away.
// scripts/quiz-results.py grades with the same hash. The bank is also checked for the habits that
// made the first quiz easy to game: the right answer in the same spot, or always the longest one.

import { readFileSync, writeFileSync } from 'node:fs';
import { createHash, randomBytes } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const page = join(root, 'docs', 'index.html');
const bank = JSON.parse(readFileSync(process.argv[2] || join(root, 'admin', 'quiz-bank.json'), 'utf8'));

const salt = randomBytes(8).toString('hex');
const hash = (id, text) => createHash('sha256').update(`${salt}|${id}|${text}`).digest('hex').slice(0, 16);

const problems = [], warnings = [], ids = new Set();
const at = [0, 0, 0, 0];
let longest = 0, sentences = 0, total = 0;
for (const r of bank.rounds) for (const q of r.qs) {
  if (ids.has(q.id)) problems.push(`${q.id}: duplicate id`);
  ids.add(q.id);
  if (!/^[a-z0-9]+$/.test(q.id)) problems.push(`${q.id}: ids are lowercase letters and digits only`);
  if (q.opts.length !== 4) problems.push(`${q.id}: needs exactly 4 options`);
  if (new Set(q.opts).size !== q.opts.length) problems.push(`${q.id}: two options are the same`);
  if (!(q.answer >= 0 && q.answer < q.opts.length)) problems.push(`${q.id}: answer must be 0 to ${q.opts.length - 1}`);
  if (!q.why) warnings.push(`${q.id}: no explanation for the review`);
  at[q.answer]++; total++;
  // Length only gives the answer away when the options are sentences, not single words.
  const len = q.opts.map((o) => o.length);
  if (len.reduce((a, b) => a + b) / len.length >= 20) {
    sentences++;
    if (len[q.answer] === Math.max(...len) && len.filter((l) => l === len[q.answer]).length === 1) longest++;
  }
}
if (problems.length) { console.error(problems.join('\n')); process.exit(1); }
if (Math.max(...at) > total * 0.4) warnings.push(`Right answers by position A–D: ${at.join(', ')}. Spread them out.`);
if (longest > sentences * 0.35) warnings.push(`The right answer is the longest option in ${longest} of ${sentences} sentence questions. Even out the lengths.`);
warnings.forEach((w) => console.warn('Warning: ' + w));

const out = {
  set: bank.set,
  salt,
  six: bank.six.map((v) => hash('six', v.toLowerCase())),
  rounds: bank.rounds.map((r) => ({
    id: r.id, title: r.title, note: r.note || '',
    qs: r.qs.map((q) => ({ id: q.id, ask: q.ask, opts: q.opts, key: hash(q.id, q.opts[q.answer]) })),
  })),
};

const json = JSON.stringify(out).replace(/</g, '\\u003c');
const html = readFileSync(page, 'utf8');
const marked = /<!-- QUIZ:BEGIN -->[\s\S]*?<!-- QUIZ:END -->/;
if (!marked.test(html)) throw new Error('QUIZ markers not found in docs/index.html');
writeFileSync(page, html.replace(marked, () =>
  `<!-- QUIZ:BEGIN --><script type="application/json" id="quiz-bank">${json}</script><!-- QUIZ:END -->`));
console.log(`Quiz "${bank.set}": ${total} questions in ${bank.rounds.length} rounds, plus Name all six. ` +
  `Right answers by position A–D: ${at.join(', ')}; the longest option is right in ${longest} of ${sentences} sentence questions.`);
