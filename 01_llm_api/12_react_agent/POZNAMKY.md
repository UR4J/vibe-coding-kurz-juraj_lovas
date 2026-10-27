# 12_react_agent: moje poznámky

Beží na `anthropic/claude-sonnet-5-5` cez LiteLLM (27. 10. 2026). Kód cyklu sa nemenil, iba `.env`.

## ReAct v jednej vete

Model v cykle **uvažuje → zavolá nástroje → dostane výsledky → uvažuje znova**, kým nemá odpoveď.
Poradie krokov nie je nikde v kóde, model si ho určí sám. Pojistka: `max_iterations = 10`.

## Čo som pridal

1. **`ReactAgent(tools=..., functions=...)`**: nástroje sa dajú vložiť zvonku. Jeden cyklus, ľubovoľná sada nástrojov.
   Pôvodné príklady (akcie) fungujú bez zmeny.
2. **`neohunter_agent.py`**: sourcing agent s nástrojmi `get_job`, `search_candidates`, `get_candidate`
   nad **vymyslenými** dátami (repo je verejné).

## Čo agent spravil sám (pozícia J-102, 4 iterácie)

| Iterácia | Akcia |
|:--|:--|
| 1 | `get_job("J-102")`: prečítal požiadavky |
| 2 | 4× `search_candidates` paralelne: retail, FMCG, regionálny manažér, predaj |
| 3 | `get_candidate` pre 3 nájdených, aby overil detaily |
| 4 | poradie, riziká, **vyradil** KAM-a bez tímu (nespĺňa must-have 10+ ľudí), napísal oslovenie |

## Poznatky

- **Popis nástroja je prompt.** "Call several times with different keywords" spôsobilo paralelné hľadanie.
- **System prompt je kontrola kvality.** "Before you rank anyone, open their full profile" zabránilo hodnoteniu len podľa titulku.
- **LiteLLM = výmena providera bez zmeny kódu.** Rovnaký agent pôjde na OpenRouter (zadarmo) aj lokálne cez Ollama, čo sa hodí pre dáta kandidátov (GDPR).

## Ďalší krok pre Neohunter

Vymeniť vymyslené dáta za Recruit CRM API (`search_candidates`, `get_candidate`, `create_note`).
Zápisové nástroje (zmena stage, odoslanie správy) iba so schválením človekom.
