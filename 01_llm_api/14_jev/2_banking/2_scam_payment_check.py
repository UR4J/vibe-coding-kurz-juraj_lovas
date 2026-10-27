"""
2) Scam check on outgoing payments - before the money leaves the bank.

Problem:
  "Safe account" calls, fake investment platforms and fake police officers
  talk clients into sending money themselves (authorised push payment scams).
  The payment is technically valid, so classic rules often let it through.
  The strongest signals are in TEXT: the payment note, the payee name, what
  the client wrote in chat.

With Jev:
  Jev reads the text signals next to the numbers and returns a calibrated
  probability in under a second, fast enough to sit INSIDE the payment flow.
  The bank then picks: allow / warn and ask again / hold and call the client.

Jev does not replace the existing fraud engine. It gives it one more feature.
"""

from jev import decide, noul, choice, score

QUESTIONS = {
    "is_scam": noul(
        "Is the client probably being manipulated into sending this payment "
        "(authorised push payment scam)?",
        true="Signs of social engineering: 'safe account', caller posing as bank or police, "
        "urgency, secrecy, investment with guaranteed profit, new payee abroad.",
        false="A normal payment the client makes for their own reason.",
    ),
    "scam_type": choice(
        "If this is a scam, which type fits best?",
        safe_account="Caller posing as bank/police says money is at risk and must be moved to a 'safe account'.",
        investment="Crypto/trading platform promising high or guaranteed returns.",
        romance="Online partner asking for money for travel, medical or customs costs.",
        invoice_fraud="Changed bank details of a known supplier or landlord.",
        none="No scam pattern.",
    ),
    "risk": score(
        "How risky is it to execute this payment right now?",
        "Low - execute",
        "Medium - show a scam warning and ask the client to confirm",
        "High - hold the payment and call the client from the fraud team",
    ),
}

# Fictional payments with context from the app session and the chat
PAYMENTS = [
    {
        "amount_czk": 1_850,
        "payee": "CEZ Prodej, a.s.",
        "payee_known": True,
        "note": "zaloha elektrina 10/2026",
        "session": "Normal login, known device.",
        "client_chat": "",
    },
    {
        "amount_czk": 480_000,
        "payee": "J. Novak",
        "payee_known": False,
        "note": "bezpecny ucet",
        "session": "Active phone call during the whole app session. "
        "Payment limit raised 5 minutes ago.",
        "client_chat": "The bank security officer told me my savings are in danger "
        "and I must move them today. He is on the phone with me now.",
    },
    {
        "amount_czk": 95_000,
        "payee": "Global Crypto Trading Ltd (Cyprus)",
        "payee_known": False,
        "note": "deposit - account manager Martin",
        "session": "Normal login, known device.",
        "client_chat": "My advisor says the bot makes 15 % per month, it is guaranteed.",
    },
    {
        "amount_czk": 22_000,
        "payee": "Stavebniny Dvorak s.r.o.",
        "payee_known": False,
        "note": "faktura 2026-0412",
        "session": "Normal login, known device.",
        "client_chat": "",
    },
]


def check(payment: dict) -> None:
    result = decide(state={"bank": "Raiffeisenbank a.s.", **payment}, questions=QUESTIONS)
    a = result["answers"]
    p_scam, risk = a["is_scam"]["noul"], a["risk"]["score"]

    if risk >= 1.5 or p_scam >= 0.8:
        action = "HOLD - fraud team calls the client"
    elif risk >= 0.5 or p_scam >= 0.4:
        action = f"WARN - show '{a['scam_type']['choice']}' scam warning, ask to confirm"
    else:
        action = "ALLOW"

    print(f"\n{payment['amount_czk']:>9,} CZK -> {payment['payee']}  (note: '{payment['note']}')")
    print(
        f"  scam={p_scam:.0%}  type={a['scam_type']['choice']}  "
        f"risk={risk:.2f}/2  [{result['latency_ms']} ms]"
    )
    print(f"  -> {action}")


if __name__ == "__main__":
    for payment in PAYMENTS:
        check(payment)
