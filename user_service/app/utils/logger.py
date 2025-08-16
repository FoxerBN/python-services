import logging

def get_logger(name: str = "app_logger") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        logger.addHandler(console_handler)

        file_handler = logging.FileHandler("logs/request.log")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        logger.addHandler(file_handler)

    return logger
