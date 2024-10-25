# error_handler.py

import traceback
import logging


def handle_error(e):
    """
    Handles exceptions by logging the error details.

    Args:
        e (Exception): The exception object.
    """
    error_message = f"An error occurred: {str(e)}"
    logging.error(error_message)
    logging.debug("Stack Trace:", exc_info=True)
    print(error_message)
