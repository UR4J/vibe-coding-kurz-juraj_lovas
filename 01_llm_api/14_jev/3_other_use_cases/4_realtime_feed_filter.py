"""
4) Real-time feed filter - label posts the moment they arrive.

A human cannot read every post in a busy feed. Jev can label each one in
~300 ms, so the label is there before you scroll to it (the same idea as
a browser extension that marks posts as "golden nugget" or "AI slop").

This script uses a REAL live feed: the newest Hacker News stories
(public API, no key). It polls for new stories and labels them as they come.

Usage:  uv run 4_realtime_feed_filter.py [seconds]   (default 60)
"""

import sys
import time
import requests
from concurrent.futures import ThreadPoolExecutor

from jev import decide, noul, choice

HN = "https://hacker-news.firebaseio.com/v0"
RUN_SECONDS = int(sys.argv[1]) if len(sys.argv) > 1 else 60
POLL_SECONDS = 10

QUESTIONS = {
    "label": choice(
        "How should this post be labelled for an AI engineer's feed?",
        golden_nugget="Deep technical content, research, a useful tool or a real lesson learned.",
        news="Important news about AI, software or the tech industry.",
        hype="Clickbait, vague claims, marketing, 'AI will replace X'.",
        off_topic="Not about software or AI.",
    ),
    "worth_reading": noul(
        "Is this worth 5 minutes of an AI engineer's time?",
        true="Likely to teach something useful about building software or AI systems.",
        false="Unlikely to be useful for that.",
    ),
}


def fetch_story(story_id: int) -> dict | None:
    item = requests.get(f"{HN}/item/{story_id}.json", timeout=10).json()
    return item if item and item.get("title") else None


def label(story: dict) -> None:
    started = time.perf_counter()
    answers = decide(
        state={"title": story["title"], "url": story.get("url", "(text post)")},
        questions=QUESTIONS,
    )["answers"]
    ms = (time.perf_counter() - started) * 1000
    worth = answers["worth_reading"]["noul"]
    star = "★" if worth >= 0.5 else " "
    print(f"{star} {worth:4.0%}  {answers['label']['choice']:<14} {ms:4.0f} ms  {story['title'][:75]}")


if __name__ == "__main__":
    seen: set[int] = set()
    deadline = time.time() + RUN_SECONDS
    first_round = True

    with ThreadPoolExecutor(max_workers=10) as pool:
        while time.time() < deadline:
            ids = requests.get(f"{HN}/newstories.json", timeout=10).json()
            new_ids = [i for i in ids[:15] if i not in seen]
            seen.update(ids[:15])

            if first_round:
                print(f"--- Latest {len(new_ids)} stories, then live for {RUN_SECONDS} s ---")
                first_round = False
            stories = [s for s in pool.map(fetch_story, new_ids) if s]
            list(pool.map(label, stories))

            time.sleep(POLL_SECONDS)
