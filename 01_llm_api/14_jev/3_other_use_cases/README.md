# Jev use cases outside banking

Use cases that fit what Jev does best: **fast, cheap, typed decisions at volume**.
Most of the ideas come from two videos (see Sources).

| File | Use case | Pattern it teaches | Measured result (2026-09-24) |
|:--|:--|:--|:--|
| `1_agent_router.py` | Jev picks the handler (code, LLM agent or a person) and blocks prompt injection | **Jev in front of an agent**. Only 1 of 6 requests needed the LLM. | route in ~300 ms. The LLM call took 1,321 ms. |
| `2_jev_then_llm.py` | Jev sorts 16 video comments, and the LLM replies only to the 7 that need a reply | **Cascade**: System 1 filters, System 2 writes | Jev $0.00032. LLM $0.00201, instead of ~$0.00459 for all 16 |
| `3_meeting_insights.py` | 6 questions per transcript are counted into a "story" (for example "50 % of meetings have clear next steps") | **Many small answers, one big picture** | 10 meetings, run in parallel |
| `4_realtime_feed_filter.py` | Live Hacker News stories, each labelled as it arrives | **Real time**: the label is ready before you read the post | 250-330 ms per story |
| `5_page_declutter.py` | Remove ads, cookie banners, pop-ups and upsells from `sample_page.html` | **One question per element, one call for the whole page** | 6 of 14 elements removed, 0 mistakes, 289 ms |
| `6_ai_slop_detector.py` | The chance that each paragraph is generic AI filler. It works with a URL too. | **A signal, not proof** | 3 slop and 2 human paragraphs, all correct |

Helper files:

- `jev.py`: the same helper as in `1_basics`
- `llm.py`: text generation with a classic LLM (used in scripts 1 and 2)

## Ideas for exercises

- **Lead or job qualification**: `score` for lead quality, and `noul` for red flags.
- **Contract vetting**: `choice` for the clause type, and `score` for the risk.
- **Brain-dump router**: voice notes sorted into task, idea or journal, with the area of life and a deadline.
- **Fuzzy "find in page"**: every paragraph is one option of a single `choice`. See `../2_banking/6_find_in_terms.py`.
- **Generative UI**: Jev picks components from a UI library. See `../2_banking/5_app_next_screen.py`.

We skipped the trading bot from video 2 on purpose. The author calls it "not very vetted", and the trading
fees were higher than the cost of the Jev decisions.

# Run

Put your `OPENROUTER_API_KEY` in `../.env` (one file for all three folders).

```bash
uv run 1_agent_router.py
uv run 4_realtime_feed_filter.py 60        # run it live for 60 seconds
uv run 6_ai_slop_detector.py https://example.com/blog-post
```

## Sources

- [Matthew Berman - 8 Jev Use Cases That Feel Like Cheating](https://www.youtube.com/watch?v=jGD_UR4wMJc)
- [Nate Herk - I Tested Jev on 12 Real Use Cases](https://www.youtube.com/watch?v=ymgH8jS6Wb8)
