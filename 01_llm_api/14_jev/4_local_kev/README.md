# Jev on your own machine - Kev-9B (open weights)

Jev is closed. You can only call it through an API. This folder runs the closest
**open** model: [**Kev**](https://github.com/jaredpalmer/kev) by Jared Palmer
(Apache-2.0, ~6,700 GitHub stars one week after Jev came out).

| | Jev | Kev-9B |
|:--|:--|:--|
| Weights | closed | open ([`jaredpalmer/kev-9b`](https://huggingface.co/jaredpalmer/kev-9b)) |
| Runs | TypeSafe / OpenRouter cloud | **your machine** (Apple Silicon through MLX, or a CUDA GPU) |
| Model | unknown | `Qwen/Qwen3.5-9B-Base` + a LoRA adapter + a small "pointer head" that scores the options |
| API | `/v1/systemone` | **the same** `/v1/systemone`, so it works as a drop-in |
| Price | $0.042 / 1M input tokens | $0, you only pay for the electricity |
| Accuracy on unseen tasks (authors' test) | 0.857 | 0.822 (0.852 on the locked test) |
| Share you can automate at ≤ 5 % error | 0.70 | 0.45-0.62 |
| Memory | - | about 17-19 GB |

**How it works.** Kev does not generate text either. It reads the state and each
question in one forward pass. A small head then gives a probability to every
option. The design copies a public guess about how Jev works
(["Jev's Architecture Unmasked"](https://archerhume.com/posts/jevs-architecture-unmasked)).
TypeSafe never confirmed that guess.

## 1. Start the server

The server runs the whole time in its own terminal:

```bash
uv sync
uv run python -m kev.serve --run jaredpalmer/kev-9b --port 8009
```

The first start downloads about 19 GB into `~/.cache/huggingface`: the Qwen base
model and the Kev adapter. On Apple Silicon the server picks the **MLX** backend
automatically.

Check that it is up:

```bash
curl -s localhost:8009/v1/models
```

## 2. Run the scripts

| File | What it shows |
|:--|:--|
| `1_three_primitives.py` | The same request as `../1_basics/1_three_primitives.py`, sent to `localhost` |
| `2_jev_vs_kev.py` | The 40-ticket golden set on Jev and on Kev: accuracy, coverage at the 0.8 gate, speed and cost |

### Measured on an Apple M5 Max, 128 GB (2026-09-24)

`2_jev_vs_kev.py` on the 40-ticket golden set:

| | Accuracy | Hard cases | Automated at the 0.8 gate | Correct among automated | Avg time per call | Cost |
|:--|--:|--:|--:|--:|--:|--:|
| Jev (OpenRouter) | 98 % | 7/8 | 92 % | 100 % | 307 ms | $0.00072 |
| Kev-9B (local, MLX) | 95 % | 6/8 | **68 %** | 100 % | **151 ms** | $0 |

Kev is almost as accurate, faster on this Mac (there is no network round trip), and free.
But it is **less sure of itself**: at the same gate it automates 68 % of tickets
instead of 92 %, so more tickets go to a person. The first call after a start took
3,088 ms. The next ones took about 110-180 ms.

## 3. Run ANY lesson script on Kev (drop-in)

Every `jev.py` in this lesson reads `JEV_URL`. Add these two lines to `../.env`:

```
JEV_URL=http://localhost:8009/v1/systemone
JEV_MODEL=kev-latest
```

Now `../2_banking/2_scam_payment_check.py` and all the other scripts run on your
local model, with no change to the code. Remove the two lines to go back to Jev.

## Things to know

- **The first request is slow.** MLX compiles the model on the first call. Measure the second call and later ones.
- **A Mac is slower than a GPU.** On a Mac a request takes hundreds of milliseconds. On an H100 it takes tens.
- **Kev is less sure of itself than Jev.** At the same confidence gate it automates fewer items. Set the gate from your own data, as in `../1_basics/5_confidence_gate.py`.
- **Kev is weaker on general knowledge** (MMLU 0.74 vs 0.90). It is close to Jev on routing and classification.
- **You can fine-tune it.** The authors trained Kev-4B for one pass on 5,219 consumer-finance complaints, and its accuracy went from 0.804 to 0.904. See "Fine-Tune on Your Own Data" in the [Kev README](https://github.com/jaredpalmer/kev).
- **Other sizes:** `jaredpalmer/kev-4b` (faster), `jaredpalmer/kev-0.8b` (for a laptop). `jaredpalmer/kev-27b`, the only Kev on Qwen3.8, needs an 80 GB GPU and has no Mac path.

## Other open alternatives

| Project | Idea |
|:--|:--|
| [SemIf, formerly OpenJev](https://github.com/TheoLeeCJ/SemIf-OpenJev) | No training. It reads the option probabilities from any open model. |
| [NanoJev](https://github.com/TianyuCodings/NanoJev) | A tiny 0.6B copy with the full training pipeline. Good for learning. |
| [Laya](https://huggingface.co/convaiinnovations/laya) | A 421M BERT-style model, 33 ms, multilingual. It is weak on banking intents (Banking77: 0.425). |
| [Simple Jev](https://github.com/featherless-ai/simple-jev) | Wraps any Hugging Face model as a Jev-style endpoint |
