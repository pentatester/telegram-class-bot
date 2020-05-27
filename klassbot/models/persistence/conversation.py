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

    # BigInteger
    first = Column(BigInteger, nullable=True)
    second = Column(BigInteger, nullable=True)
    third = Column(BigInteger, nullable=True)

    # States
    state = Column(PickleType, nullable=True)
    timeout = Column(DateTime, nullable=True)

    @property
    def key(self):
        keys = list()
        if self.first:
            keys.append(self.first)
        if self.second:
            keys.append(self.second)
        if self.third:
            keys.append(self.third)
        return tuple(keys)

    @key.setter
    def key(self, keys):
        if len(keys) == 3:
            self.first, self.second, self.third = keys
        elif len(keys) == 2:
            self.first, self.second = keys
        elif len(keys) == 1:
            self.first = keys

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
