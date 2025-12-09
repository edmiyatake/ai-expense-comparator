## Project Structure

```
ai_expense_comparator/
├── agents/
│   ├── expense_agent.py
│   ├── category_agent.py
│   ├── import_agent.py
│   ├── recurring_detector_agent.py
│   ├── comparison_agent.py
│   ├── visualization_agent.py
│   └── insight_agent.py
├── orchestrator.py
├── domain/
│   └── models.py
├── storage/
│   └── database.py
├── api/
│   └── cli.py
├── tests/
│   ├── test_expense_agent.py
│   ├── test_category_agent.py
│   ├── test_import_agent.py
│   ├── test_recurring_detector_agent.py
│   ├── test_comparison_agent.py
│   ├── test_visualization_agent.py
│   ├── test_insight_agent.py
│   └── test_end_to_end.py
└── requirements.txt
```

### File-level Descriptions

- **agents/expense_agent.py** – Handles creation, update, deletion, validation, and retrieval of expense records.
- **agents/category_agent.py** – Manages categories, including rule-based and manual mapping of expenses to categories.
- **agents/import_agent.py** – Processes CSV imports, parses files, invokes expense creation, and logs import activities and errors.
- **agents/recurring_detector_agent.py** – Detects and manages recurring expense patterns based on historical expense data.
- **agents/comparison_agent.py** – Provides comparison and aggregation logic for expenses over selected date ranges or periods.
- **agents/visualization_agent.py** – Generates visual reports (category breakdowns, time trends, comparisons) suitable for CLI/API output.
- **agents/insight_agent.py** – Extracts insights, spending trends, anomalies, and recommendations from expense data.

- **orchestrator.py** – Central controller routing CLI/API commands and managing workflow across all agents with integrated error handling.

- **domain/models.py** – Defines data models/entities: Expense, Category, RecurringPattern, ImportLog (and optional User).

- **storage/database.py** – Provides persistent storage access, ORM/database setup, and schema management for all domain entities.

- **api/cli.py** – Command-line interface handling user interaction, parsing input, and invoking orchestrator actions.

- **tests/test_expense_agent.py** – Unit tests for expense CRUD logic, validation, and edge cases.
- **tests/test_category_agent.py** – Unit tests for category management and mapping logic.
- **tests/test_import_agent.py** – Unit and integration tests for CSV import process and logging.
- **tests/test_recurring_detector_agent.py** – Tests for recurring expense detection algorithms and pattern recognition.
- **tests/test_comparison_agent.py** – Tests for period/range comparison and aggregation logic.
- **tests/test_visualization_agent.py** – Tests for rendering and output of visualizations (charts, tables).
- **tests/test_insight_agent.py** – Tests for insight generation, anomaly detection, and trend reporting.
- **tests/test_end_to_end.py** – Integration and end-to-end scenario tests covering import, processing, reports, and insights.

- **requirements.txt** – Lists required Python libraries for all components.