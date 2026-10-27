"""
3) Many questions, one call - output tokens are free.

With an LLM, each extra question costs extra output tokens (and time).
With Jev, the state is read once and output is free. So ask ALL the
questions you have about one item in ONE call.

This script asks 8 questions about one product review:
  A) in 8 separate calls
  B) in 1 call
and compares the time and the cost.
"""

from jev import decide, noul, choice, score

STATE = {
    "product": "Wireless headphones X200",
    "review": "Sound is great and the battery lasts two days. But the left ear cup "
    "cracked after 3 weeks and support did not answer my e-mail for 10 days. "
    "I would not buy it again. 2 stars.",
}

QUESTIONS = {
    "sentiment": score("Overall sentiment of the review?", "Negative", "Mixed", "Positive"),
    "mentions_quality_defect": noul(
        "Does the review report a physical defect?",
        true="Something broke, cracked, stopped working.",
        false="No defect reported.",
    ),
    "mentions_support": noul(
        "Does the review complain about customer support?",
        true="Slow, missing or unhelpful support.",
        false="Support not mentioned or praised.",
    ),
    "praises_sound": noul(
        "Does the review praise the sound?",
        true="Positive words about sound or audio.",
        false="No praise of sound.",
    ),
    "praises_battery": noul(
        "Does the review praise the battery?",
        true="Positive words about battery life.",
        false="No praise of battery.",
    ),
    "would_rebuy": noul(
        "Would the reviewer buy the product again?",
        true="Says they would buy again or recommend it.",
        false="Says they would not buy again or warns others.",
    ),
    "main_topic": choice(
        "What is the main topic of the review?",
        sound="Audio quality.",
        battery="Battery life.",
        durability="Build quality, things breaking.",
        support="Customer service.",
        price="Price and value.",
    ),
    "needs_follow_up": noul(
        "Should the brand's support team contact this customer?",
        true="Unresolved problem or a support failure is described.",
        false="Nothing to solve.",
    ),
}


if __name__ == "__main__":
    # A) One call per question
    separate_ms, separate_cost = 0, 0.0
    for name, question in QUESTIONS.items():
        result = decide(state=STATE, questions={name: question})
        separate_ms += result["latency_ms"]
        separate_cost += result["usage"]["cost"]

    # B) All questions in one call
    result = decide(state=STATE, questions=QUESTIONS)

    print("--- Answers from the single call ---")
    for name, answer in result["answers"].items():
        value = answer.get("noul", answer.get("choice", answer.get("score")))
        print(f"{name:<24} {value if isinstance(value, str) else round(value, 2)}")

    print(f"\n{len(QUESTIONS)} separate calls: {separate_ms:6} ms   ${separate_cost:.7f}")
    print(f"1 call, {len(QUESTIONS)} questions: {result['latency_ms']:6} ms   ${result['usage']['cost']:.7f}")
