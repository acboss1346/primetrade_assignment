import logging

def setup_logger():
    logger = logging.getLogger("BinanceBot")
    logger.setLevel(logging.DEBUG)

    # File Handler
    file_handler = logging.FileHandler("bot.log")
    file_handler.setLevel(logging.DEBUG)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatting
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
