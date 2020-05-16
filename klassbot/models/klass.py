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


class Klass(base):
    """The model for a user."""

    __tablename__ = "klass"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)

    # OneToMany
    teacher = relationship("User")
    student = relationship("User")
    assign = relationship("Assign")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )