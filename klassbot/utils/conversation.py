"""This module contain CustomConversationHandler."""
from telegram.ext import ConversationHandler


class CustomConversationHandler(ConversationHandler):
    def _get_key(self, update):
        chat = update.effective_chat
        user = update.effective_user
        key = list()
        # defaults set to 0
        chat_id, user_id, message_id = -1, -1, -1
        if self.per_chat:
            chat_id = chat.id
        key.append(chat_id)
        if self.per_user and user is not None:
            user_id = user.id
        key.append(user_id)
        if self.per_message:
            message_id = (
                update.callback_query.inline_message_id
                or update.callback_query.message.message_id
            )
        key.append(message_id)
        return tuple(key)
