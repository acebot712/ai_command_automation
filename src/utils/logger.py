# logger.py

import logging


def setup_logger():
    """
    Sets up the logging configuration.
    """
    logging.basicConfig(
        level=logging.DEBUG,  # Set to DEBUG to capture all levels of logs
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename="app.log",  # Log file name
        filemode="a",  # Append to the log file
    )

    # Create a console handler to output logs to the console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)  # Adjust level as needed
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)
