"""
6) AI slop detector - how much of this text looks machine-written?

Jev gives each paragraph a calibrated probability that it is generic
AI-generated filler ("slop"). The page score is the share of slop paragraphs.

This is a SIGNAL, not proof. No detector can prove who wrote a text.
Use it to sort or flag content, never to accuse a person.

Usage:
  uv run 6_ai_slop_detector.py               # built-in examples
  uv run 6_ai_slop_detector.py <url>         # paragraphs of a real web page
"""

import sys
import requests
from bs4 import BeautifulSoup

from jev import decide, noul

EXAMPLES = [
    "In today's fast-paced digital landscape, it is more important than ever to "
    "leverage cutting-edge solutions that empower stakeholders and unlock new "
    "possibilities for sustainable growth.",
    "I burned the first three batches. The fourth one worked because I finally "
    "let the dough rest overnight in the fridge - my grandmother never wrote "
    "that step down.",
    "Whether you are a seasoned professional or just starting out, this "
    "comprehensive guide will walk you through everything you need to know. "
    "Let's dive in!",
    "Our Postgres upgrade from 14 to 16 took 11 minutes of downtime. The slow "
    "part was not pg_upgrade but re-analyzing 400 GB of tables afterwards.",
    "In conclusion, by embracing these best practices, you can navigate the "
    "complexities of the modern world and achieve your goals with confidence.",
]

SLOP = noul(
    "Is this paragraph generic AI-generated filler (slop)?",
    true="Buzzwords, empty phrases ('in today's fast-paced world', 'let's dive in', 'in conclusion'), "
    "no concrete facts, numbers, names or personal experience.",
    false="Concrete details, specific facts or numbers, a personal story, or a clear individual voice.",
)


def paragraphs_from(url: str) -> list[str]:
    html = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"}).text
    texts = [p.get_text(" ", strip=True) for p in BeautifulSoup(html, "html.parser").find_all("p")]
    return [t for t in texts if len(t) > 80][:40]


if __name__ == "__main__":
    paragraphs = paragraphs_from(sys.argv[1]) if len(sys.argv) > 1 else EXAMPLES

    # One question per paragraph, all in one call. The text is in the state.
    result = decide(
        state={f"p{i}": text[:1500] for i, text in enumerate(paragraphs)},
        questions={
            f"p{i}": {**SLOP, "instructions": f"Paragraph p{i}: " + SLOP["instructions"]}
            for i in range(len(paragraphs))
        },
    )

    slop = 0
    for i, text in enumerate(paragraphs):
        p = result["answers"][f"p{i}"]["noul"]
        slop += p >= 0.5
        print(f"{p:4.0%}  {'SLOP' if p >= 0.5 else '    '}  {text[:90]}")

    print(f"\nSlop score: {slop / len(paragraphs):.0%} of {len(paragraphs)} paragraphs  "
          f"[{result['latency_ms']} ms, ${result['usage']['cost']:.6f}]")
