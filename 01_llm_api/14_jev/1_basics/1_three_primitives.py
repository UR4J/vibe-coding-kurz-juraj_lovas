"""
1) The three primitives - one raw HTTP call, no helper.

Jev does not write text. You send:
  - state     : the facts (any JSON object)
  - questions : typed questions, each with instructions + criteria
and you get typed answers:

  - noul   -> "Is this true?"                 -> probability of yes (0..1)
  - choice -> "Which one of these options?"   -> option + probabilities + confidence
  - score  -> "Where on this ordered scale?"  -> 0..N-1 + probabilities + confidence
"""

import os
import requests
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

response = requests.post(
    "https://openrouter.ai/api/alpha/decisions",
    headers={
        "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
    },
    json={
        "model": "typesafe/jev-1.13",
        # State = the facts Jev decides about
        "state": {
            "shop": "online electronics shop",
            "customer_tier": "premium",
            "ticket": "I was charged twice for order #55102 and the second payment "
            "is blocking my card limit. I need the money back today!",
        },
        # Questions = typed decisions we need. The keys are our own names.
        "questions": {
            "is_payment_issue": {
                "type": "noul",
                "instructions": "Is the customer reporting a problem with a payment?",
                "criteria": {
                    "true": "The ticket is about a charge, refund, invoice or payment method.",
                    "false": "The ticket is about something else.",
                },
            },
            "team": {
                "type": "choice",
                "instructions": "Which team should own this ticket?",
                "criteria": {
                    "shipping": "Delivery, delays, courier, address.",
                    "returns": "Returns, exchanges, damaged or wrong items.",
                    "billing": "Payments, double charges, invoices, discount codes.",
                    "technical": "Website or app errors.",
                },
            },
            # Score criteria are a LIST, ordered from lowest to highest
            "frustration": {
                "type": "score",
                "instructions": "How frustrated is the customer?",
                "criteria": [
                    "Calm - neutral tone",
                    "Annoyed - some pressure",
                    "Angry - strong pressure, deadline or threat",
                ],
            },
        },
    },
    timeout=30,
)

if not response.ok:
    print(f"Error {response.status_code}: {response.text}")
    raise SystemExit(1)

result = response.json()

print("--- Full response: ---")
pprint(result)

answers = result["answers"]
print("\n--- Typed answers: ---")
print(f"Payment issue?  {answers['is_payment_issue']['noul']:.0%}")
print(f"Team:           {answers['team']['choice']} (confidence {answers['team']['confidence']:.2f})")
print(f"Frustration:    {answers['frustration']['score']:.2f} / 2 (confidence {answers['frustration']['confidence']:.2f})")
print(f"Tokens in/out:  {result['usage']['input_tokens']} / {result['usage']['output_tokens']}  (output is free)")
print(f"Cost:           ${result['usage']['cost']:.8f}")
