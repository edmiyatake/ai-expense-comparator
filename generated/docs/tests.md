## 1. Test Strategy Overview

The Expense Comparator test suite adopts a layered strategy:

- **Unit Tests**: Exercise isolated logic for CRUD, category/account management, import/parsing, recurring pattern detection, aggregation/comparison, visualization data prep, and insights.
- **Integration Tests**: Cover flows spanning CSV import through category mapping, analysis, and visualization generation.
- **Edge/Negative Tests**: Extensive checks for malformed input, duplicate/ambiguous mappings, range overlaps, empty/missing data, invalid state transitions.
- **Use of Fixtures/Mocks**: Simulate realistic data sets, CSV inputs, and DB behavior.
- **Continuous Coverage**: Ensure ≥ 80% coverage across business logic, utility modules, and error handling.

---

## 2. Unit Test Skeletons (by module)

### tests/test_expenses.py

```python
def test_create_expense_valid():
    """Test adding a valid expense with all required fields."""
    # TODO: assert new expense is persisted with correct data

def test_create_expense_missing_fields():
    """Test creation fails if required fields are missing."""
    # TODO

def test_edit_expense_valid():
    """Test editing a single field of an expense."""
    # TODO

def test_edit_expense_invalid_id():
    """Test editing with a non-existent expense ID fails gracefully."""
    # TODO

def test_delete_expense_existing():
    """Test deleting an existing expense removes it from DB."""
    # TODO

def test_delete_expense_nonexistent():
    """Test deleting a non-existent expense is handled cleanly."""
    # TODO

def test_list_expenses_filters():
    """Test filtered expense listing by category, account, date."""
    # TODO
```

### tests/test_categories.py

```python
def test_create_category_unique():
    """Test creating a new unique category."""
    # TODO

def test_create_category_duplicate():
    """Test creating a duplicate category name raises validation error."""
    # TODO

def test_edit_category_name():
    """Test successfully renaming a category."""
    # TODO

def test_map_category_alternate_name():
    """Test mapping an alternate name to a category."""
    # TODO

def test_merge_categories_success():
    """Test merging multiple categories into a single one."""
    # TODO

def test_merge_categories_invalid_target():
    """Test merging fails if target category does not exist."""
    # TODO

def test_list_categories():
    """Test fetching all categories returns accurate list."""
    # TODO
```

### tests/test_accounts.py

```python
def test_create_account():
    """Test successful creation of a new account."""
    # TODO

def test_edit_account_name():
    """Test editing an existing account's name."""
    # TODO

def test_list_accounts():
    """Test listing all accounts."""
    # TODO
```

### tests/test_import.py

```python
def test_import_csv_valid():
    """Test importing a valid CSV creates correct expenses and import log."""
    # TODO

def test_import_csv_missing_columns():
    """Test importing CSV with missing columns is flagged appropriately."""
    # TODO

def test_import_csv_unmapped_categories():
    """Test that unmapped categories during import are detected and can be resolved."""
    # TODO

def test_import_csv_duplicates():
    """Test duplicate expense entries in CSV are handled (deduped or flagged)."""
    # TODO

def test_get_import_log():
    """Test retrieving import log after CSV import."""
    # TODO

def test_list_import_logs_all():
    """Test listing of multiple import logs."""
    # TODO
```

### tests/test_recurring.py

```python
def test_detect_patterns_basic_monthly():
    """Test recurring pattern detection for clear monthly repeated expenses."""
    # TODO

def test_detect_patterns_edge_cases():
    """Test recurring detection on noisy or sporadic data."""
    # TODO

def test_confirm_pattern():
    """Test marking a pattern as confirmed by user."""
    # TODO

def test_list_recurring_patterns():
    """Test retrieving all current recurring expense patterns."""
    # TODO
```

### tests/test_comparison.py

```python
def test_aggregate_expenses_by_category():
    """Test expense aggregation by category within a date range."""
    # TODO

def test_aggregate_expenses_by_account():
    """Test aggregation grouping by account."""
    # TODO

def test_compare_expenses_two_ranges():
    """Test comparison between two non-overlapping date ranges."""
    # TODO

def test_compare_expenses_overlapping_ranges():
    """Test comparison logic with overlapping date ranges."""
    # TODO
```

### tests/test_visualization.py

