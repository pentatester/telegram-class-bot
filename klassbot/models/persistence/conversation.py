"""The sqlite model for a user."""
from sqlalchemy import Column
from sqlalchemy.types import (
    BigInteger,
    DateTime,
    PickleType,
    String,
)

from klassbot.db import base


class Conversation(base):
    """The model to store Conversations."""

    __tablename__ = "conversation"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)

    # BigInteger
    chat_id = Column(BigInteger, nullable=True)
    user_id = Column(BigInteger, nullable=True)
    message_id = Column(BigInteger, nullable=True)

    # States
    state = Column(PickleType, nullable=True)
    timeout = Column(DateTime, nullable=True)

    @property
    def key(self):
        keys = list()
        if self.chat_id:
            keys.append(self.chat_id)
        if self.user_id:
            keys.append(self.user_id)
        if self.message_id:
            keys.append(self.message_id)
        return tuple(keys)

    @key.setter
    def key(self, keys):
        if isinstance(keys, tuple) and len(keys) == 3:
            chat_id, user_id, message_id = keys
            if chat_id != -1:
                self.chat_id = chat_id
            if user_id != -1:
                self.user_id = user_id
            if message_id != -1:
                self.message_id = message_id
        else:
            raise ValueError("`key` not instance of tuple & len != 3")

    def key_from_update(self, update):
        chat = update.effective_chat
        user = update.effective_user
        keys = list()
        if self.per_chat:
            self.first = chat.id
            keys.append(self.first)
        if self.per_user and user is not None:
            self.second = user.id
            keys.append(self.second)
        if self.per_message:
            self.third = (
                update.callback_query.inline_message_id
                or update.callback_query.message.message_id
            )
            keys.append(self.third)
        return tuple(keys)
