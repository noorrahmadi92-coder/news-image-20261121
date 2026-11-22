// Entry for the make.fun news-image-20261121 bounty (Node 22, stdlib only):
// the image is the entry.png beside this file, and the program copies it
// to /output/entry.png. It first checks the PNG magic bytes so a broken
// file fails loudly instead of entering silently.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
const bytes = readFileSync(source);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(pngMagic)) {
  throw new Error('entry.png is not a PNG file');
}
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const dest = join(outDir, 'entry.png');
copyFileSync(source, dest);
console.log(`Wrote ${dest} (${bytes.length} bytes)`);
