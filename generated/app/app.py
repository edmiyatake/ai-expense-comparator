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


def total_per_category(expenses: List[Expense]) -> Dict[str, float]:
    totals: Dict[str, float] = {}
    for expense in expenses:
        totals[expense.category] = totals.get(expense.category, 0.0) + expense.amount
    return totals


def compare_periods(
    period1: List[Expense], period2: List[Expense]
) -> Dict[str, Tuple[float, float, float]]:
    totals1 = total_per_category(period1)
    totals2 = total_per_category(period2)
    all_categories = set(totals1) | set(totals2)
    comparison: Dict[str, Tuple[float, float, float]] = {}
    for cat in sorted(all_categories):
        total1 = totals1.get(cat, 0.0)
        total2 = totals2.get(cat, 0.0)
        delta = total2 - total1
        comparison[cat] = (total1, total2, delta)
    return comparison


def print_comparison_report(
    comparison: Dict[str, Tuple[float, float, float]],
    period1_name: str = "Period 1",
    period2_name: str = "Period 2",
):
    print("=" * 60)
    print(f"Expense Comparison: {period1_name} vs {period2_name}")
    print("-" * 60)
    print(
        f"{'Category':<20}{period1_name:<14}{period2_name:<14}{'Delta':<12}"
    )
    print("-" * 60)
    total1_sum = 0.0
    total2_sum = 0.0
    for cat, (total1, total2, delta) in comparison.items():
        total1_sum += total1
        total2_sum += total2
        delta_str = (
            f"+{delta:.2f}" if delta > 0 else f"{delta:.2f}" if delta < 0 else " 0.00"
        )
        print(
            f"{cat:<20}{total1:>10.2f}      {total2:>10.2f}      {delta_str:>10}"
        )
    print("-" * 60)
    all_delta = total2_sum - total1_sum
    all_delta_str = f"+{all_delta:.2f}" if all_delta > 0 else f"{all_delta:.2f}"
    print(
        f"{'TOTAL':<20}{total1_sum:>10.2f}      {total2_sum:>10.2f}      {all_delta_str:>10}"
    )
    print("=" * 60)
    print()


def main():
    # Example period 1 expenses
    period1 = [
        Expense("2024-05-10", "Groceries - Market", 46.20, "Groceries", "Checking"),
        Expense("2024-05-11", "Coffee Shop", 7.50, "Dining", "Credit Card"),
        Expense("2024-05-12", "Monthly Rent", 1200.00, "Housing", "Checking"),
        Expense("2024-05-12", "Streaming Sub", 12.99, "Entertainment", None),
        Expense("2024-05-13", "Electricity bill", 60.50, "Utilities", "Checking"),
        Expense("2024-05-14", "Lunch with friends", 21.75, "Dining", "Credit Card"),
    ]
    # Example period 2 expenses
    period2 = [
        Expense("2024-06-10", "Groceries - Supermart", 54.90, "Groceries", "Checking"),
        Expense("2024-06-11", "Dinner Takeout", 28.40, "Dining", "Credit Card"),
        Expense("2024-06-12", "Monthly Rent", 1200.00, "Housing", "Checking"),
        Expense("2024-06-12", "Streaming Sub", 12.99, "Entertainment", None),
        Expense("2024-06-13", "Electricity bill", 62.10, "Utilities", "Checking"),
        Expense("2024-06-14", "Gasoline", 40.25, "Transport", "Credit Card"),
        Expense("2024-06-14", "Coffee", 4.00, "Dining", "Credit Card"),
    ]

    comparison = compare_periods(period1, period2)

    print_comparison_report(
        comparison, period1_name="May 2024", period2_name="June 2024"
    )


if __name__ == '__main__':
    main()