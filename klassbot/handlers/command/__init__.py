from telegram.ext import CommandHandler, Filters, MessageHandler

from klassbot.handlers.command.create import create, create_klass
from klassbot.handlers.command.help import help
from klassbot.handlers.command.start import start

commands = [
    CommandHandler("start", start),
    CommandHandler("help", help),
    MessageHandler(Filters.command("create") & Filters.private, create),
    MessageHandler(Filters.command("create") & Filters.group, create_klass),
]


def register(dispatcher):
    for command in commands:
        dispatcher.add_handler(command)
