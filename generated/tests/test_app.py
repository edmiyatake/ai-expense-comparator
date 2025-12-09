import sys
import os
import datetime

# Ensure src/ is on sys.path so imports work when running from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.app import Expense, totals_by_category, compare_periods

def test_totals_by_category_simple_case():
    expenses = [
        Expense(date=datetime.date(2023, 4, 1), amount=10.0, category="groceries"),
        Expense(date=datetime.date(2023, 4, 2), amount=15.0, category="groceries"),
        Expense(date=datetime.date(2023, 4, 3), amount=7.5, category="entertainment"),
        Expense(date=datetime.date(2023, 4, 4), amount=20.0, category="transportation"),
        Expense(date=datetime.date(2023, 4, 5), amount=3.0, category="entertainment"),
    ]
    expected = {
        "groceries": 25.0,
        "entertainment": 10.5,
        "transportation": 20.0,
    }
    result = totals_by_category(expenses)
    assert result == expected

def test_compare_periods_detects_increase():
    period_a = [
        Expense(date=datetime.date(2023, 3, 1), amount=20.0, category="groceries"),
        Expense(date=datetime.date(2023, 3, 2), amount=10.0, category="entertainment"),
    ]
    period_b = [
        Expense(date=datetime.date(2023, 4, 1), amount=30.0, category="groceries"),  # increased
        Expense(date=datetime.date(2023, 4, 2), amount=10.0, category="entertainment"),  # same
    ]
    result = compare_periods(period_a, period_b)
    assert "groceries" in result
    assert "entertainment" in result
    assert result["groceries"]["a"] == 20.0
    assert result["groceries"]["b"] == 30.0
    assert result["groceries"]["diff"] == 10.0
    assert result["entertainment"]["diff"] == 0.0

def test_compare_periods_handles_missing_categories():
    period_a = [
        Expense(date=datetime.date(2023, 3, 1), amount=20.0, category="groceries"),
        Expense(date=datetime.date(2023, 3, 2), amount=8.0, category="transportation"),
    ]
    period_b = [
        Expense(date=datetime.date(2023, 4, 1), amount=30.0, category="groceries"),
        Expense(date=datetime.date(2023, 4, 2), amount=5.0, category="entertainment"),  # new category
    ]
    result = compare_periods(period_a, period_b)
    assert "groceries" in result
    assert "transportation" in result
    assert "entertainment" in result

    # Category missing from period_b
    assert result["transportation"]["a"] == 8.0
    assert result["transportation"]["b"] == 0.0
    assert result["transportation"]["diff"] == -8.0

    # Category missing from period_a
    assert result["entertainment"]["a"] == 0.0
    assert result["entertainment"]["b"] == 5.0
    assert result["entertainment"]["diff"] == 5.0

    # Common category
    assert result["groceries"]["a"] == 20.0
    assert result["groceries"]["b"] == 30.0
    assert result["groceries"]["diff"] == 10.0