# 1. Project Structure (tree layout rooted at src/)

```
src/
├── cli/
│   └── commands.py
├── api/
│   ├── server.py
│   └── routes.py
├── core/
│   ├── import_csv.py
│   ├── normalization.py
│   ├── recurring.py
│   ├── comparison.py
│   └── insights.py
├── models/
│   ├── domain.py
│   └── storage.py
├── persistence/
│   ├── database.py
│   ├── repositories.py
│   └── archive.py
├── orchestration/
│   └── workflow.py
├── visualization/
│   └── reporting.py
├── tests/
│   └── (unit and integration tests)
└── utils/
    └── helpers.py
```

# 2. Modules and Responsibilities

- **cli/commands.py**  
  Defines CLI commands for importing CSVs, normalization, recurring detection, comparison, and report retrieval.

- **api/server.py, api/routes.py**  
  REST API setup, endpoint definitions (upload, view transactions, recurring groups, compare, reports).

- **core/import_csv.py**  
  Parses/imports various bank CSV formats to `BankTransaction` objects, resolves schema differences.

- **core/normalization.py**  
  Handles category normalization (raw → standard); supports rule, mapping, and ML-based approaches plus user overrides.

- **core/recurring.py**  
  Detects recurring transaction groups according to defined similarity and periodicity rules.

- **core/comparison.py**  
  Calculates per-category/per-bank/period expense summaries and differences.

- **core/insights.py**  
  Generates summaries, anomalies, suggestions, and improvement hints from comparisons.

- **models/domain.py**  
  Defines core data models: BankTransaction, NormalizedTransaction, RecurringExpenseGroup, ComparisonReport.

- **models/storage.py**  
  Defines database (ORM) schemas; data model entities for persistence.

- **persistence/database.py**  
  Database config/init, ORM setup for SQLite/PostgreSQL.

- **persistence/repositories.py**  
  Data access layer: CRUD for transactions, normalization mappings, recurring groups, and reports.

- **persistence/archive.py**  
  Archives and retrieves raw uploaded CSVs, linked to user and bank.

- **orchestration/workflow.py**  
  End-to-end pipeline; coordinates agents for import, normalization, recurring detection, comparison, and reporting.

- **visualization/reporting.py**  
  Text and chart/graph generation (e.g., using matplotlib); formats reporting output.

- **utils/helpers.py**  
  Shared helpers/utilities: date parsing, deduplication, error handling, etc.

- **tests/**  
  Unit and integration tests for all core, persistence, and API/CLI functions.

# 3. Core Classes and Functions

**models/domain.py**
```python
class BankTransaction:
    """Represents a raw transaction imported from a bank CSV."""
    def __init__(self, date, amount, description, raw_category, bank, account_id, transaction_id): ...

class NormalizedTransaction:
    """Standardized transaction, with normalized category and (optional) recurring group info."""
    def __init__(self, date, amount, description, normalized_category, source_bank, original_raw_category, recurring_id=None): ...

class RecurringExpenseGroup:
    """Group of recurring transactions (by pattern, similarity, periodicity)."""
    def __init__(self, group_id, normalized_category, avg_amount, frequency, transactions, banks): ...

class ComparisonReport:
    """Report containing summarized and compared expense data (per category, period, bank, etc.)."""
    def __init__(self, categories, period_range, data_by_bank, recurring_details, insights): ...
```

**core/import_csv.py**
```python
def import_csv(path: str, bank_name: str) -> list[BankTransaction]:
    """Parse and map a bank's CSV file to a list of BankTransaction objects."""
```

**core/normalization.py**
```python
def normalize_transactions(transactions: list[BankTransaction], user_id: str) -> list[NormalizedTransaction]:
    """Normalize raw transaction categories using standard mappings and user overrides."""
```

**core/recurring.py**
```python
def detect_recurring_transactions(transactions: list[NormalizedTransaction]) -> list[RecurringExpenseGroup]:
    """Detect groups of recurring expenses based on pattern and frequency."""
```

**core/comparison.py**
```python
def compare_expenses(normalized_transactions: list[NormalizedTransaction], date_range=None) -> ComparisonReport:
    """Aggregate and compare expenses by category, time period, and bank."""
```

**core/insights.py**
```python
def generate_insights(report: ComparisonReport) -> list[str]:
    """Generate actionable and explanatory text summaries from report data."""
```

**persistence/database.py**
```python
def init_db(connection_string: str):
    """Initialize and configure the database."""
```

**persistence/repositories.py**
```python
class TransactionRepository:
    def add_transactions(self, transactions: list[BankTransaction|NormalizedTransaction]): ...
    def get_transactions(self, user_id: str, filters: dict = None) -> list[NormalizedTransaction]: ...
    # Other CRUD operations as needed

class RecurringGroupRepository:
    def save_groups(self, groups: list[RecurringExpenseGroup]): ...
    def get_groups(self, user_id: str) -> list[RecurringExpenseGroup]: ...

class ReportRepository:
    def save_report(self, report: ComparisonReport, user_id: str): ...
    def get_report(self, report_id: str) -> ComparisonReport: ...
```

**persistence/archive.py**
```python
def archive_csv(file_path: str, user_id: str, bank_name: str, original_filename: str):
    """Archive uploaded CSV for traceability."""
```

**orchestration/workflow.py**
```python
class Orchestrator:
    """Runs the end-to-end workflow for a user upload and analysis session."""
    def run(self, user_id: str, csv_path: str, bank_name: str, date_range = None):
        """Import -> normalize -> detect recurring -> compare -> report."""
```

**visualization/reporting.py**
```python
def generate_text_report(report: ComparisonReport) -> str:
    """Render report as a readable text summary."""

def generate_charts(report: ComparisonReport, output_dir: str) -> list[str]:
    """Generate chart images/paths for expense trends and breakdowns."""
```

**cli/commands.py**
```python
def import_csv_command(args): ...
def normalize_command(args): ...
def detect_recurring_command(args): ...
def compare_command(args): ...
def show_report_command(args): ...
```

**api/routes.py**
```python
# Route handler signatures
def post_import(request): ...
def get_transactions(request): ...
def get_recurring(request): ...
def get_compare(request): ...
def get_report(request): ...
```

# 4. TODOs and Open Questions

- Define a minimal, extensible bank-specific CSV parsing interface to accommodate new/variant formats efficiently.
- Specify precise normalization rules and mechanisms for category mapping (rule-based? ML fallback? hybrid?).
- Determine transaction deduplication logic—across multiple overlapping CSVs and banks.
- Design database schema and indexing for scalability (esp. user separation, normalized mappings, and group linkage).
- Choose visualization/charting library and report output format(s) (e.g., PNG, SVG, HTML fragments).
- Plan user-facing error and ambiguity handling, particularly for normalization and recurring group assignment.
- Set up user authentication/authorization model for CLI/API use and data isolation.
- Finalize approach to configuration (e.g., per-user category overrides, custom recurring rules).
- Decide storage and lifecycle policies for raw CSV archives (retention period, privacy requirements).
- Clarify if the application will launch with both CLI and API, and prioritize initial deliverable interfaces.
- Detail API versioning and input validation strategies.
- Plan comprehensive test data sets for unit and integration testing scenarios.