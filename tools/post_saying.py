#!/usr/bin/env python3
"""Post a saying from the lexicon to a Discord channel.

Posts through a Discord incoming webhook, so nothing needs hosting. The
webhook URL is read from the DISCORD_WEBHOOK_URL environment variable and
is never stored in the repository.

    # see what today's post would look like, without sending it
    python3 tools/post_saying.py --dry-run

    # post today's saying
    DISCORD_WEBHOOK_URL=... python3 tools/post_saying.py

    # post from a particular situation or part
    python3 tools/post_saying.py --situation "when the weather turns"
    python3 tools/post_saying.py --part "Hunting and the Forest"

    # post one at random rather than today's
    python3 tools/post_saying.py --random

Daily selection walks a fixed shuffle of the whole lexicon, one saying per
day, so nothing repeats until every saying has been posted once. The order
depends only on SHUFFLE_SEED, so the same date always yields the same
saying and a re-run never double-posts something different.
"""

import argparse
import json
import os
import random
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

LEXICON = Path(__file__).resolve().parent.parent / "lexicon.json"
SHUFFLE_SEED = 1317  # changing this reshuffles the daily order
EPOCH = date(2026, 1, 1)  # day 0 of the cycle
ELVEN_GREEN = 0x4F6F52


def load_sayings():
    with LEXICON.open(encoding="utf-8") as handle:
        return json.load(handle)["sayings"]


def pick(sayings, args):
    """Choose one saying according to the command-line options."""
    pool = sayings

    if args.part:
        needle = args.part.casefold()
        pool = [s for s in pool if needle in s["part"].casefold()]
        if not pool:
            sys.exit(f"No part matches {args.part!r}.")

    if args.situation:
        needle = args.situation.casefold()
        pool = [s for s in pool if needle in s["situation"].casefold()]
        if not pool:
            sys.exit(f"No situation matches {args.situation!r}.")

    if args.id:
        for saying in sayings:
            if saying["id"] == args.id:
                return saying
        sys.exit(f"No saying has id {args.id!r}.")

    if args.random or args.part or args.situation:
        return random.choice(pool)

    # Today's saying: step through a fixed shuffle of the whole pool.
    order = list(range(len(pool)))
    random.Random(SHUFFLE_SEED).shuffle(order)
    day = (date.today() - EPOCH).days
    return pool[order[day % len(pool)]]


def build_payload(saying):
    """Format the saying as a Discord embed."""
    lines = [f"> {saying['text']}"]
    if "answer" in saying:
        lines = [f"> **{saying['call']}**", f"> — *{saying['answer']}*"]

    embed = {
        "title": saying["situation"],
        "description": "\n".join(lines),
        "color": ELVEN_GREEN,
        "footer": {"text": f"{saying['part']} · {saying['use_note']}"},
    }
    if saying.get("canon"):
        embed["author"] = {"name": "Canon"}

    return {"embeds": [embed]}


def post(payload, url):
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "User-Agent": "cygnus-lexicon/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status
    except urllib.error.HTTPError as error:
        # Discord's body explains the failure; the URL itself is a secret.
        detail = error.read().decode("utf-8", "replace")[:500]
        sys.exit(f"Discord rejected the post ({error.code}): {detail}")
    except urllib.error.URLError as error:
        sys.exit(f"Could not reach Discord: {error.reason}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true",
                        help="print the post instead of sending it")
    parser.add_argument("--random", action="store_true",
                        help="pick at random rather than today's saying")
    parser.add_argument("--situation", help="match a situation by substring")
    parser.add_argument("--part", help="match a part by substring")
    parser.add_argument("--id", help="post one saying by its exact id")
    args = parser.parse_args()

    saying = pick(load_sayings(), args)
    payload = build_payload(saying)

    if args.dry_run:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        print(f"\nid: {saying['id']}", file=sys.stderr)
        return

    url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not url:
        sys.exit("DISCORD_WEBHOOK_URL is not set. Use --dry-run to preview.")

    post(payload, url)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"posted {saying['id']} at {stamp}")


if __name__ == "__main__":
    main()
