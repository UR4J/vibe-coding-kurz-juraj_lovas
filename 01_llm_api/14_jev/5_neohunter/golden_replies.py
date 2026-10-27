"""
Golden set: 32 candidate replies to a headhunter's LinkedIn outreach, labelled by hand.

All replies are FICTIONAL. Languages are mixed (SK, CZ, EN) on purpose,
because that is what a Slovak headhunter's inbox looks like.
The last 8 are HARD on purpose: mixed intent, polite no, sarcasm, very short.

Labels:
  intent       one of INTENTS
  gdpr         True when the candidate asks to stop contact, delete data,
               or asks where we got their data. Always goes to a person.

A real golden set should have 100+ replies taken from the real inbox.
"""

INTENTS = {
    "interested": "Wants to hear more or agrees to a call. Positive, ready to move on.",
    "question": "Asks for details first (salary, client name, location, remote, team) before deciding.",
    "later": "Not now, but open in the future. Asks to reconnect later or gives a time.",
    "not_interested": "Clear no. Happy in the current job, not looking, or not a fit.",
    "referral": "Not for them, but recommends another person or offers to pass the job on.",
}

# (reply, intent, gdpr)
GOLDEN_REPLIES = [
    # --- clear cases ---
    ("Dobrý deň, znie to zaujímavo. Kedy by ste mali čas na krátky call?", "interested", False),
    ("Ahoj, pokojne si zavolajme, som otvorený zmene. Hodí sa mi štvrtok poobede.", "interested", False),
    ("Hi, thanks for reaching out. Happy to talk, here is my number: +421 900 000 000.", "interested", False),
    ("Dobrý den, ozvěte se mi prosím, rád se dozvím víc.", "interested", False),
    ("Áno, pošlite mi prosím popis pozície a dohodneme si stretnutie.", "interested", False),
    ("Môžete mi povedať aký je platový rozsah?", "question", False),
    ("O akú firmu ide? Bez mena klienta sa ťažko rozhoduje.", "question", False),
    ("Is the role fully remote or do I need to be in Bratislava?", "question", False),
    ("Koľko ľudí by som mal v tíme a komu by som reportoval?", "question", False),
    ("Je to v Nitre alebo treba cestovať po celom Slovensku?", "question", False),
    ("Teraz to nejde, sme uprostred projektu. Ozvite sa mi prosím na jar.", "later", False),
    ("Momentálne nie, ale o pol roka mi končí bonusové obdobie, potom sa rád porozprávam.", "later", False),
    ("Not the right time for me, maybe in Q2 next year?", "later", False),
    ("Aktuálně řeším rodinné věci, zkuste mě prosím za pár měsíců.", "later", False),
    ("Ďakujem, ale som spokojný tam kde som.", "not_interested", False),
    ("Nemám záujem, ďakujem.", "not_interested", False),
    ("Thanks, but I'm not looking for a new job.", "not_interested", False),
    ("Prosím nekontaktujte ma viac a vymažte moje údaje z vašej databázy.", "not_interested", True),
    ("Nemám zájem a nepřeji si být dále kontaktován.", "not_interested", True),
    ("Pre mňa to nie je, ale kolega Marek by mohol mať záujem. Pošlem vám na neho kontakt.", "referral", False),
    ("Not for me, but I can forward it to a friend who is looking right now.", "referral", False),
    ("Ja nie, ale poznám dvoch ľudí z predchádzajúcej firmy, môžem im to preposlať?", "referral", False),
    ("Tohle není pro mě, ale sdílím to v naší skupině na LinkedInu.", "referral", False),
    ("Super, dajte vedieť termín, rád prídem aj osobne.", "interested", False),
    # --- hard cases ---
    ("Záleží od peňazí. Pod 4000 netto sa nebavím.", "question", False),
    ("Hmm, možno. Čo je to za firmu?", "question", False),
    ("Wow, už tretí headhunter tento týždeň s 'jedinečnou príležitosťou' 🙂", "not_interested", False),
    ("Ok", "interested", False),
    ("Teraz nie, ale môj bývalý šéf by bol ideálny, a mňa skúste o rok.", "referral", False),
    ("Ďakujem, ozvem sa.", "later", False),
    ("Nemám záujem o túto, ale ak budete mať niečo v Pharma, dajte vedieť.", "later", False),
    ("Prečo mi píšete na LinkedIn? Kde ste vzali moje údaje?", "not_interested", True),
]
