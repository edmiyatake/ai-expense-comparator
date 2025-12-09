# The Perfect Prompt
## Original Software Description
Expense Comparator is a finance software application that helps users compare their expenses across different time periods. Users can input their expenses and categorize them into different categories such as groceries, transportation, entertainment, etc. The application will provide a visual representation of their expenses through charts and graphs, allowing users to easily compare their spending habits between different timeframes. Users can also set custom date ranges for comparison. The main function of the software is to provide users with a clear understanding of their spending patterns and identify areas where they can make adjustments to improve their financial well-being.

We want to separate these into separate constraints
## Constraints 
### Core Functional Requirements

- The system must allow users to manually enter expenses.
- Users must be able to import expenses from CSV files.
- Each expense must include:
  - date
  - description
  - amount 
  - category 
  - account
- Users must be able to create, edit, delete, and map categories.
- The system must store expenses, categories, recurring patterns, and import logs.

### Comparison + Analysis Requirements

- The system must compare spending across different time periods.
- Users must be able to choose preset and custom date ranges.
- The application must detect recurring expenses (e.g., subscriptions).
- The system must highlight spending patterns, anomalies, and trends.
- Insights must help users identify areas to improve their financial well-being.

### Visualization Requirements

- The system must produce clear visual representations of spending.
- Required chart types include:
  - category breakdown charts
  - time-series trend charts
  - comparison charts between date ranges
- Visual outputs must make spending comparisons intuitive and meaningful.

### Interface Requirements

- The system may be CLI-based or API-based.
- It must support:
  - entering expenses 
  - selecting time periods 
  - viewing comparisons 
  - displaying visual reports

## Converting Constraints to Prompt
The list of constraints serves as the foundation for the final prompt by transforming the original narrative description into precise, actionable requirements that the multi-agent system can reliably interpret. By breaking the software description into explicit functional, analytical, visualization, and interface constraints, we remove ambiguity and ensure that every essential capability is represented in the generated solution. The final prompt is simply a compressed version of these constraints, written in a way that is short enough for a terminal environment but detailed enough to guarantee that the agents produce complete requirements, a domain model, architecture, code skeleton, test skeleton, and design review. In other words, the constraints define what the system must do, and the final prompt distills them into a clear instruction so the agents can generate the full Expense Comparator application without missing any critical features.

## The Prompt

Build an Expense Comparator application that lets users manually enter expenses and optionally upload CSVs. Each expense includes a date, description, amount, category, and account. Users can create, edit, and map categories. The system must compare spending across different time periods, including custom date ranges, and detect recurring expenses such as subscriptions. It must also produce clear visual representations of spending using charts or graphs, including category breakdown charts, time-series trend charts, and comparison charts between selected date ranges. Additionally, the application should generate insights that highlight spending trends, anomalies, and areas to improve financial well-being. The system should store expenses, categories, recurring patterns, and import logs. The UI may be CLI or API based but must support entering expenses, selecting date ranges, viewing comparisons, and displaying visual reports. Please generate requirements, a domain model, architecture, a full code skeleton, a test skeleton, and a design review covering all these capabilities.