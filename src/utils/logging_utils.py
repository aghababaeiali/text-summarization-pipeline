import logging

# Create logger
logger = logging.getLogger("summarizer")
logger.setLevel(logging.INFO)

# Formatter for timestamps + message
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Console Output
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Avoid double logging
if not logger.handlers:
    logger.addHandler(handler)
