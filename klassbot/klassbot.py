import logging
from telegram.ext import Updater, Defaults

from klassbot.config import config
from klassbot.handlers import register
from klassbot.utils.persistence import CustomPersistence

logging.basicConfig(
    level=config["logging"]["log_level"],
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


persistence = CustomPersistence()

# Initialize telegram updater and dispatcher
updater = Updater(
    token=config["telegram"]["api_key"],
    workers=config["telegram"]["worker_count"],
    use_context=True,
    defaults=Defaults(**config["defaults"]),
    persistence=persistence,
    request_kwargs={"read_timeout": 20, "connect_timeout": 20},
)

config["me"] = updater.bot.get_me()

dispatcher = updater.dispatcher

register(dispatcher)
