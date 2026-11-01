// Animated Pixelat highlight stories.
//   NODE_PATH=$(npm root -g) node make_highlight_anim.js <storyId> frames <outDir> <f1,f2,...>   -> PNG stills for checking
//   NODE_PATH=$(npm root -g) node make_highlight_anim.js <storyId> video <out.mp4>               -> 1080x1920 30 fps + 8-bit audio
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');
(async () => {
  const [id, mode, out, list] = process.argv.slice(2);
  const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('pageerror', e => { console.error('PAGE ERROR', e.message); process.exitCode = 1; });
  await page.goto('file://' + path.resolve(__dirname, 'highlight-anim.html') + '?s=' + id);
  await page.waitForFunction('window.ready===true', null, { timeout: 30000 });
  const total = await page.evaluate(() => window.TOTAL);
  const grab = async f => Buffer.from((await page.evaluate(f => { window.draw(f); return document.getElementById('c').toDataURL('image/png'); }, f)).split(',')[1], 'base64');
  if (mode === 'frames') {
    fs.mkdirSync(out, { recursive: true });
    for (const f of list.split(',').map(Number)) fs.writeFileSync(path.join(out, `${id}-f${String(f).padStart(3, '0')}.png`), await grab(f));
  } else {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'hl-'));
    const silent = path.join(tmp, 'v.mp4'), wav = path.join(tmp, 'a.wav'), part = out.replace(/\.mp4$/, '.part.mp4');
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'png', '-i', '-',
      '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-pix_fmt', 'yuv420p', '-r', '30', silent], { stdio: ['pipe', 'ignore', 'inherit'] });
    for (let f = 0; f < total; f++) { const buf = await grab(f); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
    ff.stdin.end(); const code = await new Promise(r => ff.on('close', r)); if (code) throw new Error('ffmpeg ' + code);
    execFileSync('python3', [path.join(__dirname, 'highlight_audio.py'), id, String(total / 30), wav]);
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', silent, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', part]);
    fs.renameSync(part, out);
  }
  await browser.close();
  console.log('OK', out, 'frames', total);
})();
