import os
import requests
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

# The same call as main.py, as a plain HTTP POST. No SDK needed.
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.environ.get('CEREBRAS_API_KEY')}",
}

data = {
    "model": "qwen-3.8-27b",
    "messages": [
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "Tell me a joke."},
    ],
    "max_tokens": 8192,
    "stream": False,
}

response = requests.post(
    "https://api.cerebras.ai/v1/chat/completions",
    headers=headers,
    json=data,
)

print("--- Full response: ---")
pprint(response.json())
print("--- Response text: ---")
print(response.json()["choices"][0]["message"]["content"])