```python
def test_render_pie_chart_ascii():
    """Test ASCII pie chart rendering produces expected output."""
    # TODO

def test_render_line_chart_ascii():
    """Test ASCII line chart generation for time-series data."""
    # TODO

def test_render_bar_chart_ascii():
    """Test bar chart rendering for comparison data."""
    # TODO

def test_render_chart_json_output():
    """Test JSON output format for any supported chart type."""
    # TODO

def test_get_chart_data_format():
    """Test output data dict for chart rendering is normalized."""
    # TODO
```

### tests/test_insights.py

```python
def test_generate_insights_trend():
    """Test insight generation for a clear spending trend."""
    # TODO

def test_generate_insights_anomaly():
    """Test detection of an anomaly in expenses."""
    # TODO

def test_generate_insights_suggestion():
    """Test suggestion insights are generated based on rules."""
    # TODO

def test_list_insights_since():
    """Test retrieving all insights generated since a particular date."""
    # TODO
```

### tests/test_cli_flow.py

```python
def test_end_to_end_csv_import_to_insights(monkeypatch):
    """Simulate full flow: CSV import → category mapping → analysis → insights & chart output."""
    # TODO

def test_cli_add_edit_delete_expense(monkeypatch):
    """Test CLI commands for adding, editing, and deleting an expense."""
    # TODO

def test_cli_compare_spending(monkeypatch):
    """Test CLI user input and output for compare-spending command."""
    # TODO

def test_cli_visualization_render(monkeypatch):
    """Test CLI chart visualization renders correctly in ASCII."""
    # TODO
```

---

## 3. Edge Cases and Negative Tests

```python
def test_create_expense_zero_amount():
    """Test creation of an expense with a zero amount is allowed or handled as defined."""
    # TODO

def test_create_expense_negative_amount():
    """Test negative expense amount (e.g., refund) is handled as allowed or flagged."""
    # TODO

def test_import_csv_empty_file():
    """Test importing an empty CSV file does not create expenses/logs and returns a clear message."""
    # TODO

def test_category_merge_with_self():
    """Test merging a category into itself is rejected."""
    # TODO

def test_edit_account_nonexistent():
    """Test editing a nonexistent account ID raises an error."""
    # TODO

def test_compare_expenses_empty_ranges():
    """Test comparison when one or both ranges are empty returns zeros/graceful result."""
    # TODO

def test_visualization_missing_data():
    """Test chart rendering when input analysis data is empty or missing fields."""
    # TODO

def test_recurring_pattern_partial_match_only():
    """Test detection ignores near-matches below frequency threshold."""
    # TODO

def test_generate_insights_nonsensical_data():
    """Test insight generation with outlier/invalid input is safe."""
    # TODO

def test_cli_invalid_command(monkeypatch):
    """Test CLI gracefully handles an unknown/unsupported command."""
    # TODO
```

---

## 4. Test Data Suggestions

- **Expense Records**:  
    - Valid/invalid combinations: proper dates, missing fields, duplicate descriptions, zero/negative amounts.
    - Multiple expenses with same description/different dates (for recurring detection).
    - Expenses spread across multiple categories, accounts, time ranges.
    - Edge dates: leap year, month end/start, time zone variants (if supported).

- **CSV Samples**:  
    - Correctly formatted CSVs (all columns present).  
    - CSVs with missing/extra/unexpected columns.  
    - CSVs containing unmapped/new categories, messy/ambiguous headers.  
    - CSVs with duplicate transactions and invalid/malformed rows.  
    - Empty CSV files.

- **Category/Account Lists**:  
    - Categories with mapped alternative names.
    - Categories with similar/overlapping names (for mapping/merge tests).
    - Accounts with similar names to check conflict/resolution.

- **Date Ranges**:  
    - Overlapping and non-overlapping ranges.
    - Ranges with no expenses, all expenses, and partial coverage.

- **Visualization Data Sets**:  
    - Sufficient to generate meaningful pie/line/bar charts (multiple categories/accounts over several months).
    - Empty or sparsely populated datasets for edge-case handling.

- **Recurring Patterns**:  
    - Expenses representing typical subscriptions (monthly, yearly).
    - Expenses that almost, but not quite, form a recurring pattern.

- **Anomalies**:  
    - Outlier expense amounts or sudden spikes to test insight and anomaly reporting.

- **CLI/Input Simulations**:  
    - Command sequences that follow valid workflows, as well as intentional misuse (bad arguments, invalid flows).

All test data should be versioned and, where possible, reusable across tests for consistency and regression.