import os
import json
import requests
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

# The same call as main.py, but without the SDK - just an HTTP POST.
headers = {
    "Authorization": f"Bearer {os.environ.get('UNSLOTH_API_KEY')}",
    "Content-Type": "application/json",
}

data = {
    "model": "unsloth/gemma-4-E4B-it-qat-GGUF",
    "messages": [
        {"role": "system", "content": "You are an AI assistant."},
        {
            "role": "user",
            "content": "Tell me a joke.",
        },
    ],
    "max_tokens": 8192,
    "stream": False,
}

response = requests.post(
    "http://localhost:8888/v1/chat/completions",
    headers=headers,
    data=json.dumps(data),
)

print("--- Full response: ---")
pprint(response.json())
print("--- Response text: ---")
print(response.json()["choices"][0]["message"])
