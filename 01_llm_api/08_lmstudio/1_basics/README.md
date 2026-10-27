# Run

> Prerequisite: start the LM Studio server (`lms server start`) and make sure
> the model is loaded (`lms load google/gemma-4-e4b`). The server listens on
> `http://localhost:1234`.

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
