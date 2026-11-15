# Cygnus
For the Schooner Cygnus

## Lexicon

`LEXICON.md` holds the elven sayings — 278 of them, filed by the situation
they are spoken in rather than by subject. It is the source of truth; edit it
by hand.

| File | What it is |
| --- | --- |
| `LEXICON.md` | The sayings, in 13 parts and 70 situations. Edit this one. |
| `lexicon.json` | The same sayings as data, for anything that reads them programmatically. Generated — do not edit. |
| `tools/build_lexicon_json.py` | Regenerates `lexicon.json` from `LEXICON.md`. |
| `tools/post_saying.py` | Posts a saying to Discord. |
| `.github/workflows/daily-saying.yml` | Posts one saying a day, at 13:00 UTC. |

After editing `LEXICON.md`:

```sh
python3 tools/build_lexicon_json.py
```

### Posting to Discord

The daily post goes through a Discord incoming webhook, so there is no bot to
host and no token in the repository.

1. In Discord: **Channel Settings → Integrations → Webhooks → New Webhook**,
   choose the channel, then **Copy Webhook URL**.
2. In GitHub: **Settings → Secrets and variables → Actions → New repository
   secret**, named `DISCORD_WEBHOOK_URL`, with that URL as the value.

Until the secret exists the workflow previews the post in its log instead of
sending it, so it never fails for want of setup.

To post on demand, go to **Actions → Daily saying → Run workflow**. It takes
an optional situation or part to draw from, and a toggle for a random saying
instead of the day's.

Locally:

```sh
python3 tools/post_saying.py --dry-run                        # preview today's
python3 tools/post_saying.py --situation "when the watch changes"
DISCORD_WEBHOOK_URL=... python3 tools/post_saying.py          # actually post
```

The daily saying walks a fixed shuffle of the whole lexicon, so nothing
repeats for 278 days. Re-running the same day posts the same saying.
