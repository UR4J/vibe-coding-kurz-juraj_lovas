import os
import json
import requests
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

# The OLD completion API: one prompt string in, one text string out.
# No roles, no chat. The model just continues the text you give it.
headers = {
    "Authorization": f"Bearer {os.environ.get('UNSLOTH_API_KEY')}",
    "Content-Type": "application/json",
}

data = {
    "model": "unsloth/gemma-4-E4B-it-qat-GGUF",
    "prompt": "The capital of France is",
    "max_tokens": 50,
    "stream": False,
}

response = requests.post(
    "http://localhost:8888/v1/completions",
    headers=headers,
    data=json.dumps(data),
)

print("--- Full response: ---")
pprint(response.json())
print("--- Response text: ---")
print(response.json()["choices"][0]["text"])
