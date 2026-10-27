"""
1) Client request routing - the contact centre inbox.

Problem:
  Raiffeisenbank gets thousands of e-mails, chat and app messages per day.
  People read each one only to decide WHERE it goes and HOW FAST.

With Jev:
  One call per message answers four questions at once:
    team, urgency, "is it a formal complaint?", "is the client about to leave?"
  The bank acts ONLY when Jev is confident. Everything else goes to a person.
  This is the "confidence-gated" pattern: automate the easy 80 %, keep people
  for the hard 20 %.
"""

from jev import decide, noul, choice, score

# Below this confidence the message goes to a human triage queue
CONFIDENCE_THRESHOLD = 0.80

QUESTIONS = {
    "team": choice(
        "Which Raiffeisenbank team should handle this client message?",
        cards="Debit/credit cards: declined payments, limits, blocking, reissue.",
        payments="Transfers, standing orders, SEPA and foreign payments.",
        loans="Consumer loans, mortgages, overdrafts, refinancing.",
        digital_banking="Mobile app and internet banking: login, errors, settings.",
        accounts="Opening/closing accounts, fees, statements, account settings.",
        fraud="Suspicious transactions, scams, stolen credentials.",
    ),
    "urgency": score(
        "How urgent is this message for the bank?",
        "Routine - can be answered within 5 working days",
        "Soon - should be answered within 1 working day",
        "Immediate - the client is losing money or cannot access money now",
    ),
    "formal_complaint": noul(
        "Is the client filing a formal complaint that the bank must register "
        "and answer within the legal deadline?",
        true="The client disputes a fee, a transaction or a service and asks for a correction, refund or compensation.",
        false="The client asks a question, asks for help, or gives neutral feedback.",
    ),
    "churn_risk": noul(
        "Does the client signal that they may move to another bank?",
        true="The client mentions leaving, closing the account, moving salary, or a better offer elsewhere.",
        false="No sign that the client wants to leave.",
    ),
}

# Fictional client messages (Czech and English, like the real inbox)
MESSAGES = [
    {
        "channel": "chat",
        "text": "I can't log in to the mobile app since the update this morning. "
        "It says 'error 403'. I need to pay rent today.",
    },
    {
        "channel": "email",
        "text": "Dobrý den, v březnu mi byl stržen poplatek 250 Kč za vedení účtu, "
        "přestože mám podle smlouvy účet zdarma. Žádám o vrácení.",
    },
    {
        "channel": "email",
        "text": "Hi, what is the current interest rate for refinancing a mortgage? "
        "My fixation ends next year.",
    },
    {
        "channel": "chat",
        "text": "There are 3 card payments on my account in Lithuania that I did not "
        "make!!! Please stop it now.",
    },
    {
        "channel": "email",
        "text": "Third time this month the SEPA transfer to Germany took 4 days. "
        "Another bank offered me a free account with instant payments. "
        "If this continues I will move my salary there.",
    },
    {
        "channel": "app",
        "text": "Can you send me the statement for last year? Thank you.",
    },
    {
        # Ambiguous on purpose - shows the "human triage" path
        "channel": "chat",
        "text": "Please cancel it, I do not want it anymore.",
    },
]


def route(message: dict) -> None:
    result = decide(
        state={
            "bank": "Raiffeisenbank a.s. (Czech Republic)",
            "channel": message["channel"],
            "message": message["text"],
        },
        questions=QUESTIONS,
    )
    a = result["answers"]
    team, urgency = a["team"], a["urgency"]

    actions = []
    if team["confidence"] >= CONFIDENCE_THRESHOLD:
        actions.append(f"auto-route -> {team['choice']}")
    else:
        actions.append(f"HUMAN TRIAGE (best guess {team['choice']}, low confidence)")
    if urgency["score"] >= 1.5:
        actions.append("PRIORITY queue")
    if a["formal_complaint"]["noul"] >= 0.5:
        actions.append("register formal complaint (deadline clock starts)")
    if a["churn_risk"]["noul"] >= 0.6:
        actions.append("alert relationship manager (retention)")

    print(f"\n[{message['channel']}] {message['text'][:90]}...")
    print(
        f"  team={team['choice']} ({team['confidence']:.2f})  "
        f"urgency={urgency['score']:.2f}/2  "
        f"complaint={a['formal_complaint']['noul']:.0%}  "
        f"churn={a['churn_risk']['noul']:.0%}  "
        f"[{result['latency_ms']} ms, ${result['usage']['cost']:.7f}]"
    )
    for action in actions:
        print(f"  -> {action}")


if __name__ == "__main__":
    for message in MESSAGES:
        route(message)
