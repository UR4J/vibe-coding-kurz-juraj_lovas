import yfinance as yf
import lmstudio as lms


# Function Implementations
def get_stock_price(ticker: str):
    """
    Use this function to get the current price of a stock.
    """
    ticker_info = yf.Ticker(ticker).info
    current_price = ticker_info.get("currentPrice")
    return {"ticker": ticker, "current_price": current_price}


def get_dividend_date(ticker: str):
    """
    Use this function to get the next dividend payment date of a stock.
    """
    ticker_info = yf.Ticker(ticker).info
    dividend_date = ticker_info.get("dividendDate")
    return {"ticker": ticker, "dividend_date": dividend_date}


model = lms.llm("google/gemma-4-e4b")

# `.act()` runs the full agentic loop: the model decides which tool to call,
# LM Studio executes the Python function, feeds the result back, and repeats
# until the model produces a final answer.
result = model.act(
    "What is the current stock price for MSFT?",
    [get_stock_price, get_dividend_date],
    on_message=lambda message: print("Message:", message),
)

print("--- Final result: ---")
print(result)
