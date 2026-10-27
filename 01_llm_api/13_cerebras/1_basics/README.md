# Run

> Prerequisite: copy `.env.example` to `.env` and paste your Cerebras key.

| File | What it shows |
|:--|:--|
| `main.py` | Chat with the `openai` SDK |
| `main-http.py` | The same call as a plain HTTP POST |
| `main-reasoning.py` | Thinking eats the reply budget, and `reasoning_effort` fixes it |
| `main-speed.py` | Stream a reply and measure tokens per second |
| `main-structured-output.py` | Get a Pydantic object back instead of text |

## Run directly

`uv run main.py` (or alternative files)

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

Run script main (or alternative files)

```bash
python main.py
```
