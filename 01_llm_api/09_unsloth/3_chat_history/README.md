# Run

> Prerequisite: start Unsloth Studio, load `unsloth/gemma-4-E4B-it-qat-GGUF`, and
> turn on the API server. It listens on `http://localhost:8888`.
>
> Copy `.env.example` to `.env` and paste your key.

The server remembers nothing. Run `main-no-history.py` and the model cannot repeat
its own joke. Run `main-with-history.py` and it can, because the script sends the
whole conversation every time.

Add only `content` back to the history. Leave `reasoning_content` out - the
thinking is scratch work, and feeding it back burns context on every later turn.

## Run directly

`uv run main-no-history.py` (or alternative files)

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
python main-no-history.py
```
