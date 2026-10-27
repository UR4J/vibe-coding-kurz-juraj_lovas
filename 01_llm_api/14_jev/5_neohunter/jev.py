"""
Tiny helper for calling Jev (TypeSafe AI) through OpenRouter.

Jev does NOT generate text. You send it:
  - state     : the facts (a dict of text / values)
  - questions : typed questions (noul / choice / score)
and it returns typed answers with probabilities and a confidence value.

Docs: https://openrouter.ai/docs/guides/community/jev-tutorial
"""

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# Point JEV_URL at a local Kev server (see ../4_local_kev) to run the same code on an open model
JEV_URL = os.environ.get("JEV_URL", "https://openrouter.ai/api/alpha/decisions")
JEV_MODEL = os.environ.get("JEV_MODEL", "typesafe/jev-1.13")


def decide(state: dict, questions: dict) -> dict:
    """Ask Jev one or more typed questions about one state."""
    started = time.perf_counter()
    response = requests.post(
        JEV_URL,
        headers={
            "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json",
        },
        json={"model": JEV_MODEL, "state": state, "questions": questions},
        timeout=30,
    )
    if not response.ok:
        raise RuntimeError(f"Jev call failed ({response.status_code}): {response.text}")

    result = response.json()
    result["latency_ms"] = round((time.perf_counter() - started) * 1000)
    result.setdefault("usage", {}).setdefault("cost", 0.0)  # a local server reports no cost
    return result


# -----------------------------------------------------------------------------
# Question builders for the three Jev primitives
# -----------------------------------------------------------------------------
def noul(instructions: str, true: str, false: str) -> dict:
    """Yes/No question. Answer: probability that it is true (0..1)."""
    return {
        "type": "noul",
        "instructions": instructions,
        "criteria": {"true": true, "false": false},
    }


def choice(instructions: str, **options: str) -> dict:
    """Pick one of the named options. Answer: option + probabilities + confidence."""
    return {"type": "choice", "instructions": instructions, "criteria": options}


def score(instructions: str, *levels: str) -> dict:
    """Place on an ordered scale (lowest level first). Answer: 0..len(levels)-1."""
    return {"type": "score", "instructions": instructions, "criteria": list(levels)}
