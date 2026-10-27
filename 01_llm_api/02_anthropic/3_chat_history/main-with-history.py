import os
from pprint import pprint
import anthropic
from dotenv import load_dotenv
load_dotenv()  

def text_of(response):
    """Join all text blocks of a response. Newer models can also return
    thinking or tool_use blocks, so content[0] is not always text."""
    return "".join(block.text for block in response.content if block.type == "text")


client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# -----------------------------------------
# Initialize the chat history
messages = []
# -----------------------------------------

# First user query
messages.append({"role": "user", "content": "Tell me a joke."})

response1 = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    system="You are an AI assistant.",
    messages=messages
)

# Get assistant's response and add it to the history
messages.append({"role": "assistant", "content": response1.content})  # full content, incl. thinking blocks

print("--- Response text: ---")
print(text_of(response1))

# Second user query
messages.append({"role": "user", "content": "Repeat me please the previous joke."})

response2 = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    system="You are an AI assistant.",
    messages=messages
)

# Get assistant's response and add it to the history
messages.append({"role": "assistant", "content": response2.content})  # full content, incl. thinking blocks

print("--- Response text: ---")
print(text_of(response2))
