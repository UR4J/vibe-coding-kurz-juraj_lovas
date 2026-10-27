"""
2) Jev first, LLM second - sort everything cheaply, write only where needed.

A creator gets hundreds of comments under a video. Most of them need no
answer ("great video!", spam). Sending all of them to an LLM wastes money.

  Step 1 - Jev reads ALL comments (parallel, cheap): type + "needs a reply?"
  Step 2 - the LLM writes replies ONLY for the few that need one

This "cascade" is the most common way to combine Jev with an LLM:
System 1 (fast) filters, System 2 (slow) thinks.
"""

from concurrent.futures import ThreadPoolExecutor

from jev import decide, noul, choice
from llm import llm_chat, LLM_MODEL

VIDEO = "Tutorial: build your first AI agent in Python (25 min)"

COMMENTS = [
    "Great video, thanks!",
    "🔥🔥🔥",
    "At 12:40 I get 'ModuleNotFoundError: No module named openai'. What did I miss?",
    "Check my channel for FREE crypto signals!!!",
    "first",
    "Could you make a follow-up about adding memory to the agent?",
    "This helped me pass my uni project, thank you so much.",
    "Is this approach still valid with the new Responses API?",
    "Nice.",
    "Your mic is too quiet in the second half.",
    "Earn $5000/week from home, message me on Telegram",
    "What is the difference between a tool and an agent? Still confused.",
    "Love it",
    "Watched it twice, subscribed.",
    "Would this work with a local model in Ollama?",
    "Why don't you use LangChain for this?",
]

QUESTIONS = {
    "type": choice(
        "What kind of comment is this?",
        question="Asks something, reports a problem or an error.",
        idea="Suggests a new video topic.",
        praise="Thanks or compliments.",
        feedback="Criticism about audio, video, pace.",
        spam="Ads, scams, self-promotion, 'first'.",
    ),
    "needs_reply": noul(
        "Should the creator reply to this comment?",
        true="A real question or problem the creator can help with.",
        false="Praise, spam, emoji, or nothing to answer.",
    ),
}


def triage(comment: str) -> dict:
    result = decide(state={"video": VIDEO, "comment": comment}, questions=QUESTIONS)
    return {**result["answers"], "cost": result["usage"]["cost"]}


if __name__ == "__main__":
    # Step 1 - Jev on everything, in parallel
    with ThreadPoolExecutor(max_workers=16) as pool:
        triaged = list(pool.map(triage, COMMENTS))
    jev_cost = sum(t["cost"] for t in triaged)

    print("--- Step 1: Jev triage ---")
    for comment, t in zip(COMMENTS, triaged):
        mark = "REPLY" if t["needs_reply"]["noul"] >= 0.5 else "     "
        print(f"{mark}  {t['type']['choice']:<9} {comment[:70]}")

    # Step 2 - the LLM writes only where needed
    to_answer = [c for c, t in zip(COMMENTS, triaged) if t["needs_reply"]["noul"] >= 0.5]
    print(f"\n--- Step 2: {LLM_MODEL} writes {len(to_answer)} replies ---")
    llm_cost = 0.0
    for comment in to_answer:
        reply = llm_chat(
            f"You are the author of the YouTube video '{VIDEO}'. "
            f"Reply to this comment in max 2 friendly sentences:\n\n{comment}"
        )
        llm_cost += reply["cost"]
        print(f"\nQ: {comment}\nA: {reply['text']}")

    avg_llm = llm_cost / max(len(to_answer), 1)
    print(f"\nJev on {len(COMMENTS)} comments: ${jev_cost:.5f}")
    print(f"LLM on {len(to_answer)} comments: ${llm_cost:.5f}")
    print(f"LLM on ALL {len(COMMENTS)} would cost about ${avg_llm * len(COMMENTS):.5f}")
