# 01_openai: moje poznámky

Spustené 27. 10. 2026 na Windows cez `spusti_vsetko.bat`: **14/14 príkladov OK** (po 2 opravách).

| Časť | Čo ukazuje | Výsledok |
|:--|:--|:--|
| 1_basics | Chat Completions vs. Responses API, cez SDK aj čisté HTTP; role `developer` riadi správanie ("píš česky ako Cimrman") | OK |
| 1_basics / structured output | model vracia JSON presne podľa Pydantic schémy | OK |
| 2_multimodal | obrázok ako base64 v správe | OK, rozpoznal Subaru Impreza WRX STI |
| 3_chat_history | API je bezstavové, históriu posielam ja; Responses API ju vie držať na serveri | OK |
| 4_tools | model iba navrhne volanie funkcie, spustím ju ja a výsledok mu vrátim | OK, MSFT $532.25 (živé dáta z Yahoo) |
| 5_generate_image | generovanie obrázka z JSON popisu produktu | OK, plagát rakety s textami a variantmi veľkostí |

## Čo som musel opraviť

| Problém | Príčina | Oprava |
|:--|:--|:--|
| `The model 'dall-e-2' does not exist` | DALL-E 2 a 3 vypnuté 12. 5. 2026 | `gpt-image-2.5-flare`, zmena cez `IMAGE_MODEL` v `.env`, ukladá sa z base64 do `output.png` |
| `YFRateLimitError: Too Many Requests` | stará `yfinance` 0.2.54 | `yfinance` 1.7.0 |

## Poznatky

- **Modely sa vypínajú rýchlo.** Kód z jari už na jeseň nefunguje. Názov modelu patrí do `.env`, nie natvrdo do kódu.
- **Structured output je najužitočnejší pre Neohunter:** CV → JSON (meno, skúsenosti, jazyky, mzda) → Recruit CRM bez prepisovania.
- **Generovanie obrázkov z JSON** = vizuály pracovných ponúk na LinkedIn priamo z popisu pozície.
