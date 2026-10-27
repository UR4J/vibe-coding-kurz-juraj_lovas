import os
from openai import OpenAI
from pprint import pprint
from encode import encode_image
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="http://localhost:8888/v1",
    api_key=os.environ.get("UNSLOTH_API_KEY"),
)

# The image travels inside the message, as base64 text in a data URL.
# There is no upload step and no file id.
response = client.chat.completions.create(
    model="unsloth/gemma-4-E4B-it-qat-GGUF",
    messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{encode_image('./test_image.png')}",
                    },
                },
            ],
        },
    ],
    # An image prompt makes this model think, even though a plain text prompt
    # often does not. At max_tokens=300 the answer came back EMPTY.
    max_tokens=8192,
)

print("--- Full response: ---")
pprint(response)
print("--- Response text: ---")
print(response.choices[0].message.content)
