# Jev pre headhunting: triedenie odpovedí kandidátov

Vlastné cvičenie k lekcii 14 (nápad "lead or job qualification" z `3_other_use_cases`).
Všetci kandidáti a odpovede sú **vymyslené**, repo je verejné.

## Problém

Headhunter pošle 50 až 200 oslovení týždenne. Každá odpoveď potrebuje ďalší krok
a dnes ich človek triedi ručne. Väčšina je pritom jasná ("Nemám záujem, ďakujem.").

| Zámer (`choice`) | Ďalší krok |
|:--|:--|
| `interested` | navrhnúť termín callu (draft od LLM) |
| `question` | odpovedať na otázku (draft od LLM) |
| `later` | follow-up úloha v CRM |
| `not_interested` | poďakovať, uzavrieť |
| `referral` | poďakovať, vypýtať kontakt |
| **GDPR** (`noul`) | **vždy človek**, bez ohľadu na istotu |

## Súbory

| Súbor | Čo robí |
|:--|:--|
| `golden_replies.py` | 32 ručne označených odpovedí (SK, CZ, EN), posledných 8 je zámerne ťažkých |
| `1_reply_triage_gate.py` | zmeria presnosť pri rôznych prahoch istoty a vypíše nebezpečné chyby (istá, ale zlá odpoveď) |
| `2_inbox_then_draft.py` | pondelkový inbox: Jev roztriedi všetko, LLM píše drafty iba pre istých `interested` a `question` |

## Spustenie

V priečinku `14_jev` skopírovať `.env.example` na `.env` a vložiť `OPENROUTER_API_KEY` (účet potrebuje kredit).

```bash
cd 01_llm_api/14_jev/5_neohunter
uv run 1_reply_triage_gate.py
uv run 2_inbox_then_draft.py
```

## Výsledky (27. 10. 2026, `typesafe/jev-1.13`)

**Golden set, 32 odpovedí:**

| Prah istoty | Automaticky | Presnosť automatických | Chyby automatu |
|:--|:--|:--|:--|
| 0.50 | 84 % | 100 % | 0 |
| **0.80** | **78 %** | **100 %** | **0** |
| 0.90 | 66 % | 100 % | 0 |

- **GDPR zachytené 32/32**, vrátane nepriamej otázky "Kde ste vzali moje údaje?".
- Na človeka išli presne tie nejasné: "Ďakujem, ozvem sa." (0.45), "Nemám záujem o túto, ale ak budete mať niečo v Pharma..." (0.32), "Ok" (0.73).
- Cena **$0.00074 za 32 odpovedí**, priemerne 574 ms na odpoveď. Slovenčina aj čeština fungujú.

**Inbox, 8 odpovedí:** 6 automaticky (istota 0.82 až 1.00), GDPR na človeka, "ok pošlite info" na človeka (0.41).

**Pozor, nepreceňovať:** golden set je malý a odpovede aj označenia písal ten istý autor.
Pred nasadením treba 100+ reálnych odpovedí z inboxu, označených človekom.

## Prečo je to dôležité pre Neohunter

- **Prah istoty je obchodné rozhodnutie, nie technické.** Skript ukáže, koľko práce ušetrím pri akej chybovosti.
- **GDPR je pevné pravidlo v kóde, nie v modeli.** Žiadosť o výmaz nikdy nespracuje automat.
- **Drafty iba navrhujú.** Odoslanie a zmena stage v Recruit CRM ostávajú na človeku.
