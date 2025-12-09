# Project Structure

src/
  app/
    main.py                      # CLI entrypoint orchestrating Planner, Requirements, CodeGen
  expense_comparator/
    __init__.py
    models.py                    # Domain models: Transaction, ExpenseCategory, TimeWindow, ComparisonResult
    csv_io.py                    # Load and validate CSV files from different banks
    normalization.py             # Normalize bank-specific schemas into a common internal format
    categorization.py            # Categorize transactions into normalized categories
    time_windows.py              # Build and validate date ranges / time windows
    aggregation.py               # Aggregate expenses by category and time window
    comparison.py                # Compare aggregated expenses across time periods
    visualization.py             # Produce charts/graphs or text-based reports
  config/
    __init__.py
    settings.py                  # Global settings (paths, date formats, default categories)
  tests/
    test_csv_io.py
    test_normalization.py
    test_categorization.py
    test_time_windows.py
    test_aggregation.py
    test_comparison.py

# Modules and Responsibilities

- app.main
  - Parse CLI arguments (CSV file paths, date ranges, output options).
  - Coordinate the end-to-end pipeline:
    load → normalize → categorize → aggregate → compare → visualize.

- expense_comparator.models
  - Define core dataclasses:
    - Transaction
    - ExpenseCategory
    - TimeWindow
    - ComparisonResult
  - Provide helper methods for common conversions (e.g., from dict / CSV row).

- expense_comparator.csv_io
  - Functions to load CSV files from disk.
  - Handle bank-specific quirks (column names, date formats, decimal separators).
  - Validate required columns such as date, description, amount.

- expense_comparator.normalization
  - Convert raw CSV rows from different banks into normalized Transaction objects.
  - Apply basic cleaning for descriptions, signs (debit/credit), and currencies.

- expense_comparator.categorization
  - Assign each Transaction to an ExpenseCategory using rules or mappings.
  - Allow configuration of category rules in config.settings.

- expense_comparator.time_windows
  - Build TimeWindow objects for user-specified or default ranges.
  - Helpers for:
    - current month vs previous month
    - custom start/end dates
    - rolling windows (e.g., last 90 days)

- expense_comparator.aggregation
  - Aggregate Transactions by category and time window.
  - Compute totals, averages, and basic statistics needed for comparison.

- expense_comparator.comparison
  - Compare aggregated expenses across time windows.
  - Identify increases/decreases by category and overall spending trends.
  - Produce ComparisonResult objects summarizing differences.

- expense_comparator.visualization
  - Render ComparisonResult objects as:
    - text-based tables for CLI
    - optional charts/graphs (e.g., bar charts, line charts) if a plotting library is available.
  - Focus on clearly showing where spending has increased or decreased.

- config.settings
  - Central place for:
    - default categories
    - bank-specific CSV configurations
    - date format strings
    - any feature flags.

# Core Classes and Functions

- class Transaction:
  - Represents a single financial transaction.
  - Fields: date, description, amount, account_id, raw_category, normalized_category.

- class ExpenseCategory:
  - Represents a normalized category (e.g., GROCERIES, RENT, ENTERTAINMENT).
  - Fields: name, description, optional parent_category.

- class TimeWindow:
  - Represents a closed-open date interval [start, end).
  - Fields: start_date, end_date, label (e.g., "Jan 2025", "Last 90 days").

- class ComparisonResult:
  - Represents the result of comparing expenses across two or more TimeWindows.
  - Fields: window_a, window_b, per_category_deltas, total_delta, notes.

- function load_csv_files(paths: list[str]) -> list[Transaction]
  - Read and parse CSV files into Transaction objects.

- function normalize_transactions(raw_rows: list[dict]) -> list[Transaction]
  - Convert raw bank rows into normalized Transaction instances.

- function categorize_transactions(transactions: list[Transaction]) -> list[Transaction]
  - Apply category rules and return transactions with normalized_category set.

- function build_time_windows(config: dict, user_args: dict) -> list[TimeWindow]
  - Construct TimeWindow objects based on CLI flags or defaults.

- function aggregate_expenses(transactions: list[Transaction], windows: list[TimeWindow]) -> dict
  - Aggregate expenses by category and time window.

- function compare_expenses(aggregated: dict) -> list[ComparisonResult]
  - Compare aggregates between windows to find increases/decreases per category.

- function render_report(results: list[ComparisonResult]) -> str
  - Produce a human-readable summary of spending patterns and trends.

# TODOs and Open Questions

- Decide whether to support only CSV uploads or also manual input / API integration.
- Specify exact CSV schemas per bank (column names, locales, currencies).
- Clarify expected charting library (text-only, matplotlib, or another option).
- Determine performance requirements (max number of transactions and files per run).
- Decide how configuration (categories, rules, date ranges) will be persisted.