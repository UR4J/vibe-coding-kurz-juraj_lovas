# Vibe Coding kurz

Kurz Global Classes, 27. 10. 2026 až 1. 12. 2026, lektor Lukáš Kellerstein.
Repo `UR4J/vibe-coding-kurz-juraj_lovas` (verejné, zdieľané s lektorom): materiály z lekcií a moje riešenia na jednom mieste.

## Štruktúra

Každá lekcia má vlastný priečinok s číslom (`01_...`, `02_...`). Materiál od lektora
sa nahráva bez zmien ako samostatný commit, moja práca ide do ďalších commitov nad ním.
Vďaka tomu je v histórii vždy vidieť, čo je od lektora a čo moje.

## Domáce úlohy

| Úloha | Zadanie | Riešenie | Deadline | Stav |
|:--|:--|:--|:--|:--|
| 1 | Python skript: LLM API + nástroj, výsledok späť do LLM | [`domaci_ukoly/ukol_01_llm_tools`](domaci_ukoly/ukol_01_llm_tools) | 27. 11. 2026 | hotové |

## Lekcie

| Lekcia | Priečinok | Téma | Stav |
|:--|:--|:--|:--|
| 01 | `01_llm_api` | LLM API: OpenAI, Anthropic, Gemini, Grok, HuggingFace, OpenRouter, lokálne modely (Ollama, LM Studio, Unsloth), RunPod, LiteLLM, ReAct agent, Cerebras, Jev | OpenAI, Anthropic, ReAct, Jev hotové (viď `POZNAMKY.md`) |

## Nová lekcia

1. Na GitHube kurzu: **Code → Download ZIP**.
2. Nový priečinok lekcie (`02_...`) skopírovať sem do koreňa repa.
3. Commit `lekcia 02: materiál od lektora`, potom až vlastné úpravy.

## Spúšťanie príkladov

Každý podpriečinok s `pyproject.toml` je samostatný projekt pre [uv](https://docs.astral.sh/uv/):

```bash
cd 01_llm_api/02_anthropic/1_basics
cp .env.example .env    # sem patrí API kľúč, .env sa necommituje
uv run main.py
```

## Pravidlá

- API kľúče iba v `.env`, nikdy v kóde ani v commite (`.env` je v `.gitignore`).
- Repo je **verejné**: pred každým commitom skontrolovať, že v ňom nie je kľúč, token ani dáta kandidátov či klientov.
