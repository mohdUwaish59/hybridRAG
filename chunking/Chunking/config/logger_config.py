import logging

def get_logger(name):
    """
    Configure and return a logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    return logger
