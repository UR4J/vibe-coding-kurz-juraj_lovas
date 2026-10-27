"""
6) Jev vs. a classic LLM - speed and cost for the same task.

Task: route a support ticket to one of 5 teams.
We run 10 tickets one by one (so the latency is fair) with both models,
then project the monthly cost for 1,000,000 tickets.

Change the LLM with LLM_MODEL in .env (default openai/gpt-5.4-mini).
"""

from jev import decide, choice
from llm import llm_choice, LLM_MODEL
from golden_set import GOLDEN_SET, TEAMS

INSTRUCTIONS = "Which team should own this support ticket?"
MONTHLY = 1_000_000
TICKETS = [ticket for ticket, _ in GOLDEN_SET[::4]]  # every 4th ticket -> 10 tickets


if __name__ == "__main__":
    totals = {"jev": [0, 0.0], "llm": [0, 0.0]}  # [latency_ms, cost]

    for ticket in TICKETS:
        jev = decide(state={"ticket": ticket}, questions={"team": choice(INSTRUCTIONS, **TEAMS)})
        llm = llm_choice(INSTRUCTIONS, TEAMS, ticket)
        totals["jev"][0] += jev["latency_ms"]
        totals["jev"][1] += jev["usage"]["cost"]
        totals["llm"][0] += llm["latency_ms"]
        totals["llm"][1] += llm["cost"]

        team = jev["answers"]["team"]
        print(f"\n{ticket}")
        print(f"  Jev: {team['choice']:<10} (confidence {team['confidence']:.2f})  [{jev['latency_ms']} ms]")
        print(f"  LLM: {llm['choice']:<10} (no confidence)    [{llm['latency_ms']} ms]")

    n = len(TICKETS)
    print(f"\n--- Average per ticket ({n} tickets) ---")
    for name, label in (("jev", "typesafe/jev-1.13"), ("llm", LLM_MODEL)):
        latency, cost = totals[name][0] / n, totals[name][1] / n
        print(
            f"{label:<22} {latency:6.0f} ms   ${cost:.7f}   "
            f"-> ${cost * MONTHLY:,.0f} per {MONTHLY:,} tickets"
        )
