import logging

def get_logger(name):
    """
    Create and configure a logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # File handler
    file_handler = logging.FileHandler("graph_rag.log")
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
