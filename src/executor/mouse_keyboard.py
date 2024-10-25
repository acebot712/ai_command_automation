# mouse_keyboard.py

import pyautogui
import subprocess
import time
import os
import sys


def open_application(application_name):
    """
    Opens an application based on its name.

    Args:
        application_name (str): The name of the application to open.
    """
    print(f"Opening application: {application_name}")
    if sys.platform == "darwin":
        # macOS command to open an application
        subprocess.Popen(["open", "-a", application_name])
    elif sys.platform == "win32":
        # Windows command to open an application
        os.startfile(application_name)
    else:
        # Linux command to open an application
        subprocess.Popen([application_name])


def click_on_coordinates(x, y):
    """
    Moves the mouse to (x, y) coordinates and performs a click.

    Args:
        x (int): X-coordinate.
        y (int): Y-coordinate.
    """
    pyautogui.moveTo(x, y)
    pyautogui.click()


def type_text(text):
    """
    Types the specified text.

    Args:
        text (str): The text to type.
    """
    pyautogui.write(text, interval=0.05)


def press_key(key):
    """
    Presses a specific key.

    Args:
        key (str): The key to press.
    """
    pyautogui.press(key)


def wait_seconds(duration):
    """
    Waits for a specified number of seconds.

    Args:
        duration (int): Number of seconds to wait.
    """
    time.sleep(duration)
