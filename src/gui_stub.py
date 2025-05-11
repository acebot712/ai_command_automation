import streamlit as st
from src.nlu.interpreter import interpret_command, decompose_task
from src.executor.action_mapper import execute_action
import logging
import io
import sys

st.set_page_config(page_title="Natural Language Automation System", layout="centered")
st.title("Natural Language Automation System (GUI)")

# Capture logs for display
class StreamToLogger(io.StringIO):
    def __init__(self):
        super().__init__()
        self.contents = ""
    def write(self, s):
        self.contents += s
        super().write(s)
    def getvalue(self):
        return self.contents

def run_with_log_capture(func, *args, **kwargs):
    log_capture = StreamToLogger()
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = log_capture, log_capture
    try:
        result = func(*args, **kwargs)
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr
    return result, log_capture.getvalue()

# Session state for command, plan, approval, feedback, and logs
if 'command' not in st.session_state:
    st.session_state.command = ''
if 'interpretation' not in st.session_state:
    st.session_state.interpretation = None
if 'atomic_actions' not in st.session_state:
    st.session_state.atomic_actions = None
if 'approved' not in st.session_state:
    st.session_state.approved = False
if 'feedback' not in st.session_state:
    st.session_state.feedback = ''
if 'execution_log' not in st.session_state:
    st.session_state.execution_log = ''
if 'execution_status' not in st.session_state:
    st.session_state.execution_status = ''

st.write("Enter a natural language command to automate your MacBook:")
command = st.text_input("Command", value=st.session_state.command, key="command_input")

if st.button("Interpret & Preview Plan"):
    st.session_state.command = command
    st.session_state.approved = False
    st.session_state.feedback = ''
    st.session_state.execution_log = ''
    st.session_state.execution_status = ''
    interpretation, log = run_with_log_capture(interpret_command, command)
    st.session_state.interpretation = interpretation
    st.session_state.atomic_actions = None
    if interpretation:
        if not interpretation.get("needs_decomposition", False):
            action = interpretation.get("action")
            if action:
                st.session_state.atomic_actions = [action]
        else:
            task_description = interpretation.get("intent", "")
            if task_description:
                atomic_actions, log2 = run_with_log_capture(decompose_task, task_description)
                st.session_state.atomic_actions = atomic_actions
                log += log2
    st.session_state.execution_log = log

if st.session_state.interpretation:
    st.subheader("Interpreted Intent")
    st.json(st.session_state.interpretation)
    if st.session_state.atomic_actions:
        st.subheader("Action Plan (Dry-Run)")
        st.json(st.session_state.atomic_actions)
        st.info("Review the action plan below. You can provide feedback or corrections before execution.")
        st.session_state.feedback = st.text_area("Feedback / Corrections (optional)", value=st.session_state.feedback, key="feedback_box")
        if not st.session_state.approved:
            if st.button("Approve and Execute Plan"):
                st.session_state.approved = True
                st.session_state.execution_status = "Running..."
                log = ""
                for action in st.session_state.atomic_actions:
                    success, action_log = run_with_log_capture(execute_action, action)
                    log += action_log
                    if not success:
                        st.session_state.execution_status = f"Failed to execute action: {action}"
                        break
                else:
                    st.session_state.execution_status = "All actions executed."
                st.session_state.execution_log = log
    else:
        st.warning("No atomic actions found. Please check your command or try again.")

if st.session_state.execution_status:
    st.subheader("Execution Status")
    st.write(st.session_state.execution_status)

if st.session_state.execution_log:
    st.subheader("Execution Log")
    st.code(st.session_state.execution_log) 