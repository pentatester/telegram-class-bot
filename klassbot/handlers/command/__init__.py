from telegram.ext import CommandHandler

from klassbot.handlers.command.start import start

commands = [CommandHandler("start", start)]


def register(dispatcher):
    for command in commands:
        dispatcher.add_handler(command)
