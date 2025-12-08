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

Running the AI Expense Comparator

This project uses a src-based project layout, so the Python interpreter must be told explicitly where to find the root packages (app, agents, mcp) when running from the terminal.

1. Activate the virtual environment
source .venv/bin/activate


(Or use the equivalent activation command for your shell.)

2. Add src/ to the Python import path

Because the project modules live inside the src/ directory, you must set PYTHONPATH so Python can locate them:

export PYTHONPATH=src


You will need to do this each time you open a new terminal session unless you add it to your shell profile.

3. Run the orchestrator

With PYTHONPATH set, you can run the application from the project root:

python -m app.main "Build an AI Expense Comparator that takes in CSV exports from multiple banks, normalizes categories, and compares recurring expenses."


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

