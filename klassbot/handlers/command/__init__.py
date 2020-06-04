from telegram.ext import CommandHandler, Filters

from klassbot.handlers.command.create import klass_id, create
from klassbot.handlers.command.help import help
from klassbot.handlers.command.klass import klass_list
from klassbot.handlers.command.start import start, start_join

commands = [
    CommandHandler("start", start, filters=Filters.private),
    CommandHandler(
        "start",
        start_join,
        filters=Filters.regex("join-klass-[0-9]+$") & Filters.private,
    ),
    CommandHandler("help", help, filters=Filters.private),
    CommandHandler("create", create, filters=Filters.private),
    CommandHandler("class", klass_list, filters=Filters.private),
    CommandHandler("class_id", klass_id, filters=Filters.group),
]


def register(dispatcher):
    for command in commands:
        dispatcher.add_handler(command)
