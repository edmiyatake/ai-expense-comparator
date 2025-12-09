# Test Strategy Overview

The primary focus of testing is to ensure that:
- CSV imports and normalization behave correctly for valid and invalid inputs.
- Transactions are categorized as expected based on configuration rules.
- Aggregation and comparison logic produce correct totals and deltas.
- Visualization/report generation functions consume ComparisonResult objects
  and produce stable, deterministic outputs for the same inputs.

We will use pytest-based unit tests for core modules and functions.

# Unit Test Skeletons (by module)

## tests/test_csv_io.py

```python
import pytest

from expense_comparator.csv_io import load_csv_files

def test_load_csv_files_valid_input():
    """Loading a well-formed CSV should return a list of Transaction-like objects."""
    # TODO: Arrange a sample CSV file or in-memory representation.
    # TODO: Call load_csv_files and assert length and basic fields.
    pass

def test_load_csv_files_missing_required_columns():
    """Missing required columns should result in a clear validation error."""
    # TODO: Prepare a CSV missing the 'amount' column.
    # TODO: Assert that an appropriate exception or error is raised.
    pass
```

## tests/test_normalization.py

```python
import pytest

from expense_comparator.normalization import normalize_transactions

def test_normalize_transactions_sign_and_date_handling():
    """Normalization should correctly handle debit/credit signs and date formats."""
    # TODO: Provide raw rows with different sign conventions and date formats.
    # TODO: Assert that normalized Transaction objects have correct amounts and dates.
    pass
```

## tests/test_categorization.py

```python
import pytest

from expense_comparator.categorization import categorize_transactions

def test_categorize_transactions_basic_rules():
    """Transactions should be categorized according to configured rules."""
    # TODO: Provide transactions and a simple category rule set.
    # TODO: Assert that each transaction has the expected normalized_category.
    pass
```

## tests/test_aggregation.py

```python
import pytest

from expense_comparator.aggregation import aggregate_expenses

def test_aggregate_expenses_by_category_and_window():
    """Aggregate totals per category and time window should match expected sums."""
    # TODO: Build a small set of transactions across categories and time windows.
    # TODO: Assert that aggregation results match manually computed totals.
    pass
```

## tests/test_comparison.py

```python
import pytest

from expense_comparator.comparison import compare_expenses

def test_compare_expenses_detects_increases_and_decreases():
    """ComparisonResult should correctly indicate increases/decreases per category."""
    # TODO: Construct aggregated data for two windows with known differences.
    # TODO: Assert that per_category_deltas and total_delta match expectations.
    pass
```

# Edge Cases and Negative Tests

1. CSV rows with invalid dates (e.g., malformed strings) should be rejected with clear errors.
2. CSV rows with non-numeric amounts should be rejected or skipped with explicit logging.
3. Empty datasets (no transactions) should not crash; comparisons should yield zero totals.
4. Single-window comparisons should gracefully indicate that there is nothing to compare.
5. Overlapping time windows should be tested to ensure they are handled or explicitly disallowed.

# Test Data Suggestions

1. Small synthetic CSVs (5–20 rows) for focused unit tests of parsing and normalization.
2. A moderate-sized dataset (hundreds of rows) to validate performance and stability.
3. Cases with multiple accounts and overlapping categories to test aggregation correctness.
4. Scenarios with significant changes in spending patterns to validate comparison logic.