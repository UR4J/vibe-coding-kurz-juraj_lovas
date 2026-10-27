# Run

> Prerequisite: start the proxy first. In the folder above, run
> `docker compose up`. It listens on `http://localhost:4000`.

| File | What it shows |
|:--|:--|
| `main-chat-completion-api.py` | Call a cloud model through the proxy |
| `main-local-models.py` | The same client, three local engines |

## Run directly

`uv run main-chat-completion-api.py` (or alternative files)

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
python main-chat-completion-api.py
```
