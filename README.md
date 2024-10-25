# Natural Language Automation System

## Introduction

The **Natural Language Automation System** is a tool that allows users to execute automation tasks on their MacBook using natural language commands. The system interprets user commands, decomposes them into atomic actions, and simulates human interactions by controlling the keyboard and mouse to perform the tasks step by step.

## Features

- **Natural Language Understanding (NLU):** Interprets user commands using a language model.
- **Task Decomposition:** Breaks down complex tasks into a sequence of atomic actions.
- **Action Mapping:** Maps atomic actions to specific mouse and keyboard operations.
- **Interface Interaction:** Controls the MacBook's keyboard and mouse to simulate human actions.
- **Environmental Awareness:** Recognizes UI elements on the screen for accurate interactions.
- **Error Handling:** Provides robust error handling and logging.

![mermaid-diagram-2024-10-25-140621](https://github.com/user-attachments/assets/c2262934-2d16-4e87-be1e-ea16c0615065)


## Project Structure

```
natural_language_automation/
├── README.md
├── .gitignore
├── requirements.txt
├── src/
│   ├── main.py                    # Main execution script
│   ├── nlu/
│   │   ├── __init__.py
│   │   └── interpreter.py         # NLU module
│   ├── executor/
│   │   ├── __init__.py
│   │   ├── action_mapper.py       # Maps actions to operations
│   │   ├── mouse_keyboard.py      # Simulates mouse and keyboard actions
│   │   └── environment.py         # Environmental awareness functions
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py              # Logging utilities
│   │   └── error_handler.py       # Error handling utilities
│   └── config.py                  # Configuration settings
├── images/                        # Images for UI element recognition
│   └── address_bar.png            # Example image file
└── tests/
    ├── __init__.py
    ├── test_nlu.py
    ├── test_executor.py
    └── test_integration.py
```

## Installation

### Prerequisites

- **Python 3.7 or higher**
- **pip** package manager
- **macOS** (for controlling the MacBook)
- **Accessibility Permissions**: The application needs permission to control your MacBook's keyboard and mouse.

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/natural_language_automation.git
   cd natural_language_automation
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Configuration**

   - Create a `config.py` file in the `src/` directory with the following content:

     ```python
     # config.py

     # Llama API settings
     LLAMA_API_URL = "http://localhost:11434/api/chat"
     LLAMA_MODEL_NAME = "llama3:70b-instruct"
     ```

     Adjust the `LLAMA_API_URL` and `LLAMA_MODEL_NAME` according to your setup.

5. **Grant Accessibility Permissions**

   - Go to **System Preferences** > **Security & Privacy** > **Privacy** tab.
   - Select **Accessibility** from the left panel.
   - Click the **Lock** icon to make changes.
   - Click the **+** button and add your **Terminal** application or Python interpreter.

6. **Prepare Images for UI Elements**

   - Place images of UI elements (e.g., address bar, application icons) in the `images/` directory.
   - Ensure that the images match your screen resolution and UI theme.

## Usage

1. **Start the Llama API Server**

   - Make sure your Llama API server is running and accessible at the URL specified in `config.py`.

2. **Run the Application**

   ```bash
   python src/main.py
   ```

3. **Enter Commands**

   - After starting the application, you'll be prompted to enter a command.

     ```
     Welcome to the Natural Language Automation System
     Type 'exit' to quit.

     Enter a command:
     ```

   - **Example Commands:**

     - `Open Chrome and search for penguins.`
     - `Send an email to Alice about the meeting tomorrow.`
     - `Open Calculator.`
     - `Search for cat videos.`

4. **Exit the Application**

   - Type `exit` or `quit` to exit the application.

## Configuration

- **Llama API Settings:**

  Configure the API URL and model name in `src/config.py`.

  ```python
  # config.py

  LLAMA_API_URL = "http://localhost:11434/api/chat"
  LLAMA_MODEL_NAME = "llama3:70b-instruct"
  ```

- **Logging:**

  Logging is configured in `src/utils/logger.py`. By default, logs are written to `app.log` and output to the console.

  ```python
  # logger.py

  def setup_logger():
      logging.basicConfig(
          level=logging.DEBUG,
          format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
          filename='app.log',
          filemode='a'
      )

      console = logging.StreamHandler()
      console.setLevel(logging.INFO)
      formatter = logging.Formatter('%(levelname)s: %(message)s')
      console.setFormatter(formatter)
      logging.getLogger('').addHandler(console)
  ```

## How It Works

1. **Interpretation:**

   - The NLU module (`interpreter.py`) uses the Llama language model to interpret the user's command and determine if task decomposition is needed.

2. **Task Decomposition:**

   - If required, the command is decomposed into atomic actions using the Llama model.

3. **Action Mapping:**

   - The `action_mapper.py` module maps each atomic action to a specific function that can simulate the action.

4. **Execution:**

   - The `mouse_keyboard.py` and `environment.py` modules simulate mouse and keyboard actions to perform the tasks.

5. **Environmental Awareness:**

   - The system uses images and screen recognition to locate UI elements for interaction.

6. **Error Handling and Logging:**

   - The system includes robust error handling and logs actions and errors for debugging.

## Examples

### Example 1: Open Chrome and Search for Penguins

**Command:**

```
Open Chrome and search for penguins.
```

**Interpretation:**

```json
{
  "intent": "Open the Google Chrome browser and search for 'penguins'.",
  "needs_decomposition": true,
  "action": null
}
```

**Decomposed Actions:**

```json
[
  {
    "action_type": "open_application",
    "parameters": { "application_name": "Google Chrome" }
  },
  { "action_type": "wait", "parameters": { "duration": 2 } },
  { "action_type": "click", "parameters": { "target": "address bar" } },
  { "action_type": "type_text", "parameters": { "text": "penguins" } },
  { "action_type": "press_key", "parameters": { "key": "enter" } }
]
```

**Execution:**

- The system opens Chrome, clicks on the address bar, types "penguins", and presses Enter.

### Example 2: Open Calculator

**Command:**

```
Open Calculator.
```

**Interpretation:**

```json
{
  "intent": "Open the Calculator application.",
  "needs_decomposition": false,
  "action": {
    "action_type": "open_application",
    "parameters": {
      "application_name": "Calculator"
    }
  }
}
```

**Execution:**

- The system opens the Calculator application.

## Dependencies

- **Python Packages:**

  - `requests`
  - `pyautogui`
  - `opencv-python` (for image processing)
  - `pytesseract` (optional, for OCR)
  - `tesseract-ocr` (system dependency if using `pytesseract`)

- **System Requirements:**

  - **macOS** with Accessibility permissions granted.
  - **Llama API Server** running and accessible.

## Troubleshooting

- **LLM Response Issues:**

  - If the LLM includes extra text or formatting, adjust the prompts in `interpreter.py` to be more explicit.
  - Ensure the LLM model is correctly configured and accessible.

- **Image Recognition Failures:**

  - Verify that the images in the `images/` directory match your screen resolution and UI theme.
  - Adjust the `confidence` parameter in `pyautogui.locateCenterOnScreen()` if necessary.

- **Permission Errors:**

  - Ensure that the application has the necessary Accessibility permissions in System Preferences.

- **Logging:**

  - Check the `app.log` file for detailed error messages and debugging information.

## Extending the System

- **Adding New Actions:**

  - Extend the `execute_action` function in `action_mapper.py` to support additional actions.

- **Improving Environmental Awareness:**

  - Implement more advanced image recognition or OCR in `environment.py` to improve interaction with UI elements.

- **Cross-Platform Support:**

  - Modify the `mouse_keyboard.py` functions to support Windows or Linux if needed.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any bugs or feature requests.

## License

This project is licensed under the MIT License.

## Acknowledgments

- **Llama Language Model:** Used for natural language understanding.
- **PyAutoGUI:** For simulating mouse and keyboard actions.
- **OpenAI's GPT Model:** Inspiration for the language understanding capabilities.
