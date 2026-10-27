"""
1) The three primitives on a LOCAL model - Kev-9B on your own machine.

This is the same request as ../1_basics/1_three_primitives.py. Only two things change:
  - the URL:  http://localhost:8009/v1/systemone   (instead of OpenRouter)
  - no API key, no cost - the model runs on your GPU / Apple Silicon

Start the server first (see README.md):
  uv run python -m kev.serve --run jaredpalmer/kev-9b --port 8009
"""

import os
import requests
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

KEV_URL = os.environ.get("KEV_URL", "http://localhost:8009/v1/systemone")

response = requests.post(
    KEV_URL,
    json={
        "model": "kev-latest",
        "state": {
            "shop": "online electronics shop",
            "customer_tier": "premium",
            "ticket": "I was charged twice for order #55102 and the second payment "
            "is blocking my card limit. I need the money back today!",
        },
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
    timeout=120,
)

if not response.ok:
    print(f"Error {response.status_code}: {response.text}")
    raise SystemExit(1)

result = response.json()

print("--- Full response: ---")
pprint(result)

answers = result["answers"]
print("\n--- Typed answers (Kev-9B, local): ---")
print(f"Payment issue?  {answers['is_payment_issue']['noul']:.0%}")
print(f"Team:           {answers['team']['choice']} (confidence {answers['team']['confidence']:.2f})")
print(f"Frustration:    {answers['frustration']['score']:.2f} / 2 (confidence {answers['frustration']['confidence']:.2f})")
print(f"Model time:     {result.get('latency_ms')} ms   Cost: $0 (your machine)")
