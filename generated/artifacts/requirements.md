# Functional Requirements

1. The system SHALL allow users to manually enter individual expenses, including date, description, amount, category, and account.
2. The system SHALL allow users to upload one or more CSV files containing expenses exported from banks or financial institutions.
3. The system SHALL parse uploaded CSV files and map columns into the internal expense model (date, description, amount, category, account).
4. The system SHALL allow users to define and edit expense categories (e.g., groceries, transportation, entertainment).
5. The system SHALL support assigning each expense to exactly one primary category.
6. The system SHALL allow users to select one or more time periods (e.g., specific months, custom date ranges) for comparison.
7. The system SHALL compute total spending per category for each selected time period.
8. The system SHALL compute differences in spending per category between time periods (absolute and percentage change where applicable).
9. The system SHALL provide a summary of overall spending trends across time periods (e.g., total increase/decrease, top increasing categories).
10. The system SHALL provide textual summaries describing key insights (e.g., “Spending on groceries increased by 20% compared to last month.”).
11. The system SHALL provide a way to export or copy comparison results (e.g., as text or CSV) for external use.

# Non-Functional Requirements

1. The system SHOULD produce comparison results for typical datasets (up to tens of thousands of expenses) within a few seconds on a standard laptop.
2. The system SHOULD produce deterministic results for the same input data and configuration.
3. The system SHALL validate input data and report errors (e.g., invalid dates, missing amounts) in a clear, actionable way.
4. The system SHOULD be structured so that storage (in-memory vs database) can be swapped via a well-defined interface.
5. The system SHOULD be testable via automated unit tests for core comparison and aggregation logic.

# Data & Integration Requirements

1. The expense model SHALL, at minimum, support: id, date, description, amount, category, and account.
2. The system SHALL treat amounts as decimal-safe numeric types (not floating-point) to avoid rounding errors.
3. The system SHOULD support configurable CSV mappings, so different banks with different column names can be handled without code changes.
4. The system SHOULD separate raw imported categories from normalized categories used for comparison.
5. The system SHOULD allow default categories and mapping rules to be defined in configuration.

# Visualization & Reporting Requirements

1. The system SHALL produce chart-ready data structures (e.g., JSON suitable for bar/line charts) representing spending per category over time.
2. The system SHOULD support at least one comparison-friendly visualization format (e.g., bar chart comparing category spend for two periods).
3. The system SHALL provide textual summaries alongside any chart-friendly outputs so users can understand trends without viewing charts.
4. The system SHOULD highlight top increasing and decreasing categories in the summary (e.g., top 3 increases, top 3 decreases).

# Out-of-Scope and Assumptions

1. Real-time bank API integrations (e.g., direct connections to financial institutions) are OUT OF SCOPE for the initial version; the system assumes CSV uploads or manual input.
2. Multi-currency conversion and foreign exchange rate handling are OUT OF SCOPE; the system assumes a single currency per dataset.
3. User authentication, multi-user account management, and persistence of user profiles are OUT OF SCOPE for the initial CLI/desktop-focused implementation.
4. The system assumes that the user has already cleaned obviously corrupted CSV files (e.g., non-tabular content) before upload.
5. Advanced budgeting features (e.g., goals, alerts, or recommendations) are OUT OF SCOPE for the initial version; the focus is on comparison and insight into existing spending patterns.