from telegram.ext import CommandHandler, Filters

from klassbot.handlers.conversation.klass import my_class

conversations = [CommandHandler("my_klass", my_class, filters=Filters.private)]


def register(dispatcher):
    for conversation in conversations:
        dispatcher.add_handler(conversation)
