from telegram.ext import ConversationHandler

from klassbot.models import Conversation

class CustomConversationHandler(ConversationHandler):
    def _get_key(self, update):
        pass
