"""
Golden set - 40 support tickets of a fictional online shop, labelled by hand.

Copy of ../1_basics/golden_set.py. Used by 2_jev_vs_kev.py.

The last 8 tickets are HARD on purpose: vague, mixed topics or sarcastic.
A real golden set should have 100+ items taken from real traffic.
"""

TEAMS = {
    "shipping": "Delivery: where is my order, delays, courier, wrong address.",
    "returns": "Returns, exchanges, refunds for returned goods, damaged or wrong items.",
    "billing": "Payments, double charges, invoices, discount codes, VAT.",
    "technical": "Website or app errors, checkout bugs, login problems caused by a bug.",
    "account": "Account settings: e-mail, password reset, delete account, newsletter, GDPR.",
}

GOLDEN_SET = [
    # --- clear cases ---
    ("Where is my order #88213? It was supposed to arrive on Monday.", "shipping"),
    ("The courier says he delivered the parcel but I have nothing.", "shipping"),
    ("Can you change the delivery address for order 55102? I moved.", "shipping"),
    ("My package has been stuck in Leipzig for 6 days.", "shipping"),
    ("Do you ship to Norway? How long does it take?", "shipping"),
    ("Tracking number does not work on the DHL website.", "shipping"),
    ("I want to return the shoes, they are too small.", "returns"),
    ("The blender arrived with a cracked jar.", "returns"),
    ("You sent me a blue jacket, I ordered a black one.", "returns"),
    ("I returned the TV two weeks ago, where is my refund?", "returns"),
    ("Can I exchange the shirt for size L?", "returns"),
    ("How many days do I have to send back an item?", "returns"),
    ("I was charged twice for the same order.", "billing"),
    ("Please send me an invoice with my company VAT number.", "billing"),
    ("The discount code SUMMER20 is not applied at checkout.", "billing"),
    ("My card was charged but the order shows as unpaid.", "billing"),
    ("Can I pay by bank transfer instead of card?", "billing"),
    ("Why did you charge me 4.99 for delivery? It said free.", "billing"),
    ("The checkout page shows a blank screen after I click Pay.", "technical"),
    ("The app crashes every time I open my basket.", "technical"),
    ("Search on the website returns an error 500.", "technical"),
    ("Product images do not load in Safari.", "technical"),
    ("I get 'something went wrong' when I add items to the wishlist.", "technical"),
    ("The size filter does not work on the mobile site.", "technical"),
    ("How do I change the e-mail address on my account?", "account"),
    ("Please delete my account and all my data (GDPR).", "account"),
    ("I want to stop the newsletter, I get 3 e-mails a day.", "account"),
    ("I forgot my password, the reset e-mail never comes.", "account"),
    ("Can I merge my two accounts into one?", "account"),
    ("How do I add a second delivery address to my profile?", "account"),
    ("Please change the phone number in my profile.", "account"),
    ("Do you have my data? I want a copy of everything you store.", "account"),
    # --- hard cases ---
    ("Great, the third parcel lost this year. Amazing service.", "shipping"),
    ("Refund for the order you never delivered, please.", "billing"),
    ("I can't log in, the page just reloads when I press the button.", "technical"),
    ("The item is broken and I also want my money back for delivery.", "returns"),
    ("Hi, it is about my order.", "shipping"),
    ("Your app charged me in dollars instead of euros.", "billing"),
    ("I never got the password e-mail and now the site says my account is locked.", "account"),
    ("The return label link gives a 404 error.", "technical"),
]
