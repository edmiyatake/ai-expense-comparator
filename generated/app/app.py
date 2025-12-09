import argparse
import sys

def orchestrate_expense_comparator(prompt=None):
    print("AI Expense Comparator orchestration pipeline starting...")
    if prompt:
        print(f"Prompt received: {prompt}")
    print("Stub: Expense Comparator running (pipeline not implemented yet)")
    print("AI Expense Comparator finished.")

def main():
    parser = argparse.ArgumentParser(description="AI Expense Comparator")
    parser.add_argument('--prompt', type=str, help='Optional prompt string for comparator')
    args = parser.parse_args()
    orchestrate_expense_comparator(prompt=args.prompt)

if __name__ == "__main__":
    main()