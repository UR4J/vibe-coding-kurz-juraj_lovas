"""
5) Generative UI - the mobile app builds the next screen from ready parts.

Problem:
  The Raiffeisenbank app has hundreds of screens hidden in menus. Clients
  type into the search box ("my card was stolen") and get a list of links,
  or they call the contact centre.

With Jev:
  Jev does not write any UI code. The app already has a library of screens
  and small components. Jev only DECIDES which ones to show for what the
  client typed - in a few hundred milliseconds, so it feels instant.

  One call composes the page:
    - main screen   (choice from the screen library)
    - fraud banner? (noul)
    - human help?   (noul - offer a call/chat button)
"""

from jev import decide, noul, choice

# The app's screen library (the "UI parts" Jev can choose from)
SCREENS = {
    "block_card": "Temporarily block or permanently cancel a payment card.",
    "card_limits": "Change daily ATM and payment limits of a card.",
    "card_pin": "Show or change the card PIN.",
    "new_payment": "Send a domestic or SEPA payment.",
    "payment_dispute": "Dispute an unknown or wrong card transaction (chargeback).",
    "statements": "Download account statements and confirmations.",
    "mortgage_calculator": "Calculate mortgage payments and ask for an offer.",
    "loan_early_repayment": "Repay a loan or mortgage early, fully or partly.",
    "travel_insurance": "Buy travel insurance for a trip abroad.",
    "savings_account": "Open a savings account or change savings settings.",
    "contact_branch": "Find a branch or ATM on the map, book a meeting.",
    "profile_settings": "Change address, phone, e-mail, language, notifications.",
}

QUESTIONS = {
    "main_screen": choice(
        "Which screen from the app library best fulfils what the client wants?",
        **SCREENS,
    ),
    "show_fraud_banner": noul(
        "Should the app show a red 'possible fraud - call us' banner?",
        true="The client mentions theft, unknown payments, a suspicious call or a scam.",
        false="A normal service request.",
    ),
    "offer_human_help": noul(
        "Should the app offer a 'talk to a banker now' button?",
        true="The situation is stressful, complex, or needs a person (large sums, death, fraud, disputes).",
        false="A simple self-service task.",
    ),
}

SEARCHES = [
    "my wallet was stolen in the tram",
    "chci splatit hypotéku dřív",  # "I want to repay my mortgage early"
    "going to Croatia next week, anything I need?",
    "there is a payment from Amazon I don't recognise",
    "raise the ATM withdrawal limit to 30k",
    "moved to Brno, new address",
]


def build_page(search: str) -> None:
    result = decide(
        state={"app": "Raiffeisenbank mobile app", "client_typed": search},
        questions=QUESTIONS,
    )
    a = result["answers"]
    screen = a["main_screen"]

    # The code, not the model, assembles the page from the chosen parts
    page = []
    if a["show_fraud_banner"]["noul"] >= 0.5:
        page.append("[RED BANNER] Possible fraud - call the bank hotline now")
    page.append(f"[SCREEN] {screen['choice']}  (confidence {screen['confidence']:.2f})")
    if screen["confidence"] < 0.6:
        runner_up = sorted(screen["probabilities"], key=screen["probabilities"].get)[-2]
        page.append(f"[LINK] Did you mean: {runner_up}?")
    if a["offer_human_help"]["noul"] >= 0.5:
        page.append("[BUTTON] Talk to a banker now")

    print(f"\nClient typed: \"{search}\"  [{result['latency_ms']} ms]")
    for part in page:
        print(f"  {part}")


if __name__ == "__main__":
    for search in SEARCHES:
        build_page(search)
