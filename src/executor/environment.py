# src/executor/environment.py

import pyautogui
import time
import logging
import os


def click_on_target(target_description):
    """
    Locates the target on the screen using image recognition and performs a click action.

    Args:
        target_description (str): Description of the target to click.

    Returns:
        bool: True if the click was successful, False otherwise.
    """
    logging.info(f"Attempting to click on '{target_description}'")

    # Map target descriptions to image file names
    target_image_map = {
        "address bar": "address_bar.png",
        # Add more mappings as needed
    }

    image_filename = target_image_map.get(target_description.lower())
    if not image_filename:
        logging.error(f"No image mapping found for '{target_description}'")
        return False

    # Adjust the image path according to your project structure
    image_path = os.path.join("images", image_filename)
    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        if location:
            pyautogui.moveTo(location)
            pyautogui.click()
            logging.info(f"Clicked on '{target_description}' at {location}")
            return True
        else:
            logging.error(f"Could not locate '{target_description}' on the screen.")
            return False
    except Exception as e:
        logging.error(f"Failed to click on '{target_description}': {e}")
        return False
