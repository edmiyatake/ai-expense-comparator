1. Project Structure (tree layout rooted at src/)
```
src/
├── models/
│   ├── user.py
│   ├── account.py
│   ├── category.py
│   ├── expense.py
│   ├── recurring_pattern.py
│   ├── import_log.py
│   └── insight.py
├── db/
│   ├── orm.py
│   └── session.py
├── agents/
│   ├── expenses.py
│   ├── categories.py
│   ├── accounts.py
│   ├── import_agent.py
│   ├── recurring.py
│   ├── comparison.py
│   ├── insights.py
│   ├── visualization.py
│   └── orchestrator.py
├── visualization/
│   ├── chart_ascii.py
│   └── chart_json.py
├── cli/
│   ├── commands.py
│   └── io_utils.py
├── tests/
│   ├── test_expenses.py
│   ├── test_categories.py
│   ├── test_accounts.py
│   ├── test_import.py
│   ├── test_recurring.py
│   ├── test_comparison.py
│   ├── test_visualization.py
│   ├── test_insights.py
│   └── test_cli_flow.py
```

---

2. Modules and Responsibilities

- `models/`: Defines ORM models (User, Account, Category, Expense, RecurringPattern, ImportLog, Insight) mapping directly to domain/entities.
- `db/`: Database setup, session management, and ORM helpers for persistence, querying, and migrations.
- `agents/`: Encapsulate business/domain logic for expenses, categories, accounts, CSV import, recurring detection, comparison/aggregation, insights, visualization, and overall orchestration.
- `visualization/`: Utilities for transforming analytic results into ASCII charts (CLI) and JSON structures (API).
- `cli/`: Command-line interface logic, input/output parsing, user-driven flows, and pretty-printing utilities.
- `tests/`: Unit, integration, and regression test cases for agents, models, CLI flows, and edge cases.

---

3. Core Classes and Functions

##### models/user.py
```python
class User(Base):
    id: int
    username: str
    # For future multi-user support
```

##### models/account.py
```python
class Account(Base):
    id: int
    name: str
    user_id: int | None
```

##### models/category.py
```python
class Category(Base):
    id: int
    name: str
    mapped_names: list[str]
```

##### models/expense.py
```python
class Expense(Base):
    id: int
    date: date
    description: str
    amount: float
    category_id: int
    account_id: int
    imported: bool
    import_id: int | None
```

##### models/recurring_pattern.py
```python
class RecurringPattern(Base):
    id: int
    description: str
    frequency: str
    matched_expense_ids: list[int]
```

##### models/import_log.py
```python
class ImportLog(Base):
    id: int
    filename: str
    imported_at: datetime
    expense_ids: list[int]
```

##### models/insight.py
```python
class Insight(Base):
    id: int
    date_generated: datetime
    description: str
    insight_type: str
```

##### db/orm.py
```python
def init_db(connection_string: str) -> None:
    """Initialize database schema and tables."""
def get_session() -> Session:
    """Return a new ORM DB session."""
```

##### db/session.py
```python
Session = sessionmaker(...)
```

##### agents/expenses.py
```python
class ExpenseAgent:
    def create_expense(self, data: dict) -> Expense:
        """Create and persist an expense."""
    def edit_expense(self, expense_id: int, updates: dict) -> Expense:
        """Edit an existing expense by ID."""
    def delete_expense(self, expense_id: int) -> None:
        """Remove an expense from the database."""
    def list_expenses(self, filters: dict = None) -> list[Expense]:
        """List expenses with optional filters (date, category, etc)."""
```

##### agents/categories.py
```python
class CategoryAgent:
    def create_category(self, name: str) -> Category:
        """Add a new category."""
    def edit_category(self, category_id: int, updates: dict) -> Category:
        """Edit the name or mappings of a category."""
    def merge_categories(self, source_ids: list[int], target_id: int) -> None:
        """Combine multiple categories into one."""
    def map_category(self, name: str, to_category_id: int) -> None:
        """Map an alternative name to a category."""
    def list_categories(self) -> list[Category]:
        """List all categories."""
```

##### agents/accounts.py
```python
class AccountAgent:
    def create_account(self, name: str) -> Account:
        """Create a new account."""
    def edit_account(self, account_id: int, updates: dict) -> Account:
        """Edit an account (name, etc)."""
    def list_accounts(self) -> list[Account]:
        """List all user accounts."""
```

