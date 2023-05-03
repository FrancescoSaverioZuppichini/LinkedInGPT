import logging
import os

from rich.logging import RichHandler

logger = logging.getLogger("linkedInGPT")
logger.setLevel(os.environ.get("LOG_LEVEL", logging.INFO))
logger.addHandler(RichHandler())