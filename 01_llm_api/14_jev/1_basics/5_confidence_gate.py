"""
5) Confidence gate - how to pick the threshold.

The main Jev pattern:
    confidence >= threshold  -> act automatically
    confidence <  threshold  -> send to a person

A higher threshold means fewer mistakes, but also less automation.
The right value is a business decision, so MEASURE it on labelled data:
this script runs Jev on the golden set once and prints the trade-off.
"""

from concurrent.futures import ThreadPoolExecutor

from jev import decide, choice
from golden_set import GOLDEN_SET, TEAMS

THRESHOLDS = [0.0, 0.5, 0.7, 0.8, 0.9, 0.95]


def classify(ticket: str) -> dict:
    result = decide(
        state={"shop": "online shop", "ticket": ticket},
        questions={"team": choice("Which team should own this support ticket?", **TEAMS)},
    )
    return result["answers"]["team"]


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=16) as pool:
        answers = list(pool.map(classify, [ticket for ticket, _ in GOLDEN_SET]))
    rows = [(answer, label) for answer, (_, label) in zip(answers, GOLDEN_SET)]

    print(f"{'threshold':>9}  {'automated':>9}  {'accuracy of automated':>21}  {'wrong & automated':>17}")
    for threshold in THRESHOLDS:
        automated = [(a, label) for a, label in rows if a["confidence"] >= threshold]
        correct = sum(a["choice"] == label for a, label in automated)
        wrong = len(automated) - correct
        accuracy = correct / len(automated) if automated else 0
        print(
            f"{threshold:>9.2f}  {len(automated) / len(rows):>9.0%}  "
            f"{accuracy:>21.0%}  {wrong:>17}"
        )

    print("\nTickets Jev was NOT sure about (confidence < 0.8):")
    for answer, (ticket, label) in zip(answers, GOLDEN_SET):
        if answer["confidence"] < 0.8:
            print(f"  {answer['confidence']:.2f}  guess={answer['choice']:<10} label={label:<10} {ticket}")
