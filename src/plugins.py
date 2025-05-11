from abc import ABC, abstractmethod
from typing import Any, Dict, List

# --- Action Plugin Interface ---
class ActionPlugin(ABC):
    @abstractmethod
    def can_handle(self, action_type: str) -> bool:
        """Return True if this plugin can handle the given action type."""
        pass

    @abstractmethod
    def execute(self, action: Dict[str, Any]) -> bool:
        """Execute the action. Return True if successful."""
        pass

# --- LLM Plugin Interface ---
class LLMPlugin(ABC):
    @abstractmethod
    def interpret_command(self, user_command: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def decompose_task(self, task_description: str) -> List[Dict[str, Any]]:
        pass

# --- Plugin Registry ---
class PluginRegistry:
    def __init__(self):
        self.action_plugins: List[ActionPlugin] = []
        self.llm_plugins: List[LLMPlugin] = []

    def register_action_plugin(self, plugin: ActionPlugin):
        self.action_plugins.append(plugin)

    def register_llm_plugin(self, plugin: LLMPlugin):
        self.llm_plugins.append(plugin)

    def get_action_plugin(self, action_type: str) -> ActionPlugin:
        for plugin in self.action_plugins:
            if plugin.can_handle(action_type):
                return plugin
        raise ValueError(f"No plugin found for action type: {action_type}")

    def get_llm_plugin(self) -> LLMPlugin:
        if self.llm_plugins:
            return self.llm_plugins[0]  # For now, just return the first
        raise ValueError("No LLM plugin registered.")

# Global registry instance
plugin_registry = PluginRegistry() 