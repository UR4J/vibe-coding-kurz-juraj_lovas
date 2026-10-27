import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="http://localhost:8888/v1",
    api_key=os.environ.get("UNSLOTH_API_KEY"),
)

# Each call is a fresh start. The server keeps NOTHING between calls, so the
# second question below has no idea what the first joke was.
response1 = client.chat.completions.create(
    model="unsloth/gemma-4-E4B-it-qat-GGUF",
    messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "Tell me a joke."},
    ],
    max_tokens=8192,
)

print("--- Response text: ---")
print(response1.choices[0].message.content)

response2 = client.chat.completions.create(
    model="unsloth/gemma-4-E4B-it-qat-GGUF",
    messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "Repeat me please the previous joke."},
    ],
    max_tokens=8192,
)

print("--- Response text: ---")
print(response2.choices[0].message.content)
