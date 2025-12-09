import sys
import os
from datetime import date
import pytest

# Ensure imports work when running tests from the project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.app import Expense, totals_by_category, compare_periods

def test_totals_by_category_simple_case():
    expenses = [
        Expense(date=date(2024, 5, 1), description="Lunch", amount=12.5, category="Food", account="Checking"),
        Expense(date=date(2024, 5, 2), description="Groceries", amount=50, category="Food", account="Checking"),
        Expense(date=date(2024, 5, 3), description="Bus", amount=2.75, category="Transport", account="Checking"),
        Expense(date=date(2024, 5, 3), description="Coffee", amount=3, category="Food", account="Credit"),
    ]
    result = totals_by_category(expenses)
    assert isinstance(result, dict)
    assert result["Food"] == pytest.approx(65.5)
    assert result["Transport"] == pytest.approx(2.75)
    assert set(result.keys()) == {"Food", "Transport"}

def test_compare_periods_detects_increase():
    period_a = [
        Expense(date=date(2024, 5, 1), description="Lunch", amount=10, category="Food", account="Checking"),
        Expense(date=date(2024, 5, 2), description="Bus", amount=2, category="Transport", account="Checking"),
    ]
    period_b = [
        Expense(date=date(2024, 6, 1), description="Dinner", amount=25, category="Food", account="Checking"),
        Expense(date=date(2024, 6, 2), description="Taxi", amount=8, category="Transport", account="Credit"),
    ]
    result = compare_periods(period_a, period_b)
    assert "Food" in result
    assert "Transport" in result
    assert result["Food"]["period_a"] == pytest.approx(10)
    assert result["Food"]["period_b"] == pytest.approx(25)
    assert result["Food"]["delta"] == pytest.approx(15)
    assert result["Transport"]["period_a"] == pytest.approx(2)
    assert result["Transport"]["period_b"] == pytest.approx(8)
    assert result["Transport"]["delta"] == pytest.approx(6)

def test_compare_periods_handles_missing_categories():
    period_a = [
        Expense(date=date(2024, 5, 1), description="Lunch", amount=10, category="Food", account="Checking")
    ]
    period_b = [
        Expense(date=date(2024, 6, 1), description="Shoes", amount=50, category="Shopping", account="Credit")
    ]
    result = compare_periods(period_a, period_b)
    # Category appears in period_a only
    assert "Food" in result
    assert result["Food"]["period_a"] == pytest.approx(10)
    assert result["Food"]["period_b"] == pytest.approx(0)
    assert result["Food"]["delta"] == pytest.approx(-10)
    # Category appears in period_b only
    assert "Shopping" in result
    assert result["Shopping"]["period_a"] == pytest.approx(0)
    assert result["Shopping"]["period_b"] == pytest.approx(50)
    assert result["Shopping"]["delta"] == pytest.approx(50)
    # Only these categories in result
    assert set(result.keys()) == {"Food", "Shopping"}