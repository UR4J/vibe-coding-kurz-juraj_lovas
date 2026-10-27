import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="http://localhost:8888/v1",
    api_key=os.environ.get("UNSLOTH_API_KEY"),
)

MODEL = "unsloth/gemma-4-E4B-it-qat-GGUF"
PROMPT = "A farmer has 17 sheep. All but 9 run away. How many are left? Explain."


def ask(max_tokens: int):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": PROMPT},
        ],
        max_tokens=max_tokens,
    )

    message = response.choices[0].message

    # `reasoning_content` is an Unsloth field. The OpenAI SDK does not know it,
    # so it lands in `model_extra` instead of on the object itself.
    reasoning = message.model_extra.get("reasoning_content")

    print(f"\n=== max_tokens = {max_tokens} ===")
    print(f"finish_reason    : {response.choices[0].finish_reason}")
    print(f"completion tokens: {response.usage.completion_tokens}")
    print(f"--- Thinking ({len(reasoning or '')} chars): ---")
    print(reasoning)
    print(f"--- Answer ({len(message.content or '')} chars): ---")
    print(message.content)


# The trap. The model thinks first, and thinking spends the SAME budget as the
# answer. With only 50 tokens the whole budget goes to thinking, so `content`
# comes back EMPTY. There is no error - only finish_reason "length" tells you.
ask(50)

# The fix. Give it room and you get both parts back.
ask(8192)
