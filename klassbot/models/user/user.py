"""The sqlite model for a user."""
from sqlalchemy import Boolean, Column, func
from sqlalchemy.types import (
    BigInteger,
    DateTime,
    String,
)
from sqlalchemy.orm import relationship

from klassbot.db import base


class User(base):
    """The model for a user."""

    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False, default="User")
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
