"""
3) AML alert triage - sort the analyst queue.

Problem:
  Transaction monitoring (anti-money laundering) creates many alerts, and
  most of them are false positives. Analysts work the queue top-down, so a
  real case can wait days behind noise.

With Jev:
  Jev reads each alert narrative and returns a priority score, the most
  likely typology and the probability of a false positive. We sort the
  queue by that. Analysts see the dangerous cases first.

Jev never closes an alert. A person still decides and files the report
(regulation requires it). Jev only decides the ORDER of work.
"""

from jev import decide, noul, choice, score

QUESTIONS = {
    "priority": score(
        "How urgently must an AML analyst review this alert?",
        "Low - review in normal order",
        "Medium - review this week",
        "High - review today",
        "Critical - review now, possible freeze of funds",
    ),
    "typology": choice(
        "Which money-laundering typology fits this alert best?",
        structuring="Many cash deposits just under reporting limits.",
        money_mule="Account receives funds from many strangers and forwards them quickly.",
        sanctions_pep="Link to a sanctioned person/country or a politically exposed person.",
        fraud_proceeds="Incoming money looks like proceeds of a scam against someone else.",
        benign="Normal business or private activity that explains the pattern.",
    ),
    "false_positive": noul(
        "Is this alert most likely a false positive?",
        true="The documented facts explain the activity as normal and legal.",
        false="The activity stays unexplained or suspicious.",
    ),
}

# Fictional alerts from the transaction monitoring system
ALERTS = [
    {
        "id": "AML-10231",
        "rule": "Cash deposits > 200k CZK / 30 days",
        "narrative": "Client runs a bakery (registered business, 12 years with bank). "
        "Daily cash deposits 8-12k CZK, same pattern for 3 years, matches the tax return.",
    },
    {
        "id": "AML-10232",
        "rule": "Rapid in-out movement",
        "narrative": "Student account opened 6 weeks ago. 14 incoming transfers from "
        "different private persons (5-40k CZK), each forwarded within 2 hours to a "
        "crypto exchange. Two senders already reported fraud to their banks.",
    },
    {
        "id": "AML-10233",
        "rule": "Cash deposits just under 250k CZK",
        "narrative": "Seven cash deposits of 240-249k CZK at five different branches "
        "in 10 days. Client is unemployed according to KYC data.",
    },
    {
        "id": "AML-10234",
        "rule": "High-risk country",
        "narrative": "Company pays 1.2M CZK to a trading firm whose director shares a "
        "name with a person on the EU sanctions list. Match not yet confirmed.",
    },
]


if __name__ == "__main__":
    queue = []
    for alert in ALERTS:
        result = decide(state={"bank": "Raiffeisenbank a.s.", **alert}, questions=QUESTIONS)
        queue.append((alert, result["answers"]))

    # Highest priority first, likely false positives last
    queue.sort(key=lambda item: (-item[1]["priority"]["score"], item[1]["false_positive"]["noul"]))

    print("--- Analyst queue (sorted by Jev) ---")
    for alert, a in queue:
        print(
            f"{alert['id']}  priority={a['priority']['score']:.2f}/3  "
            f"typology={a['typology']['choice']:<14} "
            f"false_positive={a['false_positive']['noul']:.0%}"
        )
