import sys
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple


@dataclass
class Expense:
    date: str
    description: str
    amount: float
    category: str
    account: Optional[str] = None


def group_expenses_by_category(expenses: List[Expense]) -> Dict[str, List[Expense]]:
    grouped: Dict[str, List[Expense]] = {}
    for expense in expenses:
        grouped.setdefault(expense.category, []).append(expense)
    return grouped


def total_spending_per_category(expenses: List[Expense]) -> Dict[str, float]:
    totals: Dict[str, float] = {}
    for expense in expenses:
        totals[expense.category] = totals.get(expense.category, 0.0) + expense.amount
    return totals


def compare_expense_periods(
    period1: List[Expense], period2: List[Expense]
) -> Dict[str, Tuple[float, float, float]]:
    """
    Returns a dict:
        category -> (total_period1, total_period2, delta_period2_minus_period1)
    """
    totals1 = total_spending_per_category(period1)
    totals2 = total_spending_per_category(period2)
    all_categories = set(totals1) | set(totals2)
    result: Dict[str, Tuple[float, float, float]] = {}

    for cat in sorted(all_categories):
        t1 = totals1.get(cat, 0.0)
        t2 = totals2.get(cat, 0.0)
        delta = t2 - t1
        result[cat] = (t1, t2, delta)
    return result


def print_comparison_report(
    period1: List[Expense], period2: List[Expense], period1_label: str, period2_label: str
):
    comparison = compare_expense_periods(period1, period2)
    col_cat = "Category"
    col_p1 = f"Total {period1_label}"
    col_p2 = f"Total {period2_label}"
    col_delta = f"Delta"

    header = f"{col_cat:20} {col_p1:15} {col_p2:15} {col_delta:10}"
    separator = "-" * len(header)
    print(header)
    print(separator)
    for category, (total1, total2, delta) in comparison.items():
        print(
            f"{category:20} "
            f"{total1:15.2f} "
            f"{total2:15.2f} "
            f"{delta:10.2f}"
        )

    print(separator)
    grand_total1 = sum(e.amount for e in period1)
    grand_total2 = sum(e.amount for e in period2)
    grand_delta = grand_total2 - grand_total1
    print(
        f"{'TOTAL':20} "
        f"{grand_total1:15.2f} "
        f"{grand_total2:15.2f} "
        f"{grand_delta:10.2f}"
    )


def main():
    # Example period 1
    period1_expenses = [
        Expense("2024-05-01", "Supermarket", 120.00, "Groceries", "Chase"),
        Expense("2024-05-03", "Monthly MetroCard", 127.00, "Transportation", "Chase"),
        Expense("2024-05-10", "Netflix", 15.49, "Entertainment", "Amex"),
        Expense("2024-05-15", "Dinner Out", 60.00, "Dining", "Chase"),
        Expense("2024-05-21", "Uber", 22.50, "Transportation", "Amex"),
        Expense("2024-05-27", "Pharmacy", 30.00, "Health", "Chase"),
    ]

    # Example period 2
    period2_expenses = [
        Expense("2024-06-01", "Supermarket", 140.00, "Groceries", "Chase"),
        Expense("2024-06-03", "Monthly MetroCard", 127.00, "Transportation", "Chase"),
        Expense("2024-06-09", "Spotify", 9.99, "Entertainment", "Amex"),
        Expense("2024-06-12", "Dinner Out", 80.00, "Dining", "Chase"),
        Expense("2024-06-18", "Uber", 18.75, "Transportation", "Amex"),
        Expense("2024-06-28", "Pharmacy", 25.00, "Health", "Chase"),
        Expense("2024-06-28", "Clothes", 100.00, "Shopping", "Chase"),
    ]

    print("Expense Comparison Report")
    print("=========================")
    print_comparison_report(
        period1_expenses, period2_expenses, "May 2024", "June 2024"
    )


if __name__ == "__main__":
    main()