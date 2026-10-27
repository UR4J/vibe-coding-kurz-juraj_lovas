"""
Tiny helper: the SAME classification task done by a classic LLM (for comparison).

The LLM gets the options in the prompt, must answer in JSON, and we parse
the text. No probabilities, no confidence.
"""

import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL = os.environ.get("LLM_MODEL", "openai/gpt-5.4-mini")


def llm_choice(instructions: str, options: dict, text: str) -> dict:
    prompt = (
        f"{instructions}\n"
        f"Options: {json.dumps(options)}\n"
        'Answer ONLY with JSON: {"choice": "<option key>"}\n\n'
        f"Text: {text}"
    )
    started = time.perf_counter()
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}"},
        json={
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"},
            "usage": {"include": True},
        },
        timeout=60,
    )
    if not response.ok:
        raise RuntimeError(f"LLM call failed ({response.status_code}): {response.text}")

    body = response.json()
    return {
        "choice": json.loads(body["choices"][0]["message"]["content"])["choice"],
        "latency_ms": round((time.perf_counter() - started) * 1000),
        "cost": body["usage"].get("cost", 0.0),
    }
