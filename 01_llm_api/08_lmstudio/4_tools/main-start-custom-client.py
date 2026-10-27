import lmstudio as lms


def get_stock_price(ticker: str) -> str:
    """
    Use this function to get the current price of a stock.
    """
    # Simulated response (replace with actual API call if needed)
    return f"The current stock price for {ticker} is $150."


with lms.Client(api_host="localhost:1234") as client:
    model = client.llm.model("google/gemma-4-e4b")

    result = model.act(
        "What is the current stock price for MSFT?",
        [get_stock_price],  # CUSTOM TOOLS
        on_message=print,
    )

    print("--- Result: ---")
    print(result)
