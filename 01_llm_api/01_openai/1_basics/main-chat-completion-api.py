import os
from pprint import pprint
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# === Roles ===
# [OLDER models] - system: The system message is used to set the behavior of the assistant.
# [NEWER models] - developer: The developer message is used to provide input to the assistant in a way that is not visible to the user.

# - user: The user message is used to provide input to the assistant.
# - assistant: The assistant message is used to provide output from the assistant.
# - tool: The tool message is used to provide input to the assistant in a way that is not visible to the user.
# [Deprecated] - function: The function message is used to provide input to the assistant in a way that is not visible to the user.

conversation = [
    {
        "role": "developer",
        "content": "Pis vzdycky cesky, a chovej se jako Jara cimrman.",
    },
    {"role": "user", "content": "Hey"},
    {"role": "assistant", "content": "Hello! How can I assist you today?"},
    {"role": "user", "content": "I am fine, tell me a joke"},
]

response = client.chat.completions.create(model="gpt-4o", messages=conversation)

print("--- Full response: ---")
pprint(response)
print("--- Response text: ---")
print(response.choices[0].message.content)
