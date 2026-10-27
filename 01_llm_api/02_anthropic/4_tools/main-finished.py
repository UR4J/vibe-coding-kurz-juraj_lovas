import os
import json
import yfinance as yf
from pprint import pprint
import anthropic
from dotenv import load_dotenv
load_dotenv()  

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

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

# Define available functions
available_functions = {
    "get_stock_price": get_stock_price,
    "get_dividend_date": get_dividend_date,
}

# Function to process messages and handle function calls
def get_completion_from_messages(messages, model="claude-sonnet-5-5"):
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system="You are a helpful AI assistant.",
        messages=messages,
        tools=tools,
        tool_choice={"type": "auto"}
    )

    print("First response:", response)

    # The model can ask for several tools in one response (e.g. price AND dividend date)
    tool_calls = [item for item in response.content if item.type == "tool_use"]

    if tool_calls:
        # Append the assistant message exactly as returned: thinking + tool_use blocks.
        # Rebuilding it by hand drops the thinking blocks, which the API expects back.
        messages.append({"role": "assistant", "content": response.content})

        # Run every requested tool and answer each one with its own tool_result
        tool_results = []
        for tool_call in tool_calls:
            function_to_call = available_functions[tool_call.name]
            function_response = function_to_call(**tool_call.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": json.dumps(function_response),
            })

        # All results go back in ONE user message
        messages.append({"role": "user", "content": tool_results})

        # Second call to get final response based on function output.
        # Keep `tools` here: the history now contains tool_use blocks.
        second_response = client.messages.create(
            model=model,
            max_tokens=1024,
            system="You are a helpful AI assistant.",
            messages=messages,
            tools=tools,
        )
        
        return second_response
    
    return response

# Example usage
messages = [
    {"role": "user", "content": "What is the current stock price for MSFT?"},
]

response = get_completion_from_messages(messages)
print("--- Full response: ---")
pprint(response)
print("--- Response text: ---")
final_text = "".join(block.text for block in response.content if block.type == "text")
print(final_text or "No text content in the response")