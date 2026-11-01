# pixelat-media

Public media host for **بكسلات | Pixelat** (Instagram @pixelat.iq). Metricool pulls story files from here by URL.

- `kit/` — story generator (`make_story.js`, `story.html`, `story_audio.py`), brand fonts, original logo files (`kit/assets/`, never redraw), content bank (`content.json`), list of live reels (`published.json`)
- `reels/` — final reels
- `stories/YYYY-MM-DD-{designed|repost}.{mp4|png}` — daily stories
- `highlights/` — Instagram highlight covers (1080×1920, icon inside the centre circle) + `preview-profile.png`
- `brand/` — logo files (PNG/SVG), profile pictures, Facebook cover, merch mockups (`merch/`), bio texts (`bio.txt`)

Render: `cd kit && NODE_PATH=$(npm root -g) node make_story.js designed <theme> <level> ../stories/x.mp4` (or `.png` for static), `node make_story.js repost ../reels/17.mp4 ../stories/y.mp4`.

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
