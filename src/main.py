# main.py

import sys
import logging

# Import NLU module
from src.nlu.interpreter import interpret_command, decompose_task

# Import Action Mapper
from src.executor.action_mapper import execute_action

# Import Logger and Error Handler
from src.utils.logger import setup_logger
from src.utils.error_handler import handle_error

# Initialize the logger
setup_logger()


def main():
    print("Welcome to the Natural Language Automation System")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_command = input("Enter a command: ")
            if user_command.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            # Step 1: Interpret the command
            interpretation = interpret_command(user_command)
            if not interpretation:
                print("Failed to interpret the command.")
                continue

            logging.info(f"Interpretation: {interpretation}")

            if not interpretation.get("needs_decomposition", False):
                action = interpretation.get("action")
                if action:
                    atomic_actions = [action]
                else:
                    print("No action provided for immediate execution.")
                    continue
            else:
                # Step 2: Decompose the task
                task_description = interpretation.get("intent", "")
                if not task_description:
                    print("No task description found.")
                    continue

                # Step 3: Decompose the task into atomic actions
                atomic_actions = decompose_task(task_description)
                if not atomic_actions:
                    print("Failed to decompose the task.")
                    continue

            # Step 4: Process each atomic action
            for action in atomic_actions:
                logging.info(f"Processing action: {action}")

                # Execute the action
                success = execute_action(action)
                if not success:
                    print(f"Failed to execute action: {action}")
                    # Decide whether to continue or break
                    continue

            print("All actions executed.")

        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting.")
            break
        except Exception as e:
            handle_error(e)
            continue


if __name__ == "__main__":
    main()
