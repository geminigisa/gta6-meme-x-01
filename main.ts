// gta6-meme-x-01 entry — Node 22, standard library only.
// The entry is the X post itself; the house reads it from X and judges it.
// This program's whole job is to hand the gate the post's address: validate
// POST.json's shape and copy it from the repository to /output/POST.json.
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const raw = readFileSync(join(botDir, 'POST.json'), 'utf8');
if (Buffer.byteLength(raw, 'utf8') > 16384) {
  console.error("POST.json is over the gate's 16384-byte cap");
  process.exit(1);
}
const post = JSON.parse(raw) as { url?: string };
const address = typeof post.url === 'string' ? post.url.split(/[?#]/)[0] : '';
const shape = /^https:\/\/(www\.|mobile\.)?(x|twitter)\.com\/[^/]+\/status\/\d+$/;
if (!shape.test(address)) {
  console.error('POST.json must name an X post: {"url":"https://x.com/<handle>/status/<id>"}');
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(join(botDir, 'POST.json'), join(outDir, 'POST.json'));
console.log(`POST.json copied to ${outDir}: ${address}`);
