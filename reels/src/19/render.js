// usage: node render.js frames <f1,f2,...> outdir   |  node render.js video out.mp4
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs'); const path = require('path');
(async () => {
  const [mode, a, b] = process.argv.slice(2);
  const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('console', m => console.log('page:', m.text()));
  page.on('pageerror', e => console.log('ERR', e.message));
  await page.goto('file://' + path.resolve(__dirname, 'reel.html'));
  await page.waitForFunction('window.ready===true', null, { timeout: 30000 });
  const grab = async f => {
    const d = await page.evaluate(f => { window.draw(f); return document.getElementById('c').toDataURL('image/png'); }, f);
    return Buffer.from(d.split(',')[1], 'base64');
  };
  if (mode === 'layout') { console.log(JSON.stringify(await page.evaluate(() => window.layoutInfo()), null, 1)); }
  else if (mode === 'frames') {
    fs.mkdirSync(b, { recursive: true });
    for (const f of a.split(',').map(Number)) fs.writeFileSync(path.join(b, `f${String(f).padStart(3, '0')}.png`), await grab(f));
  } else {
    const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'png', '-i', '-',
      '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', '30', a], { stdio: ['pipe', 'ignore', 'inherit'] });
    const T = await page.evaluate(() => window.TOTAL); for (let f = 0; f < T; f++) { const buf = await grab(f); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})();
