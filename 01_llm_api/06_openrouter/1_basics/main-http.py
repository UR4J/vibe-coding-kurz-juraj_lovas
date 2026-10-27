import os
import requests
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
    # Optional headers used by OpenRouter for app rankings on openrouter.ai
    "HTTP-Referer": "https://github.com/lukaskellerstein/ai-agents-course",
    "X-Title": "AI Agents Course",
}

data = {
    "model": "google/gemma-4-31b-it:free",
    "messages": [
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "Tell me a joke."},
    ],
    "max_tokens": 500,
    "stream": False,
}

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    json=data,
)

print("--- Full response: ---")
pprint(response.json())
print("--- Response text: ---")
print(response.json()["choices"][0]["message"]["content"])
