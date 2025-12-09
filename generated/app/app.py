import argparse
import sys
import subprocess

def run_expense_comparator(prompt: str = None) -> int:
    command = [sys.executable, "-m", "mcp.orchestrator"]
    if prompt is not None:
        command.extend(["--prompt", prompt])

    print("[AI Expense Comparator] Starting...")
    print(f"[AI Expense Comparator] Delegating to orchestrator using: {' '.join(command)}")
    try:
        result = subprocess.run(command)
        code = result.returncode
    except Exception as e:
        print(f"[AI Expense Comparator] Error running orchestrator: {e}")
        return 1

    print("[AI Expense Comparator] Done.")
    return code if code is not None else 0

def main(argv: list = None) -> int:
    parser = argparse.ArgumentParser(description="AI Expense Comparator CLI")
    parser.add_argument(
        "--prompt",
        type=str,
        help="Task prompt for orchestrator",
        default=None
    )
    args = parser.parse_args(argv)

    default_prompt = (
        "Build an Expense Comparator application."
    )
    prompt = args.prompt if args.prompt is not None else default_prompt

    return run_expense_comparator(prompt)

if __name__ == "__main__":
    raise SystemExit(main())