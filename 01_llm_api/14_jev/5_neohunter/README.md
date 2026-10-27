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

## Výsledky

Doplním po prvom reálnom behu: presnosť pri prahu 0.8, podiel automatizácie, cena.

## Prečo je to dôležité pre Neohunter

- **Prah istoty je obchodné rozhodnutie, nie technické.** Skript ukáže, koľko práce ušetrím pri akej chybovosti.
- **GDPR je pevné pravidlo v kóde, nie v modeli.** Žiadosť o výmaz nikdy nespracuje automat.
- **Drafty iba navrhujú.** Odoslanie a zmena stage v Recruit CRM ostávajú na človeku.
