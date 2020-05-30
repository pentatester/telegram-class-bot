"""The sqlite model for a user."""
from sqlalchemy import Boolean, Column, func, ForeignKey
from sqlalchemy.types import (
    BigInteger,
    DateTime,
    String,
)
from sqlalchemy.orm import relationship

from klassbot.db import base


class Assign(base):
    """The model for a user."""

    __tablename__ = "assign"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)

    # Flags
    expired = Column(Boolean, default=False)

    # Many to One
    klass_id = Column(
        BigInteger,
        ForeignKey("klass.id", ondelete="cascade"),
        nullable=True,
        index=True,
    )
    klass = relationship("Klass", back_populates="assigns")
    teacher_id = Column(
        BigInteger,
        ForeignKey("user.id", ondelete="cascade"),
        nullable=True,
        index=True,
    )
    teacher = relationship("User", back_populates="assigns")

    # One to Many
    grades = relationship("AssignGrade", back_populates="assign")

    # Date
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
