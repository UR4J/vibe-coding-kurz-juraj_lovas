"""
3) Meeting insights - many small answers tell a big story.

Jev cannot "read 1,000 transcripts and tell me the themes". It writes no
text. But you can ask the SAME focused questions about every meeting and
count the answers. The numbers tell the story:
    "Only 40 % of our calls end with clear next steps."

Each transcript = one call with 6 questions. Then plain Python aggregates.
"""

from concurrent.futures import ThreadPoolExecutor

from jev import decide, noul, choice, score

# Fictional, very short meeting transcripts (real ones come from Fireflies, Teams, Zoom...)
MEETINGS = [
    "Anna: Let's ship the beta on Friday. Tom: I will fix the login bug by Wednesday. Anna: Great, I send the release notes Thursday.",
    "Tom: So what do we do about the pricing page? Eva: Not sure. Let's think about it. Tom: OK, talk later.",
    "Client: Your last invoice was wrong again, I am losing patience. Eva: I am sorry, I will correct it today and call you at 4 pm.",
    "Anna: Quick sync. Nothing new from my side. Tom: Same. Anna: Bye.",
    "Eva: The client wants 20 more licences next quarter. Tom: Nice! I prepare the offer by Monday.",
    "Tom: I am overloaded, I have three projects. Anna: We need to talk about priorities. Tom: When? Anna: Sometime next week maybe.",
    "Client: We are evaluating other vendors. Eva: What would make you stay? Client: Better support times.",
    "Anna: Retro. Good: releases on time. Bad: too many meetings. Action: Tom removes the Wednesday sync, starting now.",
    "Eva: Did anyone look at the security audit? Tom: No. Anna: No. Eva: Hmm.",
    "Tom: Demo went well, the client signed! Anna: Great work. Eva: I set up onboarding for Tuesday.",
]

QUESTIONS = {
    "type": choice(
        "What type of meeting is this?",
        internal_sync="Team status or sync.",
        client_call="Call with a client.",
        planning="Planning, priorities, retro.",
    ),
    "clear_next_steps": noul(
        "Does the meeting end with clear next steps, each with an owner and a time?",
        true="At least one action has a named person AND a deadline.",
        false="Vague, no owner, or no deadline.",
    ),
    "decision_made": noul(
        "Was a decision made?",
        true="The group agreed on something concrete.",
        false="Only discussion or status.",
    ),
    "tension": score(
        "How much tension or frustration is in the meeting?",
        "None", "Some", "High",
    ),
    "revenue_relevant": noul(
        "Is the meeting relevant for revenue (sales, renewals, churn)?",
        true="Deals, licences, invoices, churn risk.",
        false="No link to revenue.",
    ),
    "wasted_time": noul(
        "Could this meeting have been an e-mail?",
        true="No discussion, no decision, just status.",
        false="Real discussion or decision happened.",
    ),
}


def analyse(transcript: str) -> dict:
    return decide(state={"transcript": transcript}, questions=QUESTIONS)["answers"]


def share(results: list, key: str) -> float:
    return sum(r[key]["noul"] >= 0.5 for r in results) / len(results)


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(analyse, MEETINGS))

    print(f"--- The story of {len(MEETINGS)} meetings ---")
    print(f"Clear next steps (owner + time):  {share(results, 'clear_next_steps'):4.0%}")
    print(f"A decision was made:              {share(results, 'decision_made'):4.0%}")
    print(f"Could have been an e-mail:        {share(results, 'wasted_time'):4.0%}")
    print(f"Revenue relevant:                 {share(results, 'revenue_relevant'):4.0%}")
    print(f"Average tension (0-2):            {sum(r['tension']['score'] for r in results) / len(results):4.2f}")

    print("\nMeetings to look at (no clear next steps, or high tension):")
    for transcript, r in zip(MEETINGS, results):
        if r["clear_next_steps"]["noul"] < 0.5 or r["tension"]["score"] >= 1.5:
            print(f"  [{r['type']['choice']}] {transcript[:80]}...")
