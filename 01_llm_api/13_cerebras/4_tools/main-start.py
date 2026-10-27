import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.cerebras.ai/v1",
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Use this function to get the current price of a stock.",
            "parameters": {
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
    },
    {
        "type": "function",
        "function": {
            "name": "get_dividend_date",
            "description": "Use this function to get the next dividend payment date of a stock.",
            "parameters": {
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
    },
]

response = client.chat.completions.create(
    model="qwen-3.8-27b",
    messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {
            "role": "user",
            "content": "What is the current stock price for MSFT?",
        },
    ],
    max_tokens=8192,
    tools=tools,  # CUSTOM TOOLS
    tool_choice="auto",
)

print("--- Full response: ---")
print(response.to_json())
print("--- Response text: ---")
print(response.choices[0].message.content)
print("--- Response Tool call: ---")
print(response.choices[0].message.tool_calls)
