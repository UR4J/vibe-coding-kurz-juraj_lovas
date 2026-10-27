import os
from pprint import pprint
import anthropic
from encode import encode_image
from dotenv import load_dotenv

load_dotenv()

def text_of(response):
    """Join all text blocks of a response. Newer models can also return
    thinking or tool_use blocks, so content[0] is not always text."""
    return "".join(block.text for block in response.content if block.type == "text")


client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is in this image?"},
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": encode_image("./test_image.png"),
                    },
                },
            ],
        }
    ],
)

print("--- Full response: ---")
pprint(response)
print("--- Response text: ---")
print(text_of(response))
