# Run

> Prerequisite: start Unsloth Studio with the API server on. It listens on
> `http://localhost:8888`.
>
> Copy `.env.example` to `.env` and paste your key.

The engine runs on **your** machine, so you can drive the machine too. These four
routes are Unsloth's own, not part of the OpenAI protocol:

| Route | What it does |
|:--|:--|
| `GET /v1/models` | List every model on disk, and mark the loaded one |
| `GET /v1/status` | Describe the loaded model - context, tools, vision, reasoning |
| `POST /v1/load` | Load a model, with `{"model_path": "..."}` |
| `POST /v1/unload` | Unload it and get the memory back |

Read `/v1/status` instead of guessing. `supports_reasoning` and `context_length`
change with every model swap, and a wrong guess about either one is the cause of
most "the model returned nothing" reports.

**This script unloads the model at the end.** Load it again in the app, or just
run any chat call - auto-switch loads it back.

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
