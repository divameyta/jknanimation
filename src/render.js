// Merender src/animasi.html menjadi video MP4 frame demi frame.
// Pemakaian:
//   node src/render.js snap <outdir> <t1> <t2> ...   -> PNG cuplikan pada detik tertentu
//   node src/render.js video <out.mp4> [fps] [workers] -> video penuh (tanpa audio)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const HTML = 'file://' + path.resolve(__dirname, 'animasi.html') + '?capture=1' + (process.env.SKALA ? '&k=' + process.env.SKALA : '');

async function openPage(browser) {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto(HTML);
  await page.evaluate(() => window.ready);
  return page;
}

async function snap(outdir, times) {
  fs.mkdirSync(outdir, { recursive: true });
  const browser = await chromium.launch();
  const page = await openPage(browser);
  for (const t of times) {
    await page.evaluate(t => window.render(t), parseFloat(t));
    await page.screenshot({ path: path.join(outdir, `t${String(t).padStart(6, '0')}.png`) });
  }
  await browser.close();
}

async function chunk(browser, f0, f1, fps, out) {
  const page = await openPage(browser);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((res, rej) => ff.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg ' + c))));
  for (let f = f0; f < f1; f++) {
    await page.evaluate(t => window.render(t), f / fps);
    const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if ((f - f0) % 300 === 0) console.log(`[${out}] ${f - f0}/${f1 - f0}`);
  }
  ff.stdin.end();
  await done;
  await page.close();
}

async function video(out, fps = 30, workers = 4) {
  const browser = await chromium.launch();
  const tmp = await openPage(browser);
  const total = await tmp.evaluate(() => window.TOTAL);
  await tmp.close();
  const N = Math.round(total * fps), per = Math.ceil(N / workers);
  const dir = path.dirname(path.resolve(out));
  const parts = [];
  const jobs = [];
  for (let w = 0; w < workers; w++) {
    const f0 = w * per, f1 = Math.min(N, f0 + per);
    if (f0 >= f1) break;
    const p = path.join(dir, `_part${w}.mp4`);
    parts.push(p);
    jobs.push(chunk(browser, f0, f1, fps, p));
  }
  await Promise.all(jobs);
  await browser.close();
  const list = path.join(dir, '_parts.txt');
  fs.writeFileSync(list, parts.map(p => `file '${p}'`).join('\n'));
  await new Promise((res, rej) => spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', out], { stdio: 'inherit' })
    .on('close', c => c === 0 ? res() : rej(new Error('concat ' + c))));
  for (const p of [...parts, list]) fs.unlinkSync(p);
  console.log('Selesai:', out, `${total}s`, `${N} frame`);
}

const [, , mode, a, ...rest] = process.argv;
if (mode === 'snap') snap(a, rest).catch(e => { console.error(e); process.exit(1); });
else if (mode === 'video') video(a, parseInt(rest[0] || 30), parseInt(rest[1] || 4)).catch(e => { console.error(e); process.exit(1); });
else console.log('mode: snap | video');
