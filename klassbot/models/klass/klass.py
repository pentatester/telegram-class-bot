"""The sqlite model for a user."""
from sqlalchemy import Column, func, ForeignKey
from sqlalchemy.types import BigInteger, Boolean, DateTime, String
from sqlalchemy.orm import relationship
from telegram import Chat

from klassbot.db import base
from klassbot.models import User, UserKlass
from klassbot.utils.db import get_one_or_create


class Klass(base):
    """The model for a user."""

    __tablename__ = "klass"

    id = Column(BigInteger, primary_key=True)
    chat_id = Column(BigInteger, primary_key=True)
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
    def from_chat(chat: Chat):
        """Create an instance of `Klass` using Chat

        Arguments:
            chat {telegram.Chat} -- An instance of Telegram Chat

        Returns:
            Klass -- An instance of models.Klass
        """
        name = str(chat.title)
        for character in ["[", "]", "_", "*"]:
            name = name.replace(character, "")
        return Klass(id=chat.id, name=name)

    def add_user(
        self, user: User, session=None,
    ):
        """Add a `User` into `Klass`

        Arguments:
            user {User} -- An instance of models.User

        Keyword Arguments:
            session {sqlalchemy.Session} -- Database session (default: {None})

        Returns:
            UserKlass -- An instance of models.UserKlass
        """
        user_klass, created = get_one_or_create(
            session=session, model=UserKlass, user_id=user.id, klass_id=self.id
        )
        if created:
            self.users.append(user_klass)
        return user_klass
