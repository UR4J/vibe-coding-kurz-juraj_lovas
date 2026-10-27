import os
from pprint import pprint
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

client = OpenAI(
    base_url="https://api.cerebras.ai/v1",
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)


class JokeText(BaseModel):
    joke: str
    category: str
    funny_scale: int
    description: str


# `parse` turns the Pydantic class into a JSON schema, sends it as
# `response_format`, and parses the reply back into a JokeText object.
response = client.chat.completions.parse(
    model="qwen-3.8-27b",
    messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "Tell me a joke about programmers."},
    ],
    response_format=JokeText,
    max_tokens=8192,
)

print("--- Full response: ---")
pprint(response)
print("--- Parsed object: ---")
joke = response.choices[0].message.parsed
print(type(joke).__name__, joke)
