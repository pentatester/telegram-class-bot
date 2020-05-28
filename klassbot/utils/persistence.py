from collections import defaultdict
from sqlalchemy.orm.exc import NoResultFound
from telegram.ext import BasePersistence

from klassbot.db import get_session
from klassbot.models import Conversation
from klassbot.utils.db import get_one_or_create


class CustomPersistence(BasePersistence):
    def __init__(
        self, store_user_data=True, store_chat_data=True, store_bot_data=True
    ):
        self.store_user_data = store_user_data
        self.store_chat_data = store_chat_data
        self.store_bot_data = store_bot_data
        self.session = get_session()

    def get_conversations(self, name):
        try:
            conversations = self.session.query(Conversation).filter_by(
                Conversation.name == name
            )
            convs = dict()
            for conversation in conversations:
                convs[conversation.key] = conversation.state
            return convs
        except NoResultFound:
            return defaultdict()

    def update_conversation(self, name, key, new_state):
        chat_id, user_id, message_id = key
        conv, created = get_one_or_create(
            session=self.session,
            model=Conversation,
            name=name,
            chat_id=chat_id if chat_id != -1 else None,
            user_id=user_id if user_id != -1 else None,
            message_id=message_id if message_id != -1 else None,
        )
        conv.state = new_state
        if not created:
            self.session.flush()

    def flush(self):
        if self.session:
            self.session.flush()
            self.session.close()
