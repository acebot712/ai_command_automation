# action_mapper.py

from src.plugins import ActionPlugin, plugin_registry
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
from typing import Any, Dict

class DefaultActionPlugin(ActionPlugin):
    def can_handle(self, action_type: str) -> bool:
        return action_type in [
            "open_application",
            "click",
            "type_text",
            "press_key",
            "wait",
        ]

    def execute(self, action: Dict[str, Any]) -> bool:
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

# Register the default action plugin
default_plugin = DefaultActionPlugin()
plugin_registry.register_action_plugin(default_plugin)

def execute_action(action: Dict[str, Any]) -> bool:
    action_type = action.get("action_type")
    plugin = plugin_registry.get_action_plugin(action_type)
    return plugin.execute(action)
