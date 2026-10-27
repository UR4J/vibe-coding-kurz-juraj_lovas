# Unsloth Studio

[Unsloth Studio](https://unsloth.ai) is a desktop app that runs models on your own
machine — like LM Studio (lesson 8) and Ollama (lesson 7). It serves an
**OpenAI-compatible** HTTP API on `http://localhost:8888/v1`, so the same `openai`
SDK you used in lesson 1 talks to it. There is no separate Python SDK for the app;
the `unsloth` package on PyPI is the **fine-tuning** library, not a client.

Start the app, load a model in the UI, and the server is up.

## Four things that differ from LM Studio

Each one fails quietly, so read them before you run anything.

### 1. It needs an API key

LM Studio accepts any string. Unsloth answers **401 on every route** without a real
key, `/v1/models` included.

Create the key in the app: **Settings → API → API keys**. Then copy
`.env.example` to `.env` in the sub-lesson folder and paste it in:

```
UNSLOTH_API_KEY=sk-...
```

Every script here reads that variable.

### 2. It serves one model at a time

The limit spans chat **and** embeddings. Calling the embedding model unloads the
chat model, and the next chat call swaps it back. Turn on
**Settings → API → Model auto-switch**, or the second model you call returns
`400 No model loaded`.

A swap costs time. Measured on this machine, 2026-09-02:

| Swap | Time |
|:--|--:|
| To `gemma-4-E4B` (chat) | 8.6 s |
| To `Nomic-embed-text-v1.5` (embed) | 4.4 s |

So a retrieval loop that alternates embed and chat pays a swap on **every** call.

Leave **auto-download** OFF. With it on, a typo in a model name starts a
multi-gigabyte download instead of returning an error.

### 3. The models think, and thinking eats the reply budget

Reasoning tokens come out of the same `max_tokens` allowance as the answer. Set the
ceiling too low and you get **empty content** and no error. Only
`finish_reason: "length"` tells you what happened.

Unsloth puts the thinking in a separate field, `reasoning_content`. The OpenAI SDK
does not know that field, so read it with
`response.choices[0].message.model_extra["reasoning_content"]`.

Measured on this machine, 2026-09-02:

| Model | Prompt | Completion tokens |
|:--|:--|--:|
| `gemma-4-26B-A4B-it-qat` | "Say hi in 3 words." | 546 - 1934 |
| `gemma-4-E4B-it-qat` | "Say hi in 3 words." | 5 - 9 |
| `gemma-4-E4B-it-qat` | "What is in this image?" | 546 |

Read that first row again. The **same three-word question** costs anything from 546
to 1934 tokens, run to run, because the model decides how long to think. You cannot
budget for the average. Budget for the worst case.

**This is not an Unsloth trait.** LM Studio serves the same weights as
`google/gemma-4-26b-a4b-qat`, and that model thinks there too - 355 to 520 tokens
over three runs of the same prompt. The small E4B thinks on neither engine for a
plain question, and on both when you send it an image.

So thinking follows the **model**, not the engine. Give every chat call a large
`max_tokens` whatever you run it on. The scripts here use **8192**, which is also
the reserve lesson 11 subtracts from each model's window.

2000 is not enough, even though it looks like plenty for a three-word answer. The
worst run above spent 1934.

### 4. The model id carries a slash

`unsloth/gemma-4-E4B-it-qat-GGUF` is one model id, not a provider plus a model.
This matters in lesson 11, where LiteLLM needs its own `openai/` prefix in front:
`openai/unsloth/gemma-4-E4B-it-qat-GGUF`.

## Models used here

Load these two in the app before you start (**Models → Hub**):

| Job | Model id |
|:--|:--|
| Chat, vision, tools | `unsloth/gemma-4-E4B-it-qat-GGUF` |
| Embeddings | `second-state/Nomic-embed-text-v1.5-Embedding-GGUF` |

## Sub-lessons

| Folder | What it shows |
|:--|:--|
| `0_embedding` | Turn text into a 768-number vector |
| `1_basics` | Chat with the `openai` SDK and with raw HTTP; read `reasoning_content` |
| `2_multimodal` | Send an image and ask about it |
| `3_chat_history` | Why the model forgets, and how to fix it |
| `4_tools` | Let the model call your Python functions |
| `5_model_management` | List, inspect, load and unload models over the API |

## Run

In each folder:

```bash
uv run main.py
```
