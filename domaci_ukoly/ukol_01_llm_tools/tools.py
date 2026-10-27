"""
Calculation tools the LLM can call: a headhunter's fee and VAT.

Pure functions with no API calls, so they are easy to test (see test_tools.py).
The LLM never computes the numbers itself. It decides WHICH tool to call
and with WHAT arguments, the code does the math.
"""


def calculate_recruitment_fee(
    monthly_gross_salary_eur: float,
    fee_percent: float,
    salaries_per_year: int = 12,
) -> dict:
    """Headhunter fee = a percentage of the candidate's annual gross salary."""
    if monthly_gross_salary_eur <= 0:
        raise ValueError("monthly_gross_salary_eur must be positive")
    if not 0 < fee_percent <= 100:
        raise ValueError("fee_percent must be between 0 and 100")
    if not 12 <= salaries_per_year <= 16:
        raise ValueError("salaries_per_year must be between 12 and 16")

    annual = monthly_gross_salary_eur * salaries_per_year
    return {
        "monthly_gross_salary_eur": monthly_gross_salary_eur,
        "salaries_per_year": salaries_per_year,
        "annual_gross_salary_eur": round(annual, 2),
        "fee_percent": fee_percent,
        "fee_eur": round(annual * fee_percent / 100, 2),
    }


def add_vat(amount_eur: float, vat_percent: float = 23) -> dict:
    """Add VAT to an amount. 23 % is the standard Slovak rate since 2025."""
    if amount_eur < 0:
        raise ValueError("amount_eur must not be negative")
    vat = round(amount_eur * vat_percent / 100, 2)
    return {
        "amount_without_vat_eur": round(amount_eur, 2),
        "vat_percent": vat_percent,
        "vat_eur": vat,
        "total_with_vat_eur": round(amount_eur + vat, 2),
    }


# Tool definitions for the Anthropic Messages API (JSON Schema for the arguments)
TOOLS = [
    {
        "name": "calculate_recruitment_fee",
        "description": (
            "Calculate a headhunter's placement fee as a percentage of the candidate's "
            "ANNUAL gross salary. Use it for every fee question, never calculate fees yourself."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "monthly_gross_salary_eur": {
                    "type": "number",
                    "description": "Candidate's monthly gross salary in EUR, e.g. 3800",
                },
                "fee_percent": {
                    "type": "number",
                    "description": "Fee as a percentage of the annual salary, e.g. 18",
                },
                "salaries_per_year": {
                    "type": "integer",
                    "description": "Number of salaries per year: 12 by default, 13 or 14 with a 13th/14th salary",
                },
            },
            "required": ["monthly_gross_salary_eur", "fee_percent"],
        },
    },
    {
        "name": "add_vat",
        "description": "Add VAT to an amount in EUR. Use it when the user asks for a price including VAT.",
        "input_schema": {
            "type": "object",
            "properties": {
                "amount_eur": {"type": "number", "description": "Amount without VAT in EUR"},
                "vat_percent": {
                    "type": "number",
                    "description": "VAT rate in percent, 23 by default (Slovakia)",
                },
            },
            "required": ["amount_eur"],
        },
    },
]

FUNCTIONS = {
    "calculate_recruitment_fee": calculate_recruitment_fee,
    "add_vat": add_vat,
}
