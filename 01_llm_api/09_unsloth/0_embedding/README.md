# Run

> Prerequisite: start Unsloth Studio with the API server on, and download
> `second-state/Nomic-embed-text-v1.5-Embedding-GGUF`. It listens on
> `http://localhost:8888`.
>
> Copy `.env.example` to `.env` and paste your key.

An embedding turns text into a list of numbers. Texts with a close meaning get
close vectors. This model gives 768 numbers per text.

Two warnings:

- **This call unloads your chat model.** Unsloth holds one model at a time, and
  the limit spans chat and embeddings.
- **Vectors do not mix across models or builds.** This is the Q8_0 build of
  nomic v1.5. LM Studio serves Q4_K_M and Ollama serves F16 of the *same* model,
  and the three are not interchangeable. Mixing them returns quietly worse
  matches and never errors. Record which model built each index.

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
