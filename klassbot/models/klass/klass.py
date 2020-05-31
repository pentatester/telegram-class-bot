"""The sqlite model for a user."""
from sqlalchemy import Column, func, ForeignKey
from sqlalchemy.exc import IntegrityError
from sqlalchemy.types import BigInteger, Boolean, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from telegram import Chat, Update
from telegram.utils.helpers import create_deep_linked_url

from klassbot.config import config
from klassbot.db import base
from klassbot.models import UserKlass


class Klass(base):
    """The model for a user."""

    __tablename__ = "klass"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)

    # Flags
    started = Column(Boolean, nullable=False, default=False)

    # Date
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # One to many
    users = relationship("UserKlass", back_populates="klass")
    assigns = relationship("Assign", back_populates="klass")

    # One to one
    creator_id = Column(
        BigInteger,
        ForeignKey("user.id", ondelete="cascade"),
        nullable=True,
        index=True,
    )
    creator = relationship("User")

    @staticmethod
    def from_update(update: Update):
        chat: Chat = update.effective_chat
        name = str(chat.title)
        for character in ["[", "]", "_", "*"]:
            name = name.replace(character, "")
        return Klass(id=chat.id, name=name)

    @classmethod
    def get_or_create(cls, update: Update, session):
        chat: Chat = update.effective_chat
        try:
            return session.query(cls).filter_by(id=chat.id).one(), False
        except NoResultFound:
            klass = cls.from_update(update)
            try:
                session.add(klass)
                session.flush()
                return klass, True
            except IntegrityError:
                session.rollback()
                return (
                    session.query(cls).filter_by(id=chat.id).one(),
                    False,
                )

    def add_admin(self, user, session):
        user_klass, _ = UserKlass.get_or_create(user, self, session)
        user_klass.admin = True

    def add_teacher(self, user, session):
        user_klass, _ = UserKlass.get_or_create(user, self, session)
        user_klass.teacher = True

    def add_student(self, user, session):
        user_klass, _ = UserKlass.get_or_create(user, self, session)
        user_klass.student = True

    def remove_user(self, user: UserKlass, session):
        self.users.remove(user)
        session.delete(user)

    @property
    def invite_link(self):
        username = config["me"].username
        payload = f"join-klass-{abs(self.id)}"
        return create_deep_linked_url(username, payload=payload)
