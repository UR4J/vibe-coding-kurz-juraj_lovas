"""
Tiny helper: call a classic LLM (text generation) through OpenRouter.

Used where Jev decides and an LLM must WRITE something afterwards.
"""

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL = os.environ.get("LLM_MODEL", "openai/gpt-5.4-mini")


def llm_chat(prompt: str) -> dict:
    started = time.perf_counter()
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}"},
        json={
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "usage": {"include": True},
            # Drafts are short. Without a cap OpenRouter reserves credit for the
            # model maximum (65k tokens) and fails with 402 on a small balance.
            "max_tokens": 400,
        },
        timeout=60,
    )
    if not response.ok:
        raise RuntimeError(f"LLM call failed ({response.status_code}): {response.text}")

    body = response.json()
    return {
        "text": body["choices"][0]["message"]["content"],
        "latency_ms": round((time.perf_counter() - started) * 1000),
        "cost": body["usage"].get("cost", 0.0),
    }
