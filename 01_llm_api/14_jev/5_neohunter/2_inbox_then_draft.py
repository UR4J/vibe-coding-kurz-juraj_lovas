"""
2) Monday inbox: Jev sorts every reply, the LLM writes only where a reply is needed.

  Step 1  Jev (System 1): intent + GDPR flag for EVERY reply, in parallel, cheap
  Step 2  code: the confidence gate decides automatic action vs. a person
  Step 3  LLM (System 2): drafts a reply ONLY for confident "interested" and "question"

Drafts are drafts. A person sends them. Nothing goes out automatically.
All replies are FICTIONAL.

Run:  uv run 2_inbox_then_draft.py
"""

from concurrent.futures import ThreadPoolExecutor

from jev import decide
from llm import llm_chat, LLM_MODEL
from importlib import import_module

QUESTIONS = import_module("1_reply_triage_gate").QUESTIONS
GATE = 0.8

ROLE = "Regionálny manažér predaja, retailová sieť (dôverné), Nitra, do 3 800 EUR brutto"

INBOX = [
    ("Andrea M.", "Dobrý deň, ďakujem za správu. Znie to zaujímavo, kedy sa vám hodí krátky call?"),
    ("Tomáš V.", "Aký je platový rozsah a je to firemné auto aj na súkromné účely?"),
    ("Lucia H.", "Teraz nie, v januári mi končí projekt, skúste ma potom."),
    ("Peter R.", "Ďakujem, ale nemám záujem."),
    ("Jana K.", "Pre mňa nie, ale kolegyňa Ivana robí area managerku v drogérii, môžem vám dať kontakt?"),
    ("Martin S.", "Prosím vymažte moje údaje, nesúhlasím so spracovaním."),
    ("Eva D.", "Hmm, a o akú sieť ide? Ak je to tá, kde som už bola, tak nie."),
    ("Roman B.", "ok pošlite info"),
]

ACTIONS = {
    "interested": "navrhnúť termín callu",
    "question": "odpovedať na otázku",
    "later": "follow-up úloha v CRM",
    "not_interested": "poďakovať, uzavrieť",
    "referral": "poďakovať, vypýtať kontakt",
}

DRAFT_FOR = {"interested", "question"}


def triage(reply: str) -> dict:
    result = decide(
        state={
            "context": "Reply of a candidate to a headhunter's first LinkedIn message about a job.",
            "reply": reply,
        },
        questions=QUESTIONS,
    )
    return {**result["answers"], "cost": result["usage"]["cost"]}


def draft(name: str, reply: str, intent: str) -> dict:
    goal = "navrhni 2 konkrétne termíny na 15-min call tento týždeň" if intent == "interested" else \
        "odpovedz na otázku, čo vieš z popisu pozície; čo nevieš, sľúb doplniť na calle"
    return llm_chat(
        "Si headhunter v Neohunter. Píšeš krátku odpoveď kandidátovi na LinkedIne po slovensky, "
        "vykanie, max 3 vety, bez podpisu, nikdy nevymýšľaj meno klienta ani čísla, ktoré nepoznáš.\n"
        f"Pozícia: {ROLE}\nKandidát: {name}\nJeho správa: {reply}\nCieľ: {goal}"
    )


if __name__ == "__main__":
    # Step 1: Jev on everything
    with ThreadPoolExecutor(max_workers=16) as pool:
        triaged = list(pool.map(triage, [reply for _, reply in INBOX]))
    jev_cost = sum(t["cost"] for t in triaged)

    # Step 2: the gate
    print("--- Step 1+2: Jev triage and gate ---")
    to_draft = []
    for (name, reply), t in zip(INBOX, triaged):
        intent, conf = t["intent"]["choice"], t["intent"]["confidence"]
        if t["gdpr"]["noul"] >= 0.5:
            route = "ČLOVEK (GDPR)"
        elif conf < GATE:
            route = f"ČLOVEK (istota {conf:.2f})"
        else:
            route = f"AUTO: {ACTIONS[intent]}"
            if intent in DRAFT_FOR:
                to_draft.append((name, reply, intent))
        print(f"{name:<10} {intent:<14} {conf:.2f}  {route:<34} {reply[:60]}")

    # Step 3: the LLM writes only where needed
    print(f"\n--- Step 3: {LLM_MODEL} píše {len(to_draft)} drafty ---")
    llm_cost = 0.0
    for name, reply, intent in to_draft:
        answer = draft(name, reply, intent)
        llm_cost += answer["cost"]
        print(f"\n{name}: {reply}\nDRAFT: {answer['text']}")

    automated = sum(1 for t in triaged if t["intent"]["confidence"] >= GATE and t["gdpr"]["noul"] < 0.5)
    print(f"\nAutomaticky spracované: {automated}/{len(INBOX)}, človek: {len(INBOX) - automated}")
    print(f"Jev na {len(INBOX)} odpovediach: ${jev_cost:.5f}, LLM na {len(to_draft)} draftoch: ${llm_cost:.5f}")
