# 02_anthropic: moje poznámky

Všetky príklady bežia na `claude-sonnet-5-5` (27. 10. 2026).

## Čo som musel opraviť a prečo

| Problém | Príčina | Oprava |
|:--|:--|:--|
| `claude-3-7-sonnet-20250219` | starý model | `claude-sonnet-5-5` |
| `content[0].text` padá na `ThinkingBlock` / `ToolUseBlock` | nový model vracia aj thinking a tool_use bloky, prvý blok nemusí byť text | helper `text_of()`: spojí iba bloky typu `text` |
| história: do `messages` sa ukladal iba text | stratia sa thinking bloky | ukladá sa celé `response.content` |
| tools: ručne poskladaná assistant správa | stratia sa thinking bloky, ktoré API pri tool use očakáva späť | `messages.append({"role": "assistant", "content": response.content})` |
| tools: spracoval sa len prvý tool call | model si vie v jednej odpovedi vypýtať viac nástrojov (cena aj dividenda) | cyklus cez všetky `tool_use`, všetky `tool_result` v jednej user správe |
| tools: druhé volanie bez `tools` | história obsahuje `tool_use` bloky | `tools=tools` aj v druhom volaní |

## Hlavné poznatky

1. **Odpoveď je zoznam blokov, nie text.** Vždy filtrovať podľa `block.type`, nikdy podľa pozície.
2. **API je bezstavové.** Model si "pamätá" iba to, čo mu pošlem v `messages` (`main-no-history.py` vs `main-with-history.py`).
3. **Tool use = model nič nespúšťa.** Iba povie, ktorú funkciu s akými argumentmi chce. Spustím ju ja a výsledok mu pošlem späť ako `tool_result` s rovnakým `tool_use_id`.
4. **Multimodal** = obrázok ako base64 blok v `content` vedľa textu.

## Ako to použiť v Neohunteri

- **Tool use** je základ každého agenta: nástroje typu `search_candidates`, `get_job_details`, `create_note` nad Recruit CRM.
- **História** je kľúčová pre screening chatbot: bez nej sa kandidáta pýta dookola na to isté.
