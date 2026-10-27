import os
from openai import OpenAI
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

# OpenRouter exposes an OpenAI-compatible API.
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

response = client.chat.completions.create(
    model="google/gemma-4-31b-it:free",
    messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "Tell me a joke."},
    ],
    max_tokens=500,
    # Optional headers used by OpenRouter for app rankings on openrouter.ai
    extra_headers={
        "HTTP-Referer": "https://github.com/lukaskellerstein/ai-agents-course",
        "X-Title": "AI Agents Course",
    },
)

print("--- Full response: ---")
pprint(response)
print("--- Response text: ---")
print(response.choices[0].message.content)
