import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ONE client. Three engines running on this machine: Ollama (lesson 7),
# LM Studio (lesson 8) and Unsloth Studio (lesson 9).
#
# The client does not know which one answers. It never sees port 11434, 1234 or
# 8888, and it never sees a provider key. It sends an alias to the proxy, and
# `litellm_config.yaml` decides the rest.
client = OpenAI(
    api_key=os.getenv("LITELLM_API_KEY", "dummy-key"),
    base_url=os.getenv("LITELLM_BASE_URL", "http://0.0.0.0:4000"),
)

# The two rows below are the SAME weights on two engines. That is the point:
# swap `lmstudio-` for `unsloth-` and the only thing that changed is the engine.
#
# Start only the engines you have. An alias whose engine is off fails; the
# others keep working. Delete the lines you do not need.
LOCAL_MODELS = [
    "lmstudio-gemma-4b",
    "unsloth-gemma-4b",
    "lmstudio-gemma-26b",
    "unsloth-gemma-26b",
    "ollama-gemma-4-e4b",
]

for model in LOCAL_MODELS:
    print(f"\n=== {model} ===")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": "Tell me a joke."},
            ],
            max_tokens=8192,
        )

        message = response.choices[0].message

        # The 26B models think before they answer. The thinking is scratch work
        # you pay for but never show the user, so print its size next to the
        # answer and watch how much the same question can cost.
        reasoning = message.model_extra.get("reasoning_content")
        print(f"[{response.usage.completion_tokens} tokens, "
              f"{len(reasoning or '')} chars of thinking]")
        print(message.content)
    except Exception as error:
        # Most likely: that engine is not running, or its model is not loaded.
        print(f"failed: {error}")
