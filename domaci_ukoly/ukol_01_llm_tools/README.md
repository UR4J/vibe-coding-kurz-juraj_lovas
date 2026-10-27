# Domácí úkol č. 1: Python skript pro LLM API

> Napiš Python skript, který zavolá LLM API, použije nástroj (např. výpočetní funkci) a vrátí odpověď zpět LLM.

**Use case:** koľko headhunter fakturuje za obsadenie pozície. LLM dostane otázku v bežnej reči,
čísla však počíta kód (nástroje), nie model.

## Ako to funguje

```
otázka ──> LLM ──tool_use──> skript spustí funkciu ──tool_result──> LLM ──> ... ──> odpoveď
                 (ktorý nástroj,      (tools.py)          (výsledok
                  aké argumenty)                           späť modelu)
```

| Súbor | Obsah |
|:--|:--|
| `tools.py` | 2 nástroje: `calculate_recruitment_fee` (fee z ročného platu, 12 až 16 platov) a `add_vat` (DPH 23 %) + ich JSON schémy |
| `main.py` | cyklus: volanie Anthropic Messages API → spustenie nástrojov → `tool_result` späť → opakovať, kým model neodpovie textom (max 5 krokov) |
| `test_tools.py` | 4 testy výpočtov, bez API kľúča |

Čo cyklus zvláda:
- **viac krokov za sebou:** najprv fee, potom DPH z výsledku (otázka 1)
- **viac nástrojov naraz:** dva výpočty v jednom kroku (otázka 2)
- **chyby:** zlé argumenty sa vrátia modelu ako `is_error`, aby volanie opravil, skript nespadne

## Spustenie

```bash
cp .env.example .env        # vložiť ANTHROPIC_API_KEY
uv run test_tools.py        # testy výpočtov
uv run main.py              # 2 ukážkové otázky
uv run main.py "Plat 5000 € brutto, 14 platov, fee 22 %. Koľko je to s DPH?"
```

## Výstup (27. 10. 2026, `claude-sonnet-5-5`)

```
OTÁZKA: Kandidát nastupuje ako regionálny manažér predaja s platom 3 800 € brutto mesačne,
firma vypláca aj 13. plat. Náš fee je 18 % z ročného platu. Koľko budeme fakturovať bez DPH a s DPH?
  [krok 1] calculate_recruitment_fee({'monthly_gross_salary_eur': 3800, 'fee_percent': 18, 'salaries_per_year': 13})
           -> {"annual_gross_salary_eur": 49400, "fee_eur": 8892.0, ...}
  [krok 2] add_vat({'amount_eur': 8892}) -> {"vat_eur": 2045.16, "total_with_vat_eur": 10937.16, ...}

ODPOVEĎ:
- Ročný plat: 49 400,00 € (13 × 3 800,00 €)
- Fee 18 %, bez DPH: 8 892,00 €
- DPH 23 %: 2 045,16 €
- S DPH: 10 937,16 €

OTÁZKA: Klient váha medzi dvoma kandidátmi. A chce 4 200 € mesačne (12 platov),
B chce 3 900 € mesačne (14 platov). Pri fee 20 %: na ktorom zarobíme viac a o koľko?
  [krok 1] calculate_recruitment_fee({... 4200, 'fee_percent': 20, 'salaries_per_year': 12}) -> {"fee_eur": 10080.0, ...}
  [krok 1] calculate_recruitment_fee({... 3900, 'fee_percent': 20, 'salaries_per_year': 14}) -> {"fee_eur": 10920.0, ...}

ODPOVEĎ:
Viac zarobíme na kandidátovi B, a to o 840,00 € (bez DPH).
Kandidát B má nižší mesačný plat, ale vyšší ročný príjem, lebo má 14 platov.
```

Druhá otázka ukazuje, prečo sa čísla nemajú nechať na model: nižší mesačný plat
dáva vyšší fee, lebo rozhoduje počet platov za rok.
