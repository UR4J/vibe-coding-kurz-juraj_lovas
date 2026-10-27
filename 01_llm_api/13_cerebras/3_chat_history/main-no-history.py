import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.cerebras.ai/v1",
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)

response1 = client.chat.completions.create(
    model="qwen-3.8-27b",
    messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "Tell me a joke."},
    ],
    max_tokens=8192,
)

print("--- Response text: ---")
print(response1.choices[0].message.content)

response2 = client.chat.completions.create(
    model="qwen-3.8-27b",
    messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "Repeat me please the previous joke."},
    ],
    max_tokens=8192,
)

print("--- Response text: ---")
print(response2.choices[0].message.content)
