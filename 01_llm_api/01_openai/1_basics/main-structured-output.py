import os
from pprint import pprint
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


class JokeText(BaseModel):
    joke: str
    category: str
    funny_scale: int
    description: str


conversation = [
    {
        "role": "developer",
        "content": "Pis vzdycky cesky, a chovej se jako Jara cimrman.",
    },
    {"role": "user", "content": "Hey"},
    {"role": "assistant", "content": "Hello! How can I assist you today?"},
    {"role": "user", "content": "what is price of MSFT?"},
]

response = client.chat.completions.parse(
    model="gpt-5-mini", messages=conversation, response_format=JokeText
)

print("--- Full response: ---")
pprint(response)
print("--- Response text: ---")
print(response.choices[0].message.content)
