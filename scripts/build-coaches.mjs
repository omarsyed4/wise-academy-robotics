// Encrypts the coaches' notes into the website.
//
//   node scripts/build-coaches.mjs
//
// Reads admin/coaches.html (an HTML fragment) and the password from $COACHES_PASSWORD or
// admin/.password, then writes the ciphertext between the COACHES markers in docs/index.html.
// admin/ is gitignored: the repo and the site are public, so only the ciphertext is committed.
// The page decrypts it in the browser with the same scheme: PBKDF2-SHA256 → AES-256-GCM.

import { readFileSync, writeFileSync } from 'node:fs';
import { webcrypto as crypto } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const page = join(root, 'docs', 'index.html');
const ITER = 310000;

const password = (process.env.COACHES_PASSWORD || readFileSync(join(root, 'admin', '.password'), 'utf8')).trim();
if (password.length < 8) throw new Error('Use a password of at least 8 characters.');
const notes = readFileSync(join(root, 'admin', 'coaches.html'), 'utf8')
  .replace(/^<!--[\s\S]*?-->\s*/, ''); // the editing note at the top stays private

const salt = crypto.getRandomValues(new Uint8Array(16));
const iv = crypto.getRandomValues(new Uint8Array(12));
const base = await crypto.subtle.importKey('raw', new TextEncoder().encode(password), 'PBKDF2', false, ['deriveKey']);
const key = await crypto.subtle.deriveKey({ name: 'PBKDF2', salt, iterations: ITER, hash: 'SHA-256' },
  base, { name: 'AES-GCM', length: 256 }, false, ['encrypt']);
const data = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, new TextEncoder().encode(notes));

const b64 = (buf) => Buffer.from(buf).toString('base64');
const blob = JSON.stringify({ salt: b64(salt), iv: b64(iv), iter: ITER, data: b64(data) });

const html = readFileSync(page, 'utf8');
const marked = /<!-- COACHES:BEGIN -->[\s\S]*?<!-- COACHES:END -->/;
if (!marked.test(html)) throw new Error('COACHES markers not found in docs/index.html');
writeFileSync(page, html.replace(marked,
  `<!-- COACHES:BEGIN --><script type="application/json" id="coaches-blob">${blob}</script><!-- COACHES:END -->`));
console.log(`Encrypted ${notes.length} characters of notes into docs/index.html`);
