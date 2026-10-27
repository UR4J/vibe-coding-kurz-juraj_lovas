import os
from openai import OpenAI
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

# Cerebras exposes an OpenAI-compatible API, so the standard SDK works.
# Only the base_url and the key change.
client = OpenAI(
    base_url="https://api.cerebras.ai/v1",
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)

response = client.chat.completions.create(
    model="qwen-3.8-27b",
    messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "Tell me a joke."},
    ],
    # The model thinks first, and thinking spends THIS budget.
    # See main-reasoning.py.
    max_tokens=8192,
)

print("--- Full response: ---")
pprint(response)
print("--- Response text: ---")
print(response.choices[0].message.content)
