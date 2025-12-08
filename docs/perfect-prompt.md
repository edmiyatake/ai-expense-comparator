so ideally the project should have:

Build an Expense Comparator application with the following capabilities:

Expense Input

Users must be able to manually enter expenses.

Users may optionally upload CSV exports from banks.

Each expense includes: date, description, amount, category, and account/source.

Categorization

Users can assign categories (e.g., groceries, transportation, entertainment).

The system must support editing categories, adding new categories, and mapping raw categories from CSVs.

Automatic category suggestions are a bonus.

Time-Based Comparison

Users can compare their spending across different time periods (e.g., this month vs last month).

Users can set custom date ranges.

The system must support comparing totals, averages, and category-level breakdowns.

Recurring Transaction Detection

Identify recurring expenses (subscriptions, memberships, bills).

Show frequency, amount stability, and next expected charge.

Data Visualization

Provide charts and graphs that visually summarize spending patterns.

Examples: bar charts, line charts, category pie charts.

Visuals should support time range comparison and category breakdowns.

Insights for Financial Well-Being

Highlight categories with spending increases or decreases.

Identify unusual spikes in spending.

Suggest categories where users may consider reducing expenses.

Provide short insights explaining trends.

Data Management

Store expenses, categories, recurring transactions, and user actions.

Log CSV imports and errors.

User Interface

The final application may be CLI or API-based.

The interface must allow:

entering expenses,

selecting time ranges,

viewing charts and reports.

The system you generate should include:

A clear domain model (entities, relationships, constraints)

A file/module-level architecture

Code skeletons for each module

Test skeletons covering import, normalization, categorization, visualization, comparison, insights, and CLI/API workflows

A reviewer analysis identifying strengths, gaps, and risks

We can condense this and change it to a paragraph format so it's easier for the llm

Build an Expense Comparator application that lets users manually enter expenses and optionally upload CSVs. Each expense includes a date, description, amount, category, and account. Users can create, edit, and map categories. The system must compare spending across different time periods, including custom date ranges, and detect recurring expenses such as subscriptions. It must also produce clear visual representations of spending using charts or graphs, including category breakdown charts, time-series trend charts, and comparison charts between selected date ranges. Additionally, the application should generate insights that highlight spending trends, anomalies, and areas to improve financial well-being. The system should store expenses, categories, recurring patterns, and import logs. The UI may be CLI or API based but must support entering expenses, selecting date ranges, viewing comparisons, and displaying visual reports. Please generate requirements, a domain model, architecture, a full code skeleton, a test skeleton, and a design review covering all these capabilities.