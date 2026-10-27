import os
from openai import OpenAI
from pprint import pprint
from encode import encode_image
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.cerebras.ai/v1",
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)

response = client.chat.completions.create(
    model="qwen-3.8-27b",
    messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is in this image?"},
                {
                    "type": "image_url",
                    # Cerebras takes only base64 data URIs (PNG or JPEG).
                    # A normal https:// image URL is rejected.
                    "image_url": {
                        "url": f"data:image/png;base64,{encode_image('./test_image.png')}",
                    },
                },
            ],
        },
    ],
    max_tokens=8192,
)

print("--- Full response: ---")
pprint(response)
print("--- Response text: ---")
print(response.choices[0].message.content)
