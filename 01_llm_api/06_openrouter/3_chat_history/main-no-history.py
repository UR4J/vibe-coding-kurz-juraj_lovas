import os
from openai import OpenAI
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

response1 = client.chat.completions.create(
    model="google/gemma-4-31b-it:free",
    messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "Tell me a joke."},
    ],
    max_tokens=500,
)

print("--- Response text: ---")
print(response1.choices[0].message.content)

response2 = client.chat.completions.create(
    model="google/gemma-4-31b-it:free",
    messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "Repeat me please the previous joke."},
    ],
    max_tokens=500,
)

print("--- Response text: ---")
print(response2.choices[0].message.content)
