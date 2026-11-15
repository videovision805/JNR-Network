// Frame-accurate recorder: renders the HTML one frame at a time with Playwright
// and pipes lossless PNG frames into ffmpeg (H.264, 1080x1920, 25 fps, silent).
//
//   node record.js                       -> full video
//   node record.js --stills 0.6,5.5 out/ -> PNG stills at given seconds (for checking)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const HTML = path.resolve(__dirname, 'OLTtx-motion-graphics-loomstyle-polished.html');
const OUT = path.resolve(__dirname, 'OLTtx-motion-graphics-loomstyle-polished.mp4');

(async () => {
  const args = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('console', m => console.log('[page]', m.text()));
  page.on('pageerror', e => { console.error('[pageerror]', e.message); process.exitCode = 1; });
  await page.goto('file://' + HTML + '?record=1');
  await page.evaluate(() => window.__ready);
  const ok = await page.evaluate(() => document.fonts.check('700 60px OLTBangla', 'সব') && document.fonts.check('800 60px OLTInter', 'OLTtx'));
  if (!ok) throw new Error('fonts not loaded');
  const { DUR, FPS } = await page.evaluate(() => ({ DUR: window.DUR, FPS: window.FPS }));

  if (args[0] === '--stills') {
    const times = args[1].split(',').map(Number);
    const dir = path.resolve(args[2] || 'stills');
    fs.mkdirSync(dir, { recursive: true });
    for (const t of times) {
      await page.evaluate(t => window.renderAt(t), t);
      await page.screenshot({ path: path.join(dir, `t${t.toFixed(2).padStart(5, '0')}.png`) });
    }
    await browser.close();
    return;
  }

  const frames = Math.round(DUR * FPS);
  const ff = spawn('ffmpeg', [
    '-y', '-loglevel', 'error',
    '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
    '-vf', 'scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-profile:v', 'high', '-level', '4.2',
    '-x264-params', 'aq-mode=3:aq-strength=0.9:deblock=-1,-1',
    '-g', '50', '-r', String(FPS),
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
    '-movflags', '+faststart', '-an', OUT,
  ], { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((res, rej) => ff.on('close', c => (c === 0 ? res() : rej(new Error('ffmpeg exit ' + c)))));

  const t0 = Date.now();
  for (let f = 0; f < frames; f++) {
    await page.evaluate(t => window.renderAt(t), f / FPS);
    const buf = await page.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 50 === 0) console.log(`frame ${f}/${frames}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end();
  await done;
  await browser.close();
  console.log('wrote', OUT, `in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
})().catch(e => { console.error(e); process.exit(1); });
