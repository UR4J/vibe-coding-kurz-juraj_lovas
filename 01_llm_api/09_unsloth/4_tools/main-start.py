import os
import json
import yfinance as yf
from openai import OpenAI
from pprint import pprint
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(
    base_url="http://localhost:8888/v1",
    api_key=os.environ.get("UNSLOTH_API_KEY"),
)

MODEL = "unsloth/gemma-4-E4B-it-qat-GGUF"


# Function Implementations
def get_stock_price(ticker: str):
    ticker_info = yf.Ticker(ticker).info
    current_price = ticker_info.get("currentPrice")
    return {"ticker": ticker, "current_price": current_price}


def get_dividend_date(ticker: str):
    ticker_info = yf.Ticker(ticker).info
    dividend_date = ticker_info.get("dividendDate")
    return {"ticker": ticker, "dividend_date": dividend_date}


# Define custom tools
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

messages = [
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "What is the current stock price for MSFT?"},
]

# STEP 1 ONLY: ask the model what it wants.
# The model does NOT run your function. It answers with a plan: the tool name
# and the arguments. Running it, and sending the result back, is your job -
# that is what main-finished.py adds.
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=tools,
    tool_choice="auto",
    max_tokens=8192,
)

print("--- Full response: ---")
pprint(response)
print("--- finish_reason: ---")
print(response.choices[0].finish_reason)  # expect: tool_calls
print("--- Tool calls: ---")
print(response.choices[0].message.tool_calls)
print("--- Content (empty - the model is not done yet): ---")
print(response.choices[0].message.content)
