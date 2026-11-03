// node make_pixelrun.js <out.mp4> [frames <dir> 15,60,149]
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');
(async () => {
  const [out, cmd, dir, list] = process.argv.slice(2);
  const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('pageerror', e => { console.error('PAGE ERROR', e.message); process.exitCode = 1; });
  await page.addInitScript(c => { window.__CONTENT = c; }, JSON.parse(fs.readFileSync(path.join(__dirname, 'content.json'), 'utf8')));
  await page.goto('file://' + path.resolve(__dirname, 'story.html') + '?mode=designed&theme=0&level=1');
  await page.waitForFunction('window.ready===true', null, { timeout: 30000 });
  await page.addScriptTag({ path: path.join(__dirname, 'pixelrun.js') });
  const grab = async f => Buffer.from((await page.evaluate(f => { window.draw(f); return document.getElementById('c').toDataURL('image/png'); }, f)).split(',')[1], 'base64');
  if (cmd === 'frames') { for (const f of list.split(',')) fs.writeFileSync(path.join(dir, `f${f}.png`), await grab(+f)); }
  else {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'run-')), silent = path.join(tmp, 's.mp4'), wav = path.join(tmp, 'a.wav');
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'png', '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', silent], { stdio: ['pipe', 'ignore', 'inherit'] });
    for (let f = 0; f < 150; f++) { const b = await grab(f); if (!ff.stdin.write(b)) await new Promise(r => ff.stdin.once('drain', r)); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
    execFileSync('python3', [path.join(__dirname, 'pixelrun_audio.py'), wav]);
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', silent, '-i', wav, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out]);
  }
  await browser.close(); console.log('OK');
})();
