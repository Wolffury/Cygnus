# Block Step Planner

A tablet app (Android or any modern browser) for laying out concrete block step jobs.

- **Blueprint**: a measured plan view on blueprint paper with block-by-block layout, cut pieces,
  dimensions, a stair section, north arrow, scale bar and title block. Drag items with a finger;
  type exact measurements (`4' 6"`, `54"`, `4.5'`, `1.37m`) on the Item tab.
- **3D render**: the same job as a 3D scene with the real block size and color, trees,
  evergreens, shrubs, boulders, the house, walkways and raised grade. Orbit with a finger,
  move the sun, and save a PNG rendering.
- **AI assistant**: describe the job in plain words (and optionally attach a photo of your
  sketch). Claude draws a new layout or revises the current one. Undo always works.
- **Step checks**: riser height, tread depth, width, block overlap and handrail warnings
  (common residential limits; your local code decides).
- **Material order**: full blocks, cut pieces and order quantity with 5% waste.
- **Export sheet**: a 17 × 11 blueprint PNG with plan, sections and material schedule.
- Jobs save on the tablet; export/import job files to move them between devices.

## Put it on an Android tablet

1. Host this folder on any HTTPS static host (GitHub Pages works: Settings → Pages →
   deploy from branch, then open `https://<user>.github.io/<repo>/step-planner/`).
2. Open the link in Chrome on the tablet → menu ⋮ → **Add to Home screen / Install app**.
3. It opens full screen like a normal app and works offline after the first load
   (the AI assistant needs a connection).

## AI setup

Inside claude.ai, the assistant uses your Claude account. Anywhere else,
enter an Anthropic API key on the AI tab. The key stays on the tablet in local storage.
