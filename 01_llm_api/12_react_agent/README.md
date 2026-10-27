# Provider-agnostic ReAct AI Agent

**ONE** ReAct (Reason and Act) agent that connects to **ANY** provider — OpenAI,
Anthropic, Gemini, Grok, HuggingFace, OpenRouter, LM Studio, Ollama, and more.

Powered by [**LiteLLM**](https://docs.litellm.ai/docs/providers), which gives a
single unified interface to every provider. The ReAct loop in `main.py` never
changes — you only edit `.env`.

## Key idea

The agent logic (call the LLM → run tools → feed results back → repeat) is
**provider-agnostic**. Instead of copying it into every provider folder, there is
one implementation here. Switching providers is a config change, not a code
change.

## Configure

Copy `.env.example` to `.env` and pick a provider by setting two things:

- `MODEL` — a LiteLLM model string (e.g. `openai/gpt-4o-mini`,
  `anthropic/claude-sonnet-5-5`, `openrouter/google/gemma-4-31b-it:free`)
- the matching `<PROVIDER>_API_KEY` (e.g. `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`,
  `OPENROUTER_API_KEY`) — LiteLLM reads these automatically.

Local providers (LM Studio, Ollama) additionally set `API_BASE`.

The default `.env.example` uses the **free** `openrouter/google/gemma-4-31b-it:free`
model.

## Tools

Two example tools (via `yfinance`): `get_stock_price` and `get_dividend_date`.
The tool schema is the standard OpenAI format; LiteLLM translates it for each
provider.

# Run

## Run directly

`uv run main.py`

## Run indirectly

Create a virtual environment

```bash
uv venv
```

Activate virtual environment

```bash
source .venv/bin/activate
```

Install packages

```bash
uv sync
```

Run script

```bash
python main.py
```
