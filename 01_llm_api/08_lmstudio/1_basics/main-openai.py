import os
from openai import OpenAI
from pprint import pprint

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="none",
)

response = client.chat.completions.create(
    model="google/gemma-4-e4b",
    messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "Tell me a joke."},
    ],
    max_tokens=500,
)

print("--- Full response: ---")
pprint(response)
print("--- Response text: ---")
print(response.choices[0].message.content)