##### agents/import_agent.py
```python
class ImportAgent:
    def import_csv(self, file_path: str) -> ImportLog:
        """Parse and import expenses from a CSV; log import."""
    def get_import_log(self, import_id: int) -> ImportLog:
        """Retrieve import log details."""
    def list_import_logs(self) -> list[ImportLog]:
        """List all import logs."""
    def resolve_unmapped_categories(self, import_id: int) -> None:
        """Interactively map any new/unmapped categories found in import."""
```

##### agents/recurring.py
```python
class RecurringAgent:
    def detect_patterns(self) -> list[RecurringPattern]:
        """Identify recurring expenses using pattern matching."""
    def confirm_pattern(self, pattern_id: int) -> None:
        """User confirms a detected recurring pattern."""
    def list_recurring(self) -> list[RecurringPattern]:
        """List current recurring expense patterns."""
```

##### agents/comparison.py
```python
class ComparisonAgent:
    def compare_expenses(self, range1: tuple[date, date], range2: tuple[date, date], by: str='category') -> dict:
        """Compute spending aggregates (by category/account etc) for two time ranges."""
    def aggregate_expenses(self, date_range: tuple[date, date], group_by: str='category') -> dict:
        """Aggregate expenses for a date range, grouped by the specified field."""
```

##### agents/insights.py
```python
class InsightAgent:
    def generate_insights(self, date_range: tuple[date, date]) -> list[Insight]:
        """Produce insights (trends, anomalies, suggestions) for given period."""
    def list_insights(self, since: datetime = None) -> list[Insight]:
        """Fetch generated insights since a date."""
```

##### agents/visualization.py
```python
class VisualizationAgent:
    def render_chart(self, chart_type: str, data: dict, mode: str = 'ascii') -> str | dict:
        """Render a chart as ASCII (for CLI) or as JSON (for API) using raw data."""
    def get_chart_data(self, analysis_result: dict, chart_type: str) -> dict:
        """Produce a data dictionary ready for chart rendering."""
```

##### agents/orchestrator.py
```python
class Orchestrator:
    def handle_command(self, command: str, args: dict) -> None:
        """Route user commands to appropriate agents and coordinate flow."""
```

##### visualization/chart_ascii.py
```python
def pie_chart(data: dict) -> str:
    """Render a pie chart in ASCII for CLI output."""
def line_chart(data: dict) -> str:
    """Render a line chart in ASCII."""
def bar_chart(data: dict) -> str:
    """Render a bar chart in ASCII."""
```

##### visualization/chart_json.py
```python
def chart_json(data: dict, chart_type: str) -> dict:
    """Format chart data as a JSON-serializable object."""
```

##### cli/commands.py
```python
def main():
    """Entrypoint for CLI: parses input and invokes orchestrator."""
def add_expense(args): ...
def list_expenses(args): ...
def import_csv(args): ...
# Etc, for each command
```

##### cli/io_utils.py
```python
def print_table(data: list[dict], columns: list[str]) -> None:
    """Print tabular data prettily in the CLI."""
def prompt_user(prompt: str) -> str:
    """Prompt user for input (CLI)."""
```

##### tests/test_expenses.py
```python
def test_create_expense_valid():
    """Test adding a valid expense."""
def test_create_expense_invalid():
    """Test input validation for expense creation."""
def test_edit_expense():
    """Test editing expense fields."""
```

# ... Similar structure for all test files (CRUD, validation, flows, edge cases) ...

---

4. TODOs and Open Questions

- Confirm if multi-user support is needed in MVP; if so, expand User model, authentication, and context management.
- Specify exact CSV field mapping/normalization rules; handle ambiguous column headers or missing fields.
- Decide visualization details for complex comparisons (multiple ranges, hybrid groupings).
- Define comprehensive rules for recurring expense detection (minimum frequency, description similarity, etc.).
- Determine config process for new/unmapped categories during import (interactive, deferred, auto?).
- Finalize requirements for insight heuristics and outputs (breadth, depth, prioritization of suggestions).
- Outline error handling, logging, and user feedback/error reporting mechanisms.
- Plan for future extensibility: localization, multi-currency, more sophisticated analytics.
- Settle on exact CLI command names/options and argument handling conventions.
- Selection of CLI frameworks (argparse/click/typer) and ORM/backend tech (SQLAlchemy baseline).
- Address backup and data migration—out of scope for MVP but important for future versions.