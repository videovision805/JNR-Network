# OLTtx — Loom-style motion graphics (vertical)

- `OLTtx-motion-graphics-loomstyle-polished.mp4` — 1080x1920, 25 fps, 30 s, H.264 High, silent
- `OLTtx-motion-graphics-loomstyle-polished.html` — the source. Open it in Chrome to watch it play live (it loops).
- `record.js` — renders the HTML frame by frame with Playwright and encodes with ffmpeg
- `fonts/` — Noto Sans Bengali + Inter (variable woff2), loaded locally by the HTML

## Rebuild

```bash
cd oltx-loomstyle
node record.js                                  # full MP4 (about 10 min)
node record.js --stills 2.6,7.2,12,15.4 stills/ # PNG checks at given seconds
```

Needs Node, Playwright (Chromium) and ffmpeg.

## Scene timing

| # | Scene | Time |
|---|-------|------|
| 1 | POV hook + logo badge + wordmark | 0–4 s |
| 2 | Kinetic type "সব OLT, এক ড্যাশবোর্ডে" + brands + ONU dots | 4–8 s |
| 3 | Dashboard window, cursor clicks BDCOM row, detail card | 8–13 s |
| 4 | Bell + Telegram-style alert, cursor clicks message | 13–17 s |
| 5 | Alert card morphs → FREE card → cursor picks PRO → PRO card | 17–21 s |
| 6 | Starburst wipe → CTA, URL pill, prices, footer, end-card hold | 21–30 s |
