// Pixelat IG story builder.
//   node make_story.js designed <themeIndex> <level> <out.mp4|out.png>   (.png = static version)
//   node make_story.js repost <reel.mp4> <out.mp4>
// Needs: playwright (preinstalled; run with NODE_PATH=$(npm root -g)), ffmpeg, python3+numpy.
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');
(async () => {
  const [mode, a, b, c] = process.argv.slice(2);
  const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('pageerror', e => { console.error('PAGE ERROR', e.message); process.exitCode = 1; });
  await page.addInitScript(c => { window.__CONTENT = c; }, JSON.parse(fs.readFileSync(path.join(__dirname, 'content.json'), 'utf8')));
  const q = mode === 'repost' ? 'mode=repost' : `mode=designed&theme=${a}&level=${b}`;
  await page.goto('file://' + path.resolve(__dirname, 'story.html') + '?' + q);
  await page.waitForFunction('window.ready===true', null, { timeout: 30000 });
  const grab = async f => Buffer.from((await page.evaluate(f => { window.draw(f); return document.getElementById('c').toDataURL('image/png'); }, f)).split(',')[1], 'base64');
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'story-'));
  if (mode === 'repost') {
    const frame = path.join(tmp, 'frame.png'); fs.writeFileSync(frame, await grab(0));
    const out = b;
    // reel scaled into the window (x252 y470, 576x1024), frame on top, reel audio kept; stories max 60 s
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', a, '-i', frame, '-filter_complex',
      '[0:v]scale=576:1024,pad=1080:1920:252:470:color=#612AFF[v];[v][1:v]overlay=0:0,format=yuv420p[o]',
      '-map', '[o]', '-map', '0:a?', '-t', '60', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-c:a', 'aac', '-b:a', '160k', '-r', '30', '-movflags', '+faststart', out]);
  } else {
    const out = c;
    if (out.endsWith('.png')) { fs.writeFileSync(out, await grab(209)); }
    else {
      const silent = path.join(tmp, 's.mp4'), wav = path.join(tmp, 'a.wav');
      const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'png', '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', silent], { stdio: ['pipe', 'ignore', 'inherit'] });
      for (let f = 0; f < 210; f++) { const buf = await grab(f); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
      ff.stdin.end(); await new Promise(r => ff.on('close', r));
      execFileSync('python3', [path.join(__dirname, 'story_audio.py'), wav]);
      execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', silent, '-i', wav, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out]);
    }
  }
  await browser.close();
  console.log('OK', mode === 'repost' ? b : c);
})();
