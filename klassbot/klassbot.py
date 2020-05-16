import logging
from telegram.ext import (Updater)

from klassbot.config import config

logging.basicConfig(
    level=config["logging"]["log_level"],
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Initialize telegram updater and dispatcher
updater = Updater(
    token=config["telegram"]["api_key"],
    workers=config["telegram"]["worker_count"],
    use_context=True,
    request_kwargs={
        "read_timeout": 20,
        "connect_timeout": 20
    },
)

dispatcher = updater.dispatcher