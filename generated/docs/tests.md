# 1. Test Strategy Overview

The testing approach for the Expense Comparator is modular and layered:

- **Unit Tests**: Cover each agent/module in isolation by mocking dependencies. Focus on correctness, error handling, validation, and edge conditions at the function/class level.
- **Integration Tests**: Assemble components to test real-world data flows, ensuring modules interact as expected (e.g., importing and categorizing expenses).
- **CLI/API Tests**: Validate end-user operations through CLI commands and REST API endpoints, including input/output, error responses, and report generation.
- **Performance & Scalability**: (Not detailed here) Stress major flows such as large imports and recurring detection.
- **Test Data**: Mix representative, edge, and negative samples for validation and analytics use cases.

# 2. Unit Test Skeletons (by module)

## tests/test_expenses.py

```python
# Expense Manager
def test_add_expense_valid():
    """Adding a valid expense should store it with correct fields."""
    # TODO: Create expense and check DB state

def test_edit_expense_updates_fields():
    """Editing an expense updates selected fields only."""
    # TODO: Edit one field, verify before/after

def test_delete_expense_removes_record():
    """Deleting an expense should remove it from storage."""
    # TODO: Add + delete, assert missing

def test_list_expenses_with_pagination():
    """Listing expenses supports pagination and sorting."""
    # TODO: Create many, fetch slices, check order

# CSV Import
def test_import_csv_valid():
    """Importing a valid CSV maps all fields to expenses as expected."""
    # TODO: Parse CSV, mock mapping, assert correct rows

def test_import_csv_applies_category_mapping():
    """Category mapping rules apply during CSV import."""
    # TODO: Import with mapping rules, check categories assigned

# Recurring
def test_detect_recurring_expenses_identifies_patterns():
    """RecurringDetector identifies matching recurring patterns."""
    # TODO: Add recurring-like expenses, detect recurrence

def test_update_recurring_pattern_on_new_expense():
    """Recurring patterns are updated as new recurring expenses appear."""
    # TODO: Add more of a detected series, verify pattern updated
```

## tests/test_categories.py

```python
def test_add_category_creates_new():
    """Adding a new category is reflected in storage."""
    # TODO: Add and verify

def test_edit_category_updates_name():
    """Editing a category changes its name (and optionally its parent)."""
    # TODO: Edit and verify

def test_delete_category_unassigns_expenses():
    """Deleting a category unassigns or reassigns affected expenses."""
    # TODO: Delete with dependencies, verify

def test_apply_category_mapping_rule_to_description():
    """Mapping rule correctly matches and categorizes expenses."""
    # TODO: Rule (e.g., regex) applied to expense description

def test_category_hierarchy_allows_grouping():
    """Categories can be grouped in a hierarchy."""
    # TODO: Create parent/child, assert hierarchy
```

## tests/test_accounts.py

```python
def test_create_account_persists_data():
    """Account creation stores name and metadata."""
    # TODO: Create and fetch

def test_update_account_changes_fields():
    """Account fields (name/etc) can be edited."""
    # TODO: Edit and verify

def test_delete_account_removes_expenses_or_reassigns():
    """Account deletion handles dependent expenses as specified."""
    # TODO: Delete; check orphaned/reassigned expenses
```

## tests/test_insights.py

```python
def test_generate_spending_trends_insight():
    """Insight engine produces spending trend analytics."""
    # TODO: Add time-ordered data, check trends

def test_detect_anomalies_outlier_expenses():
    """Anomaly detection flags large/unusual expenses."""
    # TODO: Add outliers, check detection

def test_generate_recommendations_for_saving():
    """Recommendations for improvement are generated based on expense patterns."""
    # TODO: Simulate overspending, check suggestions
```

## tests/test_comparison.py

```python
def test_compare_periods_summarizes_key_stats():
    """Comparison across periods yields correct totals and category splits."""
    # TODO: Compare two sample periods

def test_compare_custom_date_ranges():
    """Custom date ranges can be selected and compared."""
    # TODO: Use arbitrary user dates

def test_compare_handling_of_empty_periods():
    """Empty or non-overlapping periods are handled gracefully."""
    # TODO: Compare to period with no data
```

## tests/test_visualization.py

