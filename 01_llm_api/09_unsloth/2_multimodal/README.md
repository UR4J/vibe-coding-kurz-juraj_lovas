# Run

> Prerequisite: start Unsloth Studio, load `unsloth/gemma-4-E4B-it-qat-GGUF`, and
> turn on the API server. It listens on `http://localhost:8888`.
>
> Copy `.env.example` to `.env` and paste your key.

Gemma 4 E4B reads images. "E4B" means few parameters, not fewer features - vision
and tool calling both work on this small model.

`encode.py` turns the PNG into base64 text. The image then rides inside the
message as a data URL.

**Give this a large `max_tokens`.** An image prompt makes the model think, even
when a plain text prompt does not. At `max_tokens=300` the answer came back empty.

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

Run script main

```bash
python main.py
```
