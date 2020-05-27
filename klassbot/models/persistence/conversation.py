"""The sqlite model for a user."""

from collections import namedtuple

from sqlalchemy import Column
from sqlalchemy.types import (
    BigInteger,
    DateTime,
    PickleType,
    String,
)

from klassbot.db import base

Key = namedtuple(
    "Key", ["user", "chat", "message"], defaults=[None, None, None]
)


def parse_key(key):
    return Key(*key)._asdict()


class Conversation(base):
    """The model to store Conversations."""

    __tablename__ = "conversation"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)

    # Boolean
    user_id = Column(BigInteger, nullable=False)
    chat_id = Column(BigInteger, nullable=False)
    message_id = Column(BigInteger, nullable=True)

    # States
    state = Column(PickleType, nullable=True)
    timeout = Column(DateTime, nullable=True)

    def key(self, update):
        chat = update.effective_chat
        user = update.effective_user
        keys = list()
        if self.per_chat:
            self.chat_id = chat.id
            keys.append(self.chat_id)
        if self.per_user and user is not None:
            self.user_id = user.id
            keys.append(self.user_id)
        if self.per_message:
            self.message_id = (
                update.callback_query.inline_message_id
                or update.callback_query.message.message_id
            )
            keys.append(self.message_id)
        return tuple(keys)
