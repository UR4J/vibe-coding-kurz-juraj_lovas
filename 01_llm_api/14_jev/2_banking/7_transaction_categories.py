"""
7) Transaction categories - many small decisions in ONE call.

Problem:
  The "My budget" view in the app needs a category for every card and
  account transaction. Raw bank text is cryptic ("ALBERT 0123 PRAHA 5",
  "GOPAY *DAMEJIDLO"). A bank has millions of transactions per day, so an
  LLM per transaction is too slow and too expensive. Hand-written rules
  break on every new merchant.

With Jev:
  One call can ask MANY questions about the same state. Here we send a whole
  statement and ask one `choice` question per transaction. Output tokens
  are free, so 10 answers cost about the same as 1.
  Low-confidence lines go to "uncategorised" instead of a wrong guess.
"""

from jev import decide, choice

CATEGORIES = {
    "groceries": "Supermarkets and food shops.",
    "restaurants": "Restaurants, cafes, food delivery.",
    "transport": "Public transport, fuel, taxi, parking.",
    "housing": "Rent, mortgage, energy, water, internet.",
    "shopping": "Clothes, electronics, online shops.",
    "health": "Pharmacy, doctor, dentist.",
    "entertainment": "Streaming, cinema, concerts, games.",
    "travel": "Flights, hotels, travel agencies.",
    "cash": "ATM withdrawals.",
    "income": "Salary and other incoming money.",
}

# Below this confidence the transaction stays "uncategorised"
MIN_CONFIDENCE = 0.6

# Fictional statement lines: raw text as the bank sees it
STATEMENT = [
    ("ALBERT 0123 PRAHA 5", -412.50),
    ("GOPAY *DAMEJIDLO", -289.00),
    ("DPP PRAHA LITACKA", -550.00),
    ("PRE ZALOHA ELEKTRINA", -1_850.00),
    ("NETFLIX.COM", -259.00),
    ("DR.MAX LEKARNA", -186.00),
    ("ATM RB PRAHA ANDEL", -3_000.00),
    ("RYANAIR FR6G2K", -2_140.00),
    ("MZDA 09/2026 ACME S.R.O.", 48_500.00),
    ("SHELL 4471 BRNO", -1_320.00),
    ("PAYPAL *XK29Z", -760.00),
]


if __name__ == "__main__":
    questions = {
        f"t{i}": choice(
            f"Budget category of transaction '{text}' ({amount:+,.2f} CZK)?",
            **CATEGORIES,
        )
        for i, (text, amount) in enumerate(STATEMENT)
    }

    result = decide(
        state={"bank": "Raiffeisenbank a.s. (Czech Republic)", "currency": "CZK"},
        questions=questions,
    )

    print(f"--- {len(STATEMENT)} transactions in ONE call ---")
    for i, (text, amount) in enumerate(STATEMENT):
        answer = result["answers"][f"t{i}"]
        if answer["confidence"] >= MIN_CONFIDENCE:
            category = answer["choice"]
        else:
            category = f"uncategorised (best guess {answer['choice']})"
        print(f"{text:<28} {amount:>11,.2f}  -> {category:<14} ({answer['confidence']:.2f})")

    cost = result["usage"]["cost"]
    print(
        f"\n{result['latency_ms']} ms, ${cost:.7f} total, "
        f"${cost / len(STATEMENT):.8f} per transaction"
    )
