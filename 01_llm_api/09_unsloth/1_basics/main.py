import os
from openai import OpenAI
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

# Unsloth Studio speaks the OpenAI protocol, so the standard SDK works.
# Unlike LM Studio, the key is NOT optional - every route 401s without it.
client = OpenAI(
    base_url="http://localhost:8888/v1",
    api_key=os.environ.get("UNSLOTH_API_KEY"),
)

response = client.chat.completions.create(
    model="unsloth/gemma-4-E4B-it-qat-GGUF",
    messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "Tell me a joke."},
    ],
    # Thinking tokens come out of THIS budget. Set it too low and `content`
    # comes back empty. See main-reasoning.py.
    max_tokens=8192,
)

print("--- Full response: ---")
pprint(response)
print("--- Response text: ---")
print(response.choices[0].message.content)
