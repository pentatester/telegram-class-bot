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
            convs = []
            for conversation in conversations:
                convs.append((conversation.key, conversation.state))
            return defaultdict(convs)
        except NoResultFound:
            return defaultdict()

    def update_conversation(self, name, key, new_state):
        conv = get_one_or_create(
            session=self.session, model=Conversation, name=name
        )
        conv.key = key
        conv.state = new_state

    def flush(self):
        self.session.commit()

    def __del__(self):
        self.session.close()
