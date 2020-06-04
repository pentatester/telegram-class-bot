from telegram.ext import CommandHandler, Filters

conversations = []


def register(dispatcher):
    if len(conversations) > 0:
        for conversation in conversations:
            dispatcher.add_handler(conversation)
