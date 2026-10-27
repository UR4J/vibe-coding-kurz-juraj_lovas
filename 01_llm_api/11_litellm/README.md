# LiteLLM proxy

One HTTP endpoint in front of every provider. Your code always talks to
`http://localhost:4000`, always in the OpenAI format. Which real provider answers
is decided by the **alias** you put in the `model` field, and the aliases live in
`litellm_config.yaml`.

Swapping a cloud model for a local one is then a one-word change in your code, not
a rewrite.

## The aliases

Every alias names its engine, so you always know who answered and who is billed.

| Alias | Engine | Cost |
|:--|:--|:--|
| `openai-gpt-5.4-nano`, `openai-text-embedding-3-small` | OpenAI | paid |
| `anthropic-claude-sonnet-5` | Anthropic | paid |
| `gemini-flash` | Google | paid |
| `grok-mini` | xAI | paid |
| `hf-gemma-4` | HuggingFace router | paid |
| `openrouter-gemma` | OpenRouter | free tier |
| `runpod-vllm-mistral` | RunPod (your own vLLM) | paid |
| `ollama-gemma-4-e4b` | **Ollama**, your machine (lesson 7) | free |

## The local twins

LM Studio (lesson 8) and Unsloth Studio (lesson 9) run the **same two Gemma
models** on your machine. So the aliases come in pairs, and swapping one for the
other measures the engine and nothing else.

| Job | LM Studio (`:1234`) | Unsloth (`:8888`) |
|:--|:--|:--|
| Chat, small | `lmstudio-gemma-4b` | `unsloth-gemma-4b` |
| Chat, large | `lmstudio-gemma-26b` | `unsloth-gemma-26b` |
| Embeddings | `lmstudio-embed` | `unsloth-embed` |
| Needs a key? | no | **yes** |

`main-local-models.py` in `1_basics` calls the pairs one after another.

Two traps:

- **The 26B models think before they answer**, and the thinking spends the same
  budget as the reply. Both engines do it - it is the model, not the engine.
- **The two embedders are not interchangeable.** Both give 768 numbers from nomic
  v1.5, but LM Studio serves the Q4_K_M build and Unsloth the Q8_0 build. An index
  built with one and searched with the other returns quietly worse matches and
  never errors.

## What a local alias must declare

LiteLLM ships a table of what every cloud model costs and how big its window is.
It knows **nothing** about a model on your machine, so each local alias states
four things itself. Leave one out and it fails quietly.

| Setting | Why | Value here |
|:--|:--|--:|
| `max_tokens` | The reply budget, which the thinking also spends. Too small returns **empty content**, `finish_reason: "length"`, no error. | `8192` |
| `timeout` | LiteLLM defaults to 600 s. Your GPU reads a big prompt for 5-15 minutes before the first token, so the default expires mid-prompt and reports a 400 that is never retried. | `3600` |
| `max_input_tokens` | Rejects an over-long prompt **before** it reaches the model, not after 10 minutes of grinding. Context minus the 8192 output reserve. | `122880` / `253952` |
| `input/output_cost_per_token` | An unpriced route logs $0, so a spend ceiling on it never trips. These are **shadow** prices - what the same work would cost on a cloud twin. | `0.00000012` / `0.00000035` |

`max_input_tokens` does nothing on its own. `router_settings.enable_pre_call_checks`
must be `true`, and it is off by default. It is set at the bottom of the config.

Windows measured 2026-09-02 with `lms ps --json` and Unsloth's `GET /v1/status`.
Do not copy them from a model card - **LM Studio can load a model with a smaller
window than the model supports**, and then `max_input_tokens` is a lie. Check
`lms ps --json` if long prompts start failing.

## When a parameter is not the problem — `custom_callbacks.py`

`drop_params` removes a **parameter** an engine does not understand. It cannot
reach **inside** the messages, and one engine here is strict about what it finds
there.

Unsloth Studio rejects a `name` field on any message that is not a tool result:

```
400 messages.2: Value error, "name" is only valid on role="tool" messages.
```

OpenAI's own API allows `name` on a user or assistant message — it labels who
spoke when a conversation has several participants. LM Studio and Ollama accept
it. Unsloth is stricter than the specification, and the check runs in its HTTP
layer, so **the model never sees the request**.

This breaks real code. `deepagents` tags a sub-agent's assistant messages with
the sub-agent name, so `4_subagents` and `8_research_agent` in
[`06_langchain-ai/3_deepagents`](../../06_langchain-ai/3_deepagents) failed on
every `unsloth-*` alias while the other six lessons passed.

`custom_callbacks.py` is a **pre-call hook**: it edits the request after the
client sends it and before the engine gets it. It removes `name` from non-tool
messages, for the `unsloth-*` aliases only. `name` is a label, not content — no
model reads it — so nothing is lost.

Three things must line up, and the hook is **silent** if any one is wrong:

| Where | What |
|:--|:--|
| `docker-compose.yml` | mounts the file at `/app/custom_callbacks.py` |
| `litellm_config.yaml` | `callbacks: custom_callbacks.proxy_handler_instance` |
| `custom_callbacks.py` | defines `proxy_handler_instance` at module level |

This is the proxy earning its keep. Without it, every framework in every language
would repeat the same repair.

## Before you start

1. Copy `.env.example` to `.env` and fill in the keys you have. An alias whose key
   is missing simply fails when you call it; the others keep working.
2. Start the local engines you want to use. They run **on the host**, not in
   Docker, because they need the GPU. The container reaches them at
   `host.docker.internal`.
3. Unsloth needs a real key in `UNSLOTH_API_KEY`. Ollama and LM Studio do not.
   The key must be in **this `.env`**. A container does not inherit your shell,
   so a key that works from a terminal still gives `401 Invalid token payload`
   here if the line is missing.

Postgres is published on host port **5439**, not 5432. Docker Desktop's
`gvproxy` already holds 5432 on a Mac, and the DB lessons hold 5433. Nothing
outside `docker-compose.yml` needs the port — LiteLLM reaches postgres inside
the compose network.

## Run

```bash
docker compose up
```

# Open

Swagger

```
http://localhost:4000/
```

UI Admin

```
http://localhost:4000/ui/
```
