---
name: logo-maker
description: Create logos as clean SVG (plus PNG export) for Saidur Rahman's brand or any client. Use when the user asks for a logo, wordmark, icon, or brand mark.
---

# Logo Maker

## Defaults
- Brand colors: red #E10600, near-black #0A0A0A, off-white #F5F2EA.
- Output: SVG (vector, master) + PNG 2048x2048 transparent + PNG on dark background.
- Save to `logos/` in the repo, then give the user the file path/link (user is on iPhone, can't run code).

## Process
1. Don't over-ask. Pick a smart concept, state the assumption in one line.
2. Make 3 variations: wordmark, icon-only, icon + wordmark.
3. Rules: max 2-3 colors, simple geometry, readable at 32px, works on dark and light backgrounds, no gradients, no tiny details.
4. Write SVG by hand (viewBox 0 0 512 512, text converted to shapes or use a safe font stack like Arial/Helvetica bold).
5. Export PNG: `render the SVG with Playwright/Chromium screenshot (omitBackground) -- rsvg is not installed.
6. Show a preview, commit, push, and share links.

## Style notes for video editor brands
Play button, timeline/cut marks, film frame, or a bold initial letter work well.
