"""
Tests for the calculation tools. No API key needed.

Run:  uv run test_tools.py
"""

from tools import add_vat, calculate_recruitment_fee


def test_fee_with_13th_salary():
    result = calculate_recruitment_fee(3800, 18, salaries_per_year=13)
    assert result["annual_gross_salary_eur"] == 49400
    assert result["fee_eur"] == 8892


def test_fee_default_12_salaries():
    assert calculate_recruitment_fee(4200, 20)["fee_eur"] == 10080


def test_vat_default_23():
    result = add_vat(8892)
    assert result["vat_eur"] == 2045.16
    assert result["total_with_vat_eur"] == 10937.16


def test_invalid_input_is_rejected():
    for bad in [(0, 18), (3800, 0), (3800, 150)]:
        try:
            calculate_recruitment_fee(*bad)
        except ValueError:
            continue
        raise AssertionError(f"accepted invalid input {bad}")


if __name__ == "__main__":
    tests = [value for name, value in dict(globals()).items() if name.startswith("test_")]
    for test in tests:
        test()
        print(f"OK  {test.__name__}")
    print(f"\n{len(tests)}/{len(tests)} testov prešlo")
