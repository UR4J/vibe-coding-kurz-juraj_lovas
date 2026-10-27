"""
6) Find by meaning - which part of the terms answers the client's question?

Problem:
  Clients (and call-centre staff) search long product terms with Ctrl+F.
  Keyword search fails: the client asks "can I pay off my mortgage early
  for free?" but the terms say "extraordinary repayment" and "fee".

With Jev:
  Each section of the terms becomes one option of a single `choice`
  question (up to 255 options). Jev returns the best section and a
  probability for every section. So we can show the top hits, and say
  "not found" when nothing is likely - instead of guessing.

This is NOT a full RAG system: the whole document must fit in Jev's
32k-token context. For short documents it is the fastest and cheapest way.
"""

from jev import decide, choice

# Fictional sections of Raiffeisenbank mortgage terms
TERMS = {
    "s1_scope": "1. Scope. These terms apply to mortgage loans for housing provided by the bank to consumers.",
    "s2_interest": "2. Interest rate. The rate is fixed for the fixation period chosen in the contract. After it ends, the bank offers a new rate.",
    "s3_extra_repayment": "3. Extraordinary repayment. The client may repay part or all of the loan early. On the fixation end date, or up to 25 % of the principal once a year, it is free of charge. Otherwise the bank charges only its actual costs.",
    "s4_payment_holiday": "4. Deferral of instalments. In case of job loss or illness the client may ask to defer instalments for up to 6 months.",
    "s5_insurance": "5. Insurance. The property must be insured for its full value for the whole term. The insurance claim is pledged to the bank.",
    "s6_late_payment": "6. Late payment. If an instalment is more than 30 days late, the bank charges default interest and may send reminders.",
    "s7_property_sale": "7. Sale of the property. The client must inform the bank before selling the pledged property. The loan becomes due on the sale.",
    "s8_changes": "8. Changes of terms. The bank informs the client about changes at least 2 months in advance. The client may terminate the contract free of charge.",
    "s9_complaints": "9. Complaints. Complaints are handled within 15 business days. The client may also contact the Financial Arbiter.",
}

QUESTIONS = [
    "Can I pay off my mortgage early without a fee?",
    "I lost my job, what happens with my monthly payments?",
    "Musím mít nemovitost pojištěnou?",  # "Must my property be insured?"
    "Can I sell my flat while I still have the mortgage?",
    "What is the bank's opening time in Olomouc?",  # not in the terms at all
]

# Below this probability we say "not found" instead of showing a section
MIN_PROBABILITY = 0.5


def find(question: str) -> None:
    result = decide(
        state={"document": "Raiffeisenbank mortgage terms", "client_question": question},
        questions={
            "section": choice(
                "Which section of the terms answers the client's question?",
                **TERMS,
                not_in_terms="No section of these terms answers the question.",
            )
        },
    )
    answer = result["answers"]["section"]
    top3 = sorted(answer["probabilities"].items(), key=lambda item: -item[1])[:3]

    print(f"\nQ: {question}  [{result['latency_ms']} ms]")
    print("  top hits: " + ", ".join(f"{name} {p:.0%}" for name, p in top3))
    best, p = top3[0]
    if best == "not_in_terms" or p < MIN_PROBABILITY:
        print("  -> Not found in the terms. Hand over to a banker.")
    else:
        print(f"  -> {TERMS[best]}")


if __name__ == "__main__":
    for question in QUESTIONS:
        find(question)
