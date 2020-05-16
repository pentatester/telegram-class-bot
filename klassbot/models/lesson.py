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


class Lesson(base):
    """The model for a Lessons."""

    __tablename__ = "lesson"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)