# Project Structure

```
ai_expense_comparator/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── migrations/
│   │   │   └── ...
│   ├── expenses/
│   │   ├── __init__.py
│   │   ├── manager.py
│   │   ├── import_csv.py
│   │   ├── recurring.py
│   ├── categories/
│   │   ├── __init__.py
│   │   ├── manager.py
│   │   ├── mapping.py
│   ├── accounts/
│   │   ├── __init__.py
│   │   ├── manager.py
│   ├── insights/
│   │   ├── __init__.py
│   │   ├── analysis.py
│   ├── comparison/
│   │   ├── __init__.py
│   │   ├── engine.py
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── charts.py
│   │   ├── cli_ascii.py
│   ├── imports/
│   │   ├── __init__.py
│   │   ├── logger.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── interface.py
│   ├── orchestrator.py
├── tests/
│   ├── __init__.py
│   ├── test_expenses.py
│   ├── test_categories.py
│   ├── test_accounts.py
│   ├── test_insights.py
│   ├── test_comparison.py
│   ├── test_visualization.py
│   ├── test_imports.py
│   ├── test_api.py
│   ├── test_cli.py
├── scripts/
│   ├── run_api.py
│   ├── run_cli.py
│   ├── init_db.py
├── requirements.txt
├── README.md
├── .env
└── pyproject.toml
```

---

## File Descriptions

### app/config.py  
Application configuration settings, including database and feature flags.

### app/db/models.py  
Defines ORM models for Expense, Category, Account, MappingRule, RecurringPattern, and ImportLog.

### app/db/migrations/  
Database schema migration scripts.

### app/expenses/manager.py  
Handles CRUD operations and business logic for expenses.

### app/expenses/import_csv.py  
Parses and imports expenses from CSV files, applying mapping rules as needed.

### app/expenses/recurring.py  
Detects and manages recurring expense patterns.

### app/categories/manager.py  
Manages category CRUD operations and category hierarchy.

### app/categories/mapping.py  
Implements category mapping rules and auto-categorization logic.

### app/accounts/manager.py  
Handles CRUD operations and logic for expense accounts.

### app/insights/analysis.py  
Generates spending insights, trend detection, anomaly discovery, and recommendations.

### app/comparison/engine.py  
Computes expense comparisons across different time periods and user-selected date ranges.

### app/visualization/charts.py  
Generates graphical charts (e.g., PNG, SVG) using visualization libraries.

### app/visualization/cli_ascii.py  
Renders text-based and ASCII-art charts for CLI output.

### app/imports/logger.py  
Logs import activities, errors, and summaries for reporting and audit.

### app/api/routes.py  
Implements RESTful API endpoints for all core functionality.

### app/cli/interface.py  
CLI entry point parsing commands, rendering outputs, and routing to core logic.

### app/orchestrator.py  
Coordinates module interactions, workflows, and session/context management.

### tests/test_expenses.py  
Unit and integration tests for expense CRUD, imports, and recurring logic.

### tests/test_categories.py  
Tests for category CRUD and mapping rule logic.

### tests/test_accounts.py  
Tests for account management operations.

### tests/test_insights.py  
Tests for insight generation and trend detection.

### tests/test_comparison.py  
Tests for period comparisons and statistics calculations.

### tests/test_visualization.py  
Tests for chart creation and CLI visual outputs.

### tests/test_imports.py  
Tests for import logging, error handling, and summaries.

### tests/test_api.py  
API endpoint tests covering all supported operations.

### tests/test_cli.py  
CLI command and output tests.

### scripts/run_api.py  
Script to launch REST API server.

### scripts/run_cli.py  
Script to start the interactive CLI application.

### scripts/init_db.py  
Database initialization and migration runner script.

### requirements.txt  
Specifies Python dependencies for the project.

### README.md  
Project overview and instructions for setting up and running the application.

### .env  
Environment variables for configuration.

### pyproject.toml  
Project metadata and build requirements.