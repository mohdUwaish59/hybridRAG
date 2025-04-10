from loguru import logger
import os
import sys

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logger
logger.remove()  # Remove default logger
logger.add(sys.stdout, level="INFO", format="{time} | {level} | {message}")
logger.add(
    "logs/preprocess.log",
    level="INFO",
    format="{time} | {level} | {message}",
    rotation="10 MB",  # Rotate log file after it reaches 10 MB
    retention="7 days"  # Retain log files for 7 days
)

def get_logger():
    """
    Returns the configured logger instance.

    Returns:
        logger: Configured loguru logger.
    """
    return logger
