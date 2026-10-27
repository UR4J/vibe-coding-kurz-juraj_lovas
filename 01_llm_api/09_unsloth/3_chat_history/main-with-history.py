import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="http://localhost:8888/v1",
    api_key=os.environ.get("UNSLOTH_API_KEY"),
)

MODEL = "unsloth/gemma-4-E4B-it-qat-GGUF"

# -----------------------------------------
# Initialize the chat history.
# YOU keep the history, not the server. Every call sends the whole list again.
messages = [{"role": "system", "content": "You are an AI assistant."}]
# -----------------------------------------

# First user query
messages.append({"role": "user", "content": "Tell me a joke."})

response1 = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    max_tokens=8192,
)
print("--- Response text: ---")
print(response1.choices[0].message.content)

# Get assistant's response and add it to the history.
# Send back only `content`. Do NOT send `reasoning_content` - the thinking is
# scratch work, and feeding it back wastes context on every later turn.
messages.append({"role": "assistant", "content": response1.choices[0].message.content})


# Second user query
messages.append({"role": "user", "content": "Repeat me please the previous joke."})

response2 = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    max_tokens=8192,
)
print("--- Response text: ---")
print(response2.choices[0].message.content)

# Get assistant's response and add it to the history
messages.append({"role": "assistant", "content": response2.choices[0].message.content})
