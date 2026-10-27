import os
from pprint import pprint
import anthropic
from dotenv import load_dotenv

load_dotenv()

def text_of(response):
    """Join all text blocks of a response. Newer models can also return
    thinking or tool_use blocks, so content[0] is not always text."""
    return "".join(block.text for block in response.content if block.type == "text")


client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# === Roles ===
# - user: The user message is used to provide input to the assistant.
# - assistant: The assistant message is used to provide output from the assistant.

# NO SYSTEM MESSAGE !!!
# But "system" parameter is available in the API

response = client.messages.create(
    model="claude-sonnet-5-5",
    system="You are an AI assistant.",
    messages=[
        {"role": "user", "content": "Tell me a joke."},
    ],
    max_tokens=100,
)

print("--- Full response: ---")
pprint(response)
print("--- Response text: ---")
print(text_of(response))
