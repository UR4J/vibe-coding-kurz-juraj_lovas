import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# These four routes are NOT part of the OpenAI protocol. They are Unsloth's own,
# and they let a script do what you would otherwise click in the app: see what is
# on disk, see what is loaded, load a model, unload it.
#
# This is the reason to script a LOCAL app. You cannot unload a model on
# api.openai.com, because you do not own the machine.

BASE_URL = "http://localhost:8888/v1"
HEADERS = {
    "Authorization": f"Bearer {os.environ.get('UNSLOTH_API_KEY')}",
    "Content-Type": "application/json",
}

CHAT_MODEL = "unsloth/gemma-4-E4B-it-qat-GGUF"


def print_status(title: str):
    """`/v1/status` describes the model that is loaded RIGHT NOW.

    Read it instead of guessing. Every field below changes with every model
    swap, and a wrong guess about `supports_reasoning` or `context_length` is
    the cause of most "the model returned nothing" reports.
    """
    status = requests.get(f"{BASE_URL}/status", headers=HEADERS).json()

    print(f"\n--- {title} ---")
    if not status.get("context_length"):
        print("  nothing is loaded")
        return

    for key in [
        "context_length",
        "supports_reasoning",
        "reasoning_always_on",
        "supports_tools",
        "is_vision",
        "has_audio_input",
    ]:
        print(f"  {key:<22}: {status.get(key)}")


# -----------------------------------------------------------------------------
# 1. What models does this machine have?
# -----------------------------------------------------------------------------
models = requests.get(f"{BASE_URL}/models", headers=HEADERS).json()

print("--- Models on this machine: ---")
for model in models["data"]:
    mark = "LOADED" if model.get("loaded") else "      "
    print(f"  {mark}  {model['id']:<60} {model.get('quant', '-')}")


# -----------------------------------------------------------------------------
# 2. What is loaded right now?
# -----------------------------------------------------------------------------
print_status("Before loading:")


# -----------------------------------------------------------------------------
# 3. Load a model on purpose.
#
# A chat call also loads it, but only if `Model auto-switch` is on, and then you
# wait inside the chat call. Loading first keeps the two costs apart.
# -----------------------------------------------------------------------------
print(f"\n--- Loading {CHAT_MODEL} ... ---")
load = requests.post(
    f"{BASE_URL}/load",
    headers=HEADERS,
    data=json.dumps({"model_path": CHAT_MODEL}),
).json()

# The full answer also carries the whole chat template, which is pages long.
for key in ["status", "model", "n_layers", "max_context_length"]:
    print(f"  {key:<22}: {load.get(key)}")

print_status("After loading:")


# -----------------------------------------------------------------------------
# 4. Unload it and get the memory back.
# -----------------------------------------------------------------------------
print(f"\n--- Unloading {CHAT_MODEL} ... ---")
unload = requests.post(
    f"{BASE_URL}/unload",
    headers=HEADERS,
    data=json.dumps({"model_path": CHAT_MODEL}),
).json()
print(f"  {unload}")

print_status("After unloading:")
