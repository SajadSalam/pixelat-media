# pixelat-media

Public media host for **بكسلات | Pixelat** (Instagram @pixelat.iq). Metricool pulls story files from here by URL.

- `kit/` — story generator (`make_story.js`, `story.html`, `story_audio.py`), brand fonts, original logo files (`kit/assets/`, never redraw), content bank (`content.json`), list of live reels (`published.json`)
- `kit/pixelrun.js`, `make_pixelrun.js`, `pixelrun_audio.py` — 5 s original mini-game story (hero collects 12 pixels, counter counts them): `cd kit && NODE_PATH=$(npm root -g) node make_pixelrun.js ../stories/x.mp4`
- `reels/` — final reels
- `stories/YYYY-MM-DD-{designed|repost}.{mp4|png}` — daily stories
- `highlights/` — Instagram highlight covers (1080×1920, icon inside the centre circle) + `preview-profile.png`
- `highlights/stories/` — the stories that go inside each highlight. «منو إحنا»: `about-1.mp4` → `about-2.mp4` → `about-3.mp4` → reel 17
- `kit/highlight-anim.html`, `make_highlight_anim.js`, `highlight_audio.py` — animated highlight stories (pixel studio world, 7–8 s, 8-bit audio); `kit/assets/svc/` — service icons incl. the film-strip video icon
- `brand/` — logo files (PNG/SVG), profile pictures, Facebook cover, merch mockups (`merch/`), bio texts (`bio.txt`)

Render: `cd kit && NODE_PATH=$(npm root -g) node make_story.js designed <theme> <level> ../stories/x.mp4` (or `.png` for static), `node make_story.js repost ../reels/17.mp4 ../stories/y.mp4`.
Highlight stories: `cd kit && NODE_PATH=$(npm root -g) node make_highlight_anim.js about-1 video ../highlights/stories/about-1.mp4` (or `frames <dir> 30,90,150` for stills to check).

## Reels

17–18 were here first. 19–29 continue the numbering (all 1080×1920, 30 fps). A reel goes into `kit/published.json` only once it is live on Instagram.

| file | reel |
|---|---|
| 19.mp4 | نسوي تطبيقات |
| 20.mp4 | نسوي مواقع |
| 21.mp4 | نسوي فيديوهات |
| 22.mp4 | نروّج لمشروعك |
| 23.mp4 | منو إحنا (music only) |
| 24.mp4 | شغلنا مو مبكسل (music only) |
| 25.mp4 | مراحل شغلنا (music only) |
| 26.mp4 | ليش تحتاج موقع |
| 27.mp4 | ليش تحتاج ترويج |
| 28.mp4 | ليش تخلي مختص يسوي فيديوهاتك |
| 29.mp4 | ليش مشروعك يحتاج تطبيق |
