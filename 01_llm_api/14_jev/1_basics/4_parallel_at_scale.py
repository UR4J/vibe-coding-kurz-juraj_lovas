"""
4) Parallel at scale - classify hundreds of items in seconds.

Jev is built for volume: thousands of e-mails, comments, tickets, logs.
One call takes ~300 ms, so one-by-one is still slow for 1,000 items.
Two ways to go faster (you can combine them):

  A) one by one            - N calls in a row              (slow, the baseline)
  B) parallel              - N calls, 32 at the same time  (threads)
  C) parallel + batched    - N/10 calls, each asks about 10 items at once

Usage:  uv run 4_parallel_at_scale.py [number_of_items]   (default 200)
"""

import sys
import time
import random
from concurrent.futures import ThreadPoolExecutor

from jev import decide, choice

N_ITEMS = int(sys.argv[1]) if len(sys.argv) > 1 else 200
WORKERS = 32
BATCH_SIZE = 10

# Build N synthetic support e-mails from templates
SUBJECTS = ["order #{n}", "invoice {n}", "my account", "the app", "parcel {n}", "refund {n}"]
BODIES = [
    "Where is {s}? It is late.",
    "I was charged twice for {s}.",
    "I cannot log in to {s}, it shows an error.",
    "Please cancel {s}, I changed my mind.",
    "Thank you, {s} arrived and all is fine!",
    "Your newsletter about {s} is spam, stop it.",
]
random.seed(42)
ITEMS = [
    random.choice(BODIES).format(s=random.choice(SUBJECTS).format(n=random.randint(1000, 9999)))
    for _ in range(N_ITEMS)
]

CATEGORY = dict(
    shipping="Delivery and order status.",
    billing="Payments and refunds.",
    technical="Errors and login problems.",
    cancellation="Cancel an order or subscription.",
    other="Thanks, spam complaints, anything else.",
)


def classify_one(email: str) -> tuple[dict, float]:
    result = decide(
        state={"source": "support inbox"},
        questions={"category": choice(f"What is this e-mail about: '{email}'?", **CATEGORY)},
    )
    return result["answers"], result["usage"]["cost"]


def classify_batch(emails: list[str]) -> tuple[list, float]:
    # One question per e-mail. The e-mail text is in the question, the state is shared.
    questions = {
        f"e{i}": choice(f"What is this e-mail about: '{email}'?", **CATEGORY)
        for i, email in enumerate(emails)
    }
    result = decide(state={"source": "support inbox"}, questions=questions)
    return list(result["answers"].values()), result["usage"]["cost"]


def run(label: str, fn, jobs: list, workers: int) -> None:
    started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(fn, jobs))
    seconds = time.perf_counter() - started
    cost = sum(cost for _, cost in results)
    print(f"{label:<34} {len(jobs):>4} calls  {seconds:6.1f} s   ${cost:.5f}")


if __name__ == "__main__":
    print(f"Classifying {N_ITEMS} e-mails\n")

    # A) One by one - measure 20 items and extrapolate, to save your time
    sample = ITEMS[:20]
    started = time.perf_counter()
    for email in sample:
        classify_one(email)
    per_item = (time.perf_counter() - started) / len(sample)
    print(f"{'A) one by one (estimated)':<34} {N_ITEMS:>4} calls  {per_item * N_ITEMS:6.1f} s")

    # B) Parallel
    run(f"B) parallel ({WORKERS} threads)", classify_one, ITEMS, WORKERS)

    # C) Parallel + batched
    batches = [ITEMS[i : i + BATCH_SIZE] for i in range(0, N_ITEMS, BATCH_SIZE)]
    run(f"C) parallel + {BATCH_SIZE} items per call", classify_batch, batches, WORKERS)

    print(
        "\nBatching saves money: the shared state and the category list are sent once per\n"
        "call, not once per e-mail. Watch OpenRouter rate limits when you add threads."
    )
