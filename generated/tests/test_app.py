import sys
import os

# Ensure the 'app' package is importable when running from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from datetime import date
from app.app import Expense, totals_by_category, compare_periods


def test_totals_by_category_simple_case():
    expenses = [
        Expense(date=date(2024, 6, 1), description="Groceries", amount=45.0, category="Food", account="Checking"),
        Expense(date=date(2024, 6, 2), description="Restaurant", amount=30.0, category="Food", account="Credit Card"),
        Expense(date=date(2024, 6, 5), description="Internet", amount=55.5, category="Utilities", account="Checking"),
    ]
    totals = totals_by_category(expenses)
    assert set(totals) == {"Food", "Utilities"}
    assert totals["Food"] == 75.0
    assert totals["Utilities"] == 55.5


def test_compare_periods_detects_increase():
    period_a = [
        Expense(date=date(2024, 5, 20), description="Lunch", amount=20.0, category="Food", account="Credit Card"),
    ]
    period_b = [
        Expense(date=date(2024, 6, 20), description="Dinner", amount=35.0, category="Food", account="Credit Card"),
    ]
    result = compare_periods(period_a, period_b)
    assert "Food" in result
    diff = result["Food"]
    # Example keys: {"period_a": float, "period_b": float, "diff": float}
    assert diff["period_a"] == 20.0
    assert diff["period_b"] == 35.0
    assert diff["diff"] == 15.0
    assert diff["diff"] > 0  # Increase in period_b


def test_compare_periods_handles_missing_categories():
    period_a = [
        Expense(date=date(2024, 5, 22), description="Movie", amount=12.0, category="Entertainment", account="Checking"),
    ]
    period_b = [
        Expense(date=date(2024, 6, 22), description="Power bill", amount=44.0, category="Utilities", account="Checking"),
    ]
    result = compare_periods(period_a, period_b)
    # "Entertainment" only in period_a; "Utilities" only in period_b
    assert set(result.keys()) == {"Entertainment", "Utilities"}
    assert result["Entertainment"]["period_a"] == 12.0
    assert result["Entertainment"]["period_b"] == 0.0
    assert result["Entertainment"]["diff"] == -12.0
    assert result["Utilities"]["period_a"] == 0.0
    assert result["Utilities"]["period_b"] == 44.0
    assert result["Utilities"]["diff"] == 44.0