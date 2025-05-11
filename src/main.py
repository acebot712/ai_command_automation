# main.py

import sys
import logging
from typing import Optional, Dict, Any

# Import NLU and Action Mapper (now plugin-based)
from src.nlu.interpreter import interpret_command, decompose_task
from src.executor.action_mapper import execute_action
from src.utils.logger import setup_logger
from src.utils.error_handler import handle_error

def main() -> None:
    """
    Main entry point for the Natural Language Automation System.
    Handles user input, command interpretation, task decomposition, and action execution.
    TODO: Add GUI, dry-run mode, feedback loop, and advanced planning/preview.
    """
    print("Welcome to the Natural Language Automation System")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_command = input("Enter a command: ")
            if user_command.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            # Step 1: Interpret the command (via plugin)
            interpretation: Optional[Dict[str, Any]] = interpret_command(user_command)
            if not interpretation:
                print("Failed to interpret the command.")
                continue

            logging.info(f"Interpretation: {interpretation}")

            # TODO: Add action plan visualization (print or display the plan before execution)
            # TODO: Add dry-run/preview mode (ask user to approve the plan before execution)
            # TODO: Add user feedback/correction step (let user edit the plan)

            if not interpretation.get("needs_decomposition", False):
                action = interpretation.get("action")
                if action:
                    atomic_actions = [action]
                else:
                    print("No action provided for immediate execution.")
                    continue
            else:
                # Step 2: Decompose the task (via plugin)
                task_description = interpretation.get("intent", "")
                if not task_description:
                    print("No task description found.")
                    continue
                atomic_actions = decompose_task(task_description)
                if not atomic_actions:
                    print("Failed to decompose the task.")
                    continue

            # Step 3: Process each atomic action (via plugin)
            for action in atomic_actions:
                logging.info(f"Processing action: {action}")
                # TODO: Add undo/rollback and error recovery here
                success = execute_action(action)
                if not success:
                    print(f"Failed to execute action: {action}")
                    # TODO: Add error recovery, user feedback, and undo/rollback
                    continue
            print("All actions executed.")

        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting.")
            break
        except Exception as e:
            handle_error(e)
            continue

if __name__ == "__main__":
    setup_logger()
    main()
