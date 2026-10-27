import os
from huggingface_hub import InferenceClient
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

client = InferenceClient(
    api_key=os.environ.get("HF_TOKEN"),
)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b:together",
    messages=[
        {"role": "user", "content": "Tell me another one."},
    ],
    max_tokens=500,
)

print("--- Full response: ---")
pprint(response)
print("--- Response text: ---")
print(response.choices[0].message.content)
