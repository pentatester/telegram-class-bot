"""The sqlite model for a user."""
from sqlalchemy import Boolean, Column, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.types import (
    BigInteger,
    DateTime,
    String,
)
from telegram import User as TgUser

from klassbot.db import base


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
    assigns = relationship("Assign", back_populates="teacher")

    # Date
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    @staticmethod
    def from_user(user: TgUser):
        return User(
            id=user.id,
            name=get_name_from_tg_user(user),
            username=user.username,
        )

    @classmethod
    def get_or_create(cls, user_: TgUser, session):
        try:
            return session.query(cls).filter_by(id=user_.id).one(), False
        except NoResultFound:
            user = cls.from_user(user_)
            try:
                session.add(user)
                session.flush()
                return user, True
            except IntegrityError:
                session.rollback()
                return (
                    session.query(cls).filter_by(id=user_.id).one(),
                    False,
                )

    @property
    def ready(self):
        return self.started and not self.banned and not self.deleted


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
