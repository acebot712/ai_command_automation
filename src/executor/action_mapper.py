# action_mapper.py

from .mouse_keyboard import (
    open_application,
    click_on_coordinates,
    type_text,
    press_key,
    wait_seconds,
)
from .environment import click_on_target  # Import from environment.py
from ..utils.error_handler import handle_error
import logging
import time


def execute_action(action):
    """
    Executes an action based on its type and parameters.

    Args:
        action (dict): The action dictionary with 'action_type' and 'parameters'.

    Returns:
        bool: True if action executed successfully, False otherwise.
    """
    action_type = action.get("action_type")
    parameters = action.get("parameters", {})

    try:
        if action_type == "open_application":
            application_name = parameters.get("application_name")
            if application_name:
                open_application(application_name)
                return True
            else:
                logging.error("No application name provided for 'open_application'.")
                return False

        elif action_type == "click":
            target_description = parameters.get("target")
            if target_description:
                success = click_on_target(target_description)
                return success
            else:
                logging.error("No target description provided for 'click'.")
                return False

        elif action_type == "type_text":
            text = parameters.get("text", "")
            type_text(text)
            return True

        elif action_type == "press_key":
            key = parameters.get("key", "enter")
            press_key(key)
            return True

        elif action_type == "wait":
            duration = parameters.get("duration", 1)
            wait_seconds(duration)
            return True

        else:
            logging.error(f"Unknown action type: {action_type}")
            return False

    except Exception as e:
        handle_error(e)
        return False