```python
def test_generate_category_breakdown_chart_data():
    """Category breakdown chart data is correct for provided expenses."""
    # TODO: Mock data and generate breakdown

def test_generate_time_series_trend_chart_data():
    """Time-series trend data reflects expenses over time."""
    # TODO: Add regular/irregular data, generate chart input

def test_generate_comparison_chart_between_ranges():
    """Comparison chart data accurately represents multi-range differences."""
    # TODO: Use two sets, check chart prep

def test_cli_ascii_chart_renders_expected_output():
    """CLI chart renderer outputs readable ASCII representation."""
    # TODO: Feed data, check output contains expected bars/labels
```

## tests/test_imports.py

```python
def test_log_import_success_entry():
    """ImportLogger logs successful import with summary."""
    # TODO: Simulate success import, check log stored

def test_log_import_error_handling():
    """ImportLogger stores errors and details for failed import."""
    # TODO: Trigger error, verify error log contents

def test_view_import_logs_paginates_results():
    """Viewing import logs supports pagination and filtering."""
    # TODO: Add logs, fetch pages
```

## tests/test_api.py

```python
def test_api_add_expense_endpoint():
    """POST /expenses adds a new expense via API."""
    # TODO: Call endpoint, check DB

def test_api_import_csv_endpoint():
    """POST /expenses/import-csv processes file and returns summary."""
    # TODO: Upload CSV, check response

def test_api_compare_periods_endpoint():
    """GET /comparison returns correct stats for requested ranges."""
    # TODO: Call, check stats JSON

def test_api_visualization_chart_endpoint():
    """GET /visualizations returns expected chart content or links."""
    # TODO: Call, check image/ASCII content

def test_api_filter_expenses_by_category_and_date():
    """GET /expenses supports filtering by category and date."""
    # TODO: Call with params, check response slice

def test_api_error_response_on_malformed_input():
    """API returns clear error for malformed requests."""
    # TODO: POST invalid data, check error

def test_api_export_json_csv_formats():
    """API export supports both JSON and CSV outputs."""
    # TODO: Request export, check format
```

## tests/test_cli.py

```python
def test_cli_add_expense_interactive_flow():
    """CLI adds expense through user prompts."""
    # TODO: Simulate prompts, verify result

def test_cli_import_csv_command():
    """CLI import-csv command processes a sample file."""
    # TODO: Invoke with file, verify summary

def test_cli_show_comparison_outputs_textual_report():
    """CLI comparison command outputs readable textual summary."""
    # TODO: Run, capture output

def test_cli_show_ascii_chart_displays_histogram():
    """CLI chart command prints ASCII-art chart in terminal."""
    # TODO: Invoke, assert on output bars

def test_cli_error_on_invalid_command_args():
    """CLI returns error/help on invalid input."""
    # TODO: Run with wrong args, check output
```

# 3. Edge Cases and Negative Tests

- Add expense with missing/invalid fields (e.g., negative amount, missing category).
- Import CSV with malformed content, incorrect columns, or encoding issues.
- Category mapping rule that matches no expenses, or ambiguous mapping.
- Detecting recurring expenses with irregular frequency, small variations in amounts or dates.
- Deleting categories/accounts in use by existing expenses.
- Visualization with no data, all data zero, or a single data point.
- Comparison across non-overlapping, empty, or identical periods.
- Insights where all expenses are constant (no trend/anomaly).
- API requests with invalid JSON or missing required params.
- CLI executed in non-interactive mode (stdin closed).
- Bulk operations (large CSVs, rapid API calls) for resource handling.

# 4. Test Data Suggestions

- Expenses: a mix of dates (current, past, future), amounts (positive, zero, negative), diverse descriptions, categories, and accounts.
- CSV samples: valid/complete; missing/extra columns; invalid dates or numbers; duplicate rows.
- Categories: simple flat set; hierarchies; names differing only by case.
- Category mapping: regex that matches multiple/non-overlapping descriptions; overlapping rules.
- Recurring expenses: regular patterns (same day, amount); "fuzzy" recurrences (±1 day, ≈amount); single occurrences.
- Comparison: two periods with overlapping categories; one with no data; periods of widely different lengths.
- Visualization: datasets with 0, 1, N categories; outlier expenses; dense and sparse time ranges.
- Import logs: success and failure entries, different timestamps, filenames, and error messages.
- API/CLI: valid and invalid payloads/inputs; batch and edge-case requests (e.g., filter outside data range).

This test plan and skeletons ensure comprehensive coverage of functional paths, validations, error handling, and user-visible behavior for the Expense Comparator.