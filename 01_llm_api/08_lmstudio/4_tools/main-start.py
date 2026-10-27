import lmstudio as lms


def get_stock_price(ticker: str) -> str:
    """
    Use this function to get the current price of a stock.
    """
    # Simulated response (replace with actual API call if needed)
    return f"The current stock price for {ticker} is $150."


model = lms.llm("google/gemma-4-e4b")

# LM Studio drives the tool-calling loop for you via `.act()`.
# Python functions (with type hints + docstrings) are passed directly as tools.
result = model.act(
    "What is the current stock price for MSFT?",
    [get_stock_price],  # CUSTOM TOOLS
    on_message=print,
)

print("--- Result: ---")
print(result)
