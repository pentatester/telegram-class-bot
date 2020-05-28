"""This module contain logger class"""

import logging

from klassbot.config import config

logging.basicConfig(
    level=config["logging"]["log_level"],
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
