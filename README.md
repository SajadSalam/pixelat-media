# pixelat-media

Public media host for **بكسلات | Pixelat** (Instagram @pixelat.iq). Metricool pulls story files from here by URL.

- `kit/` — story generator (`make_story.js`, `story.html`, `story_audio.py`), brand fonts, original logo files (`kit/assets/`, never redraw), content bank (`content.json`), list of live reels (`published.json`)
- `reels/` — final reels
- `stories/YYYY-MM-DD-{designed|repost}.{mp4|png}` — daily stories

Render: `cd kit && NODE_PATH=$(npm root -g) node make_story.js designed <theme> <level> ../stories/x.mp4` (or `.png` for static), `node make_story.js repost ../reels/17.mp4 ../stories/y.mp4`.
