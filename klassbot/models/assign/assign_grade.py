"""The sqlite model for a user."""
from sqlalchemy import Boolean, Column, func, ForeignKey
from sqlalchemy.types import (
    BigInteger,
    DateTime,
    Integer,
)
from sqlalchemy.orm import relationship

from klassbot.db import base


class AssignGrade(base):
    """The model for a user."""

    __tablename__ = "assign_grade"

    id = Column(BigInteger, primary_key=True)
    grade = Column(Integer, nullable=True)
    finish = Column(Boolean, default=False)

    # Many to One
    assign_id = Column(
        BigInteger,
        ForeignKey("assign.id", ondelete="cascade"),
        nullable=True,
        index=True,
    )
    assign = relationship("Assign", back_populates="grades")
    user_id = Column(
        BigInteger,
        ForeignKey("user_klass.id", ondelete="cascade"),
        nullable=True,
        index=True,
    )
    user = relationship("UserKlass", back_populates="grades")

    # Date
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
