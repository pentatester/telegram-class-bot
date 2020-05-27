"""The sqlite model for a user."""
from sqlalchemy import Column, func, ForeignKey
from sqlalchemy.types import BigInteger, DateTime, String
from sqlalchemy.orm import relationship

from klassbot.db import base

from klassbot.models import UserKlass
from klassbot.models.user import UserKlassConfig


class Klass(base):
    """The model for a user."""

    __tablename__ = "klass"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    chat_id = Column(BigInteger, nullable=True)

    # Date
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # One to many
    users = relationship("UserKlass", back_populates="klass")

    # One to one
    creator_id = Column(
        BigInteger,
        ForeignKey("user.id", ondelete="cascade"),
        nullable=True,
        index=True,
    )
    creator = relationship("User")

    def add_member(self, user, config: UserKlassConfig):
        uc = UserKlass()
        uc.user = user
        uc.config(config)
        self.users.append(uc)
