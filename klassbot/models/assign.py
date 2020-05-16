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


class AssignGrade(base):
    """The model for a Assignment Grade."""

    __tablename__ = "assign_grade"

    id = Column(BigInteger, primary_key=True)

    # Many To One
    assign_id = Column(
        BigInteger,
        ForeignKey("assign.id", ondelete="cascade", name="assign"),
        nullable=False,
        index=True,
    )
    assign = relationship(
        "Assign", foreign_keys="AssignGrade.assign_id", back_populates="grade"
    )

    user_id = Column(
        BigInteger,
        ForeignKey("user.id", ondelete="cascade", name="user"),
        nullable=False,
        index=True,
    )
    user = relationship("User", foreign_keys="AssignGrade.user_id")

    grader_id = Column(
        BigInteger,
        ForeignKey("user.id", ondelete="cascade", name="user"),
        nullable=False,
        index=True,
    )
    grader = relationship("User", foreign_keys="AssignGrade.grader_id")

    # Grading
    grade = Column(BigInteger)

    # Date
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
