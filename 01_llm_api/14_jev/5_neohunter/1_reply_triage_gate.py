"""
1) Candidate reply triage + confidence gate, measured on the golden set.

A headhunter sends 50-200 outreach messages a week. Every reply needs a next step:
  interested      -> book a call
  question        -> answer it (salary, client, location)
  later           -> follow-up task in X months
  not_interested  -> thank, close
  referral        -> thank, ask for the contact
  + GDPR request  -> ALWAYS a person, whatever the confidence

This script answers ONE business question:
  "Above which confidence can the CRM act on Jev's answer without me?"

Run:  uv run 1_reply_triage_gate.py
"""

from concurrent.futures import ThreadPoolExecutor

from jev import decide, choice, noul
from golden_replies import GOLDEN_REPLIES, INTENTS

THRESHOLDS = [0.0, 0.5, 0.7, 0.8, 0.9, 0.95]
GATE = 0.8  # the threshold we look at in detail

QUESTIONS = {
    "intent": choice("What does the candidate want as the next step?", **INTENTS),
    "gdpr": noul(
        "Is this a data protection request?",
        true="Asks to stop contact, to delete their data, or where we got their data.",
        false="Any other reply, including a polite no.",
    ),
}


def triage(reply: str) -> dict:
    result = decide(
        state={
            "context": "Reply of a candidate to a headhunter's first LinkedIn message about a job.",
            "reply": reply,
        },
        questions=QUESTIONS,
    )
    return {**result["answers"], "cost": result["usage"]["cost"], "latency_ms": result["latency_ms"]}


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=16) as pool:
        answers = list(pool.map(triage, [reply for reply, _, _ in GOLDEN_REPLIES]))

    rows = list(zip(answers, GOLDEN_REPLIES))
    n = len(rows)

    # --- GDPR is a hard rule, not a confidence question ---
    gdpr_hits = sum((a["gdpr"]["noul"] >= 0.5) == gdpr for a, (_, _, gdpr) in rows)
    gdpr_missed = [reply for a, (reply, _, gdpr) in rows if gdpr and a["gdpr"]["noul"] < 0.5]
    print(f"GDPR flag correct: {gdpr_hits}/{n}")
    for reply in gdpr_missed:
        print(f"  MISSED GDPR: {reply}")

    # --- Intent: the automation vs. accuracy trade-off ---
    print(f"\n{'threshold':>9}  {'automated':>9}  {'accuracy of automated':>21}  {'wrong & automated':>17}")
    for threshold in THRESHOLDS:
        automated = [(a, intent) for a, (_, intent, gdpr) in rows
                     if a["intent"]["confidence"] >= threshold and a["gdpr"]["noul"] < 0.5]
        correct = sum(a["intent"]["choice"] == intent for a, intent in automated)
        accuracy = correct / len(automated) if automated else 0
        print(f"{threshold:>9.2f}  {len(automated) / n:>9.0%}  {accuracy:>21.0%}  {len(automated) - correct:>17}")

    print(f"\nWrong but confident (confidence >= {GATE}, not GDPR), the dangerous ones:")
    for a, (reply, intent, _) in rows:
        if a["intent"]["confidence"] >= GATE and a["intent"]["choice"] != intent and a["gdpr"]["noul"] < 0.5:
            print(f"  {a['intent']['confidence']:.2f}  jev={a['intent']['choice']:<14} label={intent:<14} {reply}")

    print(f"\nSent to a person (confidence < {GATE} or GDPR):")
    for a, (reply, intent, _) in rows:
        if a["intent"]["confidence"] < GATE or a["gdpr"]["noul"] >= 0.5:
            why = "GDPR" if a["gdpr"]["noul"] >= 0.5 else f"{a['intent']['confidence']:.2f}"
            print(f"  {why:>5}  jev={a['intent']['choice']:<14} label={intent:<14} {reply}")

    total_cost = sum(a["cost"] for a in answers)
    avg_ms = sum(a["latency_ms"] for a in answers) / n
    print(f"\n{n} replies, cost ${total_cost:.5f}, average {avg_ms:.0f} ms per reply")
