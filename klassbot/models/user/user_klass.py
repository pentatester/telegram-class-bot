"""The sqlite model for a user."""

from collections import namedtuple

from sqlalchemy import Boolean, Column, func, ForeignKey
from sqlalchemy.types import (
    BigInteger,
    DateTime,
)
from sqlalchemy.orm import relationship

from klassbot.db import base

UserKlassConfig = namedtuple("UserKlassConfig", ["admin", "student", "teacher", "notification"], defaults=[False, False, False, True])


class UserKlass(base):
    """The model for a user."""

    __tablename__ = "user_klass"

    # Many to One
    id = Column(BigInteger, primary_key=True)
    user_id = Column(
        BigInteger,
        ForeignKey("user.id", ondelete="cascade"),
        nullable=True,
        index=True,
    )
    user = relationship("User", back_populates="klasses")
    klass_id = Column(
        BigInteger,
        ForeignKey("klass.id", ondelete="cascade"),
        nullable=True,
        index=True,
    )
    klass = relationship("Klass", back_populates="users")

    # One to Many
    grades = relationship("AssignGrade", back_populates="user")

    # Flags
    admin = Column(Boolean, default=False)
    student = Column(Boolean, default=True)
    teacher = Column(Boolean, default=False)
    notification = Column(Boolean, default=True)

    # Date
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def config(self, config: UserKlassConfig):
        self.admin = config.admin
        self.student = config.student
        self.teacher = config.teacher
        self.notification = config.notification
