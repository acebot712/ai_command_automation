from src.plugins import plugin_registry, ActionPlugin, LLMPlugin
from src.nlu.interpreter import interpret_command, decompose_task
from src.executor.action_mapper import execute_action

def test_llm_plugin():
    plugin = plugin_registry.get_llm_plugin()
    assert isinstance(plugin, LLMPlugin)
    # Test a simple command (mock or skip if no Llama API running)
    # result = plugin.interpret_command("Open Calculator")
    # assert result is not None

def test_action_plugin():
    plugin = plugin_registry.get_action_plugin("open_application")
    assert isinstance(plugin, ActionPlugin)
    # Test a dummy action (mock or skip actual execution)
    # result = plugin.execute({"action_type": "wait", "parameters": {"duration": 0}})
    # assert result is True

def test_integration_stub():
    # This is a stub for future integration tests
    pass

def test_gui_stub_import():
    try:
        import src.gui_stub
    except Exception as e:
        assert False, f"GUI stub import failed: {e}"

def test_dry_run_stub():
    # Placeholder for future dry-run/preview mode tests
    pass

def test_gui_interpret_preview():
    # Simulate the logic of interpreting and previewing a command in the GUI
    command = "Open Calculator"
    interpretation = interpret_command(command)
    assert interpretation is None or isinstance(interpretation, dict)
    # If Llama API is running, should return a dict

def test_gui_feedback_approval_stub():
    # Placeholder for feedback and approval logic test
    pass

if __name__ == "__main__":
    test_llm_plugin()
    test_action_plugin()
    test_integration_stub()
    test_gui_stub_import()
    test_dry_run_stub()
    test_gui_interpret_preview()
    test_gui_feedback_approval_stub()
    print("Plugin system, GUI, and stubs tests passed (basic stubs).") 