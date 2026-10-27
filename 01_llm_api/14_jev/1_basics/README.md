# Jev basics - how it works

General examples (an online shop, reviews, e-mails). No bank yet. Run them in order.

| File | What you learn | Measured result (2026-09-24) |
|:--|:--|:--|
| `1_three_primitives.py` | One raw HTTP call with `noul`, `choice` and `score`, and the full JSON response | 522 input tokens, $0.000022 |
| `2_writing_criteria.py` | The criteria are the prompt. "Is a hot dog a sandwich?" with 3 definitions | vague 72 %, structural 91 %, strict 5 % |
| `3_many_questions_one_call.py` | Output is free, so ask all your questions in one call | 8 calls: 2,358 ms, $0.000126. 1 call: 314 ms, $0.000031 |
| `4_parallel_at_scale.py` | 200 e-mails: one by one vs. parallel vs. parallel + batched | 83 s → 3.1 s → **0.4 s** |
| `5_confidence_gate.py` | How to pick the threshold between "act" and "ask a person" | at 0.8: 92 % automated, 100 % correct |
| `6_jev_vs_llm.py` | Speed and cost against `openai/gpt-5.4-mini` | Jev 305 ms, ~$18 per 1M tickets. LLM 1,020 ms, ~$155 |

Helper files:

- `jev.py`: `decide()` and the builders `noul()`, `choice()` and `score()`
- `llm.py`: the same classification with a classic LLM, for the comparisons
- `golden_set.py`: 40 hand-labelled support tickets. The last 8 are hard on purpose.

## Five things to remember

1. **Jev decides. It does not write.** It gives no text, no summaries and no code.
2. **Write criteria like a policy.** Say what counts as YES and what counts as NO, and give examples.
3. **Ask many questions in one call.** Output is free.
4. **Run in parallel and batch items.** That is how you handle thousands of items.
5. **Measure before you trust.** Label real examples and set the confidence gate from the numbers.

# Run

Put your `OPENROUTER_API_KEY` in `../.env` (one file for all three folders).
Set `LLM_MODEL` there to compare with a different LLM.

```bash
uv run 1_three_primitives.py
```
