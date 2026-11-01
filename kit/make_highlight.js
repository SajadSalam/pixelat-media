// Pixelat highlight stories (static PNG, 1080x1920).
//   NODE_PATH=$(npm root -g) node make_highlight.js <storyId> <out.png>   e.g. about-1 ../highlights/stories/about-1.png
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [id, out] = process.argv.slice(2);
  const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('pageerror', e => { console.error('PAGE ERROR', e.message); process.exitCode = 1; });
  await page.goto('file://' + path.resolve(__dirname, 'highlight.html') + '?s=' + id);
  await page.waitForFunction('window.ready===true', null, { timeout: 30000 });
  const data = await page.evaluate(() => document.getElementById('c').toDataURL('image/png'));
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, Buffer.from(data.split(',')[1], 'base64'));
  await browser.close();
  console.log('OK', out);
})();
