"""The sqlite model for a user."""
from sqlalchemy import (
    Boolean,
    Column,
    func,
    ForeignKey,
)
from sqlalchemy.types import (
    BigInteger,
    DateTime,
    String,
)
from sqlalchemy.orm import relationship

from klassbot.db import base


class Assign(base):
    """The model for a Assignment."""

    __tablename__ = "assign"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    intro = Column(String)

    # OneToMany
    grade = relationship("AssignGrade", back_populates="assign")

    # Flags
    created = Column(Boolean, nullable=False, default=False)
    closed = Column(Boolean, nullable=False, default=False)

    # Date
    duedate = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
