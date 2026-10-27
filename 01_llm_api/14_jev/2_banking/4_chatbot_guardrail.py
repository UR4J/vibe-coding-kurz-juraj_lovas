"""
4) Guardrail for an LLM chatbot - check every answer before the client sees it.

Problem:
  The bank chatbot (an LLM) sometimes writes things a bank must never say:
  investment advice, a promise of loan approval, a request for a PIN.
  A second big LLM as a "judge" doubles cost and latency of every answer.

With Jev:
  "System 2" (the LLM) writes, "System 1" (Jev) checks in ~100 ms for a
  fraction of the cost. Each rule is one typed question. The code, not a
  prompt, decides: send / rewrite / hand over to a person.

In a real app the drafts come from the LLM (see lessons 1-12). Here they
are fixed strings, so the example needs only Jev.
"""

from jev import decide, noul

POLICY = (
    "Raiffeisenbank chatbot policy: "
    "1) Never ask for PIN, password, full card number, CVV or SMS codes. "
    "2) Never give personal investment advice or recommend a specific product to buy or sell. "
    "3) Never promise that a loan or mortgage will be approved, or promise a fixed rate. "
    "4) Answer only questions about banking with Raiffeisenbank."
)

QUESTIONS = {
    "asks_for_secret": noul(
        "Does the draft ask the client for a secret credential?",
        true="Asks for PIN, password, full card number, CVV or an SMS/authorisation code.",
        false="Does not ask for any secret.",
    ),
    "investment_advice": noul(
        "Does the draft give personal investment advice?",
        true="Tells the client what to buy, sell or invest in, or predicts returns.",
        false="Gives only general, factual information.",
    ),
    "promises_approval": noul(
        "Does the draft promise a loan approval or a fixed rate?",
        true="Says or implies the loan/mortgage will surely be approved, or guarantees a rate.",
        false="Makes no such promise.",
    ),
    "follows_policy": noul(
        "Is the draft fully consistent with the chatbot policy in the state?",
        true="No rule of the policy is broken.",
        false="At least one rule of the policy is broken.",
    ),
}

DRAFTS = [
    {
        "client": "How do I change my card limit?",
        "draft": "Open the Raiffeisenbank app, go to Cards -> Limits and set the new "
        "daily limit. The change is active immediately.",
    },
    {
        "client": "My payment failed, can you check it?",
        "draft": "Sure! To verify you, please send me your card number and the "
        "SMS code you just received.",
    },
    {
        "client": "Should I put my savings into your equity fund?",
        "draft": "Yes, definitely. The equity fund will beat inflation this year, "
        "move all your savings there.",
    },
    {
        "client": "Will I get a 4 million mortgage with 60k net income?",
        "draft": "With that income your mortgage will certainly be approved at 3.9 %.",
    },
]


if __name__ == "__main__":
    for item in DRAFTS:
        result = decide(state={"policy": POLICY, **item}, questions=QUESTIONS)
        a = result["answers"]
        violations = [
            name for name in ("asks_for_secret", "investment_advice", "promises_approval")
            if a[name]["noul"] >= 0.5
        ]

        if violations:
            action = f"BLOCK -> rewrite ({', '.join(violations)})"
        elif a["follows_policy"]["noul"] < 0.8:
            action = "HAND OVER to a human agent (unsure)"
        else:
            action = "SEND"

        print(f"\nClient: {item['client']}")
        print(f"Draft:  {item['draft'][:80]}...")
        print(f"  -> {action}  [{result['latency_ms']} ms]")
