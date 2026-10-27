# Run

> Prerequisite: start Unsloth Studio, load `unsloth/gemma-4-E4B-it-qat-GGUF`, and
> turn on the API server. It listens on `http://localhost:8888`.
>
> Copy `.env.example` to `.env` and paste your key.

The model never runs your code. It only says which function it wants and with
which arguments. You run it and send the result back.

| File | What it shows |
|:--|:--|
| `main-start.py` | Step 1 only - the model asks for a tool and stops |
| `main-finished.py` | The full loop - run the tool, send the result, get the answer |

Two things to watch:

- The model **thinks before it picks a tool**. A small `max_tokens` means it
  never reaches the tool call. These scripts use 8192.
- When it wants a tool, `content` is `None` and `finish_reason` is `tool_calls`.
  That is normal, not an error.

## Run directly

`uv run main-start.py` (or alternative files)

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
python main-start.py
```
