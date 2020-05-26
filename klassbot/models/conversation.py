"""The sqlite model for a user."""

import pickle

from collections import namedtuple

from sqlalchemy import Column
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.types import (
    BigInteger,
    DateTime,
    String,
)

from klassbot.db import base
from klassbot.utils.db import get_one_or_create, session_wrapper

Key = namedtuple(
    "Key", ["user", "chat", "message"], defaults=[None, None, None]
)


def parse_key(key):
    return Key(*key)._asdict()


class Conversation(base):
    """The model for a Conversation."""

    __tablename__ = "conversation"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)

    # Boolean
    user = Column(BigInteger, nullable=False)
    chat = Column(BigInteger, nullable=False)
    message = Column(BigInteger, nullable=True)

    # States
    state = Column(String, nullable=True)
    timeout = Column(DateTime, nullable=True)

    @staticmethod
    @session_wrapper
    def get_conversations(name: str, session=None):
        try:
            results = session.query(Conversation).filter_by(name=name)
        except NoResultFound:
            results = None
        return (results, False)

    @staticmethod
    @session_wrapper
    def update_conversation(name: str, key: tuple, new_state, session=None):
        conversation, created = get_one_or_create(
            session=session, model=Conversation, name=name, **parse_key(key)
        )
        conversation.state = pickle.dumps(new_state)
        return (None, created)

    @staticmethod
    @session_wrapper
    def delete_conversation(name: str, key: tuple, session=None):
        try:
            conversation = (
                session.query(Conversation)
                .filter_by(name=name, **parse_key(key))
                .one()
            )
            session.delete(conversation)
            return (True, True)
        except NoResultFound:
            return (False, False)
