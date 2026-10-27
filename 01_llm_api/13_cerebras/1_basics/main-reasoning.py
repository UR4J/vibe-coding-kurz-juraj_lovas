import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.cerebras.ai/v1",
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)

MODEL = "qwen-3.8-27b"
PROMPT = "Write a 300-word story about a lighthouse keeper."


def ask(reasoning_effort: str | None, max_tokens: int = 4000):
    kwargs = {"reasoning_effort": reasoning_effort} if reasoning_effort else {}
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT}],
        max_tokens=max_tokens,
        **kwargs,
    )

    message = response.choices[0].message
    usage = response.usage

    # `reasoning` is a Cerebras field. The OpenAI SDK does not know it,
    # so it lands in `model_extra` instead of on the object itself.
    reasoning = (message.model_extra or {}).get("reasoning")

    print(f"\n=== reasoning_effort = {reasoning_effort} ===")
    print(f"finish_reason    : {response.choices[0].finish_reason}")
    print(f"completion tokens: {usage.completion_tokens}")
    print(f"  of it thinking : {usage.completion_tokens_details.reasoning_tokens}")
    print(f"--- Thinking ({len(reasoning or '')} chars), first 300: ---")
    print((reasoning or "")[:300])
    print(f"--- Answer ({len(message.content or '')} chars), first 300: ---")
    print((message.content or "")[:300])


# The trap. With no effort set, the model can think until the budget runs out.
# `content` comes back EMPTY. There is no error - only finish_reason "length".
ask(None)

# The fix. "none" turns thinking off, "low" keeps a short plan.
# qwen-3.8-27b accepts none, low, medium and high.
ask("none")
ask("low")
