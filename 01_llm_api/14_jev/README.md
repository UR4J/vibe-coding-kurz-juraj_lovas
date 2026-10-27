# Jev - a model that decides, not talks

[Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) by
**TypeSafe AI** (released 15 September 2026) is the first "**System One**" model.
The name comes from Daniel Kahneman: System 1 is fast and intuitive, and System 2
is slow and deliberate.

| | Classic LLM (System 2) | Jev (System 1) |
|:--|:--|:--|
| Output | free text | typed answer and probabilities |
| Typical latency | 1-10 s | 70-500 ms |
| Price | pay for input and output tokens | $0.042 / 1M input tokens, **output free** |
| Parsing | you parse text or JSON and hope | you get JSON with fixed fields |
| "How sure are you?" | you cannot trust what it says | calibrated `confidence` and `probabilities` |
| Good for | writing, reasoning, tools, agents | routing, classification, scoring, yes/no checks |

The weights are closed, so you cannot run Jev locally. The closest open model, Kev, runs locally (see `4_local_kev`). The context window is 32k tokens on OpenRouter. In this lesson we call it
through **OpenRouter**, so you need no TypeSafe account.

## The three primitives

You send a **state** (the facts) and **questions**. Each question has one of three types.

| Type | Question | Answer |
|:--|:--|:--|
| `noul` | "Is this true?" | `{"noul": 0.96}` - the probability of yes |
| `choice` | "Which one of these options?" | `{"choice": "cards", "confidence": 0.91, "probabilities": {...}}` |
| `score` | "Where on this ordered scale?" | `{"score": 1.8, "confidence": 0.9, "probabilities": {"0":..,"1":..,"2":..}}` |

One call can ask many questions about the same state.

```
POST https://openrouter.ai/api/alpha/decisions
{ "model": "typesafe/jev-1.13", "state": {...}, "questions": {...} }
```

## The key pattern: confidence-gated automation

```
             ┌─ confidence >= 0.8 ─> act automatically   (the easy 80 %)
Jev answer ──┤
             └─ confidence <  0.8 ─> hand over to a person (the hard 20 %)
```

An LLM gives you an answer, but it gives you no reliable "how sure" number.
Jev gives both. So the **code** can decide when to trust the model. This is
where most of the savings come from.

## When NOT to use Jev

- **To generate text.** It writes nothing: no replies, no summaries, no code. Use an LLM, or use Jev first and an LLM second.
- **To find themes in a big pile of text on its own.** Ask many small typed questions and count the answers instead (see `3_other_use_cases/3_meeting_insights.py`).
- **For math, lookups, or rules you can write as code.** Use code.
- **Without measuring on labelled data.** "Cheap and fast" is worth nothing if the answers are wrong (see `1_basics/5_confidence_gate.py`).

## Lesson structure

```
12_jev/
├── .env                  your OPENROUTER_API_KEY (one file for all folders)
├── 1_basics/             how Jev works: primitives, criteria, scale, confidence gate, Jev vs. LLM
├── 2_banking/            Raiffeisenbank: routing, scams, AML, guardrails, generative UI, terms, budgets
├── 3_other_use_cases/    agent router, Jev then LLM, meeting insights, live feed, page declutter, slop detector
└── 4_local_kev/          the closest OPEN model (Kev-9B on Qwen3.5), running on your own machine
```

Each folder is its own `uv` project with its own copy of `jev.py`. Start with `1_basics`.

# Run

Copy `.env.example` to `.env` and add your `OPENROUTER_API_KEY`.
Jev is **not free**, so the account needs some credits. One call costs about $0.00002.

```bash
cd 1_basics
uv run 1_three_primitives.py
```

Or create the virtual environment yourself:

```bash
uv venv
source .venv/bin/activate
uv sync
python 1_three_primitives.py
```

## Sources

- [TypeSafe AI - Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- [TypeSafe docs - Example use cases](https://docs.typesafe.ai/concepts/use-case-map)
- [OpenRouter - Jev documentation](https://openrouter.ai/docs/guides/community/jev)
- [OpenRouter - Jev tutorial (request / response schema)](https://openrouter.ai/docs/guides/community/jev-tutorial)
- [Matthew Berman - 8 Jev Use Cases That Feel Like Cheating](https://www.youtube.com/watch?v=jGD_UR4wMJc)
- [Nate Herk - I Tested Jev on 12 Real Use Cases](https://www.youtube.com/watch?v=ymgH8jS6Wb8)
