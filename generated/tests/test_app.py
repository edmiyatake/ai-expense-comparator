import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.app import Expense, totals_by_category, compare_periods

def test_totals_by_category_simple_case():
    expenses = [
        Expense(date="2024-01-01", description="Groceries", amount=50, category="Food", account="Checking"),
        Expense(date="2024-01-02", description="Lunch", amount=15, category="Food", account="Checking"),
        Expense(date="2024-01-03", description="Gas", amount=40, category="Transport", account="Credit Card"),
    ]
    totals = totals_by_category(expenses)
    assert isinstance(totals, dict)
    assert totals["Food"] == 65
    assert totals["Transport"] == 40
    assert set(totals.keys()) == {"Food", "Transport"}

def test_compare_periods_detects_increase():
    period_a = [
        Expense(date="2024-01-01", description="Dinner", amount=20, category="Food", account="CC"),
        Expense(date="2024-01-02", description="Bus", amount=5, category="Transport", account="CC"),
    ]
    period_b = [
        Expense(date="2024-02-01", description="Groceries", amount=40, category="Food", account="CC"),
        Expense(date="2024-02-03", description="Taxi", amount=12, category="Transport", account="CC"),
    ]
    comparison = compare_periods(period_a, period_b)
    assert "Food" in comparison
    assert "Transport" in comparison
    assert comparison["Food"]["period_a"] == 20
    assert comparison["Transport"]["period_a"] == 5
    assert comparison["Food"]["period_b"] == 40
    assert comparison["Transport"]["period_b"] == 12
    assert comparison["Food"]["delta"] == 20  # delta = period_b - period_a
    assert comparison["Transport"]["delta"] == 7

def test_compare_periods_handles_missing_categories():
    period_a = [
        Expense(date="2024-01-01", description="Coffee", amount=5, category="Food", account="Cash"),
        Expense(date="2024-01-05", description="Book", amount=10, category="Education", account="Cash"),
    ]
    period_b = [
        Expense(date="2024-02-03", description="Bus", amount=7, category="Transport", account="Cash"),
        Expense(date="2024-02-10", description="Groceries", amount=12, category="Food", account="Cash"),
    ]
    comparison = compare_periods(period_a, period_b)
    # Education present only in period_a
    assert "Education" in comparison
    assert comparison["Education"]["period_a"] == 10
    assert comparison["Education"]["period_b"] == 0
    assert comparison["Education"]["delta"] == -10
    # Transport present only in period_b
    assert "Transport" in comparison
    assert comparison["Transport"]["period_a"] == 0
    assert comparison["Transport"]["period_b"] == 7
    assert comparison["Transport"]["delta"] == 7
    # Food present in both
    assert comparison["Food"]["period_a"] == 5
    assert comparison["Food"]["period_b"] == 12
    assert comparison["Food"]["delta"] == 7