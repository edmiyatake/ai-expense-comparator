# SWE270P Final Project – Expense Comparator (Multi-Agent MCP System)

This repository contains our final project for SWE270P: a multi-agent system
integrated with the Model Context Protocol (MCP) that generates a complete
software application from a description and requirements provided via a user interface.

## Project Description
Our selected project is **Expense Comparator**, a finance tool that allows users to:
- Input expenses
- Categorize spending
- Compare spending across custom time periods
- View visual expense breakdowns and trends

## Project Goals
1. Build a fully functional **multi-agent system** using MCP.
2. Create a **UI** that accepts a software description + requirements.
3. Automatically generate:
   - Executable application code
   - Executable test cases
4. Track LLM usage (API calls + token count).
5. Demonstrate system design + MCP collaboration flow in Week 10.

## Running the AI Expense Comparator

This project uses a src-based project layout, so the Python interpreter must be told explicitly where to find the root packages (app, agents, mcp) when running from the terminal.

### 1. Activate the virtual environment
source .venv/bin/activate
(Or use the equivalent activation command for your shell.)

### 2. Add src/ to the Python import path

Because the project modules live inside the src/ directory, you must set PYTHONPATH so Python can locate them:
export PYTHONPATH=src
You will need to do this each time you open a new terminal session unless you add it to your shell profile.

### 3. Run the orchestrator

With PYTHONPATH set, you can run the application from the project root:
python -m app.main "Build an Expense Comparator application that lets users manually enter expenses and optionally upload CSVs. Each expense includes a date, description, amount, category, and account. Users can create, edit, and map categories. The system must compare spending across different time periods, including custom date ranges, and detect recurring expenses such as subscriptions. It must also produce clear visual representations of spending using charts or graphs, including category breakdown charts, time-series trend charts, and comparison charts between selected date ranges. Additionally, the application should generate insights that highlight spending trends, anomalies, and areas to improve financial well-being. The system should store expenses, categories, recurring patterns, and import logs. The UI may be CLI or API based but must support entering expenses, selecting date ranges, viewing comparisons, and displaying visual reports. Please generate requirements, a domain model, architecture, a full code skeleton, a test skeleton, and a design review covering all these capabilities."

If you omit PYTHONPATH=src, you will see:

ModuleNotFoundError: No module named 'app'
because Python cannot find the packages inside src/.

Why this step is required

The project uses a src/ directory to store all Python packages.

This is a common and recommended project layout, but Python does not automatically add src/ to the import path when running in the terminal.

PyCharm does automatically add src/ because it was marked as a Sources Root, which is why running inside PyCharm works without this step.

The terminal requires the explicit PYTHONPATH=src so it knows where to find app, agents, and mcp.

Optional: Making this permanent

You can avoid typing export PYTHONPATH=src every time by adding:

export PYTHONPATH=src
to your ~/.zshrc or ~/.bashrc.

