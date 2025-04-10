# utils/logger.py

from config.logger_config import setup_logger
from config.config import LOG_FILE

logger = setup_logger("Pipeline Logger", LOG_FILE)

def get_logger(name):
    """Get a logger instance."""
    return setup_logger(name, LOG_FILE)
