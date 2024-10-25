import requests
import json
from ..config import LLAMA_API_URL, LLAMA_MODEL_NAME


def llama3(messages):
    """
    Sends a prompt with separated roles to the Llama 3 API and returns the response text.
    """
    data = {
        "model": LLAMA_MODEL_NAME,
        "messages": messages,
        "stream": False,
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(LLAMA_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["message"]["content"].strip()
    except requests.RequestException as e:
        print(f"Error communicating with Llama API: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Error parsing Llama API response: {e}")
        return None


def create_initial_prompt(user_command):
    """
    Creates a list of messages for the user's command with separated system and user roles.
    """
    messages = [
        {
            "role": "system",
            "content": """
You are an AI assistant that interprets user commands for automation.
For the given command, provide an intent description and indicate if task decomposition is needed.

If the command is simple and can be executed directly, provide an action object with "action_type" and "parameters".

Respond in the following JSON format:
{
    "intent": "brief description of the intent",
    "needs_decomposition": true or false,
    "action": {
        "action_type": "string",
        "parameters": { ... }
    } or null
}

Example:

User Command: "Open Calculator"

Response:
{
    "intent": "Open the Calculator application",
    "needs_decomposition": false,
    "action": {
        "action_type": "open_application",
        "parameters": {
            "application_name": "Calculator"
        }
    }
}
""",
        },
        {"role": "user", "content": user_command},
    ]
    return messages


def create_decomposition_prompt(task_description):
    """
    Creates a list of messages for decomposing a task into atomic actions.
    """
    messages = [
        {
            "role": "system",
            "content": f"""
You are an AI assistant that decomposes tasks into atomic actions for automation.

Decompose the following task into a sequence of atomic actions.

For each action, provide a JSON object with the following keys:
- "action_type": a string representing the type of action (e.g., "open_application", "click", "type_text", "press_key")
- "parameters": a dictionary of parameters needed for the action

**Important Instructions:**
- **Respond with only a JSON array of actions.**
- **Do not include any text or explanations before or after the JSON array.**
- **Do not include code blocks, markdown, or any formatting.**
- **Ensure the JSON is properly formatted without any trailing commas or syntax errors.**

Example:

Task: Open Chrome and search for penguins.

Response:
[
    {{"action_type": "open_application", "parameters": {{"application_name": "Chrome"}}}},
    {{"action_type": "wait", "parameters": {{"duration": 2}}}},
    {{"action_type": "click", "parameters": {{"target": "address bar"}}}},
    {{"action_type": "type_text", "parameters": {{"text": "penguins"}}}},
    {{"action_type": "press_key", "parameters": {{"key": "enter"}}}}
]

Task: {task_description}
""",
        }
    ]
    return messages


def interpret_command(user_command):
    """
    Interprets the user's command and returns the intent and decomposition flag.
    """
    messages = create_initial_prompt(user_command)
    response_text = llama3(messages)
    if response_text:
        try:
            parsed_response = json.loads(response_text)
            return parsed_response
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Response Text:\n{response_text}")
            return None
    else:
        return None


def decompose_task(task_description):
    """
    Decomposes a complex task into atomic actions.
    """
    messages = create_decomposition_prompt(task_description)
    response_text = llama3(messages)
    if response_text:
        # Remove any leading/trailing whitespace
        response_text = response_text.strip()
        try:
            # Attempt to parse the response directly
            actions = json.loads(response_text)
            return actions
        except json.JSONDecodeError:
            # If parsing fails, try to extract the JSON array from the response
            json_start = response_text.find("[")
            json_end = response_text.rfind("]")
            if json_start != -1 and json_end != -1 and json_start < json_end:
                json_str = response_text[json_start : json_end + 1]
                try:
                    actions = json.loads(json_str)
                    return actions
                except json.JSONDecodeError as e:
                    print(f"Error parsing extracted JSON: {e}")
                    print(f"Extracted JSON Text:\n{json_str}")
                    return None
            else:
                print("Could not find JSON array in the response.")
                print(f"Response Text:\n{response_text}")
                return None
    else:
        return None


def parse_actions_from_response(response_text):
    """
    Parses the numbered list of actions from the LLM response.
    """
    actions = []
    lines = response_text.strip().split("\n")
    for line in lines:
        line = line.strip()
        if line and line[0].isdigit():
            # Remove the number and period
            action_description = line[line.find(".") + 1 :].strip()
            if action_description:
                actions.append(action_description)
    return actions


if __name__ == "__main__":
    # Test the NLU module
    print("Welcome to the NLU Module Test")
    user_command = input("Enter a command: ")
    interpretation = interpret_command(user_command)
    if interpretation:
        print("\nInterpretation:")
        print(json.dumps(interpretation, indent=4))
        if interpretation.get("needs_decomposition", False):
            print("\nDecomposing Task...")
            atomic_actions = decompose_task(interpretation["intent"])
            if atomic_actions:
                print("\nAtomic Actions:")
                for idx, action in enumerate(atomic_actions, start=1):
                    print(f"{idx}. {action}")
            else:
                print("Failed to decompose the task.")
        else:
            print("No decomposition needed.")
    else:
        print("Failed to interpret the command.")
