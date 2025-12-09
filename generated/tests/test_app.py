import sys
import os

# Ensure we can import from the project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from datetime import date
from app.app import Expense, totals_by_category, compare_periods


def test_totals_by_category_simple_case():
    expenses = [
        Expense(date=date(2024, 1, 10), description="Coffee", amount=3.5, category="Food", account="Checking"),
        Expense(date=date(2024, 1, 11), description="Lunch", amount=12.0, category="Food", account="Credit"),
        Expense(date=date(2024, 1, 12), description="Bus ticket", amount=2.75, category="Transport", account="Checking"),
    ]
    totals = totals_by_category(expenses)
    assert isinstance(totals, dict)
    assert set(totals.keys()) == {"Food", "Transport"}
    assert totals["Food"] == 15.5
    assert totals["Transport"] == 2.75


def test_compare_periods_detects_increase():
    period_a = [
        Expense(date=date(2024, 2, 10), description="Groceries", amount=50.0, category="Groceries", account="Debit"),
    ]
    period_b = [
        Expense(date=date(2024, 3, 10), description="Groceries", amount=75.0, category="Groceries", account="Credit"),
    ]
    result = compare_periods(period_a, period_b)
    assert "Groceries" in result
    assert result["Groceries"]["period_a"] == 50.0
    assert result["Groceries"]["period_b"] == 75.0
    assert result["Groceries"]["delta"] == 25.0
    assert result["Groceries"]["trend"] in ("increase", "up", "+")  # trend string may vary


def test_compare_periods_handles_missing_categories():
    period_a = [
        Expense(date=date(2024, 4, 10), description="Rent", amount=1000.0, category="Housing", account="Debit"),
    ]
    period_b = [
        Expense(date=date(2024, 5, 10), description="Electricity", amount=100.0, category="Utilities", account="Debit"),
    ]
    result = compare_periods(period_a, period_b)
    # Both categories must appear with zeros for their missing period
    assert "Housing" in result
    assert "Utilities" in result
    assert result["Housing"]["period_a"] == 1000.0
    assert result["Housing"]["period_b"] == 0.0
    assert result["Utilities"]["period_a"] == 0.0
    assert result["Utilities"]["period_b"] == 100.0
    # Deltas calculated properly
    assert result["Housing"]["delta"] == -1000.0
    assert result["Utilities"]["delta"] == 100.0