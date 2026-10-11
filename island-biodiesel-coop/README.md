# Island Biodiesel Co-op: website, Facebook and media control package

Everything the co-op needs to launch a website, take control of and refresh its **existing** Facebook account, and run its public communications.

```
island-biodiesel-coop/
├── website/                    Static 5-page site (no build step, no dependencies)
│   ├── index.html              Home
│   ├── fuel.html               Our fuel: blends, FAQs, engine guidance
│   ├── oil.html                Donate oil: business pickups and household drop-off, with form
│   ├── join.html               Membership tiers and sign-up form
│   ├── contact.html            Location, hours, media contact, message form
│   └── assets/                 styles.css, site.js, logo.svg, og-image (Facebook link preview)
├── facebook/
│   ├── TAKE_CONTROL_AND_REFRESH.md   Secure ownership of the existing account, then refresh it
│   ├── CONTENT_CALENDAR.md           12 ready-to-post posts for the first 4 weeks
│   ├── cover.png / cover.svg         Cover photo, 1640×624
│   └── profile.png / profile.svg     Profile picture, 720×720
└── media-kit/
    ├── MEDIA_CONTROL_POLICY.md  Who owns and controls what, approvals, moderation, crisis plan
    ├── ACCOUNTS_REGISTER.csv    Who has access to every account (never passwords)
    ├── BRAND_GUIDE.md           Name, logo, colours, fonts, voice
    └── PRESS_KIT.md             Boilerplate, fact sheet, press release template
```

## Start here

1. **Facebook first.** Work through `facebook/TAKE_CONTROL_AND_REFRESH.md` Steps 1–3. Making sure the co-op owns its existing account matters more than anything else in this package.
2. **Board adopts** `media-kit/MEDIA_CONTROL_POLICY.md` and names the media lead and backup admin.
3. **Fill in the placeholders** (below), then launch the website.
4. **Refresh the Facebook Page** (Step 4) and start the content calendar.

## Placeholders to fill in

Placeholders appear as `[BRACKETS]`. On the website they're also highlighted yellow so none slip through. Find them all with:

```sh
grep -rnI "\[[A-Z0-9$]" island-biodiesel-coop/
```

| Placeholder | Where |
|---|---|
| `[ISLAND NAME]` | Website, Facebook copy, press kit |
| `[STREET ADDRESS]`, `[DAYS & HOURS]`, `[LOCATION]` | Website, Facebook About |
| `[EMAIL]`, `[PHONE]`, `[MEDIA-EMAIL]` | Website footer and Contact page |
| `[FACEBOOK-HANDLE]` | Website footer and Contact page — the **existing** Page's username |
| `[YOUR-DOMAIN]` | Website `og:` tags, Facebook copy, policy |
| `[FORM-ENDPOINT-URL]` | The three website forms (see below) |
| `[$00]` prices, `[B100 / B20 / B5]` blends | Join page, Fuel page |
| `[0,000]` impact numbers | Home page, content calendar, press kit |
| `[BYLAWS-PDF-URL]`, `[LEGAL ENTITY / REG. NO.]` | Join page, footer |

## Launching the website

It's plain HTML/CSS, so any static host works. Free options:

- **Netlify** — drag the `website/` folder onto app.netlify.com/drop. Netlify Forms can handle the forms.
- **GitHub Pages** — publish the `website/` folder from this repository.
- **Your existing host** — upload the contents of `website/` by FTP.

Then point the co-op's domain at it, and record the domain and hosting in `media-kit/ACCOUNTS_REGISTER.csv`.

**Forms:** each form has `data-endpoint="[FORM-ENDPOINT-URL]"`. Replace it with an endpoint from a form service such as Formspree, Basin or Netlify Forms, set to deliver to a co-op email address. Until it's set, submitting shows a polite "please email us" message instead of failing.

**Link previews:** the site's Facebook preview uses `assets/og-image.png`. After launch, paste the URL into Facebook's [Sharing Debugger](https://developers.facebook.com/tools/debug/) to refresh the preview.

## Editing the graphics

The `.svg` files are the editable sources (open in Inkscape, Figma, or a text editor). The `.png` files are what you upload to Facebook, since Facebook doesn't accept SVG.
