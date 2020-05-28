"""The sqlite model for a user."""
from sqlalchemy import Boolean, Column, func
from sqlalchemy.types import (
    BigInteger,
    DateTime,
    String,
)
from sqlalchemy.orm import relationship
from telegram import User as TgUser

from klassbot.db import base
from klassbot.utils.db import get_one_or_create


class User(base):
    """The model for a user."""

    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    username = Column(String)

    # Flags
    started = Column(Boolean, nullable=False, default=False)
    banned = Column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )
    deleted = Column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )
    broadcast_sent = Column(Boolean, nullable=False, default=False)
    last_update = Column(DateTime)

    # Permanent settings
    admin = Column(Boolean, nullable=False, default=False)
    locale = Column(String, default="English")
    european_date_format = Column(Boolean, nullable=False, default=False)
    notifications_enabled = Column(Boolean, nullable=False, default=True)

    # Chat logic
    expected_input = Column(String)

    # One to many
    klasses = relationship("UserKlass", back_populates="user")

    # Date
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    @staticmethod
    def from_user(user: TgUser, session):
        user_, created = get_one_or_create(
            session=session, model=User, id=user.id,
        )
        user_.name = get_name_from_tg_user(user)
        user_.username = user.username
        # TODO Set Locale
        return user_


def get_name_from_tg_user(tg_user):
    """Return the best possible name for a User."""
    name = ""
    if tg_user.first_name is not None:
        name = tg_user.first_name
        name += " "
    if tg_user.last_name is not None:
        name += tg_user.last_name

    if tg_user.username is not None and name == "":
        name = tg_user.username

    if name == "":
        name = str(tg_user.id)

    for character in ["[", "]", "_", "*"]:
        name = name.replace(character, "")

    return name.strip()
