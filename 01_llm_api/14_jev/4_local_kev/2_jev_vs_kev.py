"""
2) Jev (closed, cloud) vs. Kev-9B (open, local) - same questions, same tickets.

Both speak the same API, so the only difference is the URL.
We run the 40-ticket golden set through both and compare:
  - accuracy          (how often the team is right)
  - hard cases        (the last 8 tickets)
  - coverage at 0.8   (share of tickets the model is sure enough to automate)
  - accuracy at 0.8   (how often those confident answers are right)
  - latency and cost

Needs: the local Kev server running, and OPENROUTER_API_KEY in ../.env for Jev.
"""

import os
import time
import requests
from dotenv import load_dotenv

from golden_set import GOLDEN_SET, TEAMS

load_dotenv()

MODELS = {
    "Jev (OpenRouter)": {
        "url": "https://openrouter.ai/api/alpha/decisions",
        "model": "typesafe/jev-1.13",
        "headers": {"Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}"},
    },
    "Kev-9B (local)": {
        "url": os.environ.get("KEV_URL", "http://localhost:8009/v1/systemone"),
        "model": "kev-latest",
        "headers": {},
    },
}
GATE = 0.8
HARD_FROM = len(GOLDEN_SET) - 8


def ask(cfg: dict, ticket: str) -> tuple[dict, float, float]:
    started = time.perf_counter()
    response = requests.post(
        cfg["url"],
        headers=cfg["headers"],
        json={
            "model": cfg["model"],
            "state": {"ticket": ticket},
            "questions": {
                "team": {
                    "type": "choice",
                    "instructions": "Which team should own this support ticket?",
                    "criteria": TEAMS,
                }
            },
        },
        timeout=120,
    )
    response.raise_for_status()
    body = response.json()
    ms = (time.perf_counter() - started) * 1000
    return body["answers"]["team"], ms, body.get("usage", {}).get("cost", 0.0)


if __name__ == "__main__":
    results = {}
    for name, cfg in MODELS.items():
        rows = [(ask(cfg, ticket), label) for ticket, label in GOLDEN_SET]
        results[name] = rows

    print(f"Golden set: {len(GOLDEN_SET)} tickets ({len(GOLDEN_SET) - HARD_FROM} hard), gate = {GATE}\n")
    print(f"{'model':<18} {'accuracy':>8} {'hard':>6} {'coverage':>9} {'acc@gate':>9} {'avg ms':>7} {'cost':>9}")
    for name, rows in results.items():
        correct = [a["choice"] == label for (a, _, _), label in rows]
        gated = [(a["choice"] == label) for (a, _, _), label in rows if a["confidence"] >= GATE]
        print(
            f"{name:<18} {sum(correct) / len(rows):>8.0%} "
            f"{sum(correct[HARD_FROM:]):>3}/{len(rows) - HARD_FROM:<2} "
            f"{len(gated) / len(rows):>9.0%} "
            f"{(sum(gated) / len(gated) if gated else 0):>9.0%} "
            f"{sum(ms for (_, ms, _), _ in rows) / len(rows):>7.0f} "
            f"${sum(cost for (_, _, cost), _ in rows):>8.5f}"
        )

    print("\n--- Where they disagree (label / Jev / Kev) ---")
    jev, kev = results["Jev (OpenRouter)"], results["Kev-9B (local)"]
    for (ticket, label), ((j, _, _), _), ((k, _, _), _) in zip(GOLDEN_SET, jev, kev):
        if j["choice"] != k["choice"] or j["choice"] != label:
            print(
                f"{label:<10} {j['choice']:<10} ({j['confidence']:.2f})  "
                f"{k['choice']:<10} ({k['confidence']:.2f})  {ticket}"
            )
