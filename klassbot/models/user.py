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


class User(base):
    """The model for a user."""

    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    username = Column(String)

    # Flags
    started = Column(Boolean, nullable=False, default=False)
    banned = Column(Boolean, nullable=False, default=False, server_default="FALSE")
    deleted = Column(Boolean, nullable=False, default=False, server_default="FALSE")
    broadcast_sent = Column(Boolean, nullable=False, default=False)
    last_update = Column(DateTime)

    # Debug time j
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Permanent settings
    admin = Column(Boolean, nullable=False, default=False)
    locale = Column(String, default="English")
    european_date_format = Column(Boolean, nullable=False, default=False)
    notifications_enabled = Column(Boolean, nullable=False, default=True)

    # Chat logic
    expected_input = Column(String)

    # One to many
    assign_grade = relationship("AssignGrade")
    # Gradings 
    gradings = relationship("AssignGrade", back_populates="grader")
    # Grades
    grades = relationship("AssignGrade", back_populates="user")

    # Many to many
    klasses = relationship("Klass", secondary="user_klass")

    def __init__(self, user_id, username):
        """Create a new user."""
        self.id = user_id
        if username is not None:
            self.username = username.lower()

    def __repr__(self):
        """Print as string."""
        return f"User with Id: {self.id}, name: {self.name}, locale: {self.locale}"


class UserKlassLink(base):
    # user to klass links
    __tablename__ = "user_klass"
    # if klass deleted  -> delete link!
    klass_id = Column(
        BigInteger,
        ForeignKey("klass.id", ondelete="cascade", name="klass"),
        primary_key=True,
    )
    # if user deleted  -> delete link!
    user_id = Column(
        BigInteger,
        ForeignKey("user.id", ondelete="cascade", name="user"),
        primary_key=True,
    )
