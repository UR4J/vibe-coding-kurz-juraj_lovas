# Cerebras

[Cerebras](https://www.cerebras.ai) runs open models on its own wafer-scale chips.
The reason to use it is **speed**: hundreds to thousands of tokens per second,
where a GPU cloud gives you tens.

It serves an **OpenAI-compatible** API on `https://api.cerebras.ai/v1`, so the same
`openai` SDK you used in lesson 1 talks to it. Only the `base_url` and the key
change. See the
[OpenAI compatibility page](https://inference-docs.cerebras.ai/resources/openai).

## Setup

Create a key at [cloud.cerebras.ai](https://cloud.cerebras.ai). Then copy
`.env.example` to `.env` in the sub-lesson folder and paste it in:

```
CEREBRAS_API_KEY=csk-...
```

Every script here reads that variable. If it is already in your shell
environment, you can skip the `.env` file.

## Model used here

All scripts use **`qwen-3.8-27b`**. It does chat, images, tools and structured
output, so one model covers the whole lesson.

`GET /v1/models` listed two models for this key on 2026-09-28:

| Model | Images | `reasoning_effort` values |
|:--|:--|:--|
| `qwen-3.8-27b` | yes | `none`, `low`, `medium`, `high` |
| `gpt-oss-120b` | **no** - `400 Only 'text' content type can be used` | `low`, `medium`, `high` |

## Four things to know

### 1. The model thinks, and thinking can eat the whole budget

Thinking tokens come out of the same `max_tokens` allowance as the answer. With no
`reasoning_effort` set, `qwen-3.8-27b` can think until the budget is gone. You get
**empty content** and no error. Only `finish_reason: "length"` tells you.

Measured on 2026-09-28 with the prompt "Write a 300-word story about a lighthouse
keeper":

| `reasoning_effort` | `max_tokens` | Thinking tokens | Answer |
|:--|--:|--:|:--|
| not set | 4000 | 4000 | **empty** |
| not set | 16000 | 16000 | **empty** |
| `none` | 16000 | 0 | full story |
| `low` | 4000 or 16000 | 160 - 179 | full story |

The thinking shows why. The model tries to count the words to exactly 300, and it
never finishes counting. A plain "Tell me a joke" thinks for only about 20 tokens.
So the risk depends on the **prompt**, and you cannot see it in advance.

The rule: set `reasoning_effort` on any prompt that asks for long or exact output.
`main-reasoning.py` shows the trap and the fix.

### 2. The thinking comes back in a separate field

The answer is in `content`. The thinking is in `reasoning`. The OpenAI SDK does
not declare that field, so read it with
`response.choices[0].message.model_extra["reasoning"]`.

`content` often starts with `"\n\n"` - the gap left where the thinking was.

### 3. Images must be base64

Send an image as a `data:image/png;base64,...` or `data:image/jpeg;base64,...`
URI. A normal `https://` image URL and the `detail` option are not supported.

### 4. Some OpenAI options do not exist here

From the compatibility page:

- `n` must be `1`.
- `service_tier` and `prediction` are not available on shared inference.
- `tool_stream` is not supported. Use `stream=True`.

Cerebras also adds its own options. Send them in `extra_body`, for example
`extra_body={"reasoning_format": "raw"}`.

## Speed

`main-speed.py` streams a story and measures it. Every Cerebras response also has
a `time_info` block, with the time the chip spent on your request. Measured on
2026-09-28, `qwen-3.8-27b`, about 760 output tokens, 3 runs:

| Measure | Result |
|:--|--:|
| Time to first token | 0.23 - 0.75 s |
| Tokens/s, your clock | 480 - 770 |
| Tokens/s, server `completion_time` | 925 - 999 |

Your clock is slower than the server because it adds the network and the queue.
Short answers are faster per token: a tool call measured about 1,700 tokens/s.

## Sub-lessons

| Folder | What it shows |
|:--|:--|
| `1_basics` | Chat with the `openai` SDK and with raw HTTP, thinking, speed, structured output |
| `2_multimodal` | Send an image and ask about it |
| `3_chat_history` | Why the model forgets, and how to fix it |
| `4_tools` | Let the model call your Python functions |

## Run

In each folder:

```bash
uv run main.py
```
