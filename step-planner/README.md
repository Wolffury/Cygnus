# Block Step Planner

A tablet app (Android or any modern browser) for planning, drawing and quoting hardscape and
stonework jobs: block steps, landings, retaining walls, walkways and patios.

## What it does

- **Blueprint**: a measured plan on blueprint paper with every block, cap and cut piece,
  dimensions, a stair section, north arrow, scale bar and title block. Drag items with a finger;
  type exact measurements (`4' 6"`, `54"`, `4.5'`, `1.37m`) on the Item tab.
- **3D render**: the same job in 3D with the real block, cap and paver sizes and colours, trees,
  shrubs, boulders, the house and raised grade. Orbit with a finger, move the sun, save a picture.
- **Many configurations**: straight flights, wraparound (one side or both, pyramid), cheek walls,
  flights that start on a landing, and one-tap layouts for two flights with a landing, L-shapes
  and U-turns. Each item picks its own block, cap, colour, cap overhang and rise per step.
- **Materials library**: Abbotsford wall blocks (SR Classic 6° and the Allan Block line),
  Garden WallScapes, Pro Cap Max caps, Classic and Old Country Stone pavers, Texada and
  Saturna slabs, plus generic precast and natural stone. Add your own materials with sizes,
  colours and prices; they're saved on the tablet for every job.
- **Estimates and quotes**: a full takeoff (blocks, caps, cut pieces, pavers, base, fill,
  drain rock, bedding sand, polymeric sand, adhesive), labour from production rates,
  equipment, delivery, disposal, contingency, overhead and profit, GST and PST, and deposit.
  Save a client quote page (with the rendering and blueprint, prints to PDF) or export the
  line items as CSV or JSON.
- **Ledgerline**: **Export to Ledgerline (CSV)** on the Quote tab, then in Ledgerline go to
  Estimates → **Import CSV**. The quote becomes a Ledgerline estimate with the client, every
  line (labour / materials, units, taxable), GST as the tax rate and PST on materials as its
  own line, so the totals match to the cent. The columns can be remapped for other apps.
- **AI assistant**: describe the job in plain words or attach a photo of your sketch; Claude
  draws a new layout or revises the current one with the materials you name.
- **Checks**: riser height, tread depth, width, first-riser match, cap/riser fit, handrails,
  and wall height.

## Default build: SR Classic + Pro Cap Max

Steps default to **Abbotsford SR Classic 6° (Grey)** risers with **18" Pro Cap Max (Grey)** treads:

- Each riser block is cut to 3¾" high so block + 3¾" cap = **7½" rise** per step.
- The cap overhangs the riser face by 1"; the next riser sits snug against the back of the cap,
  on compacted base level with the cap top. Treads are 11" nosing to nosing.
- Set **Rise per step** to 0 to use full-height blocks Allan Block style (bottom course buried).

Abbotsford sizes come from published specs; check them against your supplier's current
sheets. Prices are examples until you enter your own on the Materials tab.

## Put it on an Android tablet

1. Host this folder on any HTTPS static host (GitHub Pages works: Settings → Pages →
   deploy from branch, then open `https://<user>.github.io/<repo>/step-planner/`).
2. Open the link in Chrome on the tablet → menu ⋮ → **Add to Home screen / Install app**.
3. It opens full screen like a normal app and works offline after the first load
   (the AI assistant needs a connection).

## AI setup

Inside claude.ai, the assistant uses your Claude account. Anywhere else,
enter an Anthropic API key on the AI tab. The key stays on the tablet in local storage.

## Android app (APK)

`android/` wraps the planner in a small native Android app (min Android 10). It runs fully
offline (three.js is bundled), opens the system picker for photos and files, and saves exports
to **Downloads › Block Step Planner** with a **Send** button for email, Drive and so on.

- Install: copy `android/dist/StepPlanner-<version>.apk` to the tablet, open it, and allow
  "Install unknown apps" for the app you opened it from when Android asks.
- Rebuild: `android/build-apk.sh <version>` (needs Java, Python 3, ImageMagick, curl and npm;
  it downloads aapt2, dx and apksig from Maven Central, no Android SDK needed).
- Signing key: put your `release.p12` in `android/` before building (it is never committed; this
  repo is public). Keep using the same key: an update signed with a different key won't install
  over the old one, and uninstalling erases the jobs saved in the app. Set `KEY_PASS` if you
  change its password. Without the file, the script makes a new key.
- Inside the app the AI assistant uses your Anthropic API key (AI tab).
