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

tools = [
    {
        "name": "get_stock_price",
        "description": "Use this function to get the current price of a stock.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The ticker symbol for the stock, e.g. GOOG",
                }
            },
            "required": ["ticker"],
        },
    },
    {
        "name": "get_dividend_date",
        "description": "Use this function to get the next dividend payment date of a stock.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The ticker symbol for the stock, e.g. GOOG",
                }
            },
            "required": ["ticker"],
        },
    },
]

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    system="You are an AI assistant.",
    messages=[
        {"role": "user", "content": "What is the current stock price for MSFT?"},
    ],
    tools=tools,  # CUSTOM TOOLS
    tool_choice={"type": "auto"} # Allow AI to decide if a tool should be called
)

print("--- Full response: ---")
pprint(response)
print("--- Response text: ---")
print(text_of(response))
print("--- Response Tool call: ---")
# Find the tool_use block by type, its position in content is not fixed
print(next((block for block in response.content if block.type == "tool_use"), None))