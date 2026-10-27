# Jev for banking - Raiffeisenbank use cases

Seven runnable examples of how a retail bank can use Jev to work faster,
spend less and make better decisions. All data is fictional.

Start with [`../1_basics`](../1_basics) if you do not know how Jev works yet.

## Use cases

The ✅ rows have a runnable script in this folder. The other rows are ideas for exercises.

| # | Use case | Jev questions | What it improves |
|:--|:--|:--|:--|
| ✅ 1 | **Client request routing** (e-mail, chat, app) | `choice` team, `score` urgency, `noul` formal complaint, `noul` churn risk | Less manual triage. Urgent cases first. No missed complaint deadline. Early retention alerts. |
| ✅ 2 | **Scam check on outgoing payments** ("safe account", fake investments) | `noul` scam, `choice` scam type, `score` risk | Fast enough to run **inside** the payment flow. It reads text signals that numeric rules miss. Fewer client losses. |
| ✅ 3 | **AML alert triage** | `score` priority, `choice` typology, `noul` false positive | Analysts see real cases first. Less time on false positives. |
| ✅ 4 | **Guardrail for an LLM chatbot** | `noul` for each policy rule | Blocks bad answers (PIN requests, investment advice, promises). About 10x cheaper and 3x faster than a second LLM as a judge (see `../1_basics/6_jev_vs_llm.py`). |
| ✅ 5 | **Generative UI in the mobile app** | `choice` screen from the app's screen library, `noul` fraud banner, `noul` offer human help | The client types what they want and gets the right screen at once. No hunting in menus, fewer calls to the contact centre. Jev picks the parts, and the code builds the page. |
| ✅ 6 | **Find by meaning in product terms** | one `choice` with every section of the terms as an option, plus `not_in_terms` | Finds the right clause when the words do not match ("pay off early" vs. "extraordinary repayment"). Says "not found" instead of guessing. Works for short documents (32k context). |
| ✅ 7 | **Transaction categories for "My budget"** | one `choice` per transaction, many questions in **one** call | The whole statement in one call of about 300 ms, for about $0.00001 per transaction. Unsure lines stay uncategorised instead of getting a wrong category. |
| 8 | KYC / onboarding document check | `noul` "Is the document complete?", "Does the name match?" | Faster account opening. A person reviews only the unclear cases. |
| 9 | Card dispute (chargeback) classification | `choice` reason code, `noul` "Is evidence attached?" | Correct reason code on the first try, fewer rejected disputes. |
| 10 | Entity matching (sanctions, duplicate clients) | `noul` "Are these the same person or company?" | Fewer false sanctions hits, cleaner client data. |
| 11 | Agent router / tool picker | `choice` which agent or tool handles the request | A cheap, fast first step before an expensive LLM agent (see `../3_other_use_cases/1_agent_router.py`). |
| 12 | Call-centre QA | `score` politeness, `noul` "Was the mandatory disclosure said?" | 100 % of calls checked, not a 2 % sample. |
| 13 | Features for ML models | `score` and `noul` values from free text (notes, descriptions) | Unstructured text becomes numeric features for existing models. |

## Files

| File | What it shows |
|:--|:--|
| `1_client_request_routing.py` | Routing the contact centre inbox, with confidence gating |
| `2_scam_payment_check.py` | allow / warn / hold before a payment leaves the bank |
| `3_aml_alert_triage.py` | Sorting the AML analyst queue |
| `4_chatbot_guardrail.py` | Checking LLM chatbot drafts against the bank policy |
| `5_app_next_screen.py` | Generative UI: pick the app screen and the extra parts for what the client typed |
| `6_find_in_terms.py` | Find the right section of the mortgage terms by meaning, or say "not found" |
| `7_transaction_categories.py` | Put a whole statement into budget categories in one call |

## Rules for a bank

- **For the final decision in regulated high-impact cases, a person must decide.**
  Jev can prepare and sort the work. Examples:
  - The EU AI Act lists **credit scoring of natural persons** as *high-risk*
    (Annex III). This does not include fraud detection.
  - GDPR **Art. 22** limits fully automated decisions about people.
  - AML reports must come from a person.
- **Do not send real client data before a legal check.** The call goes to a US API
  through OpenRouter. So you must check the GDPR and the outsourcing and DORA
  rules first.

# Run

Put your `OPENROUTER_API_KEY` in `../.env` (one file for all three folders).

```bash
uv run 1_client_request_routing.py
```
