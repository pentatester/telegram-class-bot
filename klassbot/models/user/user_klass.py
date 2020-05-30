"""The sqlite model for a user."""

from collections import namedtuple
from telegram import Chat, ChatMember
from sqlalchemy import Boolean, Column, func, ForeignKey
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.types import (
    BigInteger,
    DateTime,
)

from klassbot.db import base

UserKlassConfig = namedtuple(
    "UserKlassConfig",
    ["admin", "student", "teacher", "notification"],
    defaults=[False, False, False, True],
)


class UserKlass(base):
    """The model for a user."""

    __tablename__ = "user_klass"

    # Many to One
    user_id = Column(
        BigInteger, ForeignKey("user.id", ondelete="cascade"), primary_key=True,
    )
    user = relationship("User", back_populates="klasses")
    klass_id = Column(
        BigInteger,
        ForeignKey("klass.id", ondelete="cascade"),
        primary_key=True,
    )
    klass = relationship("Klass", back_populates="users")

    # One to Many
    grades = relationship("AssignGrade", back_populates="user")

    # Flags
    admin = Column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )
    student = Column(Boolean, nullable=False, default=True)
    teacher = Column(Boolean, nullable=False, default=False)
    notification = Column(Boolean, nullable=False, default=True)

    # Date
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    @staticmethod
    def create(user, klass):
        user_klass = UserKlass()
        user_klass.user_id = user.id
        user_klass.klass_id = klass.id
        return user_klass

    @staticmethod
    def get_or_create(user, klass, session):
        try:
            return (
                session.query(UserKlass)
                .filter_by(user_id=user.id, klass_id=klass.id)
                .one(),
                False,
            )
        except NoResultFound:
            user_klass = UserKlass.create(user, klass)
            try:
                session.add(user_klass)
                session.flush()
                return user_klass, True
            except IntegrityError:
                session.rollback()
                return (
                    session.query(UserKlass)
                    .filter_by(user_id=user.id, klass_id=klass.id)
                    .one(),
                    False,
                )

    @property
    def config(self):
        return UserKlassConfig(self.admin, self.student, self.teacher, self.notification)

    @config.setter
    def config(self, config: UserKlassConfig):
        if isinstance(config, UserKlassConfig):
            self.admin = config.admin
            self.student = config.student
            self.teacher = config.teacher
            self.notification = config.notification

    def from_chat(self, chat: Chat):
        chat_member: ChatMember = chat.get_member(self.user_id)
        chat_member.status
