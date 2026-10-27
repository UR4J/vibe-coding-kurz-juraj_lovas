# Run

> Prerequisite: start Unsloth Studio, load `unsloth/gemma-4-E4B-it-qat-GGUF`, and
> turn on the API server. It listens on `http://localhost:8888`.
>
> Copy `.env.example` to `.env` and paste your key. Unsloth 401s without one.

| File | What it shows |
|:--|:--|
| `main.py` | Chat with the `openai` SDK |
| `main-http-chat.py` | The same call as a plain HTTP POST |
| `main-http.py` | The old completion API - prompt in, text out |
| `main-reasoning.py` | Thinking eats the reply budget, and how to read it |

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
